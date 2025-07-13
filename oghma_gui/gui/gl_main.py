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

import ctypes
from dat_file import dat_file
from cal_path import sim_paths
from gl_base_object import gl_base_object
from vec import vec
from color_map import color_map_item,rgb_char
from dat_file import dat_file
from vec import vec2d_int

class gl_mouse_event(ctypes.Structure):
	_fields_ = [('time', ctypes.c_double),
				('dxyz', vec),
				('rotate_x', ctypes.c_double),
				('rotate_y', ctypes.c_double),
				('working', ctypes.c_int),
				('drag', ctypes.c_int),
				('rotate', ctypes.c_int),
				('scale', ctypes.c_int),
				('mouse_mode', ctypes.c_int),
				('button', ctypes.c_int),
				('xy', vec2d_int),
				('angle_delta', ctypes.c_int),
				('xy_last', vec2d_int),
				('dxdx', ctypes.c_double),
				('dydx', ctypes.c_double),
				('dzdx', ctypes.c_double),
				('dxdy', ctypes.c_double),
				('dydy', ctypes.c_double),
				('dzdy', ctypes.c_double),
				('last_object_clicked', ctypes.c_int)]

	def __init__(self):
		self.lib=sim_paths.get_dll_py()
		self.lib.gl_mouse_event_init(ctypes.byref(self))

	def delta_time(self):
		return time.time()-self.time

class obj_color(ctypes.Structure):
	_fields_ = [('map', ctypes.c_int),
				('r', ctypes.c_double),
				('g', ctypes.c_double),
				('b', ctypes.c_double),
				('alpha', ctypes.c_double)]

class gl_view(ctypes.Structure):
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
				('background_color', obj_color),
				('render_grid', ctypes.c_int),
				('render_fdtd_grid', ctypes.c_int),
				('render_cords', ctypes.c_int),
				('render_photons', ctypes.c_int),
				('render_plot', ctypes.c_int),
				('draw_device', ctypes.c_int),
				('optical_mode', ctypes.c_int),
				('plot_graph', ctypes.c_int),
				('show_world_box', ctypes.c_int),
				('show_electrical_box', ctypes.c_int),
				('show_thermal_box', ctypes.c_int),
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
				('stars', ctypes.c_int),
				('name', ctypes.c_char * 200),
				('projection', ctypes.c_double * 16),
				('modelview', ctypes.c_double * 16),
				('viewport', ctypes.c_int * 4),
				('max_angle_shift', ctypes.c_double),
				('cut_through_frac_y',ctypes.c_double),
				('cut_through_frac_z',ctypes.c_double),
				('color_map_graph',ctypes.POINTER(color_map_item)),
				('color_map_graph_last',ctypes.POINTER(color_map_item)),
				('overlay_enabled', ctypes.c_int),
				('overlay_texture', ctypes.c_uint),
				('overlay', ctypes.c_void_p),
				('last_width', ctypes.c_int),
				('last_height', ctypes.c_int)]

class gl_light(ctypes.Structure):
	_fields_ = [('x0', ctypes.c_double),
				('y0', ctypes.c_double),
				('z0', ctypes.c_double),
				('color_r', ctypes.c_double),
				('color_g', ctypes.c_double),
				('color_b', ctypes.c_double),
				('color_alpha', ctypes.c_double),
				('uid', ctypes.c_char * 100)]

class gl_simple_shapes_lib(ctypes.Structure):
	_fields_ = [('box', dat_file),
				('stars', dat_file),
				('optical_mode', dat_file)]

class gl_scale(ctypes.Structure):
	_fields_ = [('z_mul', ctypes.c_double),
				('x_mul', ctypes.c_double),
				('y_mul', ctypes.c_double),
				('z_start', ctypes.c_double),
				('x_start', ctypes.c_double),
				('y_start', ctypes.c_double),
				('gl_universe_x0', ctypes.c_double),
				('gl_universe_x1', ctypes.c_double),
				('gl_universe_z0', ctypes.c_double),
				('gl_universe_z1', ctypes.c_double),
				('world_fills_mesh', ctypes.c_int),
				('calculated_world_min_max', ctypes.c_int),
				('world_min', vec),
				('world_max', vec),
				('electrical_world_min', vec),
				('electrical_world_max', vec),
				('thermal_world_min', vec),
				('thermal_world_max', vec),
				('gl_world_min', vec),
				('gl_world_max', vec)]

class text_lib(ctypes.Structure):
	_fields_ = [('items', ctypes.c_void_p),
				('n_items', ctypes.c_int),
				('n_items_max', ctypes.c_int),
				('buf', ctypes.c_void_p),
				('library', ctypes.c_void_p),
				('face', ctypes.c_void_p),
				('rgb',rgb_char),
				('font_size', ctypes.c_int),
				('line_spacing', ctypes.c_int),
				('center_x', ctypes.c_int),
				('center_y', ctypes.c_int),
				('vertical', ctypes.c_int)]

class gl_main(ctypes.Structure):
	_fields_ = [('objects_n', ctypes.c_int),
				('objects_max', ctypes.c_int),
				('objects', ctypes.c_void_p),
				('false_color', ctypes.c_int),
				('text', text_lib),
				('scale', gl_scale),
				('simple_shapes_lib', gl_simple_shapes_lib),
				('active_view', ctypes.POINTER(gl_view)),
				('views', ctypes.POINTER(gl_view)),
				('n_views', ctypes.c_int),
				('n_views_max', ctypes.c_int),
				('view_target', gl_view),
				('lights', ctypes.POINTER(gl_light)),
				('n_lights', ctypes.c_int),
				('mouse_event', gl_mouse_event),
				('ndata', ctypes.c_int),
				('data', ctypes.POINTER(dat_file))]

	def __init__(self):
		self.lib=sim_paths.get_dll_py()
		self.lib.gl_main_add_object.restype = ctypes.c_void_p
		self.lib.gl_main_get_object.restype = ctypes.c_void_p
		self.lib.gl_base_object_add_block.restype = ctypes.c_void_p
		self.lib.gl_main_init(ctypes.byref(self))
		#size = ctypes.sizeof(self)
		#print(f"The size of MyStruct is: {size} bytes")

	def __del__(self):
		self.lib.gl_main_free(ctypes.byref(self))

	def get_object(self,n):
		return gl_base_object.from_address(self.lib.gl_main_get_object(ctypes.byref(self),ctypes.c_int(n)))

	def get_number_objects_selected(self,only_real):
		return self.lib.gl_get_number_objects_selected(ctypes.byref(self),ctypes.c_int(only_real))
