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

## @package gl
#  The main OpenGL display.
#

import os
import sys
open_gl_ok=False

try:
	from OpenGL.GLU import *
	from OpenGL.GL import *
	from PySide2.QtOpenGL import QGLWidget
	open_gl_ok=True
except:
	print("opengl error ",sys.exc_info()[0])

#qt
from PySide2.QtGui import QFont,QFont

#path
from cal_path import sim_paths


from thumb import thumb_nail_gen

from gl_views import gl_views
from gl_object_editor import gl_object_editor
from gl_main_menu import gl_main_menu
from gl_list import gl_objects
from gl_input import gl_input
from gl_scale import gl_scale_class
from gl_main import gl_main

from gQtCore import gSignal, Qt
from gl_toolbar import gl_toolbar
from dat_file import dat_file
from bytes2str import str2bytes
from json_c import json_tree_c
from object_editor_base import object_editor_base
import ctypes
import time
from json_c import json_files_gui_config

if open_gl_ok==True:		
	class glWidget(QGLWidget, gl_objects, gl_views,gl_object_editor,gl_main_menu,gl_input, gl_toolbar, object_editor_base):


		text_output = gSignal(str)

		def __init__(self, parent,plot_ribbon_in=None,views="default"):
			self.lib=sim_paths.get_dll_py()
			self.gl_main=gl_main()
			self.lib.gl_main_load(ctypes.byref(self.gl_main),ctypes.byref(sim_paths))
			self.lib.gl_load_views(ctypes.byref(self.gl_main), ctypes.byref(json_files_gui_config),ctypes.c_char_p(str2bytes(views)))
			self.lib.gl_load_lights(ctypes.byref(self.gl_main), ctypes.byref(json_tree_c()))

			QGLWidget.__init__(self, parent)
			gl_views.__init__(self)
			gl_objects.__init__(self)
			gl_input.__init__(self)
			gl_toolbar.__init__(self)
			gl_object_editor.__init__(self)

			self.setAutoBufferSwap(False)
			self.timer=None
			self.lastPos=None
			self.mouse_click_time=0.0

			self.failed=True
			self.scene_built=False

			self.scale=gl_scale_class(self.gl_main.scale)
			self.font = QFont("Arial")
			self.font.setPointSize(15)
			self.called=False
			self.build_main_menu()
			self.open_gl_working=True
			self.bin=json_tree_c()

			self.plot_ribbon=plot_ribbon_in

			if plot_ribbon_in!=None:
				self.plot_ribbon.tb_zoom.triggered.connect(self.callback_pointer_state_toggle)
				self.plot_ribbon.tb_pointer.triggered.connect(self.callback_pointer_state_toggle)
				self.plot_ribbon.tb_move.triggered.connect(self.callback_pointer_state_toggle)
				self.plot_ribbon.tb_rotate.triggered.connect(self.callback_pointer_state_toggle)
				self.plot_ribbon.tb_pointer.setChecked(True)

		def callback_pointer_state_toggle(self):
			sender = self.sender()
			text=sender.text()
			if self.plot_ribbon!=None:
				self.plot_ribbon.tb_move.setChecked(False)
				self.plot_ribbon.tb_zoom.setChecked(False)
				self.plot_ribbon.tb_home.setChecked(False)
				self.plot_ribbon.tb_pointer.setChecked(False)
				self.plot_ribbon.tb_rotate.setChecked(False)

				if sender:
					sender.setChecked(True)

				if text==_("Pointer"):
					self.gl_main.mouse_event.mouse_mode=0
					self.update()
				elif text==_("Rotate"):
					self.gl_main.mouse_event.mouse_mode=1
				elif text==_("Move"):
					self.gl_main.mouse_event.mouse_mode=2
				elif text==_("Zoom"):
					self.gl_main.mouse_event.mouse_mode=3

		def mousePressEvent(self,event):
			self.gl_main.mouse_event.time=time.time()
			self.gl_main.mouse_event.xy.x=event.x()
			self.gl_main.mouse_event.xy.y=event.y()
			self.gl_main.mouse_event.button=event.buttons()
			self.lib.gl_mouse_press(ctypes.byref(self.gl_main.mouse_event))
			self.mousePressEvent_han(event)

		def mouseReleaseEvent(self,event):
			self.gl_main.mouse_event.xy.x=event.x()
			self.gl_main.mouse_event.xy.y=event.y()
			self.gl_main.mouse_event.button=event.buttons()
			self.lib.gl_mouse_release(ctypes.byref(self.gl_main.mouse_event))
			self.mouseReleaseEvent_han(event)

		def mouseMoveEvent(self,event):
			if 	self.timer!=None:
				self.timer.stop()
				self.timer=None
			self.gl_main.mouse_event.xy.x=event.x()
			self.gl_main.mouse_event.xy.y=event.y()
			self.gl_main.mouse_event.button=event.buttons()
			self.lib.gl_mouse_move(ctypes.byref(self.gl_main),ctypes.c_int(self.width()),ctypes.c_int(self.height()))
			self.setFocusPolicy(Qt.StrongFocus)
			self.setFocus()
			self.force_redraw(level="no_rebuild")

		def wheelEvent(self,event):
			self.gl_main.mouse_event.time=time.time()
			self.gl_main.mouse_event.xy.x=event.x()
			self.gl_main.mouse_event.xy.y=event.y()
			self.gl_main.mouse_event.angle_delta=event.angleDelta().y()
			if self.lib.gl_mouse_wheel(ctypes.byref(self.gl_main),ctypes.c_int(self.width()),ctypes.c_int(self.height()))==-1:
				return
			self.lib.gl_save_views(ctypes.byref(json_files_gui_config), ctypes.byref(self.gl_main))
			self.force_redraw(level="no_rebuild")

		def mouseDoubleClickEvent(self,event):
			self.mouseDoubleClickEvent_han(event)

		def keyPressEvent_han(self,event):
			self.keyPressEvent_han(event)

		def render_to_screen(self,do_swap=True):
			if self.scene_built==False:
				self.build_scene()

			self.makeCurrent()
			self.lib.gl_lights_add_to_world(ctypes.byref(self.gl_main))

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			
			glPolygonMode(GL_FRONT, GL_FILL)
			for n in range(0,self.gl_main.n_views):
				v=self.gl_main.views[n]
				#print(n,v.name,v.enabled)
				if v.enabled==True:
					self.lib.gl_view_save_projection_matrix(ctypes.byref(v),ctypes.c_int(self.width()),ctypes.c_int(self.height()))
					self.lib.gl_render_view(ctypes.byref(self.gl_main),ctypes.byref(v),ctypes.byref(sim_paths))

			if do_swap==True:
				self.swapBuffers()

		def paintGL(self):
			if self.failed==False:
				self.render_to_screen()

		def build_scene(self):				#This will rebuild the scene from scratch
			self.scene_built=True
			self.menu_update()
			self.lib.gl_main_clear_objects(ctypes.byref(self.gl_main))
			
			self.lib.text_lib_clear(ctypes.byref(self.gl_main.text))

			self.scale.set_m2screen()

			x=self.scale.project_m2screen_x(0)
			z=self.scale.project_m2screen_z(0)
			
			self.lib.json_load_triangles(ctypes.byref(json_tree_c()),ctypes.byref(sim_paths))
			
			if self.gl_main.active_view.contents.draw_device==True:
				self.lib.gl_draw_device(ctypes.byref(self.gl_main), ctypes.byref(json_tree_c()), ctypes.c_double(z), ctypes.c_double(x))
				self.lib.gl_draw_emission(ctypes.byref(self.gl_main), ctypes.byref(json_tree_c()))
				self.lib.gl_draw_contacts(ctypes.byref(self.gl_main), ctypes.byref(json_tree_c()))
			
			self.lib.gl_world_grid(ctypes.byref(self.gl_main))
			self.lib.gl_fdtd_mesh(ctypes.byref(self.gl_main), ctypes.byref(json_tree_c()))
			self.lib.gl_light_srcs_show(ctypes.byref(self.gl_main), ctypes.byref(json_tree_c()))
			self.lib.gl_detectors_show(ctypes.byref(self.gl_main), ctypes.byref(json_tree_c()))
			self.lib.gl_lights_show(ctypes.byref(self.gl_main))
			self.lib.gl_draw_device_text(ctypes.byref(self.gl_main), ctypes.byref(json_tree_c()), ctypes.c_double(z), ctypes.c_double(x))

			view=self.gl_main.active_view.contents
			
			if view.stars==True:
				if view.zoom>view.stars_distance:
					file_path=os.path.join(sim_paths.get_html_path(),"stars.csv")	#"hyg109399.xyz.txt"
					self.lib.gl_render_stars(ctypes.byref(self.gl_main), ctypes.c_char_p(str2bytes(file_path)))
			#self.gl_graph_load_files([os.path.join(sim_paths.get_sim_path(),"electrical_nodes.csv"), os.path.join(sim_paths.get_sim_path(),"electrical_links.csv") ])
			self.lib.gl_draw_graphs(ctypes.byref(self.gl_main))
			
		def force_redraw_hard(self):
			self.refresh_world_size=True
			self.scale.gl_scale.calculated_world_min_max=False
			self.scale.set_m2screen()
			self.force_redraw(level="reload_rebuild")

		def force_redraw(self,level="rebuild"):
			if level=="reload_rebuild":
				self.bin.triangles_loaded=False
				self.build_scene()
				self.render_to_screen()
				self.menu_update()
				self.update()
			elif level=="rebuild":
				self.build_scene()
				self.render_to_screen()
				self.menu_update()
				self.update()
			elif level=="no_rebuild":
				self.update()

		def resizeEvent(self,event):
			if self.failed==False:
				self.lib.gl_set_projection(ctypes.byref(self.gl_main),ctypes.c_int(self.width()),ctypes.c_int(self.height()))

		def initializeGL(self):
			glClearDepth(5.0)     
			glDepthFunc(GL_LESS)
			glEnable(GL_DEPTH_TEST)
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)	#GL_ONE
			
			glEnableClientState(GL_VERTEX_ARRAY)
			glShadeModel(GL_SMOOTH)
			glColorMaterial(GL_FRONT, GL_DIFFUSE)				#This means we can set the color of a material using glColor and not glMaterialfv
			glEnable(GL_COLOR_MATERIAL)							#This means we can set the color of a material using glColor and not glMaterialfv

			glEnable(GL_MULTISAMPLE)
			
			self.lib.gl_set_projection(ctypes.byref(self.gl_main),ctypes.c_int(self.width()),ctypes.c_int(self.height()))
			glEnable( GL_POLYGON_SMOOTH)

			glEnable(GL_LIGHTING)
			self.failed=False

		def gl_graph_load_files(self,files,scale=False):
			self.lib.gl_graph_free_files(ctypes.byref(self.gl_main))
			for file_name in files:
				ret=self.lib.gl_graph_load_file(ctypes.byref(self.gl_main), ctypes.c_char_p(str2bytes(file_name)),ctypes.c_int(scale),ctypes.c_int(True))

		def boom(self):
			print("oh")
else:
	from gl_fallback import gl_fallback

	class glWidget(gl_fallback):
		def __init__(self, parent):
			gl_fallback.__init__(self)
			self.show_error()

