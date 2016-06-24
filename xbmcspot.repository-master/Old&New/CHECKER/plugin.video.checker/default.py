#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,urllib2,os,re,shutil,sys
import xbmcaddon,xbmcplugin,xbmcgui
import dataparser
import time,datetime

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Hh%Mm')
dir = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')


Config = xbmcaddon.Addon()

Progress = xbmcgui.DialogProgress()

dialog = xbmcgui.Dialog()

path = os.path.join(xbmcaddon.Addon().getAddonInfo('path')) + "\\checklogs\\"

dailydir = path + '\\' + dir + '\\'

if not os.path.exists(path):
    os.makedirs(path)

if not os.path.exists(dailydir):
    os.makedirs(dailydir)

file = dailydir + st + "_checked.txt"

print "PATH " + path


folders = list(os.listdir(path))

if Config.getSetting("checklogs") == 'true':
    x = 0 
    for x in range(0,len(folders)):
        if folders[x] == dir:
            x +=1
            pass
        else:
            shutil.rmtree(path + '\\' + folders[x])
            x +=1
else: pass



def addLink(name,url,iconimage):
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)



def plx_parser(masterurl,pages):
    
    try:
        
        f = open(file,"w+")
        
        f.write("- LISTA DE ENLACES CAIDOS:\n")
        f.write("\n")
    
        page = 1
        
        if re.match(".*navixtreme.*", masterurl):
            pass
        else:
            pages = 1
        
        
        Progress.create("Chequeando..", "Comprobando enlaces caídos...")
        Progress.update(0)
        
        
        while page <= int(pages):
            
            if page <= int(pages):
                percent = ((float(page)-1) / int(pages)) * 100
                message = "Página " + str(page) + " de " + str(pages)
                Progress.update(int(percent), "", "", message )
                xbmc.sleep( 1000 )
            
                if re.match(".*navixtreme.*", masterurl):
                    url = masterurl + "?page=" + str(page)
                    print "MASTER " + url
                else:
                    url = masterurl
                    print "MASTER " + url
            
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link = response.read()
                response.close()    
                
                block = re.split(r"type=video", link)
                
                for i in range(1,len(block)):
                    names = re.findall('\nname=(.*)', block[i])
                    names = [r.replace('\r', '') for r in names]
                    try:
                        del names[1]
                    except:
                        pass
                    thumbs = re.findall('\nthumb=(.*)', block[i])
                    thumbs = [r.replace('\r', '') for r in thumbs]
                    urls = re.findall('\nURL=(.*)', block[i])
                    urls = [r.replace('\r', '') for r in urls]
                    try:
                        del urls[1]
                    except:
                        pass
                    try:
                        name = names[0]
                        thumb = thumbs[0]
                        url = urls[0]
                    except:
                        name = names[0]
                        thumb = ""
                        url = urls[0]
                    if re.match(".*allmyvideos.*", url.lower()):
                        # print url
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()            
                        match = re.compile('The file you were looking for could not be found, (.+?).').findall(link)
                        # print "THIS" + str(match)
                        for yes in match:
                            if yes != "":
                                addLink(name + "[COLOR red] [broken] [/COLOR][COLOR ff6495ed]allmyvideos[/COLOR]", url, thumb)
                                f.write("* " + name + " [broken]\n")
                                f.write("url: " + url + "\n")
                                f.write("\n")
                            else: pass
                    elif re.match(".*streamcloud.*", url.lower()):
                        # print url
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()            
                        match = re.compile('<h1>(.+?) Not Found</h1>').findall(link)
                        # print "THIS" + str(match)
                        for yes in match:
                            if yes != "":
                                addLink(name + "[COLOR red] [broken] [/COLOR][COLOR cadetblue]streamcloud[/COLOR]", url, thumb)
                                f.write("* " + name + " [broken]\n")
                                f.write("url: " + url + "\n")
                                f.write("\n")
                            else: pass
                    elif re.match(".*played.to.*", url.lower()):
                        # print url
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()            
                        match = re.compile('<b class="err" style=".+?">Removed (.+?).</b>').findall(link)
                        # print "THIS" + str(match)
                        for yes in match:
                            if yes != "":
                                addLink(name + "[COLOR red] [broken] [/COLOR][COLOR ff9acd32]played.to[/COLOR]", url, thumb)
                                f.write("* " + name + " [broken]\n")
                                f.write("url: " + url + "\n")
                                f.write("\n")
                            else: pass
                    elif re.match(".*nowvideo.*", url.lower()):
                        # print url
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()            
                        match = re.compile('<h3>(.+?) no longer exists on our servers.</h3>').findall(link)
                        # print "THIS" + str(match)
                        for yes in match:
                            if yes != "":
                                addLink(name + "[COLOR red] [broken] [/COLOR][COLOR gold]nowvideo[/COLOR]", url, thumb)
                                f.write("* " + name + " [broken]\n")
                                f.write("url: " + url + "\n")
                                f.write("\n")
                            else: pass
                    elif re.match(".*vidspot.*", url.lower()):
                        # print url
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()            
                        match = re.compile('<b>(.+?) Not Found</b>').findall(link)
                        # print "THIS" + str(match)
                        for yes in match:
                            if yes != "":
                                addLink(name + "[COLOR red] [broken] [/COLOR][COLOR ff0000cd]vidspot[/COLOR]", url, thumb)
                                f.write("* " + name + " [broken]\n")
                                f.write("url: " + url + "\n")
                                f.write("\n")
                            else: pass
                    elif re.match(".*vk.com.*", url.lower()):
                        try:
                            # print url
                            if re.match(".*m.vk.com/video[0-9].*", url.lower()):
                                addLink(name + "[COLOR darkorange] [untestable] [/COLOR][COLOR skyblue]VK MOVIL[/COLOR]", url, thumb)
                                f.write("* " + name + " [untestable]\n")
                                f.write("url: " + url + "\n")
                                f.write("\n")
                            else:
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link = response.read()
                                response.close()            
                                match = re.compile('(.+?) has been removed').findall(link)
                                # print "THIS" + str(match)
                                for yes in match:
                                    if yes != "":
                                        addLink(name + "[COLOR red] [broken] [/COLOR][COLOR lightsteelblue]VK[/COLOR]", url, thumb)
                                        f.write("* " + name + " [broken]\n")
                                        f.write("url: " + url + "\n")
                                        f.write("\n")
                                    else: pass
                        except:
                            # print url
                            # print "[ERROR]"
                            addLink(name + "[COLOR yellow] [BLOCKED] [/COLOR][COLOR skyblue]VK MOVIL[/COLOR]", url, thumb)
                            f.write("* " + name + " [BLOCKED]\n")
                            f.write("url: " + url + "\n")
                            f.write("\n")
                    elif re.match(".*youtube.*", url.lower()):
                        pass
                    else:
                        print "OUTSIDE " + url
                        server = url.split("/")
                        if Config.getSetting("notsupp") == 'true':
                            addLink(name + "[COLOR hotpink] [notSUPP] [/COLOR]" + "[COLOR antiquewhite]" + server[2] + "[/COLOR]", url, thumb)
                            f.write("* " + name + " [notSUPP]\n")
                            f.write("url: " + url + "\n")
                            f.write("\n")
                        else:
                            pass
            page += 1
        f.close()

    except:
        Progress.close()
        error = dialog.ok('ERROR', 'La URL no es válida o la página está caída.')
        if error == True:
            sett = Config.openSettings()
            sys.exit()            
        else:
            sys.exit()
            


def xml_parser(masterurl):
    
    try:
    
        f = open(file,"w+")
    
        f.write("- LISTA DE ENLACES CAIDOS:\n")
        f.write("\n")
           
        req = urllib2.Request(masterurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        matches = dataparser.etiqueta_maestra(link, "<item>(.*?)</item>")
        for item in matches:
            name = dataparser.subetiqueta(item, "<title>(.*?)</title>")
            url = dataparser.subetiqueta(item, "<link>(.*?)</link>")
            thumb = dataparser.subetiqueta(item, "<thumbnail>(.*?)</thumbnail>")
            if url == "":
                pass
            else:
                if re.match(".*allmyvideos.*", url.lower()):
                    # print url
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                    response = urllib2.urlopen(req)
                    link = response.read()
                    response.close()            
                    match = re.compile('The file you were looking for could not be found, (.+?).').findall(link)
                    # print "THIS" + str(match)
                    for yes in match:
                        if yes != "":
                            addLink(name + "[COLOR red] [broken] [/COLOR][COLOR ff6495ed]allmyvideos[/COLOR]", url, thumb)
                            f.write("* " + name + " [broken]\n")
                            f.write("url: " + url + "\n")
                            f.write("\n")
                        else: pass
                elif re.match(".*streamcloud.*", url.lower()):
                    # print url
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                    response = urllib2.urlopen(req)
                    link = response.read()
                    response.close()            
                    match = re.compile('<h1>(.+?) Not Found</h1>').findall(link)
                    # print "THIS" + str(match)
                    for yes in match:
                        if yes != "":
                            addLink(name + "[COLOR red] [broken] [/COLOR][COLOR cadetblue]streamcloud[/COLOR]", url, thumb)
                            f.write("* " + name + " [broken]\n")
                            f.write("url: " + url + "\n")
                            f.write("\n")
                        else: pass
                elif re.match(".*played.to.*", url.lower()):
                    # print url
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                    response = urllib2.urlopen(req)
                    link = response.read()
                    response.close()            
                    match = re.compile('<b class="err" style=".+?">Removed (.+?).</b>').findall(link)
                    # print "THIS" + str(match)
                    for yes in match:
                        if yes != "":
                            addLink(name + "[COLOR red] [broken] [/COLOR][COLOR ff9acd32]played.to[/COLOR]", url, thumb)
                            f.write("* " + name + " [broken]\n")
                            f.write("url: " + url + "\n")
                            f.write("\n")
                        else: pass
                elif re.match(".*nowvideo.*", url.lower()):
                    # print url
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                    response = urllib2.urlopen(req)
                    link = response.read()
                    response.close()            
                    match = re.compile('<h3>(.+?) no longer exists on our servers.</h3>').findall(link)
                    # print "THIS" + str(match)
                    for yes in match:
                        if yes != "":
                            addLink(name + "[COLOR red] [broken] [/COLOR][COLOR gold]nowvideo[/COLOR]", url, thumb)
                            f.write("* " + name + " [broken]\n")
                            f.write("url: " + url + "\n")
                            f.write("\n")
                        else: pass
                elif re.match(".*vidspot.*", url.lower()):
                    # print url
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                    response = urllib2.urlopen(req)
                    link = response.read()
                    response.close()            
                    match = re.compile('<b>(.+?) Not Found</b>').findall(link)
                    # print "THIS" + str(match)
                    for yes in match:
                        if yes != "":
                            addLink(name + "[COLOR red] [broken] [/COLOR][COLOR ff0000cd]vidspot[/COLOR]", url, thumb)
                            f.write("* " + name + " [broken]\n")
                            f.write("url: " + url + "\n")
                            f.write("\n")
                        else: pass
                elif re.match(".*vk.com.*", url.lower()):
                    try:
                        # print url
                        if re.match(".*m.vk.com/video[0-9].*", url.lower()):
                            addLink(name + "[COLOR darkorange] [untestable] [/COLOR][COLOR skyblue]VK MOVIL[/COLOR]", url, thumb)
                            f.write("* " + name + " [untestable]\n")
                            f.write("url: " + url + "\n")
                            f.write("\n")
                        else:
                            req = urllib2.Request(url)
                            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                            response = urllib2.urlopen(req)
                            link = response.read()
                            response.close()            
                            match = re.compile('(.+?) has been removed').findall(link)
                            # print "THIS" + str(match)
                            for yes in match:
                                if yes != "":
                                    addLink(name + "[COLOR red] [broken] [/COLOR][COLOR lightsteelblue]VK[/COLOR]", url, thumb)
                                    f.write("* " + name + " [broken]\n")
                                    f.write("url: " + url + "\n")
                                    f.write("\n")
                                else: pass
                    except:
                        # print url
                        # print "[ERROR]"
                        addLink(name + "[COLOR yellow] [BLOCKED] [/COLOR][COLOR skyblue]VK MOVIL[/COLOR]", url, thumb)
                        f.write("* " + name + " [BLOCKED]\n")
                        f.write("url: " + url + "\n")
                        f.write("\n")
                elif re.match(".*youtube.*", url.lower()):
                        pass
                else:
                    print "OUTSIDE " + url
                    server = url.split("/")
                    if Config.getSetting("notsupp") == 'true':
                        addLink(name + "[COLOR hotpink] [notSUPP] [/COLOR]" + "[COLOR antiquewhite]" + server[2] + "[/COLOR]", url, thumb)
                        f.write("* " + name + " [notSUPP]\n")
                        f.write("url: " + url + "\n")
                        f.write("\n")
                    else:
                        pass
        f.close()

    except:
        error = dialog.ok('ERROR', 'La URL no es válida o la página está caída.')
        if error == True:
            sett = Config.openSettings()
            sys.exit()            
        else:
            sys.exit()


masterurl = Config.getSetting("url")
pages = Config.getSetting("pages")


if Config.getSetting("eraselogs") == 'true':
    shutil.rmtree(path)
    Config.setSetting("eraselogs",'false')
    dialog.ok('INFO', 'CheckLogs borrados con éxito.')
    sys.exit()
else: pass


if masterurl == "":
    error = dialog.ok('ERROR', 'Debe ingresar una URL en la configuración.')
    if error == True:
        sett = Config.openSettings()
        sys.exit()            
    else:
        sys.exit()
elif Config.getSetting("tipo") == '1':
    plx_parser(masterurl,pages)
else:
    xml_parser(masterurl)
                


xbmcplugin.endOfDirectory(int(sys.argv[1]))
