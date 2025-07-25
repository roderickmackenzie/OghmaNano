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

## @package error_han
#  Handle errors and get the user to report them.
#


#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QTextEdit, QFileDialog, QToolBar, QLabel ,QMessageBox, QLineEdit,QVBoxLayout, QTableWidget, QAbstractItemView
from PySide2.QtGui import QPixmap

#gui_util
from icon_lib import icon_get

from spinner import spinner

from error_dlg import error_dlg
from gui_util import yes_no_dlg

import traceback
import sys

from report_error import report_error
from lock import get_lock
from json_c import json_local_root

def error_han(type, value, tback):
	print("error=",value,tback,"rod")
	if value==KeyboardInterrupt:
		print("hello")

	if json_local_root().get_token_value("gui_config","enable_betafeatures")==False:

		#formatted_lines = traceback.format_exc().splitlines()
		long_trace=traceback.format_exception(type, value, tback)
		long_trace=str("<br>".join(long_trace))
		trace=long_trace.replace("<br>","")
		trace=trace.replace(" ","")
		dialog=widget_error_han(long_trace,trace)
		dialog.exec_()
	sys.__excepthook__(type, value, tback)		
	return True


class widget_error_han(QDialog):

	def __init__(self,long_error,error):
		self.message_through_forum=True
		self.error=error
		self.file_path=""
		QDialog.__init__(self)
		self.setWindowTitle(_("Error"))

		self.main_vbox=QVBoxLayout()
		self.setFixedSize(800,400)
		h_widget=QWidget()
		h_box=QHBoxLayout()
		h_widget.setLayout(h_box)
		image=QLabel()
		icon=icon_get("warning")
		image.setPixmap(icon.pixmap(icon.actualSize(QSize(48, 48))))
		h_box.addWidget(image)

		h_box.setAlignment(image,Qt.AlignTop)
		
		self.message = QTextEdit()
		if self.message_through_forum==False:
			help_text="<big><b>An error has occurred please report this error by clicking ok:<b></big><br><br>"
			help_text2="<br><br><big><b>It would also help if you e-mailed the error message to "+get_lock().my_email+" and described what you were doing with the model to make it crash.  Very often there is not enough information in bug reports alone to fix the problem.<br><br>All error reports are gratefully received.<br><br>Rod 5/9/16<b></big>"
		else:
			help_text="<big><b>An error has occurred please report this error though the User Forum:<b></big><br><br>"
			help_text2="<br><br><big><b>Please report the bug using "+get_lock().get_help+"<br><br>Described what you were doing with the model to make it crash.  Very often there is not enough information in bug reports alone to fix the problem.<br><br>All error reports are gratefully received.<br><br>Rod 25/08/25<b></big>"
		self.message.setText(help_text+long_error+help_text2)
		h_box.addWidget(self.message)
		
		self.main_vbox.addWidget(h_widget)

		button_widget=QWidget()
		self.main_vbox.addWidget(button_widget)
		
		self.label_reporting=QLabel(_("Reporting error...."))
		self.label_reporting.hide()

		self.spin=spinner()
		self.spin.hide()
		
		okButton = QPushButton("OK")
		cancelButton = QPushButton("Cancel")

		button_layout = QHBoxLayout()
		button_layout.addWidget(self.label_reporting)
		button_layout.addWidget(self.spin)

		button_layout.addStretch(1)
		button_layout.addWidget(okButton)
		if self.message_through_forum==False:
			button_layout.addWidget(cancelButton)
		button_widget.setLayout(button_layout)

		self.setLayout(self.main_vbox)

		if self.message_through_forum==False:
			okButton.clicked.connect(self.on_ok_clicked) 
		else:
			okButton.clicked.connect(self.callback_close) 
		cancelButton.clicked.connect(self.close_clicked)

	def error_reported(self,sucess):
		self.label_reporting.hide()
		self.spin.hide()
		if sucess==True:
			error_dlg(self,"I have reported the error, for more information e-mail "+get_lock().my_email)
			self.close()
		else:
			error_dlg(self,"I could not report the error please send the error message to "+get_lock().my_email)
			self.close()

	def close_clicked(self):
		result=yes_no_dlg(self,"Are you sure you don't want to report the error?  It would be really helpful if you did.")
		if result == True:
			self.close()
		else:
			self.on_ok_clicked()

	def callback_close(self):
		self.close()
	def on_ok_clicked(self):
		print("Reporting error....")
		self.label_reporting.show()
		self.spin.show()


		self.tx=report_error()
		self.tx.reported.connect(self.error_reported)
		self.tx.set_error(self.error)
		self.tx.start()
		
