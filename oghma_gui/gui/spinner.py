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

## @package spinner
#  A spinner widget.
#

import sys
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QIcon,QPalette
from PySide2.QtGui import QPainter,QFont,QColor,QPen,QPainterPath,QBrush
from gQtCore import Qt, QTimer

from math import pi,acos,sin,cos
import random

class spinner(QWidget):
    
	def __init__(self):
		super().__init__()
		self.delta=0
		self.setFixedSize(30, 30)
		#self.setGeometry(300, 300, 300, 220)
		#self.setWindowTitle('Icon')
		#self.setWindowIcon(QIcon('web.png'))        
		#self.start()
		self.blue_target=255.0
		self.green_target=0.0
		self.red_target=0.0
		self.timer=None

	def start(self):
		if self.timer==None:
			self.timer=QTimer()
			self.timer.timeout.connect(self.update)
			self.timer.start(10)
			self.blue_target=255.0
			self.green_target=0.0
			self.red_target=0.0
		
	def stop(self):
		if self.timer!=None:
			self.timer.stop()
		self.timer=None

	def update(self):
		self.delta=self.delta+5
		if self.delta>360:
			self.delta=0

		self.blue_target=0#self.blue_target+20*random.random()-10
		self.green_target=0#self.green_target+20*random.random()-10
		self.red_target=0#self.red_target+20*random.random()-10
		if self.blue_target>255:
			self.blue_target=255

		if self.red_target>255:
			self.red_target=255

		if self.green_target>255:
			self.green_target=255

		if self.blue_target<0:
			self.blue_target=0

		if self.red_target<0:
			self.red_target=0

		if self.green_target<0:
			self.green_target=0
			
		self.repaint()
		
	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawWidget(qp)
		qp.end()
		
	def drawWidget(self, qp):
		color = self.palette().color(QPalette.Background)
		qp.setBrush(QColor(100,0,0))

		pen=QPen()
		pen.setWidth(int(self.width()/10))
		
		pen.setColor(QColor(0,0,255))
		pen.setCapStyle(Qt.RoundCap)

		w=self.width()/2
		x_shift=w+w*0.05
		y_shift=w+w*0.05
		r=0.35*w
		r1=w*0.8
		qp.setPen(pen)

		my_max=100
		p=[]
		c=[]
		for phi in range(0,360,30):
			p.append(phi)
			c.append(0)
		f=0
		for i in range(0,len(p)):
			if p[i]>self.delta:
				f=i
				break
		i=f
		m=1.0
		while(i>=0):
			c[i]=m
			m=m*0.7
			i=i-1
			
		i=len(c)-1
		
		while(i>f):
			c[i]=m
			m=m*0.7
			i=i-1

		for i in range(0,len(p)):
			self.pos=p[i]
			x = r *  cos( (2*pi)*self.pos/360 )
			y = r *  sin( (2*pi)*self.pos/360 )
		
			x1 = r1 *  cos( (2*pi)*self.pos/360 )
			y1 = r1 *  sin( (2*pi)*self.pos/360 )
			cb=self.blue_target*c[i]+color.blue()*(1.0-c[i])
			cg=self.green_target*c[i]+color.green()*(1.0-c[i])
			cr=self.red_target*c[i]+color.red()*(1.0-c[i])
			
			pen.setColor(QColor(int(cr),int(cg),int(cb)))
			qp.setPen(pen)
			qp.drawLine(int(x+x_shift),int(y+y_shift),int(x1+x_shift),int(y1+y_shift))
        
