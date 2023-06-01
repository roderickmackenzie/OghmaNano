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

## @package scripts
#  The main script editor
#


import os
from icon_lib import icon_get
from tab import tab_class
from help import my_help_class

#path
#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QSystemTrayIcon, QComboBox, QLabel
from PySide2.QtGui import QIcon

#windows
from QWidgetSavePos import QWidgetSavePos

from ribbon_simulation_notes import ribbon_simulation_notes

from css import css_apply
from gui_util import yes_no_dlg
from script_editor import script_editor
from json_root import json_root
from ref import ref_window
from cal_path import sim_paths
from tab import tab_class
 
class window_simulation_notes(QWidgetSavePos):

	def __init__(self,path="",api_callback=None):

		QWidgetSavePos.__init__(self,"simulation_notes")

		self.setWindowIcon(icon_get("script"))

		self.setMinimumSize(1000, 600)
		self.setWindowTitle2(_("Simulation notes"))    

		self.ribbon=ribbon_simulation_notes()

		data=json_root()

		self.setWindowIcon(icon_get("script"))

		self.main_vbox=QVBoxLayout()

		self.ribbon.tb_save.clicked.connect(self.callback_save)

		#self.ribbon.tb_rename.clicked.connect(self.callback_rename_page)

		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

		self.main_vbox.addWidget(self.ribbon)
		self.api_callback=api_callback


		self.notebook = QTabWidget()
		css_apply(self.notebook,"tab_default.css")
		self.notebook.setMovable(True)

		#file_name=os.path.join(self.path,f)
		a=script_editor()
		a.api_callback=self.api_callback
		a.setText(data.sim.notes)
		a.status_changed.connect(self.callback_tab_changed)
		a.save_signal.connect(self.callback_save)
		self.notebook.addTab(a,_("Notes"))

		self.ref_window=ref_window(os.path.join(sim_paths.get_sim_path(),"json.bib"),"device",show_toolbar=False)
		self.notebook.addTab(self.ref_window,_("Bibtex reference"))

		self.config_window=tab_class(data)
		self.notebook.addTab(self.config_window,_("Config"))

		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.main_vbox.addWidget(self.notebook)


		self.setLayout(self.main_vbox)

	def callback_tab_changed(self):
		tab = self.notebook.currentWidget()
		index=self.notebook.currentIndex() 

		#short_name=os.path.basename(tab.file_name)

		if tab.not_saved==True:
			self.notebook.setTabText(index, _("Simulation Notes")+"*")
		else:
			self.notebook.setTabText(index, _("Simulation Notes"))

	def callback_save(self):
		tab = self.notebook.currentWidget()
		if type(tab)==script_editor:
			data=json_root()
			data.sim.notes=tab.getText()
			data.save()
			tab.not_saved=False
			self.callback_tab_changed()

		
	def callback_run(self):
		tab = self.notebook.currentWidget()
		tab.run()

