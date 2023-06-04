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


#epitaxy
from epitaxy import epitaxy_get_epi
from epitaxy import get_epi

from vec import vec

from thumb import thumb_nail_gen

from gl_views import gl_views
from gl_object_editor import gl_object_editor

from gl_cords import gl_cords

from gl_shape_to_screen import shape_layer

from gl_main_menu import gl_main_menu

from gl_list import gl_objects
from gl_input import gl_input

from gl_lib_ray import gl_lib_ray
from gl_contacts import gl_contacts
from gl_graph import gl_graph
from gl_draw_light_profile import gl_draw_light_profile
from gl_photons import gl_photons
from gl_scale import gl_scale_class
from gQtCore import gSignal
from json_root import json_root
from gl_toolbar import gl_toolbar
from gl_default_shapes import gl_default_shapes
from gl_detectors import gl_detectors
from dat_file import dat_file
from bytes2str import str2bytes
import ctypes
from gl_lib import gl_lib
from gl_main import gl_main


if open_gl_ok==True:		
	class glWidget(QGLWidget,shape_layer, gl_lib_ray,gl_objects, gl_views,gl_object_editor,gl_cords,gl_main_menu,gl_input, gl_contacts, gl_draw_light_profile, gl_graph, gl_photons, gl_toolbar, gl_detectors, gl_lib):


		text_output = gSignal(str)

		def __init__(self, parent):
			self.lib=sim_paths.get_dll_py()
			self.gl_main=gl_main()
			font_path=os.path.join(sim_paths.get_fonts_path(),"Lato-Regular.ttf")
			self.lib.gl_main_load(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes(font_path)))

			QGLWidget.__init__(self, parent)
			gl_views.__init__(self)
			gl_objects.__init__(self)
			gl_lib_ray.__init__(self)
			gl_input.__init__(self)
			gl_graph.__init__(self)
			gl_toolbar.__init__(self)
			gl_detectors.__init__(self)

			self.setAutoBufferSwap(False)
			self.timer=None
			self.suns=0.0
			self.lastPos=None
			self.mouse_click_time=0.0

			self.failed=True
			self.graph_path=None
			self.scene_built=False
			#view pos

			self.dy_layer_offset=0.05

			self.draw_electrical_mesh=False
			self.plot_circuit=False

			self.scale=gl_scale_class(self.gl_main.scale)
			self.font = QFont("Arial")
			self.font.setPointSize(15)
			self.called=False
			self.build_main_menu()
			self.open_gl_working=True
			self.default_shapes=gl_default_shapes()
			self.data_files=[]
			self.device_z_shift=0.0

		#def bix_axis(self):
		#	for xx in range(0,10):
		#		self.box(0+xx,0,0,0.5,0.5,0.5,1.0,0,0,0.5)

		#	for yy in range(0,10):
		#		self.box(0,0+yy,0,0.5,0.5,0.5,1.0,0,0,0.5)


		#	for zz in range(0,10):
		#		self.box(0,0,0+zz,0.5,0.5,0.5,0.0,0,1,0.5)

		#this may not be the best place for this
		def epitaxy_enforce_rules(self):
			y_pos=0.0
			epi=get_epi()
			for l in epi.layers:
				l.shape_dos.enabled=False
				if l.layer_type=="active":
					l.shape_dos.enabled=True
				l.x0=0.0
				l.z0=0.0
				l.y0=y_pos

				l.dx=json_root().electrical_solver.mesh.mesh_x.get_len()
				l.dz=json_root().electrical_solver.mesh.mesh_z.get_len()
				y_pos=y_pos+l.dy

		def mousePressEvent(self,event):
			self.mousePressEvent_han(event)

		def mouseReleaseEvent(self,event):
			self.mouseReleaseEvent_han(event)

		def wheelEvent(self,event):
			self.wheelEvent_han(event)

		def mouseMoveEvent(self,event):
			self.mouseMoveEvent_han(event)

		def mouseDoubleClickEvent(self,event):
			self.mouseDoubleClickEvent_han(event)

		def keyPressEvent_han(self,event):
			self.keyPressEvent_han(event)

		def draw_device2(self,x,z):
			epi=get_epi()
			contact_layers=epi.contacts.get_layers_with_contacts()
			top_contact_layer=epi.get_top_contact_layer()
			btm_contact_layer=epi.get_btm_contact_layer()

			l=0
			btm_layer=len(epitaxy_get_epi())-1

			for obj in json_root().world.world_data.segments:
				self.shape_to_screen(obj)

			self.epitaxy_enforce_rules()

			for obj in epi.layers:
				name=obj.name
		
				if obj.layer_type=="active":
					if self.active_view.text==True:
						o=self.gl_main.add_object()
						x=self.scale.project_m2screen_x(json_root().electrical_solver.mesh.mesh_x.get_len())+0.1
						y=self.scale.project_m2screen_y(obj.y0)
						o.add_xyz(x,y,z)

						o.dx=0.1
						o.dy=obj.dy*self.gl_main.scale.y_mul

						o.r=0.0
						o.g=0.0
						o.b=1.0
						o.id=str2bytes(obj.id+"_active")
						o.type=b"plane"

				contact_layer=False
				if l==top_contact_layer:
					contact_layer=True

				if l==btm_contact_layer:
					contact_layer=True
				if contact_layer==False:
					self.shape_to_screen(obj,epitaxy=True,z_shift=self.device_z_shift)			

				l=l+1

		def draw_text(self,x,z):
			epi=get_epi()
			l=0
			for obj in epi.layers:
				display_name=obj.name
				if obj.layer_type=="active":
					if self.active_view.text==True:
						display_name=display_name+" ("+_("active")+")"
						
				if self.active_view.text==True:
					if self.active_view.zoom<40:
						o=self.gl_main.add_object()
						o.r=1.0
						o.g=1.0
						o.b=1.0

						xx=self.scale.project_m2screen_x(json_root().electrical_solver.mesh.mesh_x.get_len())+0.2
						if l==0:
							yy=self.scale.project_m2screen_y(obj.y0)
						else:
							yy=self.scale.project_m2screen_y(obj.y0)+obj.dy*self.gl_main.scale.y_mul/2.0

						zz=z+(len(epi.layers)-l)*0.1
						o.add_xyz(xx,yy,zz)
						o.id=str2bytes(obj.id)
						o.type=b"text"
						o.text=str2bytes(display_name)

				l=l+1

		def render(self):

			self.makeCurrent()
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			
			glPolygonMode(GL_FRONT, GL_FILL);
			for v in json_root().gl.views.segments:
				if v.name in self.enabled_veiws:
					glClearColor(v.color_r, v.color_g, v.color_b, 0.5)
					w=int(self.width()*v.window_w)
					h=int(self.height()*v.window_w)
					x=int(self.width()*v.window_x)
					y=int(self.height()*v.window_y)
					glViewport(x, y, w, h)
					v.projection = glGetDoublev(GL_PROJECTION_MATRIX)
					v.modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
					v.viewport = glGetIntegerv(GL_VIEWPORT)
					self.render_view(v)

		def render_view(self,view):
			data=json_root()

			x=self.scale.project_m2screen_x(0)
			y=0.0#project_m2screen_y(0)
			z=self.scale.project_m2screen_z(0)

			self.emission=False

			glLoadIdentity()
			glScalef(1.0, -1.0, -1.0) 

			glTranslatef(view.x_pos, view.y_pos, view.zoom) # Move Into The Screen
			
			glRotatef(view.xRot, 1.0, 0.0, 0.0)
			glRotatef(view.yRot, 0.0, 1.0, 0.0)
			glRotatef(view.zRot, 0.0, 0.0, 1.0)

			glColor3f( 1.0, 1.5, 0.0 )
			
			if view.render_cords==True:
				self.draw_cords()
			
			if view.optical_mode==True:
				self.draw_mode()
			
			if self.scene_built==False:
				self.build_scene()

			
			self.draw_graphs(self.data_files,scale=False)
			
			if view.plot_graph==True:
				self.draw_graphs(self.graph_data)
			
			if view.draw_rays==True:
				self.draw_graphs(self.ray_data)
			
			if view.render_photons==True:
				self.draw_photons(x,z)
			
			if view.show_world_box==True:
				self.world_box()
			
			self.lib.gl_objects_render(ctypes.byref(self.gl_main))
			
			self.active_view.stars_distance=0


			if self.active_view.stars==True:
				if view.zoom>view.stars_distance:
					file_path=os.path.join(sim_paths.get_html_path(),"hyg109399.xyz.txt")
					self.lib.gl_render_stars(ctypes.byref(self.gl_main), ctypes.c_char_p(str2bytes(file_path)))


		def do_draw(self):
			self.makeCurrent()
			self.sort_lights()
			self.render()
			self.swapBuffers()

		def paintGL(self):
			#print("paintGL",self)
			self.makeCurrent()
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			glLoadIdentity()
			glScalef(-1.0, 1.0, -1.0) 

			if self.failed==False:
				self.do_draw()



		def load_data(self):
			lines=[]

			data=json_root()
			self.dump_1d_slice_xpos=-1
			self.dump_1d_slice_zpos=-1

			self.dump_verbose_electrical_solver_results=False

			self.x_len=json_root().electrical_solver.mesh.mesh_x.get_len()
			#if os.path.isdir(os.path.join(os.path.join(sim_paths.get_sim_path(),"ray_trace")))==True:
			#	for v in json_root().gl.views.segments:
			#		v.render_photons=False

		def sort_lights(self):
			pos=0
			lights=[GL_LIGHT0,GL_LIGHT1,GL_LIGHT2,GL_LIGHT3,GL_LIGHT4,GL_LIGHT5,GL_LIGHT6,GL_LIGHT7]
			for l in json_root().gl.gl_lights.segments:
				number=lights[pos]
				if l.enabled==True:
					lightZeroColor = [1.0, 1.0, 1.0, 1.0]
					#print(l.number,GL_LIGHT1)
					glLightfv(number, GL_POSITION, [l.x0,l.y0,l.z0 ,1.0])
					r=l.color_r
					g=l.color_g
					b=l.color_b
					glLightfv(number, GL_AMBIENT, [0.2*r,0.2*g,0.2*b,1.0 ])
					glLightfv(number, GL_DIFFUSE, [0.8*r,0.8*g,0.8*b,1.0 ])
					glLightfv(number, GL_SPECULAR, [1.0*r,1.0*g,1.0*b,1.0 ])
					#glLightfv(lnumber, GL_SPOT_DIRECTION, [ 1,1,1]);
					#glLightf(number, GL_CONSTANT_ATTENUATION, 2.0)
					#glLightf(number, GL_LINEAR_ATTENUATION, 0.05)
					glEnable(number)
					
				else:
					glDisable(number)

				pos=pos+1

		#This will rebuild the scene from scratch
		def rebuild_scene(self):

			self.gl_objects_clear()

			self.menu_update()
			self.lib.gl_text_clear_lib(ctypes.byref(self.gl_main.text))
			data=json_root()
			if data.triangles_loaded==False:
				data.load_triagles()

			self.scale.set_m2screen()

			x=self.scale.project_m2screen_x(0)
			z=self.scale.project_m2screen_z(0)


			if self.active_view.render_photons==True:
				if self.active_view.render_light_sources==True:
					for source in data.optical.light_sources.lights.segments:
						self.light_arrow_to_screen(source) 

			if self.draw_electrical_mesh==True:
				self.draw_mesh()

			elif self.active_view.draw_device==True:
				self.draw_device2(x,z)
				self.draw_contacts(z_shift=self.device_z_shift)
			
			if self.active_view.render_grid==True:
				self.gl_objects_add_grid(self.scale.gl_scale.gl_universe_x0, self.scale.gl_scale.gl_universe_x1, self.scale.project_m2screen_y(self.gl_main.scale.world_max.y),self.scale.project_m2screen_y(self.gl_main.scale.world_max.y), self.scale.gl_scale.gl_universe_z0, self.scale.gl_scale.gl_universe_z1,"world_grid")

			self.add_detectors()

			if data.sim.simmode.endswith("fdtd")==True:
				if self.active_view.render_fdtd_grid==True:
					for fdtd in data.sims.fdtd.segments:
						if fdtd.fdtd_xzy=="zy":
							world_dy=(self.gl_main.scale.world_max.y-self.gl_main.scale.world_min.y)
							y0=self.scale.project_m2screen_y(self.gl_main.scale.world_min.y)
							y1=y0+world_dy*self.gl_main.scale.y_mul

							x0=0.0#self.scale.project_m2screen_y(self.gl_main.scale.world_min.y)

							world_dz=(self.gl_main.scale.world_max.z-self.gl_main.scale.world_min.z)
							z0=self.scale.project_m2screen_z(self.gl_main.scale.world_min.z)
							z1=z0+world_dz*self.gl_main.scale.z_mul

							dy=(y1-y0)/float(fdtd.fdtd_ylen)
							dz=(z1-z0)/float(fdtd.fdtd_zlen)
							
							self.gl_objects_add_grid(x0,x0,y0,y1,z0,z1,"fdtd_zy",color=[0.8,0.0,0.8,1.0],direction="zy")
						elif fdtd.fdtd_xzy=="xy":
							world_dy=(self.gl_main.scale.world_max.y-self.gl_main.scale.world_min.y)
							y0=self.scale.project_m2screen_y(self.gl_main.scale.world_min.y)
							y1=y0+world_dy*self.gl_main.scale.y_mul

							world_dz=(self.gl_main.scale.world_max.z-self.gl_main.scale.world_min.z)
							z0=self.scale.project_m2screen_z(self.gl_main.scale.world_min.z)+world_dz*self.gl_main.scale.z_mul/2.0

							world_dx=(self.gl_main.scale.world_max.x-self.gl_main.scale.world_min.x)
							x0=self.scale.project_m2screen_x(self.gl_main.scale.world_min.x)
							x1=x0+world_dx*self.gl_main.scale.x_mul

							dy=(y1-y0)/float(fdtd.fdtd_ylen)
							dx=(x1-x0)/float(fdtd.fdtd_xlen)

							self.gl_objects_add_grid(x0,x1,y0,y1,z0,z0,"fdtd_xy",color=[0.8,0.0,0.8,1.0],direction="xy")
						elif fdtd.fdtd_xzy=="zx":
							world_dy=(self.gl_main.scale.world_max.y-self.gl_main.scale.world_min.y)
							y0=self.scale.project_m2screen_y(self.gl_main.scale.world_min.y)+world_dy*self.gl_main.scale.y_mul/2.0

							world_dz=(self.gl_main.scale.world_max.z-self.gl_main.scale.world_min.z)
							z0=self.scale.project_m2screen_z(self.gl_main.scale.world_min.z)
							z1=z0+world_dz*self.gl_main.scale.z_mul

							world_dx=(self.gl_main.scale.world_max.x-self.gl_main.scale.world_min.x)
							x0=self.scale.project_m2screen_x(self.gl_main.scale.world_min.x)
							x1=x0+world_dx*self.gl_main.scale.x_mul


							dx=(x1-x0)/float(fdtd.fdtd_xlen)
							dz=(z1-z0)/float(fdtd.fdtd_zlen)
							self.gl_objects_add_grid(x0,x1,y0,y0,z0,z1,"fdtd_zx",color=[0.8,0.0,0.8,1.0],direction="zx")

			if self.active_view.show_gl_lights==True:
				for light in json_root().gl.gl_lights.segments:
					a=self.gl_main.add_object()
					a.type="ball"
					a.id=[light.id]
					a.add_xyz(light.x0,light.y0,light.z0)
					a.selectable=True
					a.dx=0.4
					a.dy=0.4
					a.dz=0.4
					a.r=light.color_r
					a.g=light.color_g
					a.b=light.color_b
					a.alpha=light.color_alpha
			self.draw_text(x,z)



		def build_scene(self):
			self.scene_built=True
			self.load_data()
			self.update()
			self.rebuild_scene()

		def force_redraw_hard(self):
			self.refresh_world_size=True
			self.scale.gl_scale.calculated_world_min_max=False
			self.scale.set_m2screen()
			self.force_redraw(level="reload_rebuild")

		def force_redraw(self,level="rebuild"):
			if level=="reload_rebuild":
				data=json_root()
				data.load_triagles()
				self.build_scene()
				self.do_draw()
				self.menu_update()
			elif level=="rebuild":
				self.build_scene()
				self.do_draw()
				self.menu_update()
			elif level=="no_rebuild":
				self.update()

		def resizeEvent(self,event):
			if self.failed==False:
				#glClearDepth(1.0)              
				#glDepthFunc(GL_LESS)
				#glEnable(GL_DEPTH_TEST)
				#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
				#glEnable(GL_BLEND);
				#glShadeModel(GL_SMOOTH)
				glViewport(0, 0, self.width(), self.height()+100)
				glMatrixMode(GL_PROJECTION)
				glLoadIdentity()
				#glScalef(1.0, 1.0, -1.0)              
				gluPerspective(45.0,float(self.width()) / float(self.height()+100),0.1, 1000.0)
				glMatrixMode(GL_MODELVIEW)

		def initializeGL(self):
			self.load_data()
			try:
				glClearDepth(5.0)     
				glDepthFunc(GL_LESS)
				glEnable(GL_DEPTH_TEST)
				glEnable(GL_BLEND)
				glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)	#GL_ONE
				
				glEnableClientState(GL_VERTEX_ARRAY)
				glShadeModel(GL_SMOOTH)
				glColorMaterial(GL_FRONT, GL_DIFFUSE)		#This means we can set the color of a material using glColor and not glMaterialfv
				glEnable(GL_COLOR_MATERIAL)							#This means we can set the color of a material using glColor and not glMaterialfv
				
				#glEnable(GL_FOG);
				#fogColor = [0.2, 0.2, 0.2, 0.0];

				#glFogi (GL_FOG_MODE, GL_EXP);
				#glFogfv (GL_FOG_COLOR, fogColor);
				#glFogf (GL_FOG_DENSITY, 0.1);
				#glHint (GL_FOG_HINT, GL_DONT_CARE);
				#glFogf (GL_FOG_START, 10.0);
				#glFogf (GL_FOG_END, 15.0);
				
				glViewport(0, 0, self.width(), self.height()+100)
				glMatrixMode(GL_PROJECTION)
				glLoadIdentity()
				#glScalef(1.0, 1.0, -1.0)                  
				gluPerspective(45.0,float(self.width()) / float(self.height()+100),0.001, 1000.0) 
				glMatrixMode(GL_MODELVIEW)
				glEnable( GL_POLYGON_SMOOTH )
				#glEnable(GL_MULTISAMPLE)
				#self.resizeEvent.connect(self.resize)
			
				pos=0
				glEnable(GL_LIGHTING)
				self.failed=False
				get_epi().add_callback(self.force_redraw)
			except:
				self.failed=True

		def boom(self):
			print("oh")
else:
	from gl_fallback import gl_fallback

	class glWidget(gl_fallback):
		def __init__(self, parent):
			gl_fallback.__init__(self)
			self.show_error()

