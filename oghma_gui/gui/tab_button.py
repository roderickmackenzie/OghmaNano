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

## @package g_select
#  A widget for the tab widget which allows the user to select files.
#


#qt
try:
	from PySide2.QtWidgets import QMessageBox, QDialog, QLineEdit,QWidget,QHBoxLayout,QPushButton
	from PySide2.QtGui import QPixmap, QIcon
	from gQtCore import QSize, Qt, QTimer, gSignal
	from QComboBoxLang import QComboBoxLang
except:
	pass

import i18n
_ = i18n.language.gettext


class tab_button(QWidget):
	changed = gSignal(str)

	def __init__(self):
		QWidget.__init__(self)
		self.data=None
		self.hbox=QHBoxLayout()
		self.edit=QLineEdit()
		self.button=QPushButton()
		self.button.setFixedSize(50, 25)
		self.button.setText("Edit")
		#self.hbox.addWidget(self.edit)
		self.hbox.addWidget(self.button)
		self.uid=None
		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.edit.setStyleSheet("QLineEdit { border: none }");

		self.button.clicked.connect(self.callback_button)
		self.setLayout(self.hbox)

	def callback_button(self):
		self.changed.emit(self.uid)
		
