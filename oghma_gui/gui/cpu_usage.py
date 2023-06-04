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

## @package cpu_usage
#  A CPU usage widget, which displays local CPU usage, local disk load, and remote CPU usage. 
#

from PySide2.QtWidgets import QApplication, QWidget

from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QIcon,QPalette
from PySide2.QtGui import QPainter,QFont,QColor,QPen,QPainterPath,QBrush
from gQtCore import Qt, QTimer

from server import server_get
from cal_path import sim_paths
import ctypes
from g_io import g_io
import time

class store():
	load=0.0
	wait=0.0
	cluster=0.0
	color=[0,0,0]

class cpu_usage(QWidget):
    
	def __init__(self):
		super().__init__()
		self.server=server_get()
		self.load=[]

		self.wait_last=0.0
		self.setMinimumSize(40, 40)

		for i in range(0,1000):
			s=store()
			self.load.append(s)

		self.delta=0
		self.g_io=g_io()		
		self.start()
		self.disk_max=1

	def start(self):
		self.timer=QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(100);

	def stop(self):
		self.timer.stop()
		
	def update(self):
		
		s=store()

		s.load=self.g_io.cpu_usage_get()
		#print("load",s.load)
		self.load.append(s)

		w_temp=self.g_io.lib.g_disk_writes()

		w_delta=w_temp-self.wait_last
		self.wait_last=w_temp
		#print("s.wait",s.wait)

		s.wait=w_delta/1000.0
		if s.wait>1.0:
			s.wait=1.0
		elif s.wait<0.0:
			s.wait=0.0

		s.color=[int(255*(s.load/100.0)),0,0]
		s.cluster=self.server.get_nodes_load()
		self.load[len(self.load)-1]=s
		self.load.pop(0)


		self.repaint()
		
	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawWidget(qp)
		qp.end()
		
	def drawWidget(self, qp):
		h=self.height()
		w=self.width()
		qp = QPainter()
		qp.begin(self)

		qp.setBrush(QColor(0,0,0))
		qp.setPen(QColor(0,0,0))
		qp.drawRect(0, 0, w, h)
		

		dy=h/len(self.load)

		for i in range(0,len(self.load)):
			#cpu
			qp.setBrush(QColor(int(self.load[i].color[0]),int(self.load[i].color[1]),int(self.load[i].color[2])))
			qp.setPen(QColor(int(self.load[i].color[0]),int(self.load[i].color[1]),int(self.load[i].color[2])))
		
			dx=self.load[i].load*w/100.0
			qp.drawRect(int(w), int(h-dy*i), int(-dx), int(dy))

			qp.setBrush(QColor(0,100,0))
			qp.setPen(QColor(0,100,0))

			dx=self.load[i].cluster*w/100.0
			qp.drawRect(int(w), int(h-dy*i), int(-dx), int(dy))

			qp.setBrush(QColor(0,0,255))
			qp.setPen(QColor(0,0,255))

			dx=self.load[i].wait*w
			if dx<=w:
				qp.drawRect(int(w), int(h-dy*i), int(-dx), int(dy))
			
			



