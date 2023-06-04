# -*- coding: utf-8 -*-
#
#   OghmaNano - Organic and hybrid Material Nano Simulation tool
#   Copyright (C) 2008-2022 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
#
#   https://www.oghma-nano.com
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#   SOFTWARE.
#

## @package status_icon
#  The status icon.
#


from win_lin import get_platform

import i18n
_ = i18n.language.gettext

from gui_enable import gui_get
if gui_get()==True:
	from PySide2.QtWidgets import QSystemTrayIcon,QMenu,QApplication
	from about import about_dlg
	import webbrowser
	from icon_lib import icon_get

from cluster import cluster
from sim_name import sim_name


statusicon = None

if gui_get()==True:
	class tray_icon(QSystemTrayIcon):

		def __init__(self,  parent=None):
			QSystemTrayIcon.__init__(self, icon_get("ball_green"), parent)
			menu = QMenu(parent)
			self.menu_about = menu.addAction(_("About"))
			self.menu_about.triggered.connect(self.callback_about)
			self.menu_man = menu.addAction(_("Manual"))
			self.menu_man.triggered.connect(self.callback_man)

			self.menu_youtube = menu.addAction("&"+_("Youtube channel"))
			self.menu_youtube.triggered.connect(self.callback_youtube)

			self.exitAction = menu.addSeparator()		
			self.exitAction = menu.addAction(_("Quit"))
			
			self.exitAction.triggered.connect(self.callback_exit)
			self.setContextMenu(menu)

		def callback_exit(self):
			QApplication.quit()

		def callback_about(self):
			dlg=about_dlg()
			dlg.exec_()

		def callback_man(self):
			webbrowser.open(sim_name.web+"/man.html")

		def	callback_youtube(self):
			webbrowser.open("https://www.youtube.com/channel/UCbm_0AKX1SpbMMT7jilxFfA")


def status_icon_init():
	if gui_get()==True:
		global statusicon
		statusicon=tray_icon()
		statusicon.show()

def status_icon_run(cluster):
	if gui_get()==True:
		global statusicon
		if cluster==False:
			statusicon.setIcon(icon_get("ball_red"))
		else:
			statusicon.setIcon(icon_get("ball_red4"))

def status_icon_stop(cluster):
	if gui_get()==True:
		global statusicon
		if cluster==False:
			statusicon.setIcon(icon_get("ball_green"))
		else:
			statusicon.setIcon(icon_get("ball_green4"))

def status_icon_get():
	if gui_get()==True:
		global statusicon
		return statusicon
