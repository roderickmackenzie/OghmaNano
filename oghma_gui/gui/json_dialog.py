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

## @package tab
#  The main tab class, used to display material properties.
#

from tab_base import tab_base

from gQtCore import gSignal

from PySide2.QtWidgets import QTextEdit,QWidget, QScrollArea,QVBoxLayout,QLabel,QHBoxLayout,QPushButton, QSizePolicy, QDialog
from gQtCore import QSize, Qt
from PySide2.QtGui import QPixmap, QIcon
from icon_lib import icon_get
from json_viewer import json_viewer

import i18n
_ = i18n.language.gettext
from sim_name import sim_name

class json_dialog(QDialog):

	def __init__(self,title=sim_name.name,icon="icon"):
		QDialog.__init__(self)
		self.editable=True
		self.setWindowTitle(title)
		self.setWindowIcon(icon_get(icon))

		self.scroll=QScrollArea()
		self.main_box_widget=QWidget()
		self.vbox=QVBoxLayout()
		self.hbox=QHBoxLayout()
		self.hbox.setAlignment(Qt.AlignTop)

		self.tab=json_viewer()
		self.tab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.vbox.addWidget(self.tab)

		self.vbox.addWidget(self.gen_button_box_widget())

		self.setMinimumWidth(400)

		self.setLayout(self.vbox)

	def set_edit(self,editable):
		self.tab.editable=editable

	def callback_close(self):
		self.reject()

	def callback_apply(self):
		self.accept()

	def run(self,data):
		self.tab.populate(data)
		return self.exec_()

	def gen_button_box_widget(self):
		button_box=QHBoxLayout()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		button_box.addWidget(spacer)

		self.close_button=QPushButton("Close", self)
		self.close_button.clicked.connect(self.callback_close)
		button_box.addWidget(self.close_button)

		self.apply=QPushButton("Apply", self)
		self.apply.clicked.connect(self.callback_apply)
		button_box.addWidget(self.apply)

		button_box_widget=QWidget()
		button_box_widget.setLayout(button_box)
		return button_box_widget
