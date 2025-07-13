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

## @package dat_file
#  Load and dump a dat file into a dat class
#

import os
import ctypes
from gQtCore import QSize, Qt
from cal_path import sim_paths
from PySide2.QtWidgets import QWidget,QMenu,QApplication
from PySide2.QtGui import QImage, QPainter
from vec import vec
from vec import vec2d_int
from dat_file import dat_file
from gl_main import text_lib
from json_c import json_c
from plot_ribbon import plot_ribbon
from icon_lib import icon_get
from lock import get_lock
from graph_menu import graph_menu
from color_map import color_map_item

class toolbar_info(ctypes.Structure):
	_fields_ = [('visible', ctypes.c_int),
				('checked', ctypes.c_int)]


class toolbar_hints(ctypes.Structure):
	_fields_ = [('home', toolbar_info),
				('pointer', toolbar_info),
				('rotate', toolbar_info),
				('log_x', toolbar_info), 
				('log_y', toolbar_info), 
				('log_z', toolbar_info)]


class graph_data_set_info(ctypes.Structure):
	_fields_ = [('y_axis', ctypes.c_char),
				('color_map_within_line', ctypes.c_int),
				('cm', ctypes.POINTER(color_map_item)),
				('hidden', ctypes.c_int)]


class graph_axis(ctypes.Structure):
	_fields_ = [('label', ctypes.c_char * 400),
				('enable', ctypes.c_int),
				('hidden', ctypes.c_int),
				('mul', ctypes.c_double),
				('label_rot', ctypes.c_int),
				('scale_shift_zxy', vec),
				('label_shift_zxy', vec),
				('scale', ctypes.POINTER(ctypes.c_double)),
				('len', ctypes.c_int),
				('start', ctypes.c_double),
				('stop', ctypes.c_double),
				('p0', vec),
				('p1', vec),
				('tic', vec),
				('label_center_x', ctypes.c_int),
				('log_scale', ctypes.c_int),
				('log_scale_auto', ctypes.c_int),
				('dry_run', ctypes.c_int),
				('use_sci', ctypes.c_int),
				('grid', ctypes.c_int)
				]


class graph(ctypes.Structure):

	_fields_ = [('width', ctypes.c_int),
				('height', ctypes.c_int),
				('pixels', ctypes.POINTER(ctypes.c_ubyte)),
				('pixels_back', ctypes.POINTER(ctypes.c_ubyte)),
				('camera', vec),
				('look', vec),
				('up', vec),
				('fov', ctypes.c_double),
				('ndata', ctypes.c_int),
				('data', ctypes.POINTER(dat_file)),
				('text_lib', text_lib),
				('plot_type', ctypes.c_char * 10),
				('cols', ctypes.c_char * 10),
				('axis_x', graph_axis),
				('axis_y', graph_axis),
				('axis_yr', graph_axis),
				('axis_z', graph_axis),
				('u', vec),
				('points', ctypes.c_int),
				('lines', ctypes.c_int),

				('info', ctypes.POINTER(graph_data_set_info)),
				('j', ctypes.POINTER(json_c)),
				('objs', ctypes.c_void_p),
				('nobjs', ctypes.c_int),
				('max_objs', ctypes.c_int),
				('camera_set', ctypes.c_int),
				('shift_2d_x', ctypes.c_int),
				('xy_shift', vec2d_int),
				('mouse_mode', ctypes.c_int),
				('mouse', vec2d_int),
				('mouse_last', vec2d_int),
				('mouse_drag_started', ctypes.c_int),
				('disable_rebuild', ctypes.c_int),

				('cm_default', ctypes.POINTER(color_map_item)),
				('toolbar', toolbar_hints),
				('cut_through_frac_z', ctypes.c_double),
				('cut_through_frac_x', ctypes.c_double),
				('cut_through_frac_y', ctypes.c_double),
				('show_key', ctypes.c_int),
				('show_title', ctypes.c_int),
				('show_free_carriers', ctypes.c_int),
				('show_trapped_carriers', ctypes.c_int)]

	def __init__(self):
		super().__init__()
		self.lib=sim_paths.get_dll_py()
		self.lib.ui_graph_init(ctypes.byref(self))
		font_path=os.path.join(sim_paths.get_fonts_path(),"Lato-Regular.ttf")
		self.lib.graph_setup_window(ctypes.byref(self),bytes(font_path, encoding='utf8'))

	def __del__(self):
		self.free()

	def free(self):
		self.lib.ui_graph_free(ctypes.byref(self))

	def set_json(self,j):
		self.lib.graph_set_json(ctypes.byref(self),ctypes.byref(j))

	def load_bands(self,j):
		self.lib.graph_load_bands(ctypes.byref(self),bytes(sim_paths.get_materials_path(), encoding='utf8'),ctypes.byref(j))

	def draw(self,width,height):
		self.lib.ui_graph_draw(ctypes.byref(self), width, height)
		buffer_size = width * height * 4
		pixel_data = ctypes.string_at(self.pixels, buffer_size)
		return pixel_data

	def rotate_y(self,ang):
		self.lib.graph_rotate_around_y(ctypes.byref(self), ctypes.c_double(ang))

	def rotate_x(self,ang):
		self.lib.graph_rotate_around_x(ctypes.byref(self), ctypes.c_double(ang))

	def load(self,files,axis=None):
		self.lib.graph_free_files(ctypes.byref(self))

		if len(files)==1:
			if type(files[0])==str:
				if self.lib.graph_load_multiplot(ctypes.byref(self), bytes(sim_paths.get_sim_path(), encoding='utf8'), bytes(files[0], encoding='utf8'))==0:
					self.lib.graph_load_set_up_axies(ctypes.byref(self))
					return

		count=0
		for file_name in files:
			a=0
			if axis!=None:
				a=axis[count]
			if type(file_name)==str:
				self.lib.graph_load_file(ctypes.byref(self), bytes(file_name, encoding='utf8'),None,ctypes.c_int(a))
			else:		#dat file
				self.lib.graph_load_file(ctypes.byref(self), None, ctypes.byref(file_name) ,ctypes.c_int(a))
			count=count+1

		self.lib.graph_load_set_up_axies(ctypes.byref(self))

	def set_margins(self):
		return
		self.lib.graph_set_white_space(ctypes.byref(self))

	def home(self):
		self.lib.graph_load_set_up_axies(ctypes.byref(self))

class graph_widget(QWidget,graph_menu):
	def __init__(self,plot_ribbon_in=None):
		super().__init__()
		self.setFocusPolicy(Qt.StrongFocus)
		self.plot_ribbon=plot_ribbon_in
		self.graph=graph()
		#self.setMinimumSize(800, 450)
		self.lastPos=None
		self.build_menu()
		if plot_ribbon_in!=None:
			self.plot_ribbon.tb_zoom.triggered.connect(self.callback_plot_state_toggle)
			self.plot_ribbon.tb_home.triggered.connect(self.callback_plot_state_toggle)
			self.plot_ribbon.tb_move.triggered.connect(self.callback_plot_state_toggle)
			self.plot_ribbon.tb_rotate.triggered.connect(self.callback_plot_state_toggle)
			self.plot_ribbon.tb_home.setChecked(True)

			self.plot_ribbon.tb_scale_log_x.triggered.connect(self.callback_menu_click)
			self.plot_ribbon.tb_scale_log_y.triggered.connect(self.callback_menu_click)
			self.plot_ribbon.tb_scale_log_z.triggered.connect(self.callback_menu_click)
			self.plot_ribbon.tb_transpose.triggered.connect(self.callback_menu_click)

			self.plot_ribbon.tb_flip_x.triggered.connect(self.callback_menu_click)
			self.plot_ribbon.tb_flip_y.triggered.connect(self.callback_menu_click)
			self.plot_ribbon.tb_flip_z.triggered.connect(self.callback_menu_click)

	def set_key_text(self,items):
		if len(items)!=self.graph.ndata:
			return

		i=0
		for item_text in items:
			self.graph.lib.graph_set_key_text(ctypes.byref(self.graph), ctypes.c_int(i), bytes(item_text, encoding='utf8'))
			i=i+1

	def set_color_map(self,cm):
		self.graph.lib.graph_update_color_maps(ctypes.byref(self.graph),cm)

	def callback_plot_state_toggle(self):
		text=""
		sender = self.sender()
		if sender!=None:
			text=sender.text()

		if self.plot_ribbon!=None:
			self.plot_ribbon.tb_move.setChecked(False)
			self.plot_ribbon.tb_zoom.setChecked(False)
			self.plot_ribbon.tb_home.setChecked(False)
			self.plot_ribbon.tb_rotate.setChecked(False)

			if sender:
				sender.setChecked(True)

			if text==_("Home"):
				self.graph.mouse_mode=0
				self.graph.home()
				self.update()
			elif text==_("Rotate"):
				self.graph.mouse_mode=1
			elif text==_("Zoom"):
				self.graph.mouse_mode=3

	def mouseReleaseEvent(self,event):
		self.show_menu()

	def load(self,file_names,axis=None):
		self.graph.load(file_names,axis)
		if self.plot_ribbon!=None:
			self.plot_ribbon.tb_rotate.setVisible(self.graph.toolbar.rotate.visible)
			self.plot_ribbon.tb_scale_log_x.setVisible(self.graph.toolbar.log_x.visible)
			self.plot_ribbon.tb_scale_log_y.setVisible(self.graph.toolbar.log_y.visible)
			self.plot_ribbon.tb_scale_log_z.setVisible(self.graph.toolbar.log_z.visible)
			if self.graph.mouse_mode==1:
				self.plot_ribbon.tb_rotate.setChecked(True)

	def redraw(self):
		width = self.width()
		height = self.height()
		
		pixel_data=self.graph.draw(width,height)
		qimage = QImage(pixel_data, width, height, QImage.Format_RGBA8888)

		painter = QPainter(self)
		painter.drawImage(0, 0, qimage)
		painter.end()

	def resizeEvent(self, event):
		self.graph.set_margins()

	def paintEvent(self, event):
		self.redraw()

	def do_clip(self,file_name=None):
		width = self.width()
		height = self.height()
		
		pixel_data=self.graph.draw(width,height)
		qimage = QImage(pixel_data, width, height, QImage.Format_RGBA8888)

		if file_name==None:
			QApplication.clipboard().setImage(qimage)
		else:
			qimage.save(file_name)

	def wheelEvent(self,event):
		p=event.angleDelta()
		self.graph.fov =self.graph.fov - p.y()/40
		#print(self.graph.fov)
		self.update()

	def mousePressEvent(self, event):
		self.graph.lib.graph_mouse(ctypes.byref(self.graph) , ctypes.c_int(event.x()), ctypes.c_int(event.y()))

	def mouseReleaseEvent(self, event):
		self.graph.lib.graph_mouse_release(ctypes.byref(self.graph))
		self.update()

	def mouseMoveEvent(self,event):
		self.graph.lib.graph_mouse(ctypes.byref(self.graph) , ctypes.c_int(event.x()), ctypes.c_int(event.y()))
		self.update()

	def keyPressEvent(self, event):
		self.blockSignals(True)
		keyname=event.key()
		modifiers = event.modifiers()
		if (keyname>64 and keyname<91 ) or (keyname>96 and keyname<123):
			keyname=chr(keyname)
			if keyname.isalpha()==True:
				if Qt.ShiftModifier == modifiers:
					keyname=keyname.upper()
				else:
					keyname=keyname.lower()

		if modifiers & Qt.ControlModifier and keyname == "c":
			self.do_clip()
		elif keyname == "l":
			self.graph.axis_y.log_scale_auto=False
			self.graph.axis_y.log_scale= not self.graph.axis_y.log_scale
			self.graph.lib.graph_load_set_up_axies(ctypes.byref(self.graph))
			self.update()
			self.plot_ribbon.tb_scale_log_y.setChecked(self.graph.axis_y.log_scale)
		elif keyname == "L":
			self.graph.axis_x.log_scale_auto=False
			self.graph.axis_x.log_scale= not self.graph.axis_x.log_scale
			self.graph.lib.graph_load_set_up_axies(ctypes.byref(self.graph))
			self.update()
			self.plot_ribbon.tb_scale_log_x.setChecked(self.graph.axis_x.log_scale)
		elif keyname == "a":
			self.graph.home()
			self.update()
		elif keyname == "g":
			self.graph.axis_y.grid= not self.graph.axis_y.grid
			self.graph.axis_x.grid= not self.graph.axis_x.grid
			self.graph.axis_z.grid= not self.graph.axis_z.grid
			self.update()
		event.ignore()
		self.blockSignals(False)
		#	elif keyname=="r":
		#		if self.lx==None:
		#			for i in range(0,len(self.ax)):
		#				self.lx = self.ax[i].axhline(color='k')
		#				self.ly = self.ax[i].axvline(color='k')
		#		self.lx.set_ydata(self.ydata)
		#		self.ly.set_xdata(self.xdata)
		#

