import urllib
from xbmctorrent import plugin
from xbmctorrent.scrapers import scraper
from xbmctorrent.ga import tracked
from xbmctorrent.caching import cached_route, shelf
from xbmctorrent.utils import ensure_fanart
from xbmctorrent.library import library_context


BASE_URL = "%s/" % plugin.get_setting("base_eztv")
HEADERS = {
    "Referer": BASE_URL,
}
SHOW_LIST_CACHE_TTL = 24 * 3600 # 24 hours caching


# Logo found on http://thesimurg.deviantart.com/art/Logo-for-EZTV-57874544
@scraper("[COLOR yellow]EZTV - Series [Pulsar mod][/COLOR]", "http://i.imgur.com/XcH6WOg.jpg")
@plugin.route("/eztv")
@ensure_fanart
@tracked
def eztv_index():
    import string
    for letter in ["0-9"] + list(string.ascii_uppercase):
        yield {
            "label": letter,
            "path": plugin.url_for("eztv_shows_by_letter", letter=letter),
            "is_playable": False,
        }


@plugin.route("/eztv/shows/<letter>")
@cached_route(ttl=SHOW_LIST_CACHE_TTL, content_type="tvshows")
@ensure_fanart
@tracked
def eztv_shows_by_letter(letter):
    import re
    import xbmc
    import xbmcgui
    from bs4 import BeautifulSoup
    from contextlib import nested, closing
    from itertools import izip, groupby
    from concurrent import futures
    from xbmctorrent.scrapers import ungenerate
    from xbmctorrent.utils import terminating, url_get, SafeDialogProgress
    from xbmctorrent import tvdb

    with shelf("it.eztv.shows") as eztv_shows:
        if not eztv_shows:
            response = url_get("%s/showlist/" % BASE_URL, headers=HEADERS)
            soup = BeautifulSoup(response, "html5lib")
            nodes = soup.findAll("a", "thread_link")
            for node in nodes:
                show_id, show_named_id = node["href"].split("/")[2:4]
                show_name = node.text
                show_first_letter = show_name[0].lower()
                if re.match("\d+", show_first_letter):
                    show_first_letter = "0-9"
                eztv_shows.setdefault(show_first_letter, {}).update({
                    show_id: {
                        "id": show_id,
                        "named_id": show_named_id,
                        "name": node.text,
                    }
                })

    shows_list = sorted(eztv_shows[letter.lower()].values(), key=lambda x: x["name"].lower())

    with closing(SafeDialogProgress(delay_close=0)) as dialog:
        dialog.create(plugin.name)
        dialog.update(percent=0, line1="Fetching serie information...", line2="", line3="")

        state = {"done": 0}
        def on_serie(future):
            data = future.result()
            state["done"] += 1
            dialog.update(
                percent=int(state["done"] * 100.0 / len(shows_list)),
                line2=data and data["seriesname"] or "",
            )

        with futures.ThreadPoolExecutor(max_workers=5) as pool_tvdb:
            tvdb_list = [pool_tvdb.submit(tvdb.search, show["name"], True) for show in shows_list]
            [future.add_done_callback(on_serie) for future in tvdb_list]
            while not all(job.done() for job in tvdb_list):
                if dialog.iscanceled():
                    return
                xbmc.sleep(100)

    tvdb_list = [job.result() for job in tvdb_list]
    for i, (eztv_show, tvdb_show) in enumerate(izip(shows_list, tvdb_list)):
        if tvdb_show:
            item = tvdb.get_list_item(tvdb_show)
            item.update({
                "path": plugin.url_for("eztv_get_show_seasons", show_id=eztv_show["id"], tvdb_id=tvdb_show["id"])
            })
            yield item
        else:
            yield {
                "label": eztv_show["name"],
                "path": plugin.url_for("eztv_get_show_seasons", show_id=eztv_show["id"])
            }


def get_episode_data_from_name(name):
    import re
    res = re.search("S(\d+)E(\d+)", name)
    if res:
        return map(int, res.groups())
    res = re.search("(\d+)x(\d+)", name)
    if res:
        return map(int, res.groups())
    return 0, 0


@plugin.route("/eztv/shows/<show_id>/seasons")
@ensure_fanart
@tracked
def eztv_get_show_seasons(show_id):
    import random
    from bs4 import BeautifulSoup
    from itertools import groupby
    from concurrent import futures
    from xbmctorrent.utils import first, terminating, url_get
    from xbmctorrent import tvdb

    plugin.set_content("seasons")

    tvdb_id = first(plugin.request.args.get("tvdb_id"))
    with futures.ThreadPoolExecutor(max_workers=2) as pool:
        def _eztv_get_show():
            plugin.log.info("Getting show")
            response = url_get("%s/shows/%s/" % (BASE_URL, show_id), headers=HEADERS)
            plugin.log.info("Got show")
            return BeautifulSoup(response, "html5lib")
        soup = pool.submit(_eztv_get_show)
        if tvdb_id:
            tvdb_show = pool.submit(tvdb.get_all_meta, plugin.request.args["tvdb_id"][0])

        soup = soup.result()
        fanarts = []
        if tvdb_id:
            tvdb_show = tvdb_show.result()
            fanarts = list([banner for banner in tvdb_show["banners"] if banner["bannertype"] == "fanart"])
            random.shuffle(fanarts)

        seasons = {}
        for node_episode in soup.findAll("a", "epinfo"):
            season, episode = get_episode_data_from_name(node_episode.text)
            seasons.setdefault(season, {})[episode] = True

        for i, season in enumerate(reversed(sorted(seasons.keys()))):
            item = tvdb_id and tvdb.get_season_list_item(tvdb_show, season) or {}
            item.update({
                "label": "Season %d [%d episodes]" % (season, len(seasons[season])),
                "path": plugin.url_for("eztv_get_episodes_for_season", show_id=show_id, season=season, tvdb_id=tvdb_id),
            })
            if fanarts:
                item.setdefault("properties", {}).update({
                    "fanart_image": fanarts[i % len(fanarts)]["bannerpath"],
                })
            yield item


@plugin.route("/eztv/shows/<show_id>/<season>/episodes")
@library_context
@ensure_fanart
@tracked
def eztv_get_episodes_for_season(show_id, season):
    import copy
    import random
    from bs4 import BeautifulSoup
    from itertools import izip
    from concurrent import futures
    from xbmctorrent.utils import first, terminating, url_get
    from xbmctorrent import tvdb

    plugin.set_content("episodes")

    season = int(season)
    tvdb_id = first(plugin.request.args.get("tvdb_id"))
    with futures.ThreadPoolExecutor(max_workers=2) as pool:
        def _eztv_get_show():
            return BeautifulSoup(url_get("%s/shows/%s/" % (BASE_URL, show_id), headers=HEADERS), "html5lib")
        soup = pool.submit(_eztv_get_show)
        if tvdb_id:
            tvdb_show = pool.submit(tvdb.get_all_meta, plugin.request.args["tvdb_id"][0])

        soup = soup.result()
        items = []
        fanarts = []
        if tvdb_id:
            tvdb_show = tvdb_show.result()
            fanarts = list([banner for banner in tvdb_show["banners"] if banner["bannertype"] == "fanart"])
            random.shuffle(fanarts)
            items = list(tvdb.build_episode_list_items(tvdb_show, int(season)))
        text_nodes = soup.findAll("a", "epinfo")
        href_nodes = soup.findAll("a", "magnet")
        season_nodes = izip(text_nodes, href_nodes)
        season_nodes = filter(lambda x: get_episode_data_from_name(x[0].text)[0] == season, season_nodes)

        for i, (node_text, node_magnet) in enumerate(season_nodes):
            season, episode = get_episode_data_from_name(node_text.text)
            if tvdb_id and episode >= 0:
                item = copy.deepcopy(items[int(episode) - 1])
                for pattern, suffix in (("720p", "(HD)"), ("1080p", "(FullHD)"), ("repack", "(REPACK)"), ("proper", "(PROPER)")):
                    if pattern in node_text.text.lower():
                        item["label"] = "%s %s" % (item["label"], suffix)
            else:
                item = {
                    "label": node_text.text,
                }
            item.setdefault("info", {}).update({
                "tvshowtitle": node_text.text,
                "title": item["label"],
            })
            stream_info = {}
            magnet_link = urllib.quote_plus(node_magnet["href"].encode("utf-8"))
            if "x264" in node_text.text:
                stream_info["codec"] = item["info"]["video_codec"] = "h264"
            if "xvid" in node_text.text.lower():
                stream_info["codec"] = item["info"]["video_codec"] = "xvid"
            if "720p" in node_text.text:
                stream_info["width"] = 1280
                stream_info["height"] = 720
            if "1080p" in node_text.text:
                stream_info["width"] = 1920
                stream_info["height"] = 1080
            item.update({
                "path": "plugin://plugin.video.pulsar/play?uri=" + magnet_link,
                # "path": plugin.url_for("play", uri=node_magnet["href"]),
                "stream_info": {"video": stream_info},
                "is_playable": True,
            })
            if fanarts:
                item.setdefault("properties", {}).update({
                    "fanart_image": fanarts[i % len(fanarts)]["bannerpath"],
                })
            yield item
