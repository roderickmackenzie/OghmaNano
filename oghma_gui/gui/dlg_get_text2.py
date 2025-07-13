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

## @package dlg_get_text2
#  Get text from the user
#

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QLineEdit,QHBoxLayout,QPushButton,QLabel,QDialog,QVBoxLayout,QSizePolicy, QDialogButtonBox
from PySide2.QtGui import QPainter,QIcon,QImage, QFont

from icon_lib import icon_get

class dlg_get_text2(QDialog):

	def __init__(self,text,default,image_name,info=[],title_text="https://www.oghma-nano.com"):
		QDialog.__init__(self)
		self.ret=None
		self.info=info
		icon=icon_get(image_name)
		self.setWindowIcon(icon)
		self.setWindowTitle(title_text) 
		#self.setWindowFlags(Qt.WindowStaysOnTopHint)

		main_vbox=QVBoxLayout()
		#main_vbox.setContentsMargins(0,0,0,0)
		widget0=QWidget()
		hbox0=QHBoxLayout()
		#hbox0.setContentsMargins(0,0,0,5)
		widget0.setLayout(hbox0)

		self.image=QLabel()
		self.image.setPixmap(icon.pixmap(icon.actualSize(QSize(64, 64))))
		self.image.resize(64,64)
		hbox0.addWidget(self.image)

		label=QLabel(text)
		label.setFont(QFont('SansSerif', 12))
		hbox0.addWidget(label)

		self.spacer0 = QWidget()
		self.spacer0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		hbox0.addWidget(self.spacer0)

		main_vbox.addWidget(widget0)
		
		#vbox
		if info==[]:
			self.text_widget = QWidget()
			self.text_layout=QHBoxLayout()
			self.text_widget.setLayout(self.text_layout)

			self.text_spacer = QWidget()
			self.text_spacer.setMinimumWidth(64)
			self.text_layout.addWidget(self.text_spacer)

			self.textbox = QLineEdit(self)
			self.text_layout.addWidget(self.textbox)

			self.textbox.setText(default)
			main_vbox.addWidget(self.text_widget)
		else:
			self.edit_boxes=[]
			for i in range(0,len(info)):
				l=QLabel(info[i][0])
				main_vbox.addWidget(l)

				self.edit_boxes.append(QLineEdit())
				self.edit_boxes[-1].setText(info[i][1])

				main_vbox.addWidget(self.edit_boxes[-1])

		#OK buttons
		self.btns = QDialogButtonBox()
		self.btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
		main_vbox.addWidget(self.btns)

		self.btns.accepted.connect(self.callback_accept)
		self.btns.rejected.connect(self.reject)

		self.setLayout(main_vbox)

		self.setMinimumWidth(400)
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		self.exec_()

	def callback_accept(self):
		if self.info==[]:
			self.ret=self.textbox.text()
		else:
			self.ret=[]
			for box in self.edit_boxes:
				self.ret.append(box.text())

		self.accept()



