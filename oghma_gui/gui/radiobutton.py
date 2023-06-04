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

## @package radiobutton
#  A radiobuttion - needs improving.
#


from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QLinearGradient,QPainter,QFont,QColor,QPen

from gQtCore import gSignal

class radiobutton(QWidget):

	changed = gSignal()

	def __init__(self):      
		super(radiobutton, self).__init__()
		self.setMinimumSize(85,30)

		self.value = False

	def get_value(self):
		if self.value==True:
			return "true"
		else:
			return "false"

	def set_value(self, value):

		self.value = value
		self.repaint()

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		self.drawWidget(qp)
		qp.end()


	def drawWidget(self, qp):
		font = QFont('Sans', 11, QFont.Normal)
		qp.setFont(font)

		pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)
		
		qp.setPen(pen)
		qp.setBrush(Qt.NoBrush)

		if self.value==True:
			qp.setBrush(QColor(72,72,72))
			qp.drawEllipse(0, 0, 45,45)

			qp.setBrush(QColor(140,140,140))
			qp.drawEllipse(2, 2, 41,41)

			qp.setBrush(QColor(43,69,201))
			qp.drawEllipse(7, 7, 31,31)

			qp.setBrush(QColor(70,140,200))
			qp.drawEllipse(9, 9, 27,27)


			qp.drawText(1, 60, _("Enabled"))
		else:
			qp.setBrush(QColor(72,72,72))
			qp.drawEllipse(0, 0, 45,45)

			qp.setBrush(QColor(140,140,140))
			qp.drawEllipse(2, 2, 41,41)
			qp.drawText(1, 60, _("Disabled"))

	def mouseReleaseEvent(self, QMouseEvent):
		if QMouseEvent.x()<80:
			self.value= True
			self.repaint()
			self.changed.emit()
