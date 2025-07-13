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

## @package QComboBoxNewtonSelect
#  This combobox is used to select the newton solver to use.
#
import i18n
_ = i18n.language.gettext

#qt
import os
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QSizePolicy,QVBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QLabel,QComboBox
from QComboBoxLang import QComboBoxLang
from cal_path import sim_paths
from json_c import json_tree_c
from error_dlg import error_dlg


class QComboBoxNetworkInputs(QComboBox):

	def __init__(self):
		QComboBox.__init__(self)
		self.bin=json_tree_c()

	def refresh(self,uid):
		path=self.bin.find_path_by_uid("ml",uid)
		dataset_name=self.bin.get_token_value(path.split(".ml_networks")[0],"name")
		self.dataset_path=os.path.join(sim_paths.get_sim_path(),dataset_name)

		self.blockSignals(True)
		self.clear()
		file_name=os.path.join(self.dataset_path,"input_vec.txt")
		if os.path.isfile(file_name):
			file1 = open(file_name, 'r')
			all_inputs = file1.readlines()
			file1.close()
			for item in all_inputs:
				self.addItem(item.strip())
		else:
			error_dlg(self,"no file: "+file_name)

		self.blockSignals(False)

	def set_value(self,value):
		all_items  = [self.itemText(i) for i in range(self.count())]
		for i in range(0,len(all_items)):
			if all_items[i] == value:
				self.setCurrentIndex(i)
				break

	def get_value(self):
		return self.currentText()


