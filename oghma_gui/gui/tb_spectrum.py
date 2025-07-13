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

## @package tb_spectrum
#  Select which solar spectrum to use.
#


from tab import tab_class

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QTabWidget,QSystemTrayIcon,QMenu, QComboBox, QLabel
from PySide2.QtGui import QIcon

from materials_io import find_db_items
from cal_path import sim_paths

class tb_spectrum(QComboBox):

	def __init__(self):
		QComboBox.__init__(self)
		self.update()

	def set_value(self,val):
		self.setCurrentIndex(self.findText(val))

	def get_value(self):
		return self.currentText()

	def update(self):
		self.blockSignals(True)
		models=find_db_items(sim_paths.get_spectra_path(),file_type="spectra")

		for i in range(0, len(models)):
			self.addItem(models[i])
	
		self.blockSignals(False)
