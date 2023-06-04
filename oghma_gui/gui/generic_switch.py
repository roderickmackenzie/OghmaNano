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

## @package generic_switch
#  A generic switch
#


import math
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPainter,QFont,QColor,QPen,QFontMetrics

from gQtCore import gSignal

class generic_switch(QWidget):

	changed = gSignal()

	def __init__(self,state0="True",state1="False",state0_value=True,state1_value=False):      
		super(generic_switch, self).__init__()
		self.state0=state0
		self.state1=state1
		self.state0_value=state0_value
		self.state1_value=state1_value

		self.font = QFont('Sans', 11, QFont.Normal)
		fm = QFontMetrics(self.font)
		self.w0 = fm.width(self.state0)
		self.w1 = fm.width(self.state1)
		if self.w0>self.w1:
			self.my_width=self.w0
		else:
			self.my_width=self.w1

		#print(self.my_width)
		self.setMaximumSize(self.my_width+120,20)

		#self.setMinimumSize(1, 30)
		self.value = self.state0_value

	def get_value(self):
		return self.value

	def set_value(self, value):

		self.value = value


	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawWidget(qp)
		qp.end()


	def drawWidget(self, qp):

		qp.setFont(self.font)

		pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)
		
		qp.setPen(pen)
		qp.setBrush(Qt.NoBrush)

		if self.value==self.state0_value:
			qp.setBrush(QColor(95,163,235))
			qp.drawRoundedRect(0, 0.0, self.my_width+51,22.0,5.0,5.0)			
			qp.setBrush(QColor(230,230,230))
			qp.drawRoundedRect(self.my_width+15, 2, 30,18.0,5.0,5.0)
			qp.drawText(2, 17, self.state0)
		else:
			qp.setBrush(QColor(180,180,180))
			qp.drawRoundedRect(0, 0.0, self.my_width+51,22.0,5.0,5.0)			
			qp.setBrush(QColor(230,230,230))
			qp.drawRoundedRect(2, 2, 30,18.0,5.0,5.0)
			qp.drawText(40, 17, self.state1)

	def mouseReleaseEvent(self, QMouseEvent):
		if QMouseEvent.x()<160:
			if self.value== self.state0_value:
				self.value=self.state1_value
			else:
				self.value=self.state0_value

			self.repaint()
			self.changed.emit()
