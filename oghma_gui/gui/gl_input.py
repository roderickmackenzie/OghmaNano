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

## @package gl_input
#  The mouse and keyboard input to the OpenGL display.
#

import sys
open_gl_ok=False

import sys
from math import fabs

from PySide2.QtWidgets import QApplication
from gQtCore import QTimer, Qt
from PySide2.QtGui import QCursor,QKeySequence,QKeyEvent

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	pass


import time
from math import cos
from math import sin
from epitaxy import get_epi
from json_root import json_root
import webbrowser
from bytes2str import bytes2str
from vec import vec

class mouse_event():
	def __init__(self):
		self.time=0
		self.x=0
		self.y=0
		self.dxyz=vec()
		self.rotate_x=0.0
		self.rotate_y=0.0
		self.working=False
		self.drag=False
		self.rotate=False
		self.scale=False

	def delta_time(self):
		return time.time()-self.time

class gl_input():

	def __init__(self):
		self.cursor=None
		self.last_object_clicked=None

	def keyPressEvent_han(self, event):
		keyname=event.key()
		modifiers = event.modifiers()

		if (keyname>64 and keyname<91 ) or (keyname>96 and keyname<123):
			keyname=chr(keyname)
			if keyname.isalpha()==True:
				if Qt.ShiftModifier == modifiers:
					keyname=keyname.upper()
				else:
					keyname=keyname.lower()


		if type(event) == QKeyEvent:
			modifiers = QApplication.keyboardModifiers()
			if event.text()=="f":
				self.showFullScreen()
			elif event.text()=="r":
				if self.timer==None:
					self.start_rotate()
				else:
					self.timer.stop()
					self.timer=None
			elif event.text()=="z":
				if self.timer==None:
					self.start_rotate()
					if self.active_view.zoom>-40:
						self.active_view.zoom =-400
					self.timer=QTimer()
					self.timer.timeout.connect(self.fzoom_timer)
					self.timer.start(50)
				else:
					self.timer.stop()
					self.timer=None

		if  modifiers == Qt.ControlModifier and keyname=='c':
			self.object_copy_json()
		if  modifiers == Qt.ControlModifier and keyname=='v':
			self.callback_paste_object()
		if event.key() == Qt.Key_Delete:
			self.layer_delete()

	def event_to_3d_obj(self,event):
		x = event.x()
		y = self.height()-event.y()
		self.set_false_color(True)

		old_val=self.active_view.text
		self.render()

		data=glReadPixelsub(x, y, 1, 1, GL_RGBA,GL_FLOAT)
		#print(data[0][0][0],data[0][0][1],data[0][0][2])
		obj=self.gl_objects_search_by_color(data[0][0][0],data[0][0][1],data[0][0][2])

		self.set_false_color(False)
		return obj

	def mouseDoubleClickEvent_han(self,event):
		#thumb_nail_gen()
		self.obj=self.event_to_3d_obj(event)
		#if self.obj!=None:
		#	if gl_obj_id_starts_with(self.obj.id,"layer")==True:
		#		self.selected_obj=self.obj
		#		self.do_draw()

	def set_cursor(self,cursor):
		if self.cursor!=cursor:
			if cursor==None:
				QApplication.restoreOverrideCursor()
			else:
				QApplication.setOverrideCursor(cursor)
			self.cursor=cursor

	def get_3d_pos(self,event):
		self.lastPos=event.pos()
		modelview=self.active_view.modelview
		projection=self.active_view.projection
		viewport=self.active_view.viewport

		winX = event.x()
		#if winX>viewport[2]:
		#	winX=winX-viewport[2]

		y=event.y()

		#if y>viewport[3]:
		#	y=y-viewport[3]

		#print(viewport,winX,y)

		winY = viewport[3] - y

		winZ=glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
		x0,y0,z0=gluUnProject(winX, winY, winZ, modelview, projection, viewport)
		x1,y1,z1=gluUnProject(winX+2, winY, winZ, modelview, projection, viewport)
		dxdx=(x1-x0)/2.0
		dydx=(y1-y0)/2.0
		dzdx=(z1-z0)/2.0

		#print(x0,y0,z0,x1,y1,z1)

		x0,y0,z0=gluUnProject(winX, winY, winZ, modelview, projection, viewport)
		x1,y1,z1=gluUnProject(winX, winY+2, winZ, modelview, projection, viewport)
		dxdy=(x1-x0)/2.0
		dydy=(y1-y0)/2.0
		dzdy=(z1-z0)/2.0
		return dxdx,dydx,dzdx,dxdy,dydy,dzdy 
		
	def mouseMoveEvent_han(self,event):
		if 	self.timer!=None:
			self.timer.stop()
			self.timer=None

		if self.lastPos==None:
			self.lastPos=event.pos()

		dx = event.x() - self.lastPos.x();
		dy = event.y() - self.lastPos.y();
		obj=self.gl_objects_is_selected()
		if obj==False:
			if event.buttons()==Qt.LeftButton:
				if self.active_view.enable_view_move==True:
					self.active_view.xRot =self.active_view.xRot + 1 * dy
					self.active_view.yRot =self.active_view.yRot - 1 * dx

			if event.buttons()==Qt.RightButton:
				self.set_cursor(QCursor(Qt.SizeAllCursor))
				self.active_view.x_pos =self.active_view.x_pos + 0.1 * dx
				self.active_view.y_pos =self.active_view.y_pos + 0.1 * dy
		else:
			if self.mouse_click_event.working==False:
				self.mouse_click_event.dxyz.set(0.0,0.0,0.0)
				self.mouse_click_event.rotate_x=0.0
				self.mouse_click_event.rotate_y=0.0
				self.mouse_click_event.working=True
			modifiers = QApplication.keyboardModifiers()

			if self.view_count_enabled()==1:
				dx_=self.dxdx*dx-self.dxdy*dy
				dy_=self.dydx*dy-self.dydy*dy
				dz_=self.dzdx*dx-self.dzdy*dy

				if self.last_object_clicked!=None:
					#print(self.last_object_clicked.id1)
					if self.last_object_clicked.id1==b"rotate":
						self.mouse_click_event.rotate=True
						dtheta=float(360*dx/self.width())
						dphi=float(360*dy/self.height())
						self.gl_objects_rotate(dphi,dtheta)
						self.mouse_click_event.rotate_x=self.mouse_click_event.rotate_x+dphi
						self.mouse_click_event.rotate_y=self.mouse_click_event.rotate_y+dtheta
					elif self.last_object_clicked.id1==b"rotate_x":
						self.mouse_click_event.rotate=True
						dtheta=0.0
						dphi=float(360*dy/self.height())
						self.gl_objects_rotate(dphi,dtheta)
						self.mouse_click_event.rotate_x=self.mouse_click_event.rotate_x+dphi
					elif self.last_object_clicked.id1==b"rotate_y":
						self.mouse_click_event.rotate=True
						dtheta=float(360*dx/self.width())
						dphi=0.0
						self.gl_objects_rotate(dphi,dtheta)
						self.mouse_click_event.rotate_y=self.mouse_click_event.rotate_y+dtheta
					elif self.last_object_clicked.id1==b"resize_ball":
						self.mouse_click_event.scale=True
						self.gl_objects_scale(dx_,dy_,dz_)
					else:
						self.mouse_click_event.drag=True
						self.gl_objects_move(dx_,dy_,dz_)
		
			else:
				dx_=dx*cos(2.0*3.14159*self.active_view.yRot/360)+dy*sin(2.0*3.14159*self.active_view.xRot/360)
				dz_=dx*sin(2.0*3.14159*self.active_view.yRot/360)-dy*sin(2.0*3.14159*self.active_view.xRot/360)
				dy_=dy*cos(2.0*3.14159*self.active_view.xRot/360)
				self.gl_objects_move(dx_*0.2/self.active_view.zoom,dy_*0.2/self.active_view.zoom,dz_*0.2/self.active_view.zoom)
			self.mouse_click_event.dxyz.x=self.mouse_click_event.dxyz.x+dx_
			self.mouse_click_event.dxyz.y=self.mouse_click_event.dxyz.y+dy_
			self.mouse_click_event.dxyz.z=self.mouse_click_event.dxyz.z+dz_

		self.lastPos=event.pos()
		self.setFocusPolicy(Qt.StrongFocus)
		self.setFocus()
		self.force_redraw(level="no_rebuild")
		#self.view_dump()

	def event_to_view(self,event):
		for v in json_root().gl.views.segments:
			if v.name in self.enabled_veiws:
				if event.x()>v.window_x*self.width():
					if self.height()-event.y()>v.window_y*self.height():
						if event.x()<v.window_x*self.width()+v.window_w*self.width():
							if self.height()-event.y()<v.window_y*self.height()+v.window_h*self.height():
								return v

		return False

	def mousePressEvent_han(self,event):
		self.lastPos=None
		self.mouse_click_event=mouse_event()
		self.mouse_click_event.time=time.time()
		self.mouse_click_event.x=event.x()
		self.mouse_click_event.y=event.y()
		self.active_view=self.event_to_view(event)
		if self.active_view!=False:
			self.gl_main.active_view=ctypes.addressof(self.active_view)
		else:
			self.gl_main.active_view=None

		if event.buttons()==Qt.LeftButton or event.buttons()==Qt.RightButton:
			obj=self.event_to_3d_obj(event)
			if obj!=None:
				if obj.id!=b"":
					self.dxdx,self.dydx,self.dzdx,self.dxdy,self.dydy,self.dzdy = self.get_3d_pos(event)
					self.last_object_clicked=obj
					if obj.selected==False:
						modifiers = QApplication.keyboardModifiers()
						if modifiers != Qt.ShiftModifier:
							self.gl_object_deselect_all()
						
						self.gl_objects_select_by_id(obj.id)
						self.lib.gl_selection_box(ctypes.byref(self.gl_main))
						self.set_cursor(QCursor(Qt.SizeAllCursor))
						self.text_output.emit(bytes2str(obj.id)+" "+bytes2str(obj.text))
						self.force_redraw(level="no_rebuild")
			else:
				self.gl_object_deselect_all()
				self.lib.gl_main_remove_selection_box(ctypes.byref(self.gl_main))
				self.force_redraw(level="no_rebuild")

	def mouseReleaseEvent_han(self,event):
		self.set_cursor(None)
		#print(self.mouse_click_event.drag)
		if self.mouse_click_event.working==True:
			self.gl_objects_move_update_json()
			self.mouse_click_event.drag=False
			self.mouse_click_event.rotate=False
			self.mouse_click_event.scale=False
			self.mouse_click_event.working=False
			return

		delta=time.time() - self.mouse_click_event.time

		obj=self.event_to_3d_obj(event)

		#print(self.mouse_click_event.y,self.mouse_click_event.delta_time())
		if event.button()==Qt.RightButton:
			#print(self.obj)
			if (delta)<3:
				if obj!=None:
					if len(obj.id)>0:
						data_obj=json_root().find_object_by_id(bytes2str(obj.id))
						if data_obj!=None:
							self.menu_obj(event,data_obj)

				else:
					self.menu(event)


			json_root().save()

		if event.button()==Qt.LeftButton:
			try:
				if obj!=None:
					if obj.html!=b"":
						webbrowser.open(bytes2str(obj.html))
			except:
				pass
			json_root().save()

	def wheelEvent_han(self,event):
		p=event.angleDelta()
		self.active_view=self.event_to_view(event)
		if self.active_view!=False:
			self.active_view.zoom =self.active_view.zoom - p.y()/120
			self.force_redraw(level="no_rebuild")

