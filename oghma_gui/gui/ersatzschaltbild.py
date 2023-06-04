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

## @package gtkswitch
#  Package to provide an equivlent to the gnome switch
#


import os
import math
from gQtCore import QSize, Qt , QPoint, QRect
from PySide2.QtWidgets import QWidget, QDialog, QMenu
from PySide2.QtGui import QPainter,QFont,QColor,QPen,QPolygon

from gQtCore import gSignal
from math import fabs, pow, sqrt
from cal_path import get_components_path
from inp import inp
from vec import vec

from cal_path import sim_paths
from gui_util import yes_no_dlg

from json_dialog import json_dialog
from json_circuit import json_component
from json_root import json_root
from json_base import json_base

class draw_object():
	def __init__(self):
		self.v0=vec()
		self.v1=vec()
		self.type="l"
		self.r=1.0
		self.text=""
		self.I=""
		self.V=""

class ersatzschaltbild(QWidget):

	def __init__(self):      
		super(ersatzschaltbild, self).__init__()
		self.dx=160
		self.dy=160

		self.objects=[]
		self.origonal_objects=[]

		self.editable=True

		self.selected="diode"
		#self.setMouseTracking(True)
		self.init()
		self.hover=json_component()
		self.menu_build()
		self.file_current_voltage=None
		self.show_resistance_values=True

	def objects_push(self):
		self.origonal_objects=[]
		for o in self.objects:
			self.origonal_objects.append(o)

	def objects_pop(self):
		self.objects=[]
		for o in self.origonal_objects:
			self.objects.append(o)

	def init(self):
		self.shift_x=-self.dx/2
		self.shift_y=-self.dy/2

	def clear(self):
		self.objects=[]

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawWidget(qp)
		qp.end()


	def drawWidget(self, qp):
		font = QFont('Sans', 11, QFont.Normal)
		qp.setFont(font)

		pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)
		
		qp.setPen(pen)
		qp.setBrush(Qt.NoBrush)

		width = self.width()
		height = self.height()

		maxx=int(width/self.dx)+1
		maxy=int(height/self.dy)+1
		self.xmesh=[]
		self.ymesh=[]

		for nx in range(0,maxx):
			x=self.dx*nx
			self.xmesh.append(x)

		for ny in range(0,maxy):
			y=self.dy*ny
			self.ymesh.append(y)


		for nx in range(0,maxx):
			for ny in range(0,maxy):
				x=self.dx*nx
				y=self.dy*ny

				pen = QPen(QColor(0, 0, 255), 1, Qt.SolidLine)
				qp.setPen(pen)
				qp.setBrush(Qt.NoBrush)
				for xx in range(-2+x,3+x):
					qp.drawPoint(xx+self.shift_x, y+self.shift_y)
					
				for yy in range(-3+y,3+y):
					qp.drawPoint(x+self.shift_x, yy+self.shift_y)





		for o in self.objects:
			#qp.drawLine(o.x0*self.dx, o.y0*self.dx, o.x1*self.dx, o.y1*self.dx)
			#qp.drawEllipse(QRect(o.x0*self.dx, o.y0*self.dx,10,10));
			pen = QPen(QColor(0, 0, 0), 4, Qt.SolidLine)
			qp.setPen(pen)
			for draw_obj in o.lines:
				if draw_obj.type=="l":
					x0=o.x0*self.dx+draw_obj.v0.x
					y0=o.y0*self.dy+draw_obj.v0.y
					x1=o.x0*self.dx+draw_obj.v1.x
					y1=o.y0*self.dy+draw_obj.v1.y

					qp.drawLine(x0+self.shift_x, y0+self.shift_y, x1+self.shift_x, y1+self.shift_y)
				elif draw_obj.type=="c":
					x0=o.x0*self.dx+draw_obj.v0.x-draw_obj.r/2.0
					y0=o.y0*self.dy+draw_obj.v0.y-draw_obj.r/2.0
					qp.drawEllipse(QRect(x0+self.shift_x, y0+self.shift_y, draw_obj.r, draw_obj.r));
				elif draw_obj.type=="t":
					qp.drawText(o.x0*self.dx+draw_obj.v0.x+self.shift_x, o.y0*self.dy+draw_obj.v0.y+self.shift_y, draw_obj.text)

			pen = QPen(QColor(0, 0, 255), 1, Qt.SolidLine)
			qp.setPen(pen)

			try:
				if o.I!="":
					qp.drawText(o.x0*self.dx-self.dx/2.5, o.y0*self.dy-self.dy/1.1, o.I)
			except:
				pass

			try:
				if o.V!="":
					qp.drawText(o.x0*self.dx-self.dx/2.5, o.y0*self.dy-self.dy/1.4, o.V)
			except:
				pass
			if self.show_resistance_values==True:
				if o.comp=="resistor":
					qp.drawText(o.x0*self.dx-self.dx/4.0, o.y0*self.dy-self.dy/8, self.resistance_to_text(o.R))
			

	def resistance_to_text(self,r):
		if r<1e-3:
			return str(round(r*1e6))+"u\u03A9"
		elif r<1.0:
			return str(round(r*1e3))+"m\u03A9"
		elif r<1e3:
			return str(round(r*1e0))+"\u03A9"
		elif r<1e6:
			return str(round(r*1e-3))+"k\u03A9"
		else:
			return str(round(r*1e-6))+"M\u03A9"
		
	def save(self):
		data=json_root()
		data.circuit.circuit_diagram.segments=[]
		for o in self.objects:
			data.circuit.circuit_diagram.segments.append(o)
		data.save()

	def load(self):
		self.objects=[]
		data=json_root()
		for s in data.circuit.circuit_diagram.segments:
			s.I=""
			s.V=""
			self.add_object(s)

		if self.file_current_voltage!=None:
			self.f=inp()
			self.f.load_json(self.file_current_voltage)
			segments=self.f.json['segments']
			for i in range(0,segments):
				s=self.f.json['segment'+str(i)]
				uid=s['uid']
				I=s['i']
				v0=s['v0']
				v1=s['v1']
				self.objects[uid].I=str("{:.2e}".format(fabs(I)))+"A"
				self.objects[uid].V=str("{:.2e}".format(fabs(v0-v1)))+"V"
				self.objects[uid].V=self.objects[uid].V.replace("e+00","")
				self.objects[uid].V=self.objects[uid].V.replace("e-0","e-")
				self.objects[uid].I=self.objects[uid].I.replace("e-0","e-")
		self.repaint()

	def load_component(self,c):
		f=inp()
		file_name=os.path.join(get_components_path(),c.comp+".inp")
		f.load(file_name)
		if f.lines==False:
			return []

		pi=[]
		for l in f.lines:
			s=l.split()
			if len(s)>1:
				if s[0]=="l":
					draw_obj=draw_object()
					draw_obj.v0.x=float(s[1])
					draw_obj.v0.y=float(s[2])
					draw_obj.v0.x*=self.dx
					draw_obj.v0.y*=self.dy

					draw_obj.v1.x=float(s[3])
					draw_obj.v1.y=float(s[4])
					draw_obj.v1.x*=self.dx
					draw_obj.v1.y*=self.dy
					draw_obj.type="l"
					pi.append(draw_obj)

				if s[0]=="c":
					draw_obj=draw_object()
					draw_obj.v0.x=float(s[1])
					draw_obj.v0.y=float(s[2])
					draw_obj.v0.x*=self.dx
					draw_obj.v0.y*=self.dy
					draw_obj.type="c"
					draw_obj.r=float(s[3])*self.dx
					pi.append(draw_obj)
				if s[0]=="t":
					draw_obj=draw_object()
					draw_obj.v0.x=float(s[1])
					draw_obj.v0.y=float(s[2])
					draw_obj.v0.x*=self.dx
					draw_obj.v0.y*=self.dy
					draw_obj.type="t"
					draw_obj.text=s[3]
					pi.append(draw_obj)

		if c.get_direction()=="down":
			self.rotate(pi,degrees=-90)
		elif c.get_direction()=="up":
			self.rotate(pi,degrees=90)

		return pi

	def rotate(self,lines,degrees=90,add_y=0.0):
		for i in range(0,len(lines)):
			if lines[i].type=="l" or lines[i].type=="c" or lines[i].type=="t": 
				lines[i].v0=lines[i].v0.rotate(degrees)
				lines[i].v0.y=lines[i].v0.y+add_y
				lines[i].v1=lines[i].v1.rotate(degrees)
				lines[i].v1.y=lines[i].v1.y+add_y

			
	def add_object(self,component):
		component.lines=self.load_component(component)
		self.objects.append(component)

		return len(self.objects)-1

	def add_object0(self,x0,y0,x1,y1,comp):
		component=json_component()
		component.x0=x0
		component.y0=y0
		component.x1=x1
		component.y1=y1
		component.comp=comp
		component.name=comp
		component.lines=self.load_component(component)
		self.objects.append(component)

		return len(self.objects)-1


	def find_click_points(self,event):
		xmin_list=[]
		xpos=-1
		ypos=-1
		xx=0
		yy=0

		for x in self.xmesh:
			x0=event.x()-self.shift_x
			y0=event.y()-self.shift_y
			x1=x
			y1=0
			x2=x
			y2=self.height()+self.dy
			d=fabs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/sqrt(pow(y2-y1,2.0)+pow(x2-x1,2.0))
			xmin_list.append([xx, d])
			xx=xx+1

		ymin_list=[]
		for y in self.ymesh:
			x0=event.x()-self.shift_x
			y0=event.y()-self.shift_y
			x1=0
			y1=y
			x2=self.width()+self.dx
			y2=y
			d=fabs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/sqrt(pow(y2-y1,2.0)+pow(x2-x1,2.0))
			ymin_list.append([yy,d])
			yy=yy+1
		ymin_list=sorted(ymin_list,key=lambda x: x[1])
		xmin_list=sorted(xmin_list,key=lambda x: x[1])

		direction=""
		if ymin_list[0][1]<xmin_list[0][1]:		#closer to x or y axis
			x0=xmin_list[0][0]
			y0=ymin_list[0][0]
			x1=xmin_list[1][0]
			y1=ymin_list[0][0]
			if x0>x1:
				temp=x0
				x0=x1
				x1=temp
			direction="right"
		else:
			x0=xmin_list[0][0]
			y0=ymin_list[0][0]
			x1=xmin_list[0][0]
			y1=ymin_list[1][0]
			if y0>y1:
				temp=y0
				y0=y1
				y1=temp
			direction="up"

		return x0,y0,x1,y1,direction

	def find_component_index(self,c_in):
		for i in range(0,len(self.objects)):
			if (self.objects[i]==c_in):
				return i
		return -1

	def mouseReleaseEvent(self, event):

		if self.editable==False:
			return
		data=json_root()

		if data.circuit.enabled==False:
			result=yes_no_dlg(self,_("Are you sure you want to edit the circuit directly?  The circuit will no longer automaticly be updated as you change the layer structure, and the electrical parameters editor will be disabled.  Use can use the reset function in the circuit diagram editor to resore this functionality"))
			if result == False:
				return
			else:
				data.circuit.enabled=True
				data.save()

		if event.button() == Qt.LeftButton:
			x0,y0,x1,y1,direction=self.find_click_points(event)
			c=json_component()
			c.x0=x0
			c.y0=y0
			c.x1=x1
			c.y1=y1

			index=self.find_component_index(c)

			if self.selected=="clean":
				if index!=-1:
					self.objects.pop(index)
			else:
				if index==-1:
					c.comp=self.selected
					c.lines=self.load_component(c)
					#if direction=="up":
					#	self.rotate(c.lines)

					self.objects.append(c)
				else:
					self.a=json_dialog(_("Component")+": "+self.objects[index].name)
					ret=None
					data=json_base("dlg")
					data.var_list.append(["comp",self.objects[index].comp])
					data.var_list.append(["name0",self.objects[index].name])
					if self.objects[index].comp=="resistor":
						data.var_list.append(["com_R",self.objects[index].R])
						data.var_list_build()
						ret=self.a.run(data)
						if ret==QDialog.Accepted:
							self.objects[index].R=data.com_R
					elif self.objects[index].comp=="capacitor":
						data.var_list.append(["com_C",self.objects[index].C])
						data.var_list_build()
						ret=self.a.run(data)
						if ret==QDialog.Accepted:
							self.objects[index].C=data.com_C
					elif self.objects[index].comp=="inductor":
						data.var_list.append(["com_L",self.objects[index].L])
						data.var_list_build()
						ret=self.a.run(data)
						if ret==QDialog.Accepted:
							self.objects[index].L=data.com_L
					elif self.objects[index].comp=="diode":
						data.var_list.append(["com_nid",self.objects[index].nid])
						data.var_list.append(["com_I0",self.objects[index].I0])
						data.var_list.append(["com_layer",self.objects[index].layer])
						data.var_list.append(["Dphotoneff",self.objects[index].Dphotoneff])
						data.var_list_build()
						ret=self.a.run(data)
						if ret==QDialog.Accepted:
							self.objects[index].nid=data.com_nid
							self.objects[index].I0=data.com_I0
							self.objects[index].layer=data.com_layer
							self.objects[index].Dphotoneff=data.Dphotoneff
					elif self.objects[index].comp=="power":
						data.var_list.append(["com_a",self.objects[index].a])
						data.var_list.append(["com_b",self.objects[index].b])
						data.var_list.append(["com_c",self.objects[index].c])
						data.var_list.append(["com_I0",self.objects[index].I0])
						data.var_list.append(["com_layer",self.objects[index].layer])
						data.var_list.append(["Dphotoneff",self.objects[index].Dphotoneff])
						data.var_list_build()
						ret=self.a.run(data)
						if ret==QDialog.Accepted:
							self.objects[index].I0=data.com_I0
							self.objects[index].a=data.com_a
							self.objects[index].b=data.com_b
							self.objects[index].c=data.com_c
							self.objects[index].layer=data.com_layer
							self.objects[index].Dphotoneff=data.Dphotoneff
					if ret==QDialog.Accepted:
						self.objects[index].comp=data.comp
						self.objects[index].name=data.name0

			self.save()
			self.load()

		elif event.button() == Qt.RightButton:
            #do what you want here
			print("Right Button Clicked")

	def menu_build(self):
		self.main_menu = QMenu(self)

		export=self.main_menu.addMenu(_("Circuit diagram"))

		self.menu_circuit_from_epitaxy=export.addAction(_("Use epitaxy as base"))
		self.menu_circuit_from_epitaxy.triggered.connect(self.callback_toggle_diagram_src)
		self.menu_circuit_from_epitaxy.setCheckable(True)

		self.menu_circuit_freehand=export.addAction(_("Free hand drawing"))
		self.menu_circuit_freehand.triggered.connect(self.callback_toggle_diagram_src)
		self.menu_circuit_freehand.setCheckable(True)
		self.menu_update()

	def menu_update(self):
		data=json_root()
		if data.circuit.enabled==True:
			self.menu_circuit_from_epitaxy.setChecked(False)
			self.menu_circuit_freehand.setChecked(True)
		else:
			self.menu_circuit_from_epitaxy.setChecked(True)
			self.menu_circuit_freehand.setChecked(False)

	def contextMenuEvent(self,event):
		self.main_menu.exec_(event.globalPos())

	def callback_toggle_diagram_src(self):
		data=json_root()
		data.circuit.enabled=not data.circuit.enabled
		self.menu_update()
		data.save()


