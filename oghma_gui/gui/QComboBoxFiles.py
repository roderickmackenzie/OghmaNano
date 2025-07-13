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

## @package QComboBoxFiles
#  A combobox used to select layers
#
import os
import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QSizePolicy,QComboBox
from gQtCore import gSignal

class QComboBoxFiles(QComboBox):
	
	def __init__(self):
		QComboBox.__init__(self)
		self.path=None
	
	def update(self):
		self.blockSignals(True)
		self.clear()

		all_files=[]
		print(self.path,os.listdir(self.path))
		if os.path.isdir(self.path)==True:
			for name in os.listdir(self.path):
				full_path=os.path.join(self.path, name)

				if os.path.isfile(full_path):
					if name!="data.json":
						all_files.append(name)

		all_files.sort()
		
		for a in all_files:
			self.addItem(a)

		#for i in range(0,len(all_files)):
		#	if all_files[i] == "Jn.csv":
		#		self.setCurrentIndex(i)

		self.blockSignals(False)

	def setValue(self,value):
		all_items  = [self.itemText(i) for i in range(self.count())]
		for i in range(0,len(all_items)):
			if all_items[i] == value:
				self.setCurrentIndex(i)
				break
	



