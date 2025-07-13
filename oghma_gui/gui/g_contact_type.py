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

## @package g_contact_type
#  Select the voltage to apply to a contact
#



from PySide2.QtWidgets import QMessageBox, QDialog
from PySide2.QtWidgets import QLineEdit,QWidget,QHBoxLayout,QPushButton,QLabel
from gQtCore import gSignal, Qt
from QComboBoxLang import QComboBoxLang

#cal_path
from cal_path import subtract_paths
from json_c import json_tree_c

import i18n
_ = i18n.language.gettext


class g_contact_type(QWidget):

	changed = gSignal()

	def __init__(self,contact_type):
		QWidget.__init__(self)
		self.contact_type=contact_type
		self.uid=None
		self.bin=json_tree_c()
		self.hbox=QHBoxLayout()
		self.edit=QLineEdit()
		self.units=QLabel("U")
		self.units.setTextFormat(Qt.TextFormat.RichText)
		self.combobox = QComboBoxLang()
		self.combobox.addItemLang("ohmic",_("Ohmic"))
		self.combobox.addItemLang("blocking",_("Blocking (full)"))
		self.combobox.addItemLang("ohmic_barrier",_("Ohmic+barrier"))
		self.combobox.addItemLang("schottky",_("Schottky barrier"))

		self.combobox.currentIndexChanged.connect(self.callback_combobox)
		self.edit.textChanged.connect(self.callback_edit)

		self.hbox.addWidget(self.combobox)
		self.hbox.addWidget(self.edit)
		self.hbox.addWidget(self.units)

		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.edit.setStyleSheet("QLineEdit { border: none }");
		
		self.setLayout(self.hbox)

	def update(self):
		self.edit.blockSignals(True)
		self.combobox.blockSignals(True)
		path=self.find_contact_path()
		physical_model=self.bin.get_token_value(path,self.contact_type+"_model")
		self.combobox.setValue_using_english(physical_model)
		if physical_model=="ohmic":
			self.edit.setVisible(False)
			self.units.setVisible(False)
		elif physical_model=="blocking":
			self.edit.setVisible(False)
			self.units.setVisible(False)
		elif physical_model=="ohmic_barrier":
			val=self.bin.get_token_value(path,self.contact_type+"_mu")
			self.edit.setVisible(True)
			self.edit.setText(self.bin.format_float(val))
			self.units.setVisible(True)
			self.units.setText("m<sup>2</sup> V<sup>-1</sup> s<sup>-1</sup>")
		elif physical_model=="schottky":
			val=self.bin.get_token_value(path,self.contact_type+"_v0")
			self.edit.setVisible(True)
			self.edit.setText(self.bin.format_float(val))
			self.units.setVisible(True)
			self.units.setText("m s<sup>-1</sup>")
		self.combobox.blockSignals(False)
		self.edit.blockSignals(False)


	def callback_edit(self):
		try:
			str(float(self.edit.text()))
		except:
			return

		path=self.find_contact_path()
		physical_model=self.bin.get_token_value(path,self.contact_type+"_model")

		if physical_model=="ohmic":
			pass
		elif physical_model=="blocking":
			pass
		elif physical_model=="ohmic_barrier":
			self.bin.set_token_value(path,self.contact_type+"_mu",float(self.edit.text()))
			self.changed.emit()
		elif physical_model=="schottky":
			self.bin.set_token_value(path,self.contact_type+"_v0",float(self.edit.text()))
			self.changed.emit()

		
	def callback_combobox(self):
		path=self.find_contact_path()
		self.bin.set_token_value(path,self.contact_type+"_model",self.combobox.currentText_english())
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
		return str(self.bin.get_token_value(path,"_model"))

class g_majority_contact(g_contact_type):

	def __init__(self):
		g_contact_type.__init__(self,"majority")

class g_minority_contact(g_contact_type):

	def __init__(self):
		g_contact_type.__init__(self,"minority")

