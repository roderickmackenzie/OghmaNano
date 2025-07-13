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

## @package edit_with_units
#  A widget to adjust mobility
#

#qt
from PySide2.QtWidgets import QLabel, QFrame, QTextEdit, QAction, QLineEdit,QWidget,QHBoxLayout,QPushButton,QSizePolicy
from PySide2.QtGui import QPixmap, QIcon
from gQtCore import QSize, Qt, QTimer, QPersistentModelIndex, gSignal
from QComboBoxLang import QComboBoxLang
from json_c import json_tree_c

import i18n
_ = i18n.language.gettext

class edit_with_units(QWidget):

	changed = gSignal()

	def __init__(self):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.hbox=QHBoxLayout()

		self.edit_box=QLineEdit()
		self.edit_box.setMaximumWidth( 200 )
		self.hbox.addWidget(self.edit_box,Qt.AlignLeft)

		self.combobox = QComboBoxLang()
		self.combobox.setMaximumWidth( 80 )
		self.combobox.addItemLang("m",_("m"))
		self.combobox.addItemLang("cm",_("cm"))
		self.combobox.addItemLang("mm",_("mm"))
		self.combobox.addItemLang("um",_("um"))
		self.combobox.addItemLang("nm",_("nm"))
		self.combobox.addItemLang("pm",_("pm"))
		self.combobox.addItemLang("fm",_("fm"))
		self.combobox.currentIndexChanged.connect(self.callback_combobox)

		self.hbox.addWidget(self.combobox)
		self.hbox.addStretch()

		self.hbox.setSpacing(0)

		self.edit_box.textChanged.connect(self.callback_edit)

		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.token=None
		#self.edit_box.setStyleSheet("QLineEdit { border: none }");

		#self.edit.textChanged.connect(self.callback_edit)
		#self.setStyleSheet("background-color:black;");
		self.setLayout(self.hbox)

		self.real_value=-1.0

	def update(self):
		val=self.real_value/self.get_mul()
		text_value=self.bin.format_float(val)
		self.edit_box.blockSignals(True)
		self.edit_box.setText(text_value)
		self.edit_box.blockSignals(False)

	def callback_edit(self):
		try:
			val=float(self.edit_box.text())
		except:
			return
		self.real_value=val*self.get_mul()
		self.changed.emit()

	def callback_combobox(self):
		self.update()
		self.changed.emit()

	def get_mul(self):
		val=self.combobox.currentText_english()
		if val=="m":
			return 1.0
		elif val=="cm": 
			return 1e-2
		elif val=="mm":
			return 1e-3
		elif val=="um": 
			return 1e-6
		elif val=="nm": 
			return 1e-9
		elif val=="pm": 
			return 1e-12
		elif val=="fm": 
			return 1e-15

		return -1.0

		
	def set_value(self,in_value):
		try:
			self.real_value=float(in_value[0])
		except:
			return

		self.combobox.blockSignals(True)
		self.combobox.setValue_using_english(in_value[1])
		self.combobox.blockSignals(False)
		self.update()

	def get_value(self):
		return [self.real_value ,self.combobox.currentText_english()]
