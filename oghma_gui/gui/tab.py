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


from token_lib import tokens
from undo import undo_list_class
from tab_base import tab_base
from help import help_window

from PySide2.QtWidgets import QTextEdit,QWidget, QScrollArea,QVBoxLayout,QLabel,QHBoxLayout,QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,QComboBox,QGridLayout,QLineEdit
from gQtCore import QSize, Qt, QTimer, gSignal
from PySide2.QtGui import QPixmap, QIcon

from icon_lib import icon_get

import i18n
_ = i18n.language.gettext

from json_viewer import json_viewer
from json_root import json_root

class tab_class(QWidget,tab_base):

	changed = gSignal(str)

	def __init__(self,template_widget,data=json_root(),db_json_file=None,json_path=None,uid=None,enable_apply_button=False,db_json_db_path=None):
		QWidget.__init__(self)
		self.editable=True
		self.enable_apply_button=enable_apply_button
		self.data=data
		self.scroll=QScrollArea()
		self.main_box_widget=QWidget()
		self.vbox=QVBoxLayout()
		self.main_vbox=QVBoxLayout()
		self.main_vbox.setAlignment(Qt.AlignTop)

		self.tab=json_viewer(db_json_file=db_json_file,db_json_db_path=db_json_db_path)
		self.tab.populate(template_widget,json_path=json_path,uid=uid)

		self.vbox.addWidget(self.tab)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.vbox.addWidget(spacer)
		self.main_box_widget.setLayout(self.vbox)
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.main_box_widget)

		self.main_vbox.addWidget(self.scroll)
		
		if self.enable_apply_button==True:
			button_box = QWidget()
			button_layout=QHBoxLayout()
			button_box.setLayout(button_layout)
			spacer = QWidget()
			spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
			button_layout.addWidget(spacer)
			button=QPushButton("Apply")
			button_layout.addWidget(button)
			button.clicked.connect(self.callback_edit)
			self.main_vbox.addWidget(button_box)
		else:
			self.tab.changed.connect(self.callback_edit)

		self.setLayout(self.main_vbox)
	def callback_edit(self,token):
		if self.enable_apply_button==False:
			self.data.save()
		self.changed.emit(token)

	def set_edit(self,editable):
		self.tab.editable=editable



