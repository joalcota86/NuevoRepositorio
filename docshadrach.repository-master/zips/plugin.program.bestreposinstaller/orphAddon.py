# -*- coding: utf-8 -*-
import os, urllib, xbmc, zipfile

def ExtractAll(_in, _out):
	try:
		zin = zipfile.ZipFile(_in, 'r')
		zin.extractall(_out)
	except Exception, e:
		print str(e)
		return False

	return True


def Plexus():
		
	url = "http://shadrach.pcriot.com/Add-ons/program.plexus-0.1.3.zip"
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


def Latino():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.latinototal')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/plugin.video.latinototal-0.2.0.zip"
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
	
	
def Pelisalacarta13():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.pelisalacarta')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/pelisalacarta-xbmc-gotham-4.0.3.zip"
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


def Pelisalacarta14():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.pelisalacarta')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/pelisalacarta-kodi-helix-4.0.3.zip"
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


def Pelisalacarta15():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.pelisalacarta')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/pelisalacarta-kodi-isengard-4.0.3.zip"
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


def TValacarta():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.tvalacarta')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/tvalacarta-xbmc-addon-gotham-3.9.99.zip"
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
	
	
def Kmedia():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.kmediatorrent')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/plugin.video.kmediatorrent-2.3.7.zip"
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
	
	
def Mashup():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.movie25')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/plugin.video.movie25-1.4.2.zip"
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
	
	
def Streamnation():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.streamnation')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/plugin.video.streamnation-0.7.2.zip"
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
	
	
def BBC():
	# if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'service.bbclivefootballscores')):
	#	return
		
	url = "http://shadrach.pcriot.com/Add-ons/service.bbclivefootballscores.v0.3.0rc.zip"
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
	

	




