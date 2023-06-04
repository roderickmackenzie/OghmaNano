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

## @package plot_widget_menu
#  The main plot widget menu
#

from __future__ import unicode_literals

from PySide2.QtWidgets import QMenu
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView, QMenuBar,QApplication
from PySide2.QtGui import QPainter,QIcon,QImage

from icon_lib import icon_get
from lock import get_lock

class plot_widget_menu(QWidget):

	def menu_build(self):
		self.main_menu = QMenu(self)
		sub_icon=None
		if get_lock().encode_output==True:
			sub_icon="lock"

		clipboard=self.main_menu.addMenu(icon_get("edit-copy"),_("Copy"))

		action=clipboard.addAction(icon_get("image-x-generic"),_("Image"))
		action.triggered.connect(self.callback_do_clip)

		save_as=self.main_menu.addMenu(_("Save as"))
		action=save_as.addAction(icon_get("edit-copy"),_("Image"))
		action.triggered.connect(self.callback_save_image)

		#export
		action=save_as.addAction(icon_get("export_gnuplot",sub_icon=sub_icon),_("Gnuplot"))
		action.triggered.connect(self.callback_save_gnuplot)

		action=save_as.addAction(icon_get("export_csv",sub_icon=sub_icon),_("Csv"))
		action.triggered.connect(self.callback_save_csv)

		action=save_as.addAction(icon_get("text-x-generic",sub_icon=sub_icon),_("Text file (txt)"))
		action.triggered.connect(self.callback_save_txt)

		action=save_as.addAction(icon_get("wps-office-xls",sub_icon=sub_icon),_("MS Excel (xlsx)"))
		action.triggered.connect(self.callback_save_xlsx)

		graph=self.main_menu.addMenu(_("Graph"))
		self.menu_show_title=graph.addAction(_("Show title"))
		self.menu_show_title.setCheckable(True)
		self.menu_show_title.setChecked(self.show_title)
		self.menu_show_title.triggered.connect(self.callback_hide_show_title)

		self.menu_show_key=graph.addAction(_("Show key"))
		self.menu_show_key.setCheckable(True)
		self.menu_show_key.setChecked(True)
		self.menu_show_key.triggered.connect(self.callback_hide_show_key)



	def callback_hide_show_title(self):
		self.show_title=self.menu_show_title.isChecked()
		self.do_plot()

	def callback_hide_show_key(self):
		self.show_key=self.menu_show_key.isChecked()
		self.do_plot()
