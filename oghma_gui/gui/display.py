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

## @package display
#  The display widget, this either displays the 3D OpenGL image of the device or the fallback non OpenGL widget.
#

import os

from gl import glWidget
from gl_fallback import gl_fallback

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout, QLineEdit,QLabel
from gQtCore import QTimer
from gQtCore import gSignal

from icon_lib import icon_get

from cal_path import sim_paths
from global_objects import global_object_register
from global_objects import global_object_run
from global_objects import global_object_get
from json_c import json_local_root
from dat_file import dat_file
import ctypes
from json_c import json_tree_c

open_gl_working=False

class display_widget(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.complex_display=False

		self.hbox=QVBoxLayout()
		data=json_local_root()
		enable_3d=data.get_token_value("gui_config","enable_opengl")
		
		#if enable_3d==True:
		self.display=glWidget(self)
		#if self.display.failed==True:
		#	self.display=gl_fallback()
		#	self.display.show_error()
		global_object_get("main_fx_box").cb.currentIndexChanged.connect(self.fx_box_changed)

		self.hbox.addWidget(self.display)

		self.setLayout(self.hbox)
		global_object_register("display_recalculate",self.recalculate)
		global_object_register("display_set_selected_obj",self.set_selected_obj)
		global_object_register("gl_force_redraw",self.display.force_redraw)
		global_object_register("gl_force_redraw_hard",self.display.force_redraw_hard)

		self.timer=QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.callback_check_opengl_working)
		self.timer.start(7000)

	def fx_box_changed(self):
		fx_box=global_object_get("main_fx_box")
		files=fx_box.get_file_name()
		self.display.gl_graph_load_files(files)

		self.bin.set_token_value("optical.ray","rays_display",fx_box.get_english_text())
		self.bin.save()
		self.display.force_redraw()

	def set_selected_obj(self,obj_id):
		if self.display.open_gl_working==True:
			self.display.gl_object_deselect_all()
			self.display.gl_objects_select_by_id(obj_id)
			self.display.lib.gl_selection_box(ctypes.byref(self.display.gl_main))
			self.display.force_redraw(level="no_rebuild")

	#This will reclaculate all the display elements in the display widget.
	def recalculate(self):
		global_object_get("main_fx_box").update()
		files=global_object_get("main_fx_box").get_file_name()
		self.display.gl_graph_load_files(files)
		self.display.force_redraw()

		
	def update(self):
		files=global_object_get("main_fx_box").get_file_name()
		self.display.gl_graph_load_files(files)
		self.display.force_redraw()

	def callback_check_opengl_working(self):
		if self.display.failed==True:
			print("OpenGL is not working going to fallback")

			self.hbox.removeWidget(self.display)
			self.display.deleteLater()
			self.display = None

			global open_gl_working
			open_gl_working=False

			self.display=gl_fallback()
			self.hbox.addWidget(self.display)
			self.display.show_error()

