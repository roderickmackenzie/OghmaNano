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

## @package QColorPicker
#  A color picker widget
#

#qt
from PySide2.QtGui import QIcon, QColor, QPixmap
from gQtCore import QSize, Qt, QTimer, gSignal
from PySide2.QtWidgets import QColorDialog,QLineEdit,QWidget,QHBoxLayout,QPushButton,QLineEdit,QLabel, QSpinBox

#cal_path
from help import help_window

import i18n
_ = i18n.language.gettext


class QColorPicker(QWidget):

	changed = gSignal()
	
	def __init__(self,r,g,b,alpha):
		QWidget.__init__(self)
		self.r=r
		self.g=g
		self.b=b
		self.alpha=alpha
		self.hbox=QHBoxLayout()
		self.edit=QLineEdit()
		self.label=QLabel("Alpha:")
		self.button=QPushButton()
		self.button.setFixedSize(25, 25)
		self.button.setText("...")
		self.spin = QSpinBox()
		self.spin.setRange(0.0, 100)
		self.hbox.addWidget(self.edit)
		self.hbox.addWidget(self.button)
		self.hbox.addWidget(self.label)
		self.hbox.addWidget(self.spin)

		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.update_color()

		
		self.button.clicked.connect(self.callback_button_click)
		self.spin.valueChanged.connect(self.callback_spin_click)

		self.setLayout(self.hbox)

	def update_color(self):
		rgb=(self.r*255,self.g*255,self.b*244)
		self.edit.setStyleSheet("QLineEdit { border: none;  background-color: rgb(%d,%d,%d)  }" % rgb);
		self.edit.setText(str(round(self.r*255))+" "+str(round(self.g*255))+" "+str(round(self.b*255)))
		self.spin.setValue(round(self.alpha*100))

	def callback_spin_click(self):
		self.alpha=self.spin.value()/100.0
		self.changed.emit()

	def callback_button_click(self):
		self.col = QColorDialog()
		self.col.setCurrentColor(QColor(int(self.r*255),int(self.g*255),int(self.b*255)))
		#col.setCurrentColor(Qt.red)
		ret=self.col.getColor(Qt.white, self, options=QColorDialog.DontUseNativeDialog and QColorDialog.DontUseNativeDialog)
		#col.setOption(QColorDialog::ShowAlphaChannel)
		#col.setOption(QColorDialog.DontUseNativeDialog)
		if ret.isValid():
			self.r=ret.red()/255
			self.g=ret.green()/255
			self.b=ret.blue()/255
			self.alpha=self.spin.value()/100.0
			self.update_color()
			self.changed.emit()

	def get_value(self):
		return self.edit.text()

class QColorPicker_one_line(QColorPicker):

	def __init__(self):
		QColorPicker.__init__(self,1.0,1.0,1.0,1.0)

	def setText(self,val):
		vals=val.split(",")
		self.r=float(vals[0])
		self.g=float(vals[1])
		self.b=float(vals[2])
		self.alpha=float(vals[3])
		self.update_color()
		#self.col.setCurrentColor(QColor(int(self.r*255),int(self.g*255),int(self.b*255)))

	def text(self):
		return str(self.r)+","+str(self.g)+","+str(self.b)+","+str(self.alpha)


