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
import time
import ctypes
from gQtCore import QSize, Qt , QPoint, QRect
from PySide2.QtWidgets import QWidget, QDialog, QMenu
from PySide2.QtGui import QPainter,QFont,QColor,QPen,QPolygon

from gQtCore import gSignal
from math import fabs, pow, sqrt
from inp import inp
from vec import vec

from cal_path import sim_paths
from gui_util import yes_no_dlg

from json_dialog import json_dialog
from bytes2str import bytes2str

from NSVGimage import NSVGimage,NSVGpath,NSVGpaint,NSVGshape
from json_c import json_c
from json_c import json_tree_c

class display_component():
	def __init__(self):
		self.x0=-1
		self.y0=-1
		self.x1=-1
		self.y1=-1
		self.I=""
		self.V=""
		self.comp="none"
		self.name="none"
		self.dir="north"

	def __str__(self):
		return str(self.x0)+" "+str(self.y0)+" "+str(self.x1)+" "+str(self.y1)+" "+self.name

	def __eq__(self,a):
		if self.x0==a.x0:
			if self.y0==a.y0:
				if self.x1==a.x1:
					if self.y1==a.y1:
						return True

		if self.x0==a.x1:
			if self.y0==a.y1:
				if self.x1==a.x0:
					if self.y1==a.y0:
						return True
		return False

	def get_direction(self):
		if self.x0==self.x1:
			if self.y1>self.y0:
				return "up"
			else:
				return "down"

		if self.y0==self.y1:
			if self.x1>self.x0:
				return "right"
			else:
				return "left"

class ersatzschaltbild(QWidget):

	def __init__(self):
		super(ersatzschaltbild, self).__init__()
		self.bin=json_tree_c()

		self.dx=80
		self.dy=80
		self.lib=sim_paths.get_dll_py()

		self.objects=[]
		self.origonal_objects=[]

		self.editable=True

		self.selected="diode"
		self.shift_x=-self.dx/2
		self.shift_y=-self.dy/2
		self.hover=display_component()
		self.menu_build()
		self.file_current_voltage=None
		self.show_resistance_values=True
		self.svgs={}
		self.load_svgs()
		self.drag_start_x=None
		self.drag_start_y=None

	def load_svgs(self):
		for f in os.listdir(sim_paths.get_components_path()):
			if f.endswith(".svg"):
				svg_file=os.path.join(sim_paths.get_components_path(),f)
				image = NSVGimage()
				image.load(svg_file)
				image.norm(self.dx,self.dy)
				self.svgs[f[:-4]]=image

	def __del__(self):
		for attr, value in self.svgs.items():
			value.free()

	def objects_push(self):
		self.origonal_objects=[]
		for o in self.objects:
			self.origonal_objects.append(o)

	def objects_pop(self):
		self.objects=[]
		for o in self.origonal_objects:
			self.objects.append(o)


	def clear(self):
		self.objects=[]

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		self.drawWidget(qp)
		qp.end()

	def draw_mesh(self,qp):
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

	def drawWidget(self, qp):
		font = QFont('Sans', 11, QFont.Normal)
		qp.setFont(font)

		self.draw_mesh(qp)
		component_index=0
		for o in self.objects:
			if o.comp in self.svgs:
				image=self.svgs[o.comp]
				shape=image.p.contents.shapes
				r=ctypes.c_int()
				g=ctypes.c_int()
				b=ctypes.c_int()
				image.lib.svg_get_rgb(shape,ctypes.byref(r),ctypes.byref(g),ctypes.byref(b))
				pen = QPen(QColor(r.value, g.value, b.value), 4, Qt.SolidLine)
				qp.setPen(pen)
				while(shape):
					path=shape.contents.paths
					while(path):
						i=0
						while(i<path.contents.npts-1):
							p=ctypes.POINTER(ctypes.c_float)
							x=path.contents.pts[i*2]
							y=path.contents.pts[i*2+1]
							if o.get_direction()=="down":
								x,y=path.contents.rotate(x,y,-90)
							elif o.get_direction()=="up":
								x,y=path.contents.rotate(x,y,90)
							#print(o.get_direction())
							x0=o.x0*self.dx+x*self.dx
							y0=o.y0*self.dy+y*self.dy

							x=path.contents.pts[i*2+6]
							y=path.contents.pts[i*2+7]
							if o.get_direction()=="down":
								x,y=path.contents.rotate(x,y,-90)
							elif o.get_direction()=="up":
								x,y=path.contents.rotate(x,y,90)

							x1=o.x0*self.dx+x*self.dx
							y1=o.y0*self.dy+y*self.dy
							
							qp.drawLine(x0+self.shift_x, y0+self.shift_y, x1+self.shift_x, y1+self.shift_y)
							i=i+3

						path=path.contents.next
					shape=shape.contents.next

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
					path="circuit.circuit_diagram"+".segment"+str(component_index)
					R=self.bin.get_token_value(path,"R")
					if R!=None:
						qp.drawText(o.x0*self.dx+self.dx/4.0+self.shift_x, o.y0*self.dy-self.dy*2/8.0+self.shift_y, self.resistance_to_text(R))

			component_index=component_index+1
	def wheelEvent(self, event):
		numDegrees = event.delta() / 8
		numSteps = numDegrees / 15
		self.dx=self.dx+int(numSteps)
		self.dy=self.dy+int(numSteps)
		self.repaint()

	def resistance_to_text(self,val):
		buf = (ctypes.c_char * 64)()
		self.lib.ohms_with_units(buf,ctypes.c_double(val))
		ret=bytes2str(ctypes.cast(buf, ctypes.c_char_p).value)
		return ret+"\u03A9"

	def load(self):
		t=time.time()  
		self.objects=[]
		segments=self.bin.get_token_value("circuit.circuit_diagram","segments")
		for s in range(0,segments):
			path="circuit.circuit_diagram"+".segment"+str(s)
			o=display_component()
			o.x0=self.bin.get_token_value(path,"x0")
			o.y0=self.bin.get_token_value(path,"y0")
			o.x1=self.bin.get_token_value(path,"x1")
			o.y1=self.bin.get_token_value(path,"y1")

			o.name=self.bin.get_token_value(path,"name")
			o.comp=self.bin.get_token_value(path,"comp")
			
			o.I=""
			o.V=""
			self.add_object(o)

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

		
	def add_object(self,component):
		self.objects.append(component)
		return len(self.objects)-1

	def add_object0(self,x0,y0,x1,y1,comp):
		component=display_component()
		component.x0=x0
		component.y0=y0
		component.x1=x1
		component.y1=y1
		component.comp=comp
		component.name=comp
		self.objects.append(component)

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
		self.drag_start_x=None
		self.drag_start_y=None
		data=json_c("")

		if self.editable==False:
			return

		if self.bin.get_token_value("circuit","enabled")==False:
			result=yes_no_dlg(self,_("Are you sure you want to edit the circuit directly?  The circuit will no longer automaticly be updated as you change the layer structure, and the electrical parameters editor will be disabled.  Use can use the reset function in the circuit diagram editor to resore this functionality"))
			if result == False:
				return
			else:
				self.bin.set_token_value("circuit","enabled",True)
				self.bin.save()

		if event.button() == Qt.LeftButton:
			x0,y0,x1,y1,direction=self.find_click_points(event)
			c=display_component()
			c.x0=x0
			c.y0=y0
			c.x1=x1
			c.y1=y1

			index=self.find_component_index(c)

			if self.selected=="clean":
				if index!=-1:
					self.objects.pop(index)
					self.bin.delete_segment("circuit.circuit_diagram","segment"+str(index))
			else:
				if index==-1:
					if self.selected=="pointer":
						return
					if self.selected=="all-scroll":
						return

					c.comp=self.selected

					self.objects.append(c)
					path_of_new_segment=self.bin.make_new_segment("circuit.circuit_diagram","",-1)
					self.bin.set_token_value(path_of_new_segment,"x0",x0)
					self.bin.set_token_value(path_of_new_segment,"x1",x1)
					self.bin.set_token_value(path_of_new_segment,"y0",y0)
					self.bin.set_token_value(path_of_new_segment,"y1",y1)
					self.bin.set_token_value(path_of_new_segment,"comp",self.selected)

				else:
					path="circuit.circuit_diagram"+".segment"+str(index)

					self.a=json_dialog(data,title=_("Component")+": "+self.bin.get_token_value(path,"name"))
					ret=None

					data.json_py_add_obj_string("", "comp", self.bin.get_token_value(path,"comp"))
					data.json_py_add_obj_string("", "name0", self.bin.get_token_value(path,"name"))
					if self.objects[index].comp=="resistor":
						data.json_py_add_obj_double("", "com_R", self.bin.get_token_value(path,"R"))
						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"R",data.get_token_value("","com_R"))
					elif self.objects[index].comp=="capacitor":
						data.json_py_add_obj_double("", "com_C", self.bin.get_token_value(path,"C"))
						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"C",data.get_token_value("","com_C"))
					elif self.objects[index].comp=="inductor":
						data.json_py_add_obj_double("", "com_L", self.bin.get_token_value(path,"L"))
						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"L",data.get_token_value("","com_L"))
					elif self.objects[index].comp=="diode":
						data.json_py_add_obj_double("", "com_nid", self.bin.get_token_value(path,"nid"))
						data.json_py_add_obj_double("", "com_I0", self.bin.get_token_value(path,"I0"))
						data.json_py_add_obj_string("", "com_layer", self.bin.get_token_value(path,"layer"))
						data.json_py_add_obj_double("", "Dphotoneff", self.bin.get_token_value(path,"Dphotoneff"))
						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"nid",data.get_token_value("","com_nid"))
							self.bin.set_token_value(path,"I0",data.get_token_value("","com_I0"))
							self.bin.set_token_value(path,"layer",data.get_token_value("","com_layer"))
							self.bin.set_token_value(path,"Dphotoneff",data.get_token_value("","Dphotoneff"))
					elif self.objects[index].comp=="power":
						data.json_py_add_obj_double("", "com_a", self.bin.get_token_value(path,"a"))
						data.json_py_add_obj_double("", "com_b", self.bin.get_token_value(path,"b"))
						data.json_py_add_obj_double("", "com_c", self.bin.get_token_value(path,"c"))
						data.json_py_add_obj_double("", "com_I0", self.bin.get_token_value(path,"I0"))
						data.json_py_add_obj_string("", "com_layer", self.bin.get_token_value(path,"layer"))
						data.json_py_add_obj_double("", "Dphotoneff", self.bin.get_token_value(path,"Dphotoneff"))

						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"I0",data.get_token_value("","com_I0"))
							self.bin.set_token_value(path,"a",data.get_token_value("","com_a"))
							self.bin.set_token_value(path,"b",data.get_token_value("","com_b"))
							self.bin.set_token_value(path,"c",data.get_token_value("","com_c"))
							self.bin.set_token_value(path,"layer",data.get_token_value("","com_layer"))
							self.bin.set_token_value(path,"Dphotoneff",data.get_token_value("","Dphotoneff"))
					elif self.objects[index].comp=="barrier":
						data.json_py_add_obj_double("", "com_I0", self.bin.get_token_value(path,"I0"))
						data.json_py_add_obj_double("", "com_phi0", self.bin.get_token_value(path,"phi0"))
						data.json_py_add_obj_double("", "com_b0", self.bin.get_token_value(path,"b0"))
						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"I0",data.get_token_value("","com_I0"))
							self.bin.set_token_value(path,"phi0",data.get_token_value("","com_phi0"))
							self.bin.set_token_value(path,"b0",data.get_token_value("","com_b0"))
					elif self.objects[index].comp=="diode_n":
						data.json_py_add_obj_double("", "com_nid", self.bin.get_token_value(path,"nid"))
						data.json_py_add_obj_double("", "com_nid_sigma", self.bin.get_token_value(path,"nid_sigma"))
						data.json_py_add_obj_double("", "com_I0", self.bin.get_token_value(path,"I0"))
						data.json_py_add_obj_double("", "com_I0_sigma", self.bin.get_token_value(path,"I0_sigma"))
						data.json_py_add_obj_string("", "com_layer", self.bin.get_token_value(path,"layer"))
						data.json_py_add_obj_double("", "Dphotoneff", self.bin.get_token_value(path,"Dphotoneff"))
						print(">>>>>",path)
						data.json_py_add_obj_double("", "com_Rs", self.bin.get_token_value(path,"a"))
						data.json_py_add_obj_double("", "com_Rs_sigma", self.bin.get_token_value(path,"a_sigma"))
						data.json_py_add_obj_double("", "com_Rsh", self.bin.get_token_value(path,"b"))
						data.json_py_add_obj_double("", "com_Rsh_sigma", self.bin.get_token_value(path,"b_sigma"))
						data.json_py_add_obj_int("", "com_count", self.bin.get_token_value(path,"count"))
						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"nid",data.get_token_value("","com_nid"))
							self.bin.set_token_value(path,"nid_sigma",data.get_token_value("","com_nid_sigma"))
							self.bin.set_token_value(path,"I0",data.get_token_value("","com_I0"))
							self.bin.set_token_value(path,"I0_sigma",data.get_token_value("","com_I0_sigma"))
							self.bin.set_token_value(path,"layer",data.get_token_value("","com_layer"))
							self.bin.set_token_value(path,"Dphotoneff",data.get_token_value("","Dphotoneff"))
							self.bin.set_token_value(path,"a",data.get_token_value("","com_Rs"))
							self.bin.set_token_value(path,"a_sigma",data.get_token_value("","com_Rs_sigma"))
							self.bin.set_token_value(path,"b",data.get_token_value("","com_Rsh"))
							self.bin.set_token_value(path,"b_sigma",data.get_token_value("","com_Rsh_sigma"))
							self.bin.set_token_value(path,"count",data.get_token_value("","com_count"))
					elif self.objects[index].comp=="diode_ns1":
						data.json_py_add_obj_double("", "com_nid", self.bin.get_token_value(path,"nid"))
						data.json_py_add_obj_double("", "com_nid_sigma", self.bin.get_token_value(path,"nid_sigma"))
						data.json_py_add_obj_double("", "com_I0", self.bin.get_token_value(path,"I0"))
						data.json_py_add_obj_double("", "com_I0_sigma", self.bin.get_token_value(path,"I0_sigma"))
						data.json_py_add_obj_string("", "com_layer", self.bin.get_token_value(path,"layer"))
						data.json_py_add_obj_double("", "Dphotoneff", self.bin.get_token_value(path,"Dphotoneff"))
						data.json_py_add_obj_double("", "com_Rs", self.bin.get_token_value(path,"a"))
						data.json_py_add_obj_double("", "com_Rs_sigma", self.bin.get_token_value(path,"a_sigma"))
						data.json_py_add_obj_double("", "com_Rsh", self.bin.get_token_value(path,"b"))
						data.json_py_add_obj_double("", "com_Rsh_sigma", self.bin.get_token_value(path,"b_sigma"))
						#s_shape_circuit
						data.json_py_add_obj_double("", "com_Rs1", self.bin.get_token_value(path,"b0"))
						data.json_py_add_obj_double("", "com_Rs1_sigma", self.bin.get_token_value(path,"b0_sigma"))
						data.json_py_add_obj_double("", "com_I0_1", self.bin.get_token_value(path,"phi0"))
						data.json_py_add_obj_double("", "com_I0_1_sigma", self.bin.get_token_value(path,"phi0_sigma"))
						data.json_py_add_obj_double("", "com_nid_1", self.bin.get_token_value(path,"c"))
						data.json_py_add_obj_double("", "com_nid_1_sigma", self.bin.get_token_value(path,"c_sigma"))
						data.json_py_add_obj_bool("", "com_enable_sigma", self.bin.get_token_value(path,"com_enable_sigma"))
						#count
						data.json_py_add_obj_int("", "com_count", self.bin.get_token_value(path,"count"))
						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"nid",data.get_token_value("","com_nid"))
							self.bin.set_token_value(path,"nid_sigma",data.get_token_value("","com_nid_sigma"))
							self.bin.set_token_value(path,"I0",data.get_token_value("","com_I0"))
							self.bin.set_token_value(path,"I0_sigma",data.get_token_value("","com_I0_sigma"))
							self.bin.set_token_value(path,"layer",data.get_token_value("","com_layer"))
							self.bin.set_token_value(path,"Dphotoneff",data.get_token_value("","Dphotoneff"))
							self.bin.set_token_value(path,"a",data.get_token_value("","com_Rs"))
							self.bin.set_token_value(path,"a_sigma",data.get_token_value("","com_Rs_sigma"))
							self.bin.set_token_value(path,"b",data.get_token_value("","com_Rsh"))
							self.bin.set_token_value(path,"b_sigma",data.get_token_value("","com_Rsh_sigma"))
							#s_shape_circuit
							self.bin.set_token_value(path,"b0",data.get_token_value("","com_Rs1"))
							self.bin.set_token_value(path,"b0_sigma",data.get_token_value("","com_Rs1_sigma"))
							self.bin.set_token_value(path,"phi0",data.get_token_value("","com_I0_1"))
							self.bin.set_token_value(path,"phi0_sigma",data.get_token_value("","com_I0_1_sigma"))
							self.bin.set_token_value(path,"c",data.get_token_value("","com_nid_1"))
							self.bin.set_token_value(path,"c_sigma",data.get_token_value("","com_nid_1_sigma"))
							self.bin.set_token_value(path,"com_enable_sigma",data.get_token_value("","com_enable_sigma"))
							#count
							data.json_py_add_obj_int("", "com_count", self.bin.get_token_value(path,"count"))
					elif self.objects[index].comp=="diode_ns2":
						data.json_py_add_obj_double("", "com_nid", self.bin.get_token_value(path,"nid"))
						data.json_py_add_obj_double("", "com_nid_sigma", self.bin.get_token_value(path,"nid_sigma"))
						data.json_py_add_obj_double("", "com_I0", self.bin.get_token_value(path,"I0"))
						data.json_py_add_obj_double("", "com_I0_sigma", self.bin.get_token_value(path,"I0_sigma"))
						data.json_py_add_obj_string("", "com_layer", self.bin.get_token_value(path,"layer"))
						data.json_py_add_obj_double("", "Dphotoneff", self.bin.get_token_value(path,"Dphotoneff"))
						data.json_py_add_obj_double("", "com_Rs", self.bin.get_token_value(path,"a"))
						data.json_py_add_obj_double("", "com_Rs_sigma", self.bin.get_token_value(path,"a_sigma"))
						data.json_py_add_obj_double("", "com_Rsh", self.bin.get_token_value(path,"b"))
						data.json_py_add_obj_double("", "com_Rsh_sigma", self.bin.get_token_value(path,"b_sigma"))
						#s_shape_circuit
						data.json_py_add_obj_double("", "com_Rs1", self.bin.get_token_value(path,"b0"))
						data.json_py_add_obj_double("", "com_Rs1_sigma", self.bin.get_token_value(path,"b0_sigma"))
						data.json_py_add_obj_double("", "com_I0_1", self.bin.get_token_value(path,"phi0"))
						data.json_py_add_obj_double("", "com_I0_1_sigma", self.bin.get_token_value(path,"phi0_sigma"))
						data.json_py_add_obj_double("", "com_nid_1", self.bin.get_token_value(path,"c"))
						data.json_py_add_obj_double("", "com_nid_1_sigma", self.bin.get_token_value(path,"c_sigma"))
						data.json_py_add_obj_bool("", "com_enable_sigma", self.bin.get_token_value(path,"com_enable_sigma"))
						#count
						data.json_py_add_obj_int("", "com_count", self.bin.get_token_value(path,"count"))

						ret=self.a.run()
						if ret==QDialog.Accepted:
							self.bin.set_token_value(path,"nid",data.get_token_value("","com_nid"))
							self.bin.set_token_value(path,"nid_sigma",data.get_token_value("","com_nid_sigma"))
							self.bin.set_token_value(path,"I0",data.get_token_value("","com_I0"))
							self.bin.set_token_value(path,"I0_sigma",data.get_token_value("","com_I0_sigma"))
							self.bin.set_token_value(path,"layer",data.get_token_value("","com_layer"))
							self.bin.set_token_value(path,"Dphotoneff",data.get_token_value("","Dphotoneff"))
							self.bin.set_token_value(path,"a",data.get_token_value("","com_Rs"))
							self.bin.set_token_value(path,"a_sigma",data.get_token_value("","com_Rs_sigma"))
							self.bin.set_token_value(path,"b",data.get_token_value("","com_Rsh"))
							self.bin.set_token_value(path,"b_sigma",data.get_token_value("","com_Rsh_sigma"))
							#s_shape_circuit
							self.bin.set_token_value(path,"b0",data.get_token_value("","com_Rs1"))
							self.bin.set_token_value(path,"b0_sigma",data.get_token_value("","com_Rs1_sigma"))
							self.bin.set_token_value(path,"phi0",data.get_token_value("","com_I0_1"))
							self.bin.set_token_value(path,"phi0_sigma",data.get_token_value("","com_I0_1_sigma"))
							self.bin.set_token_value(path,"c",data.get_token_value("","com_nid_1"))
							self.bin.set_token_value(path,"c_sigma",data.get_token_value("","com_nid_1_sigma"))
							self.bin.set_token_value(path,"com_enable_sigma",data.get_token_value("","com_enable_sigma"))

							#count
							data.json_py_add_obj_int("", "com_count", self.bin.get_token_value(path,"count"))
							
					if ret==QDialog.Accepted:
						self.bin.set_token_value(path,"comp",data.get_token_value("","comp"))
						self.bin.set_token_value(path,"name",data.get_token_value("","name0"))

			self.bin.save()
			self.load()

		elif event.button() == Qt.RightButton:
            #do what you want here
			print("Right Button Clicked")
		data.free()

	def mouseMoveEvent(self, event):
		if event.buttons() & Qt.LeftButton:
			if self.selected=="all-scroll":
				if self.drag_start_x==None:
					self.drag_start_x=event.globalPos().x()
					self.drag_start_y=event.globalPos().y()

				self.shift_x=self.shift_x+event.globalPos().x()-self.drag_start_x
				self.shift_y=self.shift_y+event.globalPos().y()-self.drag_start_y

				self.drag_start_x=event.globalPos().x()
				self.drag_start_y=event.globalPos().y()
				self.repaint()

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
		if self.bin.get_token_value("circuit","enabled")==True:
			self.menu_circuit_from_epitaxy.setChecked(False)
			self.menu_circuit_freehand.setChecked(True)
		else:
			self.menu_circuit_from_epitaxy.setChecked(True)
			self.menu_circuit_freehand.setChecked(False)

	def contextMenuEvent(self,event):
		self.main_menu.exec_(event.globalPos())

	def callback_toggle_diagram_src(self):
		enabled=not self.bin.get_token_value("circuit","enabled")
		self.bin.set_token_value("circuit","enabled",enabled)
		self.menu_update()
		self.bin.save()


