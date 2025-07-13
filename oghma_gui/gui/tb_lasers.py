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

## @package tb_lasers
#  Toolbar item to select the type of laser a user wants.
#


import i18n
_ = i18n.language.gettext

#qt
from gQtCore import gSignal
from PySide2.QtWidgets import  QTextEdit
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox
from json_c import json_tree_c

class tb_lasers(QWidget):

	laser_changed = gSignal(str)

	def update(self,laser_name):
		if type(laser_name)!=str:
			print("ERROR in tb_lasers!")
			asdads
		self.sim_mode.blockSignals(True)
		self.sim_mode.clear()

		segments=self.bin.get_token_value("optical.lasers","segments")

		for i in range(0,segments):
			name=self.bin.get_token_value("optical.lasers.segment"+str(i),"name")
			name=name.rstrip()
			self.sim_mode.addItem(name)

		all_items  = [self.sim_mode.itemText(i) for i in range(self.sim_mode.count())]

		for i in range(0,len(all_items)):
			if all_items[i] == laser_name:
				self.sim_mode.setCurrentIndex(i)

		self.sim_mode.blockSignals(False)

	def __init__(self):

		QWidget.__init__(self)
		layout=QVBoxLayout()
		label=QLabel()
		label.setText(_("Laser:"))
		layout.addWidget(label)
		self.bin=json_tree_c()

		self.sim_mode = QComboBox(self)
		self.sim_mode.setEditable(True)

		self.sim_mode.currentIndexChanged.connect(self.call_back_sim_mode_changed)

		layout.addWidget(self.sim_mode)

		self.setLayout(layout)

		return

	def call_back_sim_mode_changed(self):
		mode=self.sim_mode.currentText()
		self.laser_changed.emit(mode)

