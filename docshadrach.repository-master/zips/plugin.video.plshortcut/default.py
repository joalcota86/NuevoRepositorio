#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,os
import xbmc,xbmcaddon,xbmcgui,xbmcplugin

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

istreampath = xbmc.translatePath(os.path.join('special://home/addons/script.icechannel'))

if os.path.isdir(istreampath) == False:
    dialog.ok('ERROR', 'Needs iStream to work. Get it at XunityTalk.')
    sys.exit()
else: pass

if Config.getSetting("playlisturl") != "":
    url = Config.getSetting("playlisturl")
else:
    Config.openSettings()
    url = Config.getSetting("playlisturl")


if Config.getSetting("format") == '0':
    format = "xml"
elif Config.getSetting("format") == '1':
    format = "plx"
  

if url:
    xbmc.executebuiltin('ActivateWindow(10025,plugin://script.icechannel/?name=Any&amp;img=&amp;title=Any&amp;fanart=&amp;section=file_stores&amp;format=xbmc'+format+'&amp;indexer=file_stores&amp;url='+urllib.quote_plus(url.encode("utf-8"))+'&amp;mode=read_file_item&amp;format_display_name=XBMC+'+format.upper()+'&amp;type=playlist,return)')
else:
    sys.exit()

xbmcplugin.endOfDirectory(int(sys.argv[1]))

