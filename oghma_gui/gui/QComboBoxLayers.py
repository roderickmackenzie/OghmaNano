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

## @package QComboBoxLayers
#  A combobox used to select layers
#
import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QSizePolicy,QComboBox
from gQtCore import gSignal
from json_c import json_tree_c

class QComboBoxLayers(QComboBox):
	
	def __init__(self):
		QComboBox.__init__(self)
		self.bin=json_tree_c()
		segments=self.bin.get_token_value("epitaxy","segments")
		for s in range(0,segments):
			path="epitaxy.segment"+str(s)
			name=self.bin.get_token_value(path,"name")
			self.addItem(name)
		self.addItem("none")
	
	def setValue(self,value):
		all_items  = [self.itemText(i) for i in range(self.count())]
		for i in range(0,len(all_items)):
			if all_items[i] == value:
				self.setCurrentIndex(i)
				break
	



