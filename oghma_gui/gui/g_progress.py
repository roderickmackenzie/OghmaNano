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

## @package g_progress
#  Progress Widget
#


from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QPushButton
from PySide2.QtGui import QPainter,QColor,QPainterPath,QPolygonF
from PySide2.QtWidgets import QWidget, QHBoxLayout
from gQtCore import QRectF,QPoint
from gQtCore import QTimer

class g_progress(QWidget):
	def update(self):
		self.setValue()
		self.repaint()
		
	def __init__(self):
		QWidget.__init__(self)
		self.setMaximumHeight(40)
		self.pulse_direction=True

		self.value=0.0
		self.enable_pulse=False


	def enablePulse(self,value):
		self.enable_pulse=value

	def setValue(self,v):
		self.enable_pulse=False
		self.value=v
		self.repaint()

	def pulse(self):
		self.enable_pulse=True
		
		if self.pulse_direction==True:
			self.value=self.value+0.1
		else:
			self.value=self.value-0.1

		if self.value>=1.0 or self.value<=0.0:
			self.pulse_direction= not self.pulse_direction
			if self.value>0.5:
				self.value=1.0

			if self.value<0.5:
				self.value=0.0
				
		self.repaint()

	def paintEvent(self, e):
		w=self.width()
		h=self.height()
		
		if self.enable_pulse==True:
			l=(w-3)*0.2
			bar_start=((w-3)-l)*self.value
		else:
			l=(w-3)*self.value
			bar_start=0
		
		qp = QPainter()
		qp.begin(self)

		color = QColor(0, 0, 0)
		color.setNamedColor('#d4d4d4')
		qp.setBrush(color)
		
		path=QPainterPath()
		path.addRoundedRect(QRectF(0, 0, w, h), 0, 0)
		qp.fillPath(path,QColor(206 , 206, 206));


		path=QPainterPath()
		path.addRoundedRect(QRectF(bar_start, 3, l, h-6), 5, 5)
		qp.fillPath(path,QColor(71 , 142, 216));

		
		#path.addPolygon(QPolygonF([QPoint(0,0), QPoint(10,0), QPoint(10,10), QPoint(10,0)]));
		#qp.setBrush(QColor(71 , 142, 216))

		#path.addPolygon(QPolygonF([QPoint(0,0), QPoint(50,0), QPoint(40,10), QPoint(10,0)]))
		#qp.setBrush(QColor(71 , 142, 216))
		#qp.setBrush(QColor(206 , 207, 206))




		qp.end()
