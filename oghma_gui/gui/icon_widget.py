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

## @package icon_widget
#  A widget to show the icon
#



#qt
from PySide2.QtWidgets import QLabel,QTextEdit, QTableWidgetItem,QComboBox, QDialog,QLineEdit,QWidget,QHBoxLayout,QPushButton,QSizePolicy
from PySide2.QtGui import QPixmap, QIcon
from gQtCore import QSize, Qt, QTimer, gSignal
from QComboBoxLang import QComboBoxLang


#cal_path
from icon_lib import icon_get
from cal_path import subtract_paths


import i18n
_ = i18n.language.gettext


class icon_widget(QWidget):

	changed = gSignal()

	def __init__(self):
		QWidget.__init__(self)
		self.hbox=QHBoxLayout()
		self.edit=QLineEdit()
		self.button=QLabel()
		self.button.setFixedSize(32, 32)


		self.hbox.addWidget(self.button)

		self.hbox.addWidget(self.edit)

		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.edit.setStyleSheet("QLineEdit { border: none }");


		self.edit.textChanged.connect(self.text_changed)
		self.setLayout(self.hbox)

	def text_changed(self):
		self.changed.emit()

	def callback_button_click(self):
		from g_open import g_open
		self.path="/root/icons/"
		dialog=g_open(self.path,act_as_browser=False)

		ret=dialog.exec_()
		if ret==QDialog.Accepted:
			file_name=dialog.get_filename()
			rel_path=subtract_paths(self.path,file_name)
			rel_path=rel_path.replace("\\", "/")
			self.setText(rel_path)
			self.changed.emit()

	def setText(self,text):
		self.edit.blockSignals(True)
		self.edit.setText(text)
		icon=icon_get(text)
		if icon!=False:
			self.button.setPixmap(icon.pixmap(QSize(32, 32)))
		self.edit.blockSignals(False)
	
	def text(self):
		return self.edit.text()
