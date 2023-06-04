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

## @package spectra_main
#  An editro for optical spectra.
#

import os
from tab import tab_class
from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget
from PySide2.QtGui import QPainter,QIcon

#python modules

from help import help_window

from plot_widget import plot_widget
from win_lin import desktop_open

from QWidgetSavePos import QWidgetSavePos

from ribbon_spectra import ribbon_spectra

from import_data_json import import_data_json
from json_spectra_db_item import json_spectra_db_item

from ref import ref_window
from bibtex import bibtex
from sim_name import sim_name

class spectra_main(QWidgetSavePos):

	def changed_click(self):

		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Refractive index"):
			b=bibtex()
			if b.load(os.path.join(self.path,"spectra.bib"))!=False:
				text=b.get_text()
				help_window().help_set_help(["spectra_file.png",_("<big><b>Spectra</b></big><br>"+text)])

	def update(self):
		self.alpha.update()

	def callback_ref(self):
		self.ref_window=ref_window(os.path.join(self.path,"spectra.csv"),"spectra")
		self.ref_window.show()

	def callback_import(self):
		self.im=import_data_json(self.data.spectra_import,export_path=self.path)
		self.im.run()
		self.update()

	def __init__(self,path):
		QWidgetSavePos.__init__(self,"spectra_main")
		self.path=path
		self.setMinimumSize(900, 600)
		self.setWindowIcon(icon_get("spectra_file"))

		self.setWindowTitle2(_("Optical spectrum editor")+" "+os.path.basename(self.path)) 
		

		self.main_vbox = QVBoxLayout()

		self.ribbon=ribbon_spectra()
		

		self.ribbon.import_data.clicked.connect(self.callback_import)
		self.ribbon.tb_ref.triggered.connect(self.callback_ref)

		self.main_vbox.addWidget(self.ribbon)

		self.notebook = QTabWidget()

		self.notebook.setMovable(True)
		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.main_vbox.addWidget(self.notebook)

		mat_file=os.path.join(self.path,"data.json")
		self.data=json_spectra_db_item()
		self.data.load(mat_file)
		self.data.spectra_import.data_file="spectra.csv"

		fname=os.path.join(self.path,"spectra.csv")
		self.alpha=plot_widget(enable_toolbar=False)
		self.alpha.set_labels([_("Spectra")])
		self.alpha.load_data([fname])

		self.alpha.do_plot()
		self.alpha.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.notebook.addTab(self.alpha,_("Spectra"))

		tab=tab_class(self.data)
		self.alpha.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.notebook.addTab(tab,_("Basic"))


		self.setLayout(self.main_vbox)
		
		self.notebook.currentChanged.connect(self.changed_click)



