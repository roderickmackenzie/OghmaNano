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

## @package pl_main
#  PL editing window
#


from tab_base import tab_base
from tab import tab_class
from global_objects import global_object_register

#qt5
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QMessageBox,QTabWidget
from about import about_dlg

#windows
from QHTabBar import QHTabBar
from icon_lib import icon_get

from css import css_apply
from json_root import json_root
from help import QAction_help
from sim_name import sim_name
from ribbon_page import ribbon_page

class pl_main(QWidget,tab_base):

	def __init__(self):
		QWidget.__init__(self)
		self.main_vbox = QVBoxLayout()

		self.setWindowIcon(icon_get("preferences-system"))

		self.setWindowTitle(_("Luminescence editor")+sim_name.web_window_title) 

		self.setMinimumSize(1000, 600)
		toolbar=ribbon_page()
		#toolbar.setIconSize(QSize(48, 48))

		self.tb_pl_enabled = QAction(icon_get("emission"), _("Optical\nEmission"), self)
		self.tb_pl_enabled.setCheckable(True)
		self.tb_pl_enabled.triggered.connect(self.callback_pl_enabled)
		toolbar.addAction(self.tb_pl_enabled)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		toolbar.addWidget(spacer)


		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)

		self.notebook = QTabWidget()
		if len(json_root().epi.layers)>8:
			self.tab_bar=QHTabBar()
			css_apply(self.notebook,"style_h.css")
			self.notebook.setTabBar(self.tab_bar)
			self.notebook.setTabPosition(QTabWidget.West)
		else:
			css_apply(self,"tab_default.css")

		self.main_vbox.addWidget(self.notebook)
		self.setLayout(self.main_vbox)


		global_object_register("pl_update",self.update)
		self.notebook.currentChanged.connect(self.changed_click)
		self.update()

	def update(self):
		self.notebook.clear()
		epi=json_root().epi

		for l in epi.layers:
			if l.layer_type=="active":

				widget=tab_class(l.shape_pl)

				self.notebook.addTab(widget,l.name)

	def help(self):
		help_window().help_set_help(["tab.png",_("<big><b>Luminescence</b></big>\nIf you set 'Turn on luminescence' to true, the simulation will assume recombination is a raditave process and intergrate it to produce Voltage-Light intensity curves (lv.dat).  Each number in the tab tells the model how efficient each recombination mechanism is at producing photons.")])

	def changed_click(self):
		data=json_root()

		tab = self.notebook.currentWidget()
		if tab==None:
			return
		tab.tab.refind_template_widget()
		self.tb_pl_enabled.setChecked(tab.tab.template_widget.pl_emission_enabled)


	def callback_pl_enabled(self):
		data=json_root()
		tab = self.notebook.currentWidget()
		tab.tab.refind_template_widget()
		tab.tab.template_widget.pl_emission_enabled=self.tb_pl_enabled.isChecked()

		tab.tab.hide_show_widgets()
		data.save()

