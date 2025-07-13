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

## @package g_applied_voltage
#  Select the voltage to apply to a contact
#



from PySide2.QtWidgets import QMessageBox, QDialog
from PySide2.QtWidgets import QLineEdit,QWidget,QHBoxLayout,QPushButton
from gQtCore import gSignal
from QComboBoxLang import QComboBoxLang

#cal_path
from cal_path import subtract_paths
from json_c import json_tree_c

import i18n
_ = i18n.language.gettext


class g_applied_voltage(QWidget):

	changed = gSignal()

	def __init__(self,file_box=True):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.raw_value="ground"
		self.hbox=QHBoxLayout()
		self.edit=QLineEdit()
		self.combobox = QComboBoxLang()
		self.combobox.addItemLang("ground",_("Ground"))
		self.combobox.addItemLang("constant",_("Constant bias"))
		self.combobox.addItemLang("change",_("Change"))

		self.hbox.addWidget(self.combobox)
		self.hbox.addWidget(self.edit)

		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.edit.setStyleSheet("QLineEdit { border: none }");


		#self.button.clicked.connect(self.callback_button_click)
		self.combobox.currentIndexChanged.connect(self.callback_combobox)
		self.edit.textChanged.connect(self.callback_edit)
		self.setLayout(self.hbox)

	def update(self):
		self.edit.blockSignals(True)
		self.combobox.blockSignals(True)
		path=self.find_contact_path()
		applied_voltage_type=self.bin.get_token_value(path,"applied_voltage_type")
		applied_voltage=self.bin.get_token_value(path,"applied_voltage")
		self.combobox.setValue_using_english(applied_voltage_type)
		if applied_voltage_type!="ground" and applied_voltage_type!="change":
			self.edit.setEnabled(True)
			self.edit.setText(str(applied_voltage))
		else:
			self.edit.setEnabled(False)
			if applied_voltage_type=="ground":
				self.edit.setText("Gnd")
			elif applied_voltage_type=="change":
				self.edit.setText("Vsig")

		self.combobox.blockSignals(False)
		self.edit.blockSignals(False)


	def callback_edit(self):
		try:
			str(float(self.edit.text()))
		except:
			return
		path=self.find_contact_path()
		self.bin.set_token_value(path,"applied_voltage",float(self.edit.text()))
		self.changed.emit()

	def callback_combobox(self):
		path=self.find_contact_path()
		self.bin.set_token_value(path,"applied_voltage_type",self.combobox.currentText_english())
		self.update()
		self.changed.emit()

	def updateValue(self,uid):
		self.uid=uid
		self.update()

	def find_contact_path(self):
		self.contact=None
		segments=self.bin.get_token_value("epitaxy.contacts","segments")
		for l in range(0,segments):
			path="epitaxy.contacts.segment"+str(l)
			uid=self.bin.get_token_value(path,"id")
			if self.uid==uid:
				return path+".contact"
		return None

	def text(self):
		path=self.find_contact_path()
		return str(self.bin.get_token_value(path,"applied_voltage"))


