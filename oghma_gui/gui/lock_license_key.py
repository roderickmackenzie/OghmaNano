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

## @package register
#  Registration window
#



#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QLineEdit,QComboBox,QHBoxLayout,QPushButton,QLabel,QDialog,QVBoxLayout,QSizePolicy
from PySide2.QtGui import QPainter,QIcon,QImage
from PySide2.QtGui import QFont

from icon_lib import icon_get
from gQtCore import QSize, Qt
from error_dlg import error_dlg
from lock import get_lock
from sim_name import sim_name

class license_key(QDialog):

	def callback_ok(self):
		print("boom")
		#get_lock().register(email=self.email0.text(),name=self.name.text())
		#get_lock().get_license()

		self.accept()

	def __init__(self):
		QDialog.__init__(self)
		self.setWindowIcon(icon_get("icon"))
		self.setWindowTitle(_("Registration window"+sim_name.web_window_title)) 
		self.setWindowFlags(Qt.WindowStaysOnTopHint)

		vbox=QVBoxLayout()

		l=QLabel(_("Enter the license key below:"))
		l.setFont(QFont('SansSerif', 14))
		vbox.addWidget(l)

		hbox_widget=QWidget()
		hbox=QHBoxLayout()
		hbox_widget.setLayout(hbox)
		l=QLabel("<b>"+_("Key")+"</b>:")
		l.setFont(QFont('SansSerif', 14))
		hbox.addWidget(l)
		self.name = QLineEdit()
		hbox.addWidget(self.name)
		vbox.addWidget(hbox_widget)

		button_box=QHBoxLayout()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		button_box.addWidget(spacer)

		self.register=QPushButton("Register", self)
		self.register.clicked.connect(self.callback_ok)
		button_box.addWidget(self.register)

		button_box_widget=QWidget()
		button_box_widget.setLayout(button_box)
		vbox.addWidget(button_box_widget)

		self.setLayout(vbox)

		self.setMinimumWidth(400)

		self.name.setText("key")
		
		
	def run(self):
		return self.exec_()


