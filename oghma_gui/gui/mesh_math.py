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

## @package mesh_math
#  Generate mesh grids, this is a bit of a sticking plaster until it is converted to C
#

from json_c import json_tree_c
from bytes2str import str2bytes
import ctypes

class mesh_math(ctypes.Structure):

	_fields_ = [('enabled', ctypes.c_int),
				('nlayers', ctypes.c_int),
				('remesh', ctypes.c_int),
				('layers', ctypes.c_void_p ),
				('start', ctypes.c_double),
				('stop', ctypes.c_double),
				('tot_points', ctypes.c_int),
				('automatic', ctypes.c_int),
				('start_at_zero', ctypes.c_int),
				('stop_at_end', ctypes.c_int),
				('mesh', ctypes.POINTER(ctypes.c_double)),
				('dmesh', ctypes.POINTER(ctypes.c_double))]

	def __init__(self,json_path):
		self.bin=json_tree_c()
		self.json_path=json_path
		self.direction=self.json_path[-1]
		self.mesh_pos=[]
		self.mesh_val=[]
		self.bin.lib.mesh_init(ctypes.byref(self))

	def __del__(self):
		self.bin.lib.mesh_free(ctypes.byref(self))

	#This exists in C as well
	def get_len(self):
		tot=0.0
		segments=self.bin.get_token_value(self.json_path,"segments")
		for s in range(0,segments):
			length=self.bin.get_token_value(self.json_path+".segment"+str(s),"len")
			tot=tot+length

		return tot

	def enabled(self):
		enabled=self.bin.get_token_value(self.json_path,"enabled")
		return enabled

	def segments(self):
		segments=self.bin.get_token_value(self.json_path,"segments")
		return segments

	#This exists in C as well
	def get_points(self):
		tot=0.0
		segments=self.bin.get_token_value(self.json_path,"segments")
		for s in range(0,segments):
			points=self.bin.get_token_value(self.json_path+".segment"+str(s),"points")
			tot=tot+points

		return tot

	def set_len(self,value):
		segments=self.bin.get_token_value(self.json_path,"segments")
		if segments==1:
			self.bin.set_token_value(self.json_path+".segment0","len",value)
			return True
		else:
			return False

	def set_segment_len(self,seg,length):
		self.bin.set_token_value(self.json_path+".segment"+str(seg),"len",length)

	def calculate_points(self,one_point_per_layer=False):
		self.tot_points=0
		self.mesh_pos=[]
		self.mesh_val=[]
		self.bin.lib.mesh_free(ctypes.byref(self))
		done=False

		if one_point_per_layer==True:
			self.bin.lib.mesh_to_lin_array_one_point_per_layer(ctypes.byref(self), ctypes.byref(self.bin))
			done=True

		if self.direction=="l" or self.direction=="t":
			ret=self.bin.json_obj_find_by_path(self.json_path)
			self.bin.lib.mesh_load_from_json(None, ctypes.byref(self), ret)
			self.bin.lib.mesh_to_lin_array_lambda(None, ctypes.byref(self))
			done=True

		if done==False:			#This is electrical
			ret=self.bin.json_obj_find_by_path(self.json_path)
			self.bin.lib.mesh_load_from_json(None, ctypes.byref(self), ret)
			self.bin.lib.mesh_to_lin_array(None, None, ctypes.byref(self.mesh) , None, ctypes.byref(self))
			#self.bin.lib.mesh_dump_to_file(ctypes.c_char_p(str2bytes("one.csv")), ctypes.byref(self))

		if (self.tot_points>0):
			mesh = ctypes.cast(self.mesh, ctypes.POINTER(ctypes.c_double * self.tot_points)).contents
			self.mesh_pos = list(mesh)
			self.mesh_val = [1] * len(self.mesh_pos)
		return self.mesh_pos,self.mesh_val

	def gen_dat_file(self,dat_file):
		self.bin.lib.mesh_to_dat_file(ctypes.byref(dat_file), ctypes.byref(self), ctypes.c_int(True))

