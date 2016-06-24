#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,urllib
import xbmcaddon,xbmcplugin,xbmcgui

import zipfile

def ExtractAll(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
        return False

    return True
    
def UpdateRepo():
    if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'repository.docshadrach')):
        return
        
    url = "https://github.com/XBMCSpot/docshadrach.repository/raw/master/zips/repository.docshadrach-1.0.zip"
    addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
    packageFile = os.path.join(addonsDir, 'packages', 'isr.zip')
    
    urllib.urlretrieve(url, packageFile)
    ExtractAll(packageFile, addonsDir)
        
    try:
        os.remove(packageFile)
    except:
        pass
            
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")

UpdateRepo()

Config = xbmcaddon.Addon()
dialog = xbmcgui.Dialog()

pulsarpath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.pulsar'))
xbmctpath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.xbmctorrent'))
kmediapath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmediatorrent'))
streampath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.stream'))

if os.path.isdir(pulsarpath) == False and os.path.isdir(xbmctpath) == False and os.path.isdir(kmediapath) == False and os.path.isdir(streampath) == False:
    dialog.ok('ERROR', '                                  Para utilizar este add-on,', '             necesita tener instalado algún reproductor.')
    sys.exit()
else: pass

list = []

if os.path.isdir(pulsarpath) == True:
    list.append("Pulsar")
if os.path.isdir(xbmctpath) == True:
    list.append("XBMCtorrent")
if os.path.isdir(kmediapath) == True:
    list.append("KMediaTorrent")
if os.path.isdir(streampath) == True:
    list.append("Stream")



ret = dialog.select('SELECCIONE REPRODUCTOR', list)

if ret == 0 and "Pulsar" in list[0]:
    magnet = "plugin://plugin.video.pulsar/play?uri="
    print "- PULSAR"
elif ret == 0 and "XBMCtorrent" in list[0]:
    magnet = "plugin://plugin.video.xbmctorrent/play/"
    print "- XBMCTORRENT"
elif ret == 0 and "KMediaTorrent" in list[0]:
    magnet = "plugin://plugin.video.kmediatorrent/play/"
    print "- KMEDIATORRENT"
elif ret == 0 and "Stream" in list[0]:
    magnet = "plugin://plugin.video.stream/play/"
    print "- STREAM"
elif ret == 1 and "XBMCtorrent" in list[1]:
    magnet = "plugin://plugin.video.xbmctorrent/play/"
    print "- XBMCTORRENT"
elif ret == 1 and "KMediaTorrent" in list[1]:
    magnet = "plugin://plugin.video.kmediatorrent/play/"
    print "- KMEDIATORRENT"
elif ret == 1 and "Stream" in list[1]:
    magnet = "plugin://plugin.video.stream/play/"
    print "- STREAM"
elif ret == 2 and "KMediaTorrent" in list[2]:
    magnet = "plugin://plugin.video.kmediatorrent/play/"
    print "- KMEDIATORRENT"
elif ret == 2 and "Stream" in list[2]:
    magnet = "plugin://plugin.video.stream/play/"
    print "- STREAM"
elif ret == 3 and "Stream" in list[3]:
    magnet = "plugin://plugin.video.stream/play/"
    print "- STREAM"  
else: sys.exit()

kb = xbmc.Keyboard('','Ingrese su Magnet Link',False)
kb.doModal()

if (kb.isConfirmed()):
    url = kb.getText()
else:
    sys.exit()
    
if str(url).startswith("magnet"):
    pass
elif url == "":
    dialog.ok('ERROR', 'Debe ingresar un Magnet Link.')
else:
    dialog.ok('ERROR', 'No es un Magnet Link válido.')

    
if str(url).startswith("magnet:"):
    url = urllib.quote_plus(url.encode("utf-8"))
else:
    pass


magnetlink = magnet + str(url)
    



xbmc.Player().play(magnetlink)

sys.exit()

