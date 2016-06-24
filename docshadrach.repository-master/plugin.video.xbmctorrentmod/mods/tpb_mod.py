import urllib
from xbmctorrent import plugin
from xbmctorrent.scrapers import scraper
from xbmctorrent.ga import tracked
from xbmctorrent.caching import cached_route
from xbmctorrent.utils import ensure_fanart
from xbmctorrent.library import library_context


# Temporary, will be fixed later by them
IMMUNICITY_TPB_URL = "http://thepiratebay.pe"
BASE_URL = "%s/" % (plugin.get_setting("immunicity", bool) and IMMUNICITY_TPB_URL or plugin.get_setting("base_tpb"))
HEADERS = {
    "Referer": BASE_URL,
}


CATEGORIES = [
    ("Movies", 201, [
        ("in HD", 207),
        ("in 3D", 209),
    ]),
    ("Music videos", 203),
    ("TV shows", 205, [
        ("in HD", 208),
    ]),
    ("Other", 299),
]

if plugin.get_setting("porn", bool):
    CATEGORIES += [
        ("XXX", 500, [
            ("Movies", 501),
            ("in HD", 503),
            ("Movie clips", 504),
            ("Other", 599),
        ]),
    ]

# Cache TTLs
DEFAULT_TTL = 24 * 3600 # 24 hours


@scraper("[COLOR yellow]The Pirate Bay - Movies and Series [Pulsar mod][/COLOR]", "%s/static/img/tpb.jpg" % BASE_URL)
@plugin.route("/tpb")
@ensure_fanart
@tracked
def piratebay_index():
    yield {"label": "Search", "path": plugin.url_for("piratebay_search")}

    def make_cats(root, prefix=""):
        for cat in root:
            yield {
                "label": "%s%s" % (prefix, cat[0]),
                "path": plugin.url_for("piratebay_page", root="/browse/%d" % cat[1], page=0),
            }
            if len(cat) > 2:
                for entry in make_cats(cat[2], prefix="%s    " % prefix):
                    yield entry

    for cat in make_cats(CATEGORIES):
        yield cat


@plugin.route("/tpb/<root>/<page>")
@library_context
@ensure_fanart
@tracked
def piratebay_page(root, page):
    import re
    from bs4 import BeautifulSoup
    from urlparse import urljoin
    from xbmctorrent.utils import url_get

    page = int(page)
    html_data = url_get(urljoin(BASE_URL, "%s/%d/7/100,200,500" % (root, page)), headers=HEADERS)
    soup = BeautifulSoup(html_data, "html5lib")
    nodes = soup.findAll("div", "detName")
    
    for node in nodes:
        seeds, peers = map(lambda x: x.text, node.parent.parent.findAll("td")[2:])
        magnet_node = node.parent.findAll("a")[1]
        magnet_link = urllib.quote_plus(magnet_node["href"].encode("utf-8"))
        desc_node = node.parent.findAll("font", "detDesc")[0]
        size = re.search("Size (.*?),", desc_node.text).group(1)
        text = "%s (%s S:%s P:%s)" % (node.a.text, size.replace("&nbsp;", " "), seeds, peers)
        yield {
            "label": text,
            "path": "plugin://plugin.video.pulsar/play?uri=" + magnet_link,
            # "path": plugin.url_for("play", uri=magnet_node["href"]),
            "is_playable": True,
        }
    yield {
        "label": ">> Next page",
        "path": plugin.url_for("piratebay_page", root=root, page=page + 1),
        "is_playable": False,
    }


@plugin.route("/tpb/search")
@tracked
def piratebay_search():
    import urllib

    query = plugin.request.args.get("query")
    if query:
        query = query[0]
    else:
        query = plugin.keyboard("", "XBMCtorrent - The Pirate Bay - Search")
    if query:
        plugin.redirect(plugin.url_for("piratebay_page", root="/search/%s" % urllib.quote(query, safe=""), page=0))
