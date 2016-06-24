#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,urllib2,os,re,sys,zipfile
import xbmc,xbmcaddon,xbmcplugin,xbmcgui
import dataparser,verifier
import time,datetime
from shutil import move


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')


Config = xbmcaddon.Addon()

dialog = xbmcgui.Dialog()

Progress = xbmcgui.DialogProgress()

 
# path = os.path.join(xbmcaddon.Addon().getAddonInfo('path'))



advert = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/tools', 'advert.txt'))


timestamp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/tools', 'timestamp.txt'))

update_source = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/tools', 'update_source.txt'))

update_index = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/tools', 'update_index.txt'))


pw = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/tools', 'pw.txt'))


file = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/database', 'source.xml'))

file2 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/database', 'source_add.xml'))

output = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/database', 'output.xml'))

offline = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/database', 'offline_db.xml'))

offline2 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/database', 'offline_add.xml'))

database = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/database', 'DataBase.xml'))

database2 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zz/resources/database', 'DataBase_add.xml'))

filenames = file2, file

off_filenames = offline2, offline

db_filenames = database2, database



def ExtractAll(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
        return False

    return True
    
def Repo():
    if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'repository.busterdiggler')):
        return
        
    url = "https://github.com/XBMCSpot/busterdiggler.repository/blob/master/zips/repository.busterdiggler-1.0.zip?raw=true"
    addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
    packageFile = os.path.join(addonsDir, 'packages', 'repo.zip')
    
    urllib.urlretrieve(url, packageFile)
    ExtractAll(packageFile, addonsDir)
        
    try:
        os.remove(packageFile)
    except:
        pass
            
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")


Repo()


def Kmedia():
        
    url = "https://www.dropbox.com/s/sbezwcon2kyj112/plugin.video.kmediatorrent-2.3.6.zip?dl=1"
    addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
    packageFile = os.path.join(addonsDir, 'packages', 'kmt.zip')
    
    urllib.urlretrieve(url, packageFile)
    ExtractAll(packageFile, addonsDir)
        
    try:
        os.remove(packageFile)
    except:
        pass
            
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")
    
    


def offline_update():
    
    try:
        f = open(offline2,"w+")
        
        NOM_list = []
        SIZE_list = []
        THUMB_list = []
        CATZZ_list = []
        SECC_list = []
        
        direc = 'http://www.brazzers.com/videos/all-sites/all-pornstars/all-categories/thisyear/bydate/'
        page = 1
        
        while page <= 23:
            url= direc + str(page)
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('<a href="/scenes/view/(.+?)"\n               title="(.+?)">\n                <img src="(.+?)"\n').findall(link)
            i = 0
            for id, name, thumb in match:
                url = "http://www.brazzers.com/scenes/view/" + id
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<li>SD MP4 <span>(.+?)</span>').findall(link)
                #match=re.compile('<li>HD MP4 720P <span>(.+?)</span>').findall(link)
                repl = str(match).replace("['[","")
                size = repl.replace(" MB]']", "")
                #size = repl.replace(" GiB]']", "")
                
                block = re.split(r'<div class=', link)
                catzz = re.findall('data-trackid="BZ:TOUR:RELEASE:LINK tag-name"\n                               title="(.+?)">', block[35])
                secc = re.compile('"BZ:TOUR:RELEASE:LINK niche-site"\n                       title="(.+?)"></a>').findall(block[34])
    
                if size != "" and size != "[]":
                    NOM_list.append(name)
                    SIZE_list.append(size)
                    THUMB_list.append(thumb)
                    CATZZ_list.append(str(catzz))
                    SECC_list.append(secc[0])
                    print name + " YES"
                    print size
                    
                    with open(offline) as sf:
                        last = sf.readline()
                        print "ultim: " + last
        
                        if size in last:
                            content = ''
                            for f in off_filenames:
                                content = content + open(f).read()
                                open(output,'wb').write(content)
                            move(output,offline)
                            open(update_index,'w+').write(st)
                            dialog.ok('ZZ', '[B]INDEX DATA[/B] is updated!')
                            sys.exit()
                        else:
                            f.write(SIZE_list[i] +"\n")
                            f.write("<item>\n")
                            f.write("<name>" +NOM_list[i] +"</name>\n")
                            f.write("<thumb>" +THUMB_list[i] +"</thumb>\n")
                            f.write("<size>" +SIZE_list[i] +"</size>\n")
                            f.write("<tags>" +CATZZ_list[i] +"</tags>\n")
                            f.write("<secc>" +SECC_list[i] +"</secc>\n")
                            f.write("</item>\n")
                            f.write("\n")
                            f.write("\n")
                            i += 1
                else: pass
            page += 1        
            
        
        i = 0    
        
        while i < int(len(NOM_list)):
            
            f.write("<item>\n")
            f.write("<name>" +NOM_list[i] +"</name>\n")
            f.write("<thumb>" +THUMB_list[i] +"</thumb>\n")
            f.write("<size>" +SIZE_list[i] +"</size>\n")
            f.write("</item>\n")
            f.write("\n")
            f.write("\n")
            
            i +=1
            
        f.close()
    
    except:
        open(update_index,'w+').write(st)
        pass


def mixer():
    
    lines = open(file).readlines()
    print "LINEA: " + lines[0]
    open(output, 'wb').writelines(lines[0])
    move(output,file)
    
    f = open(database2,"w+")
    
    opciones = open(offline, "r+")
    contenido = opciones.read()
    
    NOM_list = []
    SIZE_list = []
    THUMB_list = []
    CATZZ_list = []
    SECC_list = []
    
    matches = dataparser.etiqueta_maestra(contenido, "<item>(.*?)</item>")
    for item in matches:
        NAME = dataparser.subetiqueta(item, "<name>(.*?)</name>")
        THUMB = dataparser.subetiqueta(item, "<thumb>(.*?)</thumb>")
        SIZE = dataparser.subetiqueta(item, "<size>(.*?)</size>")
        CATZZ = dataparser.subetiqueta(item, "<tags>(.*?)</tags>")
        SECC = dataparser.subetiqueta(item, "<secc>(.*?)</secc>")
        
        NOM_list.append(NAME)
        SIZE_list.append(SIZE)
        THUMB_list.append(THUMB)       
        CATZZ_list.append(CATZZ)
        SECC_list.append(SECC)
    
    i = 0
    
    while i < int(len(NOM_list)):
        
        searchfile = open(file2)
    
        for line in searchfile:
            if SIZE_list[i] in line:
                rawtitle = re.compile('<title>(.+?)</title>').findall(line)
                cleantitle = str(rawtitle[0]).replace("&#039;", "'")
                title_sc = str(cleantitle).replace("&#39;", "'")
                rawid = re.compile('<id>(.+?)</id>').findall(line)
                id = str(rawid[0])
                match = re.compile('<url>(.+?)</url>').findall(line)
                nommatch = NOM_list[i].split(" ")
                if len(str(nommatch[0])) < 4:
                    matchtitle = str(nommatch[1])
                else:
                    matchtitle = str(nommatch[0])
                           
                    
                if matchtitle.lower() in title_sc.lower():
                    print matchtitle.lower()
                    print title_sc.lower()
                    

                    f.write(id +"\n")
                    f.write("<item>\n")
                    f.write("<name>" +NOM_list[i] +"</name>\n")
                    f.write("<title>" +title_sc +"</title>\n")
                    f.write("<thumb>" +THUMB_list[i] +"</thumb>\n")
                    f.write("<link>" +str(match[0]) +"</link>\n")
                    f.write("<size>" +SIZE_list[i] +"</size>\n")
                    f.write("<tags>" +CATZZ_list[i] +"</tags>\n")
                    f.write("<secc>" +SECC_list[i] +"</secc>\n")
                    f.write("<id>" +id +"</id>\n")
                    f.write("</item>\n")
                    f.write("\n")
                    f.write("\n")
                     
                        
            else:
                pass
        
        i +=1
        
    searchfile.close()
    f.close()


    content = ''
    for line in db_filenames:
        content = content + open(line).read()
        open(output,'wb').write(content)
    move(output,database)
    open(timestamp,'w+').write(st)
    dialog.ok('ZZ', 'The [B]DATABASE[/B] is updated!')
    sys.exit()



######################  SOURCE  ####################### 



def source_update():
    
    f = open(file2,"w+")
    
    try:
        direc = "http://kasto.come.in/usearch/category%3Axxx%20user%3Achkm8te%20seeds%3A2%20files%3A1/"
    
        page = 1
    
        sort = "/?field=time_add&sorder=desc"
        
        direc_var = direc + str(page) + sort
        
        response = urllib2.urlopen(direc_var)
        link = response.read()
        response.close()
        match = re.compile('class="turnoverButton siteButton bigButton">5</a><a class="blank turnoverButton siteButton nohov"><span></span></a><a rel="nofollow" href=".+?" class="turnoverButton siteButton bigButton">(.+?)</a>').findall(link)
        print "THIS " + str(match[0])
    
        maxpage = str(match[0])
        
        while page <= maxpage:
            print maxpage
              
            direc_var = direc + str(page) + sort
            response = urllib2.urlopen(direc_var)
            link = response.read()
            response.close()
            # match = re.compile('<a title="Torrent magnet link" href="(.+?)" class=".+?"><span></span></a>\n                <a title="Download torrent file" href=".+?" class=".+?"><span></span></a>\n            </div>\n            <div class=".+?">\n                <a href=".+?" class=".+?"></a>\n                <a href=".+?" class=".+?"></a>\n            <div class=".+?">\n\n                <a href=".+?" class=".+?">(.+?)</a>\n\n                                                <span class=".+?">\n                                Posted by <a class=".+?" href=".+?">.+?</a>&nbsp;<img src=".+?" alt=".+?"/>  in <span id="(.+?)"><strong><a href=".+?">.+?</a> > <a href=".+?">.+?</a></strong></span>                \t                </span>\n            \t            </div>\n            </td>\n\t\t\t\t\t\t\t\t\t<td class=".+?">(.+?) <span>MB</span></td>').findall(link)        
            # match = re.compile('<a title="Torrent magnet link" href="(.+?)" class=".+?"><span></span></a>\n                <a title="Download torrent file" href=".+?" class=".+?"><span></span></a>\n            </div>\n            <div class=".+?">\n                <a href=".+?" class=".+?"></a>\n                <a href=".+?" class=".+?"></a>\n            <div class=".+?">\n\n                <a href=".+?" class=".+?">(.+?)</a>\n\n                                                <span class=".+?">\n                                Posted by <a class=".+?" href=".+?">.+?</a> in <span id="(.+?)"><strong><a href=".+?">.+?</a> > <a href=".+?">.+?</a></strong></span>                \t                </span>\n            \t            </div>\n            </td>\n\t\t\t\t\t\t\t\t\t<td class=".+?">(.+?) <span>MB</span></td>\n\t\t\t<td class=".+?">.+?</td>\n\t\t\t<td class=".+?">.+?</td>\n\t\t\t<td class="green center">(.+?)</td>').findall(link)
            match = re.compile('<a title="Torrent magnet link" href="(.+?)" class=".+?"><i class=".+?"></i></a>\n                <a title="Download torrent file" href=".+?" class=".+?"><i class=".+?"></i></a>\n            </div>\n            <div class=".+?">\n                <a href=".+?" class=".+?"></a>\n                <a href=".+?" class=".+?"></a>\n            <div class=".+?">\n\n                <a href=".+?" class=".+?">(.+?)</a>\n\n                                                <span class=".+?">\n                                Posted by <a class=".+?" href=".+?">.+?</a> in <span id="(.+?)"><strong><a href=".+?">.+?</a> > <a href=".+?">.+?</a></strong></span>                \t                </span>\n            \t            </div>\n            </td>\n\t\t\t\t\t\t\t\t\t<td class=".+?">(.+?) <span>MB</span></td>\n\t\t\t<td class=".+?">.+?</td>\n\t\t\t<td class=".+?">.+?</td>\n\t\t\t<td class="green center">(.+?)</td>').findall(link)
    
            
            # print match
            with open(file) as sf:
                last = sf.readline()
           
                for url,name,id,size,seeds in match:
    
                    if id in last:
                        content = ''
                        for f in filenames:
                            content = content + open(f).read()
                            open(output,'wb').write(content)
                        move(output,file)
                        open(update_source,'w+').write(st)
                        dialog.ok('ZZ', '[B]SOURCE DATA[/B] is updated!')
                        sys.exit()
                    else:
                        if len(str(size)) == 5:
                            size = str(size) + "0"
                        else:
                            size = str(size)
                        f.write(id +"\n")
                        # f.write(">> Page " +str(page) +" of " +str(maxpage) +"\n")
                        f.write("\n")
                        f.write("<item>\n")
                        f.write(size +"<title>" +str(name) +"</title>")
                        f.write("<url>" +urllib.quote_plus(url.encode("utf-8")) +"</url>")
                        f.write("<id>" +str(id) +"</id>\n")
                        f.write("</item>\n")
                        f.write("\n")
                        f.write("\n")
    
            page += 1
        f.close()
        
    except:
        open(update_source,'w+').write(st)
        pass

    """
    
    try:
        
        web = verifier.verify()

        print "ESTA: " + web
        
        direc = web + "usearch/category%3Axxx%20user%3Achkm8te%20seeds%3A2%20files%3A1/"
  
        page = 1
    
        sort = "/?field=time_add&sorder=desc"
        
        direc_var = direc + str(page) + sort
        
        response = urllib2.urlopen(direc_var)
        link = response.read()
        response.close()
        match = re.compile('class="turnoverButton siteButton bigButton">5</a><a class="blank turnoverButton siteButton nohov"><span></span></a><a rel="nofollow" href=".+?" class="turnoverButton siteButton bigButton">(.+?)</a>').findall(link)
        print "THIS " + str(match[0])

        maxpage = str(match[0])
        
        while page <= maxpage:
            print maxpage
              
            direc_var = direc + str(page) + sort
            response = urllib2.urlopen(direc_var)
            link = response.read()
            response.close()
            match = re.compile('<a title="Torrent magnet link" href="(.+?)" class=".+?"><i class=".+?"></i></a>\n<a title="Download torrent file" href=".+?" class=".+?"><i class=".+?"></i></a>\n</div>\n<div class=".+?">\n<a href=".+?" class=".+?"></a>\n<a href=".+?" class=".+?"></a>\n<div class=".+?">\n<a href=".+?" class=".+?">(.+?)</a>\n<span class=".+?">\nPosted by <a class="plain" href="/user/chkm8te/">chkm8te</a> in <span id="(.+?)"><strong><a href="/xxx/">XXX</a> > <a href="/xxx-video/">Video</a></strong></span> </span>\n</div>\n</td>\n<td class=".+?">(.+?) <span>MB</span></td>\n<td class=".+?">.+?</td>\n<td class=".+?">.+?</td>\n<td class="green center">(.+?)</td>\n').findall(link)
            with open(file) as sf:
                last = sf.readline()
           
                for url,name,id,size,seeds in match:
    
                    if id in last:
                        content = ''
                        for f in filenames:
                            content = content + open(f).read()
                            open(output,'wb').write(content)
                        move(output,file)
                        open(update_source,'w+').write(st)
                        dialog.ok('ZZ', '[B]SOURCE DATA[/B] is updated!')
                        sys.exit()
                    else:
                        if len(str(size)) == 5:
                            size = str(size) + "0"
                        else:
                            size = str(size)
                        f.write(id +"\n")
                        # f.write(">> Page " +str(page) +" of " +str(maxpage) +"\n")
                        f.write("\n")
                        f.write("<item>\n")
                        f.write(size +"<title>" +str(name) +"</title>")
                        f.write("<url>" +urllib.quote_plus(url.encode("utf-8")) +"</url>")
                        f.write("<id>" +str(id) +"</id>\n")
                        f.write("</item>\n")
                        f.write("\n")
                        f.write("\n")
    
            page += 1
        f.close()
        
    except: pass
    """




def filters():

    if Config.getSetting("anal") == 'true':
        tag1 = "Anal"
    else:
        tag1 = ""
        

    if Config.getSetting("blackhair") == 'true':
        tag2 = "Black Hair"
    else:
        tag2 = ""
        
        
    if Config.getSetting("blonde") == 'true':
        tag3 = "Blonde"
    else:
        tag3 = ""
        
        
    if Config.getSetting("blowjob") == 'true':
        tag4 = "Blowjob"
    else:
        tag4 = ""


    if Config.getSetting("brunette") == 'true':
        tag5 = "Brunette"
    else:
        tag5 = ""
        
        
    if Config.getSetting("dbpen") == 'true':
        tag6 = "Double Penetration"
    else:
        tag6 = ""


    if Config.getSetting("ebony") == 'true':
        tag7 = "Ebony"
    else:
        tag7 = ""
        
        
    if Config.getSetting("handjob") == 'true':
        tag8 = "Handjob"
    else:
        tag8 = ""
        
        
    if Config.getSetting("htits") == 'true':
        tag9 = "Huge Tits"
    else:
        tag9 = ""
        

    if Config.getSetting("lesbian") == 'true':
        tag10 = "Lesbian"
    else:
        tag10 = ""
        
        
    if Config.getSetting("milf") == 'true':
        tag11 = "MILF"
    else:
        tag11 = ""


    if Config.getSetting("naturalt") == 'true':
        tag12 = "Natural Tits"
    else:
        tag12 = ""
        
        
    if Config.getSetting("redhead") == 'true':
        tag13 = "Red Head"
    else:
        tag13 = ""
        
        
    if Config.getSetting("sextoys") == 'true':
        tag14 = "Sex Toys"
    else:
        tag14 = ""


    if Config.getSetting("squirt") == 'true':
        tag15 = "Squirt"
    else:
        tag15 = ""
        
    
    if Config.getSetting("tittyfuck") == 'true':
        tag16 = "Tittyfuck"
    else:
        tag16 = ""

    return tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8,tag9,tag10,tag11,tag12,tag13,tag14,tag15,tag16



def database_reader():
    
    opciones = open(database, "r+")
    contenido = opciones.read()
    

    matches = dataparser.etiqueta_maestra(contenido, "<item>(.*?)</item>")
    for item in matches:
        NAME = dataparser.subetiqueta(item, "<name>(.*?)</name>")
        THUMB = dataparser.subetiqueta(item, "<thumb>(.*?)</thumb>")
        LINK = dataparser.subetiqueta(item, "<link>(.*?)</link>")
        id = dataparser.subetiqueta(item, "<id>(.*?)</id>")
        title_sc = dataparser.subetiqueta(item, "<title>(.*?)</title>")
        tags = dataparser.subetiqueta(item, "<tags>(.*?)</tags>")
        
                        
                    
        if Config.getSetting("engine") == '1':
            torrent = "plugin://plugin.video.pulsar/play?uri=" + str(LINK)
        else:
            torrent = "plugin://plugin.video.kmediatorrent/play/" + str(LINK)
        
        if Config.getSetting("enable_tags") == 'true':
            
            
            if Config.getSetting("anal") == 'true':
                tag1 = "Anal"
            else:
                tag1 = ""
                
        
            if Config.getSetting("blackhair") == 'true':
                tag2 = "Black Hair"
            else:
                tag2 = ""
                
                
            if Config.getSetting("blonde") == 'true':
                tag3 = "Blonde"
            else:
                tag3 = ""
                
                
            if Config.getSetting("blowjob") == 'true':
                tag4 = "Blowjob"
            else:
                tag4 = ""
        
        
            if Config.getSetting("brunette") == 'true':
                tag5 = "Brunette"
            else:
                tag5 = ""
                
                
            if Config.getSetting("dbpen") == 'true':
                tag6 = "Double Penetration"
            else:
                tag6 = ""
        
        
            if Config.getSetting("ebony") == 'true':
                tag7 = "Ebony"
            else:
                tag7 = ""
                
                
            if Config.getSetting("handjob") == 'true':
                tag8 = "Handjob"
            else:
                tag8 = ""
                
                
            if Config.getSetting("htits") == 'true':
                tag9 = "Huge Tits"
            else:
                tag9 = ""
                
        
            if Config.getSetting("lesbian") == 'true':
                tag10 = "Lesbian"
            else:
                tag10 = ""
                
                
            if Config.getSetting("milf") == 'true':
                tag11 = "MILF"
            else:
                tag11 = ""
        
        
            if Config.getSetting("naturalt") == 'true':
                tag12 = "Natural Tits"
            else:
                tag12 = ""
                
                
            if Config.getSetting("redhead") == 'true':
                tag13 = "Red Head"
            else:
                tag13 = ""
                
                
            if Config.getSetting("sextoys") == 'true':
                tag14 = "Sex Toys"
            else:
                tag14 = ""
        
        
            if Config.getSetting("squirt") == 'true':
                tag15 = "Squirt"
            else:
                tag15 = ""
                
            
            if Config.getSetting("tittyfuck") == 'true':
                tag16 = "Tittyfuck"
            else:
                tag16 = ""
        
            
            if tag1 in str(tags) and tag2 in str(tags) and tag3 in str(tags) and tag4 in str(tags) and tag5 in str(tags) and tag6 in str(tags) and tag7 in str(tags) and tag8 in str(tags) and tag9 in str(tags) and tag10 in str(tags) and tag11 in str(tags) and tag12 in str(tags) and tag13 in str(tags) and tag14 in str(tags) and tag15 in str(tags) and tag16 in str(tags):
                addLink(NAME,torrent,THUMB)
        else:
            """
            Config.setSetting("anal", 'false')
            Config.setSetting("blackhair", 'false')
            Config.setSetting("blonde", 'false')
            Config.setSetting("blowjob", 'false')
            Config.setSetting("brunette", 'false')
            Config.setSetting("dbpen", 'false')
            Config.setSetting("ebony", 'false')
            Config.setSetting("handjob", 'false')
            Config.setSetting("htits", 'false')
            Config.setSetting("lesbian", 'false')
            Config.setSetting("milf", 'false')
            Config.setSetting("naturalt", 'false')
            Config.setSetting("redhead", 'false')
            Config.setSetting("sextoys", 'false')
            Config.setSetting("squirt", 'false')
            Config.setSetting("tittyfuck", 'false')
            """
            addLink(NAME,torrent,THUMB)



######################  RUNNER  #######################



xbmctpath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmediatorrent'))
pulsarpath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.pulsar'))


if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.kmediatorrent')):
    pass
elif os.path.isfile(advert) == False and Config.getSetting("initquest") == 'true':
    ret = dialog.yesno('ZZ', 'KMediaTorrent add-on is recommended.', 'Do you want to install it?')
    if ret == True:
        Kmedia()
        dialog.ok('ZZ', 'KMediaTorrent is installed.', "Please check KMedia's configuration first.")
        Config.setSetting("initquest", 'false')
        f = open(advert,"w+")
        f.write('')
        f.close()
        sys.exit()
    else:
        Config.setSetting("initquest", 'false')
        f = open(advert,"w+")
        f.write('')
        f.close()
        pass


if os.path.isdir(xbmctpath) == True and os.path.isdir(pulsarpath) == True:
    pass
elif os.path.isdir(xbmctpath) == False and os.path.isdir(pulsarpath) == False:
    dialog.ok('ERROR', 'You need Pulsar or KMediaTorrent.')
    sys.exit()
elif os.path.isdir(xbmctpath) == True and os.path.isdir(pulsarpath) == False:
    Config.setSetting("engine", "0")
elif os.path.isdir(xbmctpath) == False and os.path.isdir(pulsarpath) == True:
    Config.setSetting("engine", "1")






def addLink(name,url,iconimage):
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty('Video', 'true')
    liz.setProperty('IsPlayable', 'true')       
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)




def run_addon():
    
    if os.path.isfile(pw) == False and Config.getSetting("pword") == "":
        dialog.ok('WARNING', 'This add-on contains [B]ADULT[/B] material,', 'you need to configure a "password" to continue.', "If you want no password please type 'nopass123'.")
        kb = xbmc.Keyboard('','Type your password:',False)
        kb.doModal()
        if (kb.isConfirmed()):
            pword = kb.getText()
            f = open(pw,"w+")
            f.write(pword)
            f.close()
            Config.setSetting("pword", pword)
        else:
            sys.exit()
    elif os.path.isfile(pw) == False and Config.getSetting("pword") != "":
        f = open(pw,"w+")
        f.write(Config.getSetting("pword"))
        f.close()
        pass
    else: pass
    

    if Config.getSetting("pword") != "nopass123" and Config.getSetting("pword") != "'nopass123'":
        kb = xbmc.Keyboard('','Type your password:',True)
        kb.doModal()
        if (kb.isConfirmed()):
            pword = kb.getText()
            with open(pw) as f:
                pwread = f.readline()
                if pword in pwread and pword != "":
                    database_reader()
                    xbmc.executebuiltin('Container.SetViewMode(500)')
                else:
                    dialog.ok('ERROR', 'Your password is incorrect.')
                    sys.exit()
        else: sys.exit()
    else: run_addon_nopass()

        

def run_addon_nopass():
    
    database_reader()
    xbmc.executebuiltin('Container.SetViewMode(500)')


def runner():
    
    try:
        with open(pw) as f:
            pwread = f.readline()
            if "nopass123" in pwread or "'nopass123'" in pwread or Config.getSetting("pword") == "nopass123" or Config.getSetting("pword") == "'nopass123'":
                run_addon_nopass()
            else:
                run_addon()
    except:
        run_addon()


updater_list = ['one','','Cancel the [B]Daily Updater[/B] and PASS']

"""
with open(update_source) as f:
    date1 = f.readline()
    if st in date1:     
        updater_list[0] = '[COLOR green][B]1/3[/B] .. UPDATE THE [B]SOURCE DATA[/B] [B][UPDATED][/B][/COLOR]'
    else:
        updater_list[0] = '[COLOR red][B]1/3[/B] .. UPDATE THE [B]SOURCE DATA[/B][/COLOR]     [I]Last: ' + date1 +'[/I]'
 

with open(update_index) as f:
    date2 = f.readline()
    if st in date2:     
        updater_list[1] = '[COLOR green][B]2/3[/B] .. UPDATE THE [B]INDEX DATA[/B] [B][UPDATED][/B][/COLOR]'
    else:
        updater_list[1] = '[COLOR red][B]2/3[/B] .. UPDATE THE [B]INDEX DATA[/B][/COLOR]     [I]Last: ' + date2 +'[/I]'


with open(timestamp) as f:
    date3 = f.readline()
    if st in date3:     
        updater_list[2] = '[COLOR green][B]3/3[/B] .. APPLY CHANGES [B][UPDATED][/B][/COLOR]'
    else:
        updater_list[2] = '[COLOR red][B]3/3[/B] .. APPLY CHANGES[/COLOR]     [I]Last: ' + date3 +'[/I]'
"""



with open(update_source) as f1:
    with open(update_index) as f2:
        with open(timestamp) as f3:
            date1 = f1.readline()
            date2 = f2.readline()
            date3 = f3.readline()
            if st in date3:
                pass
            elif st not in date1:
                updater_list[0] = '[COLOR red][B]1/3[/B] .. UPDATE THE [B]SOURCE DATA[/B][/COLOR]     [I]Last: ' + date1 +'[/I]'
            
            elif st not in date2:
                updater_list[0] = '[COLOR red][B]2/3[/B] .. UPDATE THE [B]INDEX DATA[/B][/COLOR]     [I]Last: ' + date2 +'[/I]'
                updater_list.pop()
                updater_list.pop()
            
            elif st not in date3:
                updater_list[0] = '[COLOR red][B]3/3[/B] .. APPLY CHANGES[/COLOR]     [I]Last: ' + date3 +'[/I]'
                updater_list.pop()
                updater_list.pop()


if Config.getSetting("database") == 'true':      
    if st in date1 and st in date2 and st in date3:
        runner()
    else:      
        ret = dialog.select('RUN THE 3 UPDATES', updater_list)
        
        if ret == 0 and "SOURCE" in updater_list[0]:
            source_update()
        elif ret == 0 and "INDEX" in updater_list[0]:
            offline_update()
        elif ret == 0 and "APPLY" in updater_list[0]:
            mixer()
        elif ret == 1:
            pass
        elif ret == 2:
            Config.setSetting("database",'false')
            runner()
        else:
            sys.exit()
            
        """
        if ret == 0:
            source_update()
        elif ret == 1:
            offline_update()
        elif ret == 2:
            mixer()
        elif ret == 3:
            pass
        elif ret == 4:
            runner()
        else:
            sys.exit()
        """
else:
    runner()



xbmcplugin.endOfDirectory(int(sys.argv[1]))
