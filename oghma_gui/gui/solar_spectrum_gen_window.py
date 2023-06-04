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

## @package solar_main
#  Part of solar module - delete?
#
import sys
from PySide2.QtWidgets import QMenuBar, QWidget, QApplication, QAction,QDesktopWidget,QTabWidget,QVBoxLayout
from PySide2.QtGui import QIcon

import os

from ribbon_solar import ribbon_solar

from icon_lib import icon_get
from gQtCore import gSignal

from spctral2_gui import spctral2_gui

class solar_spectrum_gen_window(QWidget):

	update = gSignal()

	def __init__(self):
		self.export_file_name="data.dat"#os.path.join(self.path,"spectra.csv")
		super().__init__()
		self.resize(1200,600)
		self.setWindowIcon(icon_get("weather-few-clouds"))

		self.vbox=QVBoxLayout()

		self.ribbon = ribbon_solar()
		self.vbox.addWidget(self.ribbon)
		
		self.ribbon.run.clicked.connect(self.callback_run)

		self.ribbon.export.triggered.connect(self.callback_export)
		
		self.setWindowTitle(_("Solar Spectrum Generator"))


		self.notebook = QTabWidget()

		self.vbox.addWidget(self.notebook)
		self.spctral2_gui=spctral2_gui()
		self.notebook.addTab(self.spctral2_gui,"spctral2")
		self.setLayout(self.vbox)


	def callback_run(self):
		tab = self.notebook.currentWidget()
		tab.calculate()


	def save(self):
		self.notebook.currentWidget().save()

	def copy(self):
		self.notebook.currentWidget().copy2clip()

	def callback_export(self):
		self.notebook.currentWidget().export()



