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

## @package gl_fallback
#  If OpenGL does not work fall back to this.
#

import math
import os

import i18n
_ = i18n.language.gettext

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QMessageBox, QLineEdit,QLabel
from gQtCore import QTimer
from PySide2.QtGui import QPainter,QFont,QColor,QPen,QPainterPath,QBrush

from dat_file import dat_file
from global_objects import global_object_register
from cal_path import sim_paths

from PySide2.QtWidgets import QMessageBox
from gl_toolbar import gl_toolbar
from gl_views import gl_views
from gl_main import gl_main
from gl_scale import gl_scale_class
from json_c import json_tree_c
import ctypes

class gl_fallback(QWidget, gl_toolbar,gl_views):

	def __init__(self):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		gl_toolbar.__init__(self)
		#self.setMinimumSize(600, 500)
		self.box_shown=False
		self.gl_main=gl_main()
		self.scale=gl_scale_class(self.gl_main.scale)
		self.failed=False
		self.open_gl_working=False
		self.timer=None
		self.suns=0.0
		self.lastPos=None
		self.mouse_click_time=0.0
		self.wx = []
		self.wy = []

		x = 0.0
		while x < 100.0:
			self.wx.append(x)
			self.wy.append(math.sin(x * math.pi * 0.1) * 15)
			x += 0.1


	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawWidget(qp)
		qp.end()


	def drawWidget(self, qp):
		font = QFont('Sans', 11, QFont.Normal)
		qp.setFont(font)

		pos=0.0
		emission=False
		tot=self.bin.lib.json_epitaxy_get_len(ctypes.byref(json_tree_c()))
		layers=self.bin.get_token_value("epitaxy","segments")
		self.suns=self.bin.get_token_value("optical.light_sources","Psun")

		for l in range(0,layers):
			path="epitaxy.segment"+str(l)
			obj_type=self.bin.get_token_value(path,"obj_type")
			dy=self.bin.get_token_value(path,"dy")
			red=self.bin.get_token_value(path,"color_r")
			green=self.bin.get_token_value(path,"color_g")
			blue=self.bin.get_token_value(path,"color_b")
			pl_emission_enabled=self.bin.get_token_value(path+".shape_pl","pl_emission_enabled")

			if obj_type=="active":
				if pl_emission_enabled==True:
					emission=True

			thick=200.0*dy/tot
			pos=pos+thick

			self.draw_box(qp,200,450.0-pos,thick*0.9,red,green,blue,layers-1-l)

		step=50.0

		if self.suns<=0.01:
			step=200
		elif self.suns<=0.1:
			step=100
		elif self.suns<=1.0:
			step=50
		elif self.suns<=10.0:
			step=10
		else:
			step=5.0
		if self.suns!=0:
			for x in range(0,200,step):
				self.draw_photon(qp,210+x,100,False)

		if emission==True:
			for x in range(0,200,50):
				self.draw_photon(qp,240+x,140,True)

		self.draw_mode(qp,200,250)
		
		#if self.box_shown==False:
		#	self.box_shown=True
		#	self.show_error()

	def show_error(self):
		msgBox = QMessageBox(self)
		msgBox.setIcon(QMessageBox.Warning)
		msgBox.setText("Warning:")
		text="You do not have working 3D graphics hardware acceleration on your PC. This could be because:\n 1. If your PC is modern it is likely that you don't have the correct drivers installed.\n 2. If your PC is older it is possible you don't have 3D acceleration hardware.\n 3.  If you are using the software through a virtual machine it could be that your VM is not correctly configured for 3D graphics acceleration.\n\nYou can continue using the software but it will be using a 2D fallback mode. The model will still work, the results will be the same the interface just won't be as nice and some 3D features won't work."
		msgBox.setInformativeText(text)
		print(text)
		msgBox.setStandardButtons(QMessageBox.Ok )
		msgBox.setDefaultButton(QMessageBox.Ok)
		msgBox.setMinimumWidth(700)
		msgBox.exec_()


	def draw_photon(self,qp,start_x,start_y,up):
		pen=QPen()
		pen.setWidth(2)
		
		if up==True:
			pen.setColor(QColor(0,0,255))
		else:
			pen.setColor(QColor(0,255,0))

		qp.setPen(pen)

		for i in range(1,len(self.wx)):
			qp.drawLine((int)(start_x-self.wy[i-1]),(int)(start_y+self.wx[i-1]),(int)(start_x-self.wy[i]),(int)(start_y+self.wx[i]))

		if up==True:
			path=QPainterPath()

			path.moveTo (start_x-10, start_y);
			path.lineTo (start_x-10, start_y);

			path.lineTo (start_x+10,   start_y);

			path.lineTo (start_x, start_y-20);
			
			qp.fillPath (path, QBrush (QColor (0,0,255)))
		else:
			path=QPainterPath()

			path.moveTo (start_x-10, start_y+100.0);
			path.lineTo (start_x-10, start_y+100.0);

			path.lineTo (start_x+10,   start_y+100.0);

			path.lineTo (start_x, start_y+100.0+20);

			qp.setPen (Qt.NoPen);
			qp.fillPath (path, QBrush (QColor (0,255,0)))


	def draw_box(self,qp,x,y,h,r,g,b,layer):

		text=""
		w=200
		qp.setBrush(QColor(r*255,g*255,b*255))
		qp.drawRect(x, y, 200,h)

		path="epitaxy.segment"+str(layer)
		obj_type=self.bin.get_token_value(path,"obj_type")
		name=self.bin.get_token_value(path,"name")

		if obj_type=="active":
			text=name+" (active)"
			qp.setBrush(QColor(0,0,0.7*255))
			qp.drawRect(x+w+5, y, 20,h)
		else:
			text=name

		qp.drawText(x+200+40, y+h/2, text)
		
		return

	def draw_mode(self,qp,start_x,start_y):
		pen=QPen()
		pen.setWidth(3)
		pen.setColor(QColor(0,0,0))

		qp.setPen(pen)
		data=dat_file()
		if data.load(os.path.join(sim_paths.get_sim_path(),"optical_output","photons_yl_norm.csv"))==True:
			for i in range(1,data.y_len):
				
				x0=(start_x-data.data[0][0][i-1]*40-10)
				y0=(start_y+(200*(i-1)/data.y_len))
				x1=(start_x-data.data[0][0][i]*40-10)
				y1=(start_y+(200*i/data.y_len))
				if math.isnan(x0)==False and math.isnan(y0)==False :
					x0=(int)(x0)
					y0=(int)(y0)
					x1=(int)(x1)
					y1=(int)(y1)
					qp.drawLine(x0,y0,x1,y1)


	def set_sun(self,suns):
		self.suns=suns

	def force_redraw(self):
		self.repaint()

	def force_redraw_hard(self):
		self.repaint()

	def rebuild_scene(self):
		pass

	def gl_graph_load_files(self,files):
		pass

