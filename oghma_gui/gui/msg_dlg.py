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

## @package msg_box
#  A message box class.
#

#qt
from PySide2.QtWidgets import QDialog,QVBoxLayout,QLabel,QHBoxLayout,QWidget,QSizePolicy,QPushButton
from gui_enable import gui_get
from icon_lib import icon_get
from PySide2.QtGui import QFont,QPixmap
from sim_name import sim_name

class msg_dlg(QDialog):

	def __init__(self,title=sim_name.web,image_file=""):
		QDialog.__init__(self)
		self.setWindowIcon(icon_get("icon"))
		self.setWindowTitle(title)

		vbox=QVBoxLayout()

		main_hbox=QHBoxLayout()

		if image_file!="":
			self.image=QLabel()
			#self.text.setFont(QFont('SansSerif', 16))
			self.image.setPixmap(QPixmap(image_file))
			main_hbox.addWidget(self.image)

		self.text=QLabel()
		self.text.setFont(QFont('SansSerif', 16))
		main_hbox.addWidget(self.text)

		main_hbox_widget=QWidget()
		main_hbox_widget.setLayout(main_hbox)
		vbox.addWidget(main_hbox_widget)

		button_box=QHBoxLayout()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		button_box.addWidget(spacer)

		self.ok=QPushButton("Ok", self)
		self.ok.clicked.connect(self.callback_ok)
		button_box.addWidget(self.ok)

		button_box_widget=QWidget()
		button_box_widget.setLayout(button_box)
		vbox.addWidget(button_box_widget)
		self.text.setWordWrap(True)
		self.setLayout(vbox)
		self.setMinimumWidth(500)

	def setText(self,data):
		self.text.setText(data)


	def callback_ok(self):

		self.accept()

