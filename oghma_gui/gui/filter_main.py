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

## @package filter_main
#  Dialog to show information about a filters
#

import os
from tab import tab_class
from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QDialog
from PySide2.QtGui import QPainter,QIcon

from help import help_window

from win_lin import desktop_open

from ref import ref_window

from g_open import g_open

from QWidgetSavePos import QWidgetSavePos
from plot_widget import plot_widget

from ribbon_emission_db import ribbon_emission_db
from ribbon_filter_db import ribbon_filter_db
from import_data_json import import_data_json
from equation_editor import equation_editor
from json_filter_db_item import json_filter_db_item

class filter_main(QWidgetSavePos):

	def changed_click(self):
		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Filters"):
			help_window().help_set_help(["filter_wheel.png",_("<big><b>Filters</b></big><br>Use this tab to edit the optical filters")])
			self.ribbon.tb_save.setEnabled(True)
			self.ribbon.import_data.setEnabled(True)


	def __init__(self,path):
		QWidgetSavePos.__init__(self,"filter_main")
		self.path=path
		self.setFixedSize(900, 600)
		self.setWindowIcon(icon_get("filter_wheel"))

		self.setWindowTitle2(_("Filter editor")+" "+os.path.basename(self.path)) 
		

		self.main_vbox = QVBoxLayout()

		self.ribbon=ribbon_emission_db()
		
		self.ribbon.import_data.clicked.connect(self.import_data)
		self.ribbon.equation.clicked.connect(self.callback_equation_editor)

		self.ribbon.tb_ref.triggered.connect(self.callback_ref)

		self.main_vbox.addWidget(self.ribbon)

		self.notebook = QTabWidget()

		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)

		fname=os.path.join(self.path,"filter.csv")
		self.emission=plot_widget(enable_toolbar=False)
		self.emission.set_labels([_("Filter")])
		self.emission.load_data([fname])

		self.emission.do_plot()
		self.notebook.addTab(self.emission,_("Filter"))


		mat_file=os.path.join(self.path,"data.json")
		self.data=json_filter_db_item()
		self.data.load(mat_file)
		self.data.filter_import.data_file="filter.csv"

		tab=tab_class(self.data,data=self.data)
		self.notebook.addTab(tab,_("Basic"))

		self.setLayout(self.main_vbox)
		
		self.notebook.currentChanged.connect(self.changed_click)

	def callback_equation_editor(self):

		file_name="spectra.csv"
		equation_file="spectra_eq.inp"
		data_label="Emission"
		data_units="au"


		os.path.join(self.path,file_name)
		os.path.join(self.path,file_name+"import.inp")

		self.equation_editor=equation_editor(self.path,equation_file,file_name)
		self.equation_editor.data_written.connect(self.update)

		self.equation_editor.data.y_label="Wavelength"
		self.equation_editor.data.data_label=data_label

		self.equation_editor.data.y_units="nm"
		self.equation_editor.data.data_units=data_units
		self.equation_editor.load()

		self.equation_editor.show()

	def import_data(self):
		self.im=import_data_json(self.data.filter_import,export_path=self.path)
		self.im.run()
		self.update()
		self.data.save()

	def update(self):
		self.emission.update()

	def callback_ref(self):
		file_name=None
		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Filter"):
			file_name="filter.bib"

		if file_name!=None:
			self.ref_window=ref_window(os.path.join(self.path,file_name),"filter")
			self.ref_window.show()

