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

## @package json_jv
#  Store the cv domain json data
#

from json_base import json_base
from math import fabs
from json_gl_lights import json_gl_lights
import ctypes

class json_gl_view(ctypes.Structure,json_base):
	_fields_ = [('enabled', ctypes.c_int),
				('xRot', ctypes.c_double),
				('yRot', ctypes.c_double),
				('zRot', ctypes.c_double),
				('x_pos', ctypes.c_double),
				('y_pos', ctypes.c_double),
				('zoom', ctypes.c_double),
				('window_x', ctypes.c_double),
				('window_y', ctypes.c_double),
				('window_w', ctypes.c_double),
				('window_h', ctypes.c_double),

				('enable_view_move', ctypes.c_int),
				('color_r', ctypes.c_double),
				('color_g', ctypes.c_double),
				('color_b', ctypes.c_double),
				('color_alpha', ctypes.c_double),
				('render_grid', ctypes.c_int),
				('render_fdtd_grid', ctypes.c_int),
				('render_cords', ctypes.c_int),
				('render_photons', ctypes.c_int),
				('render_plot', ctypes.c_int),
				('draw_device', ctypes.c_int),
				('optical_mode', ctypes.c_int),
				('plot_graph', ctypes.c_int),
				('show_world_box', ctypes.c_int),
				('show_detectors', ctypes.c_int),
				('text', ctypes.c_int),
				('dimensions', ctypes.c_int),
				('stars_distance', ctypes.c_int),
				('transparent_objects', ctypes.c_int),
				('draw_rays', ctypes.c_int),
				('ray_solid_lines', ctypes.c_int),
				('render_light_sources', ctypes.c_int),
				('show_gl_lights', ctypes.c_int),
				('show_buttons', ctypes.c_int),
				('stars', ctypes.c_int)]

	def __init__(self):
		json_base.__init__(self,"gl_view")
		self.var_list=[]

		#paramters which can be saved (Allso added to C types)
		self.var_list.append(["enabled",False])
		self.var_list.append(["xRot",25.0])
		self.var_list.append(["yRot",1.0])
		self.var_list.append(["zRot",0.0])
		self.var_list.append(["x_pos",0.0])
		self.var_list.append(["y_pos",0.0])
		self.var_list.append(["zoom",16.0])
		self.var_list.append(["window_x",0.0])
		self.var_list.append(["window_y",0.0])
		self.var_list.append(["window_w",0.0])
		self.var_list.append(["window_h",0.0])
		self.var_list.append(["enable_view_move",True])
		self.var_list.append(["color_r",0.0])
		self.var_list.append(["color_g",0.0])
		self.var_list.append(["color_b",0.0])
		self.var_list.append(["color_alpha",0.5])
		self.var_list.append(["render_grid",True])
		self.var_list.append(["render_fdtd_grid",True])
		self.var_list.append(["render_cords",True])
		self.var_list.append(["render_photons",True])
		self.var_list.append(["render_plot",True])
		self.var_list.append(["draw_device",True])
		self.var_list.append(["optical_mode",True])
		self.var_list.append(["plot_graph",True])
		self.var_list.append(["show_world_box",False])
		self.var_list.append(["show_detectors",True])
		self.var_list.append(["text",True])
		self.var_list.append(["dimensions",False])
		self.var_list.append(["stars_distance",60])
		self.var_list.append(["transparent_objects",False])
		self.var_list.append(["draw_rays",True])
		self.var_list.append(["ray_solid_lines",False])
		self.var_list.append(["render_light_sources",True])
		self.var_list.append(["show_gl_lights",False])
		self.var_list.append(["show_buttons",True])
		self.var_list.append(["stars",False])

		#not in C types
		self.var_list.append(["name","view"])
		self.var_list.append(["id",self.random_id()])

		self.var_list_build()
		self.reset_shift_max_angles()


	def reset_shift_max_angles(self):
		self.max_angle_shift=4.0

	def shift(self,target):
		if self.enabled==False:
			return True

		if self.name!="3d":
			return True

		stop=False
		move=0.0
		max_xy_shift=0.2
		delta=(target.xRot-self.xRot)
		if fabs(delta)>self.max_angle_shift:
			delta=self.max_angle_shift*delta/fabs(delta)

		self.xRot=self.xRot+delta
		move=move+fabs(delta)

		delta=(target.yRot-self.yRot)
		if fabs(delta)>self.max_angle_shift:
			delta=self.max_angle_shift*delta/fabs(delta)

		self.yRot=self.yRot+delta
		move=move+fabs(delta)

		delta=(target.zRot-self.zRot)
		if fabs(delta)>self.max_angle_shift:
			delta=self.max_angle_shift*delta/fabs(delta)

		self.zRot=self.zRot+delta
		move=move+fabs(delta)
		
		delta=(target.x_pos-self.x_pos)
		if fabs(delta)>max_xy_shift:
			delta=max_xy_shift*delta/fabs(delta)

		self.x_pos=self.x_pos+delta
		move=move+fabs(delta)
		
		delta=(target.y_pos-self.y_pos)
		if fabs(delta)>max_xy_shift:
			delta=max_xy_shift*delta/fabs(delta)

		self.y_pos=self.y_pos+delta
		move=move+fabs(delta)

		delta=(target.zoom-self.zoom)
		if fabs(delta)>1.0:
			delta=1.0*delta/fabs(delta)

		self.zoom=self.zoom+delta
		move=move+fabs(delta)
		
		if move==0.0:
			stop=True

		return stop

	def set_value(self,data):
		self.xRot=data.xRot
		self.yRot=data.yRot
		#self.zRot=data.zRot
		self.x_pos=data.x_pos
		self.y_pos=data.y_pos
		self.zoom=data.zoom

	def set_xy(self):
		self.xRot=3
		self.yRot=0.0
		self.zRot=0.0
		self.x_pos=0.0
		self.y_pos=0.0
		self.zoom=16
		self.name="xy"

	def set_xz(self):
		self.xRot=90.0
		self.yRot=90.0
		self.zRot=0.0
		self.x_pos=0.0
		self.y_pos=0.0
		self.zoom=16
		self.name="xz"

	def set_yz(self):
		self.xRot=3
		self.yRot=90
		self.zRot=0.0
		self.x_pos=0.0
		self.y_pos=0.0
		self.zoom=16
		self.name="yz"


class json_flybys(json_base):
	def __init__(self):
		json_base.__init__(self,"flyby",segment_class=True,segment_example=json_gl_view())

	def load_from_json(self,json):
		self.var_list=[]

		self.segments=[]
		try:
			segs=json['segments']
		except:
			self.segments.append(json_gl_view())
			self.segments.append(json_gl_view())
			return
		for i in range(0,segs):
			a=json_gl_view()
			simulation_name="segment"+str(i)
			a.load_from_json(json[simulation_name])
			self.segments.append(a)

class json_views(json_base):
	def __init__(self):
		json_base.__init__(self,"views",segment_class=True,segment_example=json_gl_view())
		self.safe_init(0)

	def load_from_json(self,json):
		self.var_list=[]
		segs=0
		try:
			segs=json['segments']
		except:
			pass

		if self.safe_init(segs)==False:
			self.segments=[]
			for i in range(0,segs):
				a=json_gl_view()
				simulation_name="segment"+str(i)
				a.load_from_json(json[simulation_name])
				self.segments.append(a)

	def safe_init(self,segs):
		if segs!=6:
			self.segments=[]
			v=json_gl_view()
			v.window_x=0.0
			v.window_y=0.0
			v.window_w=1.0
			v.window_h=1.0
			v.name="3d"
			v.enable_view_move=True
			v.enabled=True
			self.segments.append(v)

			v=json_gl_view()
			v.window_x=0.0
			v.window_y=0.0
			v.window_w=0.5
			v.window_h=0.5
			v.name="3d_small"
			v.enable_view_move=True
			self.segments.append(v)

			v=json_gl_view()
			v.window_x=0.5
			v.window_y=0.5
			v.window_w=0.5
			v.window_h=0.5
			v.enable_view_move=False
			v.set_xy()
			self.segments.append(v)

			v=json_gl_view()
			v.window_x=0.0
			v.window_y=0.5
			v.window_w=0.5
			v.window_h=0.5
			v.enable_view_move=False
			v.set_xz()
			self.segments.append(v)

			v=json_gl_view()
			v.window_x=0.5
			v.window_y=0.0
			v.window_w=0.5
			v.window_h=0.5
			v.enable_view_move=False
			v.set_yz()
			self.segments.append(v)

			v=json_gl_view()
			v.window_x=0.0
			v.window_y=0.0
			v.window_w=1.0
			v.window_h=1.0
			v.name="plot"
			self.segments.append(v)
			return True
		return False


class json_gl(json_base):

	def __init__(self):
		json_base.__init__(self,"gl")
		self.var_list=[]
		self.var_list.append(["flybys",json_flybys()])
		self.var_list.append(["views",json_views()])
		self.var_list.append(["gl_lights",json_gl_lights()])
		self.var_list_build()
