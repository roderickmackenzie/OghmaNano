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

## @package tb_pulse_load_type
#  tool bar item to select the type of load to have on a pulsed simulation.
#


#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QLabel,QComboBox
from gQtCore import gSignal
from json_c import json_tree_c

class tb_pulse_load_type(QWidget):

	changed = gSignal()

	def __init__(self,json_search_path,uid):
		QWidget.__init__(self)
		self.json_search_path=json_search_path
		self.uid=uid

		self.bin=json_tree_c()
		layout=QHBoxLayout()
		label=QLabel()
		label.setText(_("Load type")+":")
		layout.addWidget(label)

		self.sim_mode = QComboBox(self)
		self.sim_mode.setEditable(True)

		layout.addWidget(self.sim_mode)

		self.setLayout(layout)

		self.sim_mode.addItem("open_circuit")
		self.sim_mode.addItem("load")
		self.sim_mode.addItem("ideal_diode_ideal_load")

		json_path=self.refind_json_path()
		mode=self.bin.get_token_value(json_path+".config","load_type")
		all_items  = [self.sim_mode.itemText(i) for i in range(self.sim_mode.count())]
		for i in range(0,len(all_items)):
		    if all_items[i] == mode:
		        self.sim_mode.setCurrentIndex(i)

		self.sim_mode.currentIndexChanged.connect(self.call_back_sim_mode_changed)

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid(self.json_search_path,self.uid)
		return ret

	def call_back_sim_mode_changed(self):
		mode=self.sim_mode.currentText()
		json_path=self.refind_json_path()
		self.bin.set_token_value(json_path+".config","load_type",mode)
		self.bin.save()
		self.changed.emit()

