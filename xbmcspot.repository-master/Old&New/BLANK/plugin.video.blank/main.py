
import os
import xbmcaddon, xbmcgui


file = os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'LEER.txt')

dialog = xbmcgui.Dialog()

texto = str(file)

tupla = texto.partition("XBMC")


dialog.ok('Encuentra las instrucciones en:', str(tupla[0]), str(tupla[1]) + str(tupla[2]), "[COLOR ff708090]- - - - [I]version 1.1 (ver cambios en changelog.txt)[/I][/COLOR]")

sys.exit()

