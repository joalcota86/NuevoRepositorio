#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,urllib
import xbmcaddon,xbmcplugin,xbmcgui
import orphAddon
import repoCheck

import shutil

Config = xbmcaddon.Addon()
dialog = xbmcgui.Dialog()

Progress = xbmcgui.DialogProgress()

showed = xbmc.translatePath(os.path.join('special://home/addons/plugin.program.bestreposinstaller', 'showed'))


if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.bestreposinstaller')):
    shutil.rmtree(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.bestreposinstaller'))
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")
else: pass


def TextBoxes(heading,anounce):
    class TextBox():
        """Thanks to BSTRDMKR for this code:)"""
            # constants
        WINDOW = 10147
        CONTROL_LABEL = 1
        CONTROL_TEXTBOX = 5

        def __init__( self, *args, **kwargs):
            # activate the text viewer window
            xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
            # get window
            self.win = xbmcgui.Window( self.WINDOW )
            # give window time to initialize
            xbmc.sleep( 500 )
            self.setControls()

        def setControls( self ):
            # set heading
            self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
            try:
                f = open(anounce)
                text = f.read()
            except: text=anounce
            self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
            return
    TextBox()


def Notify():
    dir = os.path.join(xbmcaddon.Addon().getAddonInfo('path'))
    changelog = os.path.join(dir, 'changelog.txt')
    TextBoxes("[B][COLOR green]BEST REPOS INSTALLER - CHANGELOG[/B][/COLOR]",changelog)


if os.path.isfile(showed) == False and Config.getSetting("changelog") == 'true':
    f = open(showed,"w+")
    f.write("")
    f.close()
    
    Notify()
else: Config.openSettings()

repoCheck.DocRepo()


if Config.getSetting("anon") == 'true' or Config.getSetting("bromix") == 'true' or Config.getSetting("husham") == 'true' or Config.getSetting("jason") == 'true' or Config.getSetting("kinkin") == 'true' or Config.getSetting("pulsar") == 'true' or Config.getSetting("lambda") == 'true' or Config.getSetting("metal") == 'true' or Config.getSetting("shani") == 'true' or Config.getSetting("enter") == 'true' or Config.getSetting("highway") == 'true' or Config.getSetting("tknorris") == 'true' or Config.getSetting("tvaddons") == 'true' or Config.getSetting("israeli") == 'true' or Config.getSetting("xunity") == 'true':
    
    dialog.ok('BEST REPOS INSTALLER', 'Se instalarán los repositorios que has seleccionado.', '', 'Por favor, espera a que el proceso de instalación acabe.')
    Progress.create("Instalando..", "Descargando repositorios...")
    Progress.update(0)
    if Progress.iscanceled() == True:
        sys.exit()
    
    if Config.getSetting("anon") == 'true':
        repoCheck.Anon()
        Progress.update(6)
    else: pass
    
    if Config.getSetting("bromix") == 'true':
        repoCheck.Bromix()
        Progress.update(12)
    else: pass
    
    if Config.getSetting("husham") == 'true':
        repoCheck.Husham()
        Progress.update(18)
    else: pass
    
    if Config.getSetting("jason") == 'true':
        repoCheck.Jason()
        Progress.update(25)
    else: pass
    
    if Config.getSetting("kinkin") == 'true':
        repoCheck.Kinkin()
        Progress.update(32)
    else: pass
       
    if Config.getSetting("pulsar") == 'true':
        repoCheck.Pulsar()
        Progress.update(44)
    else: pass
    
    if Config.getSetting("lambda") == 'true':
        repoCheck.Lambda()
        Progress.update(50)
    else: pass
    
    if Config.getSetting("metal") == 'true':
        repoCheck.Metal()
        Progress.update(56)
    else: pass
    
    if Config.getSetting("shani") == 'true':
        repoCheck.Shani()
        Progress.update(62)
    else: pass

    if Config.getSetting("enter") == 'true':
        repoCheck.Enter()
        Progress.update(68)
    else: pass

    if Config.getSetting("highway") == 'true':
        repoCheck.Highway()
        Progress.update(74)
    else: pass
    
    if Config.getSetting("tknorris") == 'true':
        repoCheck.Tknorris()
        Progress.update(80)
    else: pass
    
    if Config.getSetting("tvaddons") == 'true':
        repoCheck.Tvaddons()
        Progress.update(86)
    else: pass
    
    if Config.getSetting("israeli") == 'true':
        repoCheck.Israeli()
        Progress.update(92)
    else: pass
    
    if Config.getSetting("xunity") == 'true':
        repoCheck.Xunity()
        Progress.update(98)
    else: pass
        
    Progress.update(100)
    dialog.ok('HECHO!', 'Repositorios instalados.')
    
else: pass


if Config.getSetting("plexus") == 'true' or Config.getSetting("latino") == 'true' or Config.getSetting("pelisalacarta") == 'true' or Config.getSetting("tvalacarta") == 'true' or Config.getSetting("kmedia") == 'true' or Config.getSetting("mashup") == 'true' or Config.getSetting("streamnation") == 'true' or Config.getSetting("bbc") == 'true':

    dialog.ok('BEST REPOS INSTALLER', 'Se instalarán los add-ons que has seleccionado.', '', 'Por favor, espera a que el proceso de instalación acabe.')
    Progress.create("Instalando..", "Descargando add-ons...")
    Progress.update(0)

    if Config.getSetting("plexus") == 'true':
        orphAddon.Plexus()
        Progress.update(10)
    else: pass

    if Config.getSetting("latino") == 'true':
        orphAddon.Latino()
        Progress.update(20)
    else: pass

    if Config.getSetting("pelisalacarta") == 'true':
        if Config.getSetting("pelisver") == '0':
            orphAddon.Pelisalacarta13()
            Progress.update(30)
        if Config.getSetting("pelisver") == '1':
            orphAddon.Pelisalacarta14()
            Progress.update(30)
        if Config.getSetting("pelisver") == '2':
            orphAddon.Pelisalacarta15()
            Progress.update(30)
    else: pass

    if Config.getSetting("tvalacarta") == 'true':
        orphAddon.TValacarta()
        Progress.update(40)
    else: pass

    if Config.getSetting("kmedia") == 'true':
        Progress.update(40, 'KMediaTorrent puede tardar mucho, NO CANCELES!')
        orphAddon.Kmedia()
        Progress.update(55, 'Descargando add-ons...')
    else: pass

    if Config.getSetting("mashup") == 'true':
        orphAddon.Mashup()
        Progress.update(70)
    else: pass

    if Config.getSetting("streamnation") == 'true':
        orphAddon.Streamnation()
        Progress.update(80)
    else: pass

    if Config.getSetting("bbc") == 'true':
        orphAddon.BBC()
        Progress.update(90)
    else: pass
    
    Progress.update(100)
    dialog.ok('HECHO!', 'Add-ons instalados.')

else: pass

Config.setSetting(id='anon', value='false')
Config.setSetting(id='bromix', value='false')
Config.setSetting(id='husham', value='false')
Config.setSetting(id='jason', value='false')
Config.setSetting(id='kinkin', value='false')
Config.setSetting(id='pulsar', value='false')
Config.setSetting(id='lambda', value='false')
Config.setSetting(id='metal', value='false')
Config.setSetting(id='shani', value='false')
Config.setSetting(id='enter', value='false')
Config.setSetting(id='highway', value='false')
Config.setSetting(id='tknorris', value='false')
Config.setSetting(id='tvaddons', value='false')
Config.setSetting(id='israeli', value='false')
Config.setSetting(id='xunity', value='false')

Config.setSetting(id='plexus', value='false')
Config.setSetting(id='latino', value='false')
Config.setSetting(id='pelisalacarta', value='false')
Config.setSetting(id='tvalacarta', value='false')
Config.setSetting(id='kmedia', value='false')
Config.setSetting(id='mashup', value='false')
Config.setSetting(id='streamnation', value='false')
Config.setSetting(id='bbc', value='false')



sys.exit()

