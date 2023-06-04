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
	from PySide2.QtWidgets import QTextEdit, QAction, QListView,QLineEdit,QWidget,QHBoxLayout,QPushButton
	from PySide2.QtGui import QPixmap
	from gQtCore import QSize, Qt, QTimer, QPersistentModelIndex
	from QComboBoxLang import QComboBoxLang
	from PySide2.QtGui import QIcon
except:
	pass

#cal_path
from open_save_dlg import open_as_filter

import i18n
_ = i18n.language.gettext


class g_select(QWidget):

	def __init__(self,file_box=False):
		QWidget.__init__(self)
		self.hbox=QHBoxLayout()
		self.edit=QLineEdit()
		self.button=QPushButton()
		self.button.setFixedSize(25, 25)
		self.button.setText("...")
		self.hbox.addWidget(self.edit)
		self.hbox.addWidget(self.button)

		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.edit.setStyleSheet("QLineEdit { border: none }");

		if file_box==True:
			self.button.clicked.connect(self.callback_button_click)

		self.setLayout(self.hbox)

	def callback_button_click(self):
		file_name=open_as_filter(self,"dat (*.dat);;csv (*.csv);;txt (*.txt)")
		if file_name!=None:
			self.setText(file_name)

	def setText(self,text):
		blocked=False
		if self.signalsBlocked()==True:
			blocked=True

		if blocked==True:
			self.edit.blockSignals(True)

		self.edit.setText(text)

		if blocked==True:
			self.edit.blockSignals(False)

	def text(self):
		return self.edit.text()
		
