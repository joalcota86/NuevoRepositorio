#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,urllib
import xbmcaddon,xbmcplugin,xbmcgui
import orphAddon
import repoCheck

Config = xbmcaddon.Addon()
dialog = xbmcgui.Dialog()

Progress = xbmcgui.DialogProgress()

showed = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.bestreposinstaller', 'showed'))


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
    TextBoxes("[B][COLOR red]BEST REPOS INSTALLER - INFO[/B][/COLOR]",changelog)


Notify()

def Check():
    if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.program.bestreposinstaller')):
        return
    else:
        repoCheck.DocRepo()
        orphAddon.NewRepo()

Check()

sys.exit()

