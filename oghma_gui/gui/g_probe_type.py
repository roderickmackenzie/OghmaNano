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

## @package g_probe_type
#  Select the voltage to apply to a contact
#



from PySide2.QtWidgets import QMessageBox, QDialog
from PySide2.QtWidgets import QLineEdit,QWidget,QHBoxLayout,QPushButton,QLabel
from gQtCore import gSignal
from QComboBoxLang import QComboBoxLang

#cal_path
from cal_path import subtract_paths
from json_c import json_tree_c

import i18n
_ = i18n.language.gettext


class g_probe_type(QWidget):

	changed = gSignal()

	def __init__(self,file_box=True):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.raw_value="ground"
		self.hbox=QHBoxLayout()

		self.combobox = QComboBoxLang()
		self.combobox.addItemLang("point",_("Mesh point"))
		self.combobox.addItemLang("average",_("Average"))
		self.combobox.addItemLang("max",_("Max"))
		self.combobox.addItemLang("min",_("Min"))
		self.combobox.addItemLang("max_pos_y_slice",_("Max pos y-slice"))
		self.combobox.addItemLang("max_pos_y_slice0",_("Max pos y-slice STD-Left"))
		self.combobox.addItemLang("max_pos_y_slice1",_("Max pos y-slice STD-Right"))
		self.combobox.addItemLang("max_pos_y_val_slice",_("Max pos y-slice val"))
		self.combobox.addItemLang("max_pos_y_val_slice0",_("Max pos y-slice STD-Left val"))
		self.combobox.addItemLang("max_pos_y_val_slice1",_("Max pos y-slice STD-Right val"))
		self.combobox.addItemLang("val_at_y",_("Value at x point"))
		self.hbox.addWidget(self.combobox)

		self.label_x=QLabel(_("x:"))
		self.hbox.addWidget(self.label_x)
		self.edit_x=QLineEdit()
		self.edit_x.setStyleSheet("QLineEdit { border: none }")
		self.edit_x.textChanged.connect(self.callback_edit)
		self.hbox.addWidget(self.edit_x)

		self.label_y=QLabel(_("y:"))
		self.hbox.addWidget(self.label_y)
		self.edit_y=QLineEdit()
		self.edit_y.setStyleSheet("QLineEdit { border: none }")
		self.edit_y.textChanged.connect(self.callback_edit)
		self.hbox.addWidget(self.edit_y)

		self.label_z=QLabel(_("z:"))
		self.hbox.addWidget(self.label_z)
		self.edit_z=QLineEdit()
		self.edit_z.setStyleSheet("QLineEdit { border: none }")
		self.edit_z.textChanged.connect(self.callback_edit)
		self.hbox.addWidget(self.edit_z)

		self.hbox.setContentsMargins(0, 0, 0, 0)

		self.combobox.currentIndexChanged.connect(self.callback_combobox)

		self.setLayout(self.hbox)

	def update(self):
		self.edit_x.blockSignals(True)
		self.edit_y.blockSignals(True)
		self.edit_z.blockSignals(True)

		self.combobox.blockSignals(True)
		json_path=self.find_probe()
		cb_value=self.bin.get_token_value(json_path,"probe_type")
		self.combobox.setValue_using_english(cb_value)

		self.edit_x.setText(str(self.bin.get_token_value(json_path,"px")))
		self.edit_z.setText(str(self.bin.get_token_value(json_path,"pz")))

		if cb_value.startswith("val_at_y")==True:
			self.edit_y.setText(str(self.bin.get_token_value(json_path,"py_double")))
		else:
			self.edit_y.setText(str(self.bin.get_token_value(json_path,"py")))

		if cb_value=="point":
			self.edit_x.setVisible(True)
			self.label_x.setVisible(True)

			self.edit_y.setVisible(True)
			self.label_y.setVisible(True)

			self.edit_z.setVisible(True)
			self.label_z.setVisible(True)
		elif cb_value.startswith("max_pos_y")==True:
			self.edit_x.setVisible(True)
			self.label_x.setVisible(True)

			self.edit_y.setVisible(False)
			self.label_y.setVisible(False)

			self.edit_z.setVisible(True)
			self.label_z.setVisible(True)
		elif cb_value.startswith("val_at_y")==True:
			self.edit_x.setVisible(False)
			self.label_x.setVisible(False)

			self.edit_y.setVisible(True)
			self.label_y.setVisible(True)

			self.edit_z.setVisible(False)
			self.label_z.setVisible(False)
		else:
			self.edit_x.setVisible(False)
			self.label_x.setVisible(False)

			self.edit_y.setVisible(False)
			self.label_y.setVisible(False)

			self.edit_z.setVisible(False)
			self.label_z.setVisible(False)

		self.combobox.blockSignals(False)
		self.edit_x.blockSignals(False)
		self.edit_y.blockSignals(False)
		self.edit_z.blockSignals(False)

	def callback_edit(self):
		json_path=self.find_probe()
		cb_value=self.combobox.currentText_english()
		self.bin.set_token_value(json_path,"probe_type",cb_value)
		self.bin.set_token_value(json_path,"px",self.edit_x.text())
		self.bin.set_token_value(json_path,"pz",self.edit_z.text())

		if cb_value.startswith("val_at_y")==True:
			self.bin.set_token_value(json_path,"py_double",self.edit_y.text())
		else:
			self.bin.set_token_value(json_path,"py",self.edit_y.text())

		self.changed.emit()

	def callback_combobox(self):
		json_path=self.find_probe()
		self.bin.set_token_value(json_path,"probe_type",self.combobox.currentText_english())
		self.update()
		self.changed.emit()

	def updateValue(self,uid):
		self.uid=uid
		
		self.update()

	def find_probe(self):
		ret=self.bin.find_path_by_uid("dump.probes",self.uid)
		return ret

	def text(self):
		return self.combobox.currentText_english()
