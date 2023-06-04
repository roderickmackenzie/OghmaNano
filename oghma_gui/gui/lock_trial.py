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

## @package lock_trial
#  The trial window
#




#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QLineEdit,QComboBox,QHBoxLayout,QPushButton,QLabel,QDialog,QVBoxLayout,QSizePolicy
from PySide2.QtGui import QPainter,QIcon,QImage
from PySide2.QtGui import QFont

from icon_lib import icon_get

from gQtCore import QSize, Qt


from error_dlg import error_dlg
from lock import lock

from lock import get_lock

import webbrowser
from lock_license_key import license_key
from error_dlg import error_dlg
from msg_dlg import msg_dlg
from sim_name import sim_name

class lock_trial(QDialog):

	def callback_trial(self):
		webbrowser.open(sim_name.web+"/buy.php")
		self.reject()

	def callback_close(self):
		self.reject()

	def callback_validate(self):
		val=get_lock().validate_key(self.keybox.text().strip())
		if val==True:
			self.accept()
			return
		elif get_lock().error=="notfound":
			error_dlg(self,_("Not a valid license number"))
		elif get_lock().error=="key_not_found":
			error_dlg(self,_("Key not found"))
		elif get_lock().error=="user_not_found":
			error_dlg(self,_("User not found"))
		elif get_lock().error=="limreached":
			error_dlg(self,_("This key has been used too many times."))
		elif get_lock().error=="outoftime":
			error_dlg(self,_("This key has expired."))
		elif get_lock().error=="too_old":
			error_dlg(self,_("This version of the software is too old to validate it's key, please download the latest version."))
		else:
			error_dlg(self,_("Can't access the internet"))

		self.reject()

	def callback_keybox_edit(self):
		if self.keybox.text()=="":
			self.buy.show()
			self.close_button.show()
			self.validate.hide()
		else:
			self.buy.hide()
			self.close_button.hide()
			self.validate.show()


	def __init__(self,show_text=True,override_text=False,title_font_size=25):
		QDialog.__init__(self)
		self.setWindowIcon(icon_get("icon"))
		self.setWindowTitle(_("OghmaNano trial")+sim_name.web_window_title) 
		self.setWindowFlags(Qt.WindowStaysOnTopHint)

		vbox=QVBoxLayout()

		if override_text!=False:
			text=override_text
		self.title_text=QLabel(text)
		self.title_text.setFont(QFont('SansSerif', title_font_size))
		self.title_text.setWordWrap(True)
		vbox.addWidget(self.title_text)


		button_box=QHBoxLayout()

		l=QLabel("Key")
		l.setFont(QFont('SansSerif', 14))
		button_box.addWidget(l)

		self.keybox = QLineEdit()
		button_box.addWidget(self.keybox)
		self.keybox.textChanged.connect(self.callback_keybox_edit)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		button_box.addWidget(spacer)

		self.close_button=QPushButton("Close", self)
		self.close_button.clicked.connect(self.callback_close)
		button_box.addWidget(self.close_button)

		self.buy=QPushButton("Get upgrade key", self)
		self.buy.clicked.connect(self.callback_trial)
		button_box.addWidget(self.buy)

		self.validate=QPushButton("Validate key", self)
		self.validate.clicked.connect(self.callback_validate)
		button_box.addWidget(self.validate)
		self.validate.hide()

		button_box_widget=QWidget()
		button_box_widget.setLayout(button_box)
		vbox.addWidget(button_box_widget)

		self.setLayout(vbox)

		self.setMinimumWidth(600)

		
	def run(self):
		return self.exec_()


