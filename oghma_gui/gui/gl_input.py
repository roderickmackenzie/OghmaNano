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
from json_c import json_tree_c

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	pass


import time
from bytes2str import bytes2str
from json_c import json_files_gui_config

class gl_input():

	def __init__(self):
		self.cursor=None

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
					if self.gl_main.active_view.contents.zoom>-40:
						self.gl_main.active_view.contents.zoom =-400
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
		glDisable(GL_LIGHTING)
		self.gl_main.false_color=True

		self.render_to_screen(do_swap=False)

		#data=glReadPixelsub(x, y, 1, 1, GL_RGBA,GL_FLOAT)	(data[0][0][0],data[0][0][1],data[0][0][2])

		pixel = (ctypes.c_float * 4)()

		glReadPixels(x, y, 1, 1, GL_RGBA, GL_FLOAT, pixel)

		r, g, b, a = pixel

		obj,number=self.gl_objects_search_by_color(r,g,b)

		self.gl_main.false_color=False
		glEnable(GL_LIGHTING)
		return obj,number

	def mouseDoubleClickEvent_han(self,event):
		self.obj,number=self.event_to_3d_obj(event)

	def set_cursor(self,cursor):
		if self.cursor!=cursor:
			if cursor==None:
				QApplication.restoreOverrideCursor()
			else:
				QApplication.setOverrideCursor(cursor)
			self.cursor=cursor

	def get_3d_pos(self,event):
		self.lib.gl_view_unproject(ctypes.byref(self.gl_main.mouse_event) ,ctypes.byref(self.gl_main), ctypes.c_int(event.x()), ctypes.c_int(event.y()))

	def mousePressEvent_han(self,event):
		self.lastPos=None
		
		wx=ctypes.c_int(self.width())
		wy=ctypes.c_int(self.height())

		if self.lib.gl_set_active_view_from_click(ctypes.byref(self.gl_main), wx, wy)!=0:
			return

		if event.buttons()==Qt.LeftButton or event.buttons()==Qt.RightButton:
			obj,number=self.event_to_3d_obj(event)

			self.gl_main.mouse_event.last_object_clicked=-1
			if obj!=None:
				uid=bytes2str(obj.id)
				text=bytes2str(obj.text)
				self.gl_main.mouse_event.last_object_clicked=number
				if obj.id!=b"":
					self.get_3d_pos(event)
					if obj.selected==False:
						modifiers = QApplication.keyboardModifiers()
						if modifiers != Qt.ShiftModifier:
							self.gl_object_deselect_all()
						for uid in self.bin.groups_get_all_linked_uids(bytes2str(obj.id)):
							self.gl_objects_select_by_id(uid)
						
						self.lib.gl_selection_box(ctypes.byref(self.gl_main))
						self.set_cursor(QCursor(Qt.SizeAllCursor))
						self.text_output.emit(uid+" "+text)
						self.force_redraw(level="no_rebuild")
						
			else:
				self.gl_object_deselect_all()
				self.lib.gl_main_remove_selection_box(ctypes.byref(self.gl_main))
				self.force_redraw(level="no_rebuild")

	def mouseReleaseEvent_han(self,event):
		self.set_cursor(None)
		#print(self.gl_main.mouse_event.drag)
		if self.gl_main.mouse_event.working==True:
			self.gl_objects_move_update_json()
			self.gl_main.mouse_event.drag=False
			self.gl_main.mouse_event.rotate=False
			self.gl_main.mouse_event.scale=False
			self.gl_main.mouse_event.working=False
			return

		delta=time.time() - self.gl_main.mouse_event.time
		
		obj,number=self.event_to_3d_obj(event)

		#print(self.gl_main.mouse_event.y,self.gl_main.mouse_event.delta_time())

		self.lib.gl_save_views(ctypes.byref(json_files_gui_config), ctypes.byref(self.gl_main))

		if event.button()==Qt.RightButton:
			if (delta)<3:
				if obj!=None:
					if len(obj.id)>0:
						self.menu_obj(event,obj.id)
				else:
					self.menu(event)

			self.bin.save()

		if event.button()==Qt.LeftButton:
			try:
				if obj!=None:
					if obj.html!=b"":
						webbrowser.open(bytes2str(obj.html))
			except:
				pass
		
			self.bin.save()
		#self.lib.gl_views_dump(ctypes.byref(self.gl_main))

