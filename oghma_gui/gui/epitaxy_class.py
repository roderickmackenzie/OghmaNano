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

## @package epitaxy_class
#  The epitaxy class.
#

import os
import math

from cal_path import get_materials_path
from cal_path import get_default_material_path

from cal_path import sim_paths
from json_contacts import json_contacts
from shape import shape

from gui_enable import gui_get
if gui_get()==True:
	#from file_watch import get_watch
	from PySide2.QtWidgets import QWidget
from json_base import json_base
from json_epi_interface import json_epi_interface
from json_material_db_item import json_material_db_item

class epi_layer(shape):
	def __init__(self):
		super().__init__() 
		self.var_list.append(["layer_type","other"])
		self.var_list.append(["layer_interface",json_epi_interface()])
		self.var_list.append(["solve_optical_problem","yes_nk"])
		self.var_list.append(["solve_thermal_problem",True])
		self.var_list_build()
		self.start=0.0
		self.end=0.0

	def set_dy(self,data):
		if type(data)==float or type(data)==int:
			self.dy=float(data)
		if type(data)==str:
			try:
				self.dy=float(data)
			except:
				return False

		return True

	def cal_rgb(self):
		if self.color_r==0.0 and self.color_g==0.8 and self.color_b==0.0:
			mat_db_item=json_material_db_item()
			if mat_db_item.load(os.path.join(os.path.join(get_materials_path(),self.optical_material),"data.json"))==False:
				return

			self.color_r=mat_db_item.color_r
			self.color_g=mat_db_item.color_g
			self.color_b=mat_db_item.color_b
			self.color_alpha=mat_db_item.color_alpha

class epitaxy(json_base):

	def __init__(self):
		self.layers=[]
		self.callbacks=[]
		json_base.__init__(self,"epitaxy")
		self.segments_name=["layers"]
		self.var_list.append(["contacts",json_contacts()])
		self.var_list.append(["icon_","layers"])
		self.var_list_build()

		self.loaded=False

	def dump_tree(self):
		for i in range(0,len(self.layers)):
			l=self.layers[i]
			print("layer:"+str(i)+" "+str(l.name))
			for s in l.segments:
				print(s.name)

	def dump(self):
		lines=self.gen_output()
		for l in lines:
			print(l)

	def get_new_material_name(self):
		count=0
		while(1):
			found=False
			name="newlayer"+str(count)
			for l in self.layers:
				if name==l.name:
					found=True
					break

			if found==False:
				break
			count=count+1

		return name


	def layer_to_index(self,index):
		if type(index)==int:
			return index
		else:
			for i in range(0,len(self.layers)):
				if self.layers[i].name==index:
					return i
		return -1

	def add_new_layer(self,pos=-1):
		if pos!=-1:
			pos=self.layer_to_index(pos)

		a=epi_layer()
		a.dy=100e-9

		a.name=self.get_new_material_name()

		a.segments=[]
		a.color_r=1.0
		a.color_g=0
		a.color_b=0
		a.color_alpha=0.5
		a.load_triangles()
		if pos==-1:
			self.layers.append(a)
		else:
			self.layers.insert(pos, a)
		return a


	def move_up(self,pos):
		pos=self.layer_to_index(pos)
		if pos<1:
			return

		self.layers.insert(pos-1, self.layers.pop(pos))

	def move_down(self,pos):
		pos=self.layer_to_index(pos)
		#print(pos)
		if pos>len(self.layers)-1 or pos<0:
			return

		self.layers.insert(pos+1, self.layers.pop(pos))

	def gen_json(self):
		lines=[]
		lines.append("\"epitaxy\": {")
		lines.append("\t\"layers\":"+str(len(self.layers))+",")
		for i in range(0,len(self.layers)):
			lines.append("\t\"layer"+str(i)+"\": {")
			lines.extend(self.layers[i].gen_json(include_bracket=False))
			lines.append("},")

		lines[-1]=lines[-1][:-1]

		lines[-1]=lines[-1]+","
		lines.extend(self.contacts.gen_json())
		lines.append("}")
		return lines


	def update_layer_type(self,layer,data):
		l=self.layers[layer]

		l.layer_type=data
		if l.layer_type=="active":
			l.shape_dos.enabled=True
		else:
			l.shape_dos.enabled=False

	def find_object_by_id(self,id):

		for c in self.contacts.segments:
			if c.id==id:
				return c

		for l in self.layers:
			obj=l.find_object_by_id(id)
			if obj!=None:
				return obj

			for s in l.segments:
				obj=s.find_object_by_id(id)
				if obj!=None:
					return obj
		return None

	def find_layer_by_id(self,id):

		nl=0
		for c in self.contacts.segments:
			if c.id==id:
				if c.position=="top":
					return 0

				if c.position=="bottom":
					return len(self.layers)-1

		for l in self.layers:

			if l.id==id:
				return nl

			for s in l.segments:
				if s.id==id:
					return nl

			nl=nl+1

		return None

	def find_shape_by_name(self,name):
		for c in self.contacts.segments:
			if c.name==name:
				return c

		for l in self.layers:
			if l.name==name:
				return l

			for s in l.segments:
				if s.name==name:
					return s

		return None

	def get_top_contact_layer(self):
		for l in range(0,len(self.layers)):
			if self.layers[l].layer_type=="contact": 
				return l

		return -1

	def get_btm_contact_layer(self):
		found=0
		for l in range(0,len(self.layers)):
			if self.layers[l].layer_type=="contact":
				if found==1:
					return l
				found=found+1

		return -1

	def get_all_sub_shapes(self,id):
		ret=[]
		for l in self.layers:
			if l.id==id:
				ret.append(l)

				for s in l.segments:
					ret.append(s)
					#return ret

		return ret

	def ylen(self):
		tot=0
		for a in self.layers:
			tot=tot+a.dy

		return tot


	def get_layer_by_cordinate(self,y):
		tot=0
		for i in range(0,len(self.layers)):
			tot=tot+self.layers[i].dy
			#print(tot, y,i)
			if tot>=y or math.isclose(tot, y, rel_tol=1e-10):
				return i

		return -1


	def reload_shapes(self):
		for a in self.layers:
			for s in a.segments:
				#print(s.file_name)
				s.load(s.file_name)

	def get_shapes_between_x(self,x0,x1):
		segments=[]
		for layer in self.layers:
			for s in layer.segments:
				for pos in s.expand_xyz0(layer):
					if pos.x>x0 and pos.x<x1:
						segments.append(s)
		return segments

	def add_callback(self,fn):
		self.callbacks.append(fn)


	def load_from_json(self,json):
		if type(json)!=dict:
			asdasd

		self.layers=[]

		y_pos=0.0

		number_of_layers=json['layers']

		for layer in range(0,number_of_layers):
			layer_json=json['layer'+str(layer)]

			a=epi_layer()

			a.decode_from_json(layer_json)

			if a.layer_type=="active":
				a.shape_dos.enabled=True

			a.cal_rgb()

			#shape
			a.segments=[]
			use_segs=False
			try:
				segs=int(layer_json['layer_shapes'])
				use_segs=False
			except:
				pass

			try:
				segs=int(layer_json['segments'])
				use_segs=True
			except:
				pass

			for ns in range(0,segs):
				my_shape=shape()
				if use_segs==True:
					if "segment"+str(ns) in layer_json:
						my_shape.decode_from_json(layer_json["segment"+str(ns)])
						my_shape.moveable=True
						a.segments.append(my_shape)
				else:
					if "shape"+str(ns) in layer_json:
						my_shape.decode_from_json(layer_json["shape"+str(ns)])
						my_shape.moveable=True
						a.segments.append(my_shape)
	
			a.start=y_pos

			y_pos=y_pos+a.dy

			a.end=y_pos
			self.layers.append(a)

		self.contacts.load_json(json['contacts'])
		self.loaded=True
		#self.dump_tree()



	def get_layer_end(self,l):

		pos=0.0
		for i in range(0, l+1):
			pos=pos+self.layers[i].dy

		return pos

	def get_layer_start(self,l):

		pos=0.0
		for i in range(0, l):
			pos=pos+self.layers[i].dy

		return pos

	def get_device_start(self,data):
		if data.electrical_solver.solver_type=="circuit":
			return 0.0

		pos=0.0
		for i in range(0, len(self.layers)):
			if self.layers[i].layer_type=="active":
				return pos

			pos=pos+self.layers[i].dy

		return None

	def get_next_dos_layer(self,layer):
		layer=layer+1
		for i in range(layer,len(self.layers)):
			if self.layers[i].layer_type=="active":
				return i

		return False



	def symc_to_mesh(self,mesh_y):
		active_layers=0
		tot_dy=0.0
		for l in self.layers:
			if l.layer_type=="active":
				active_layers=active_layers+1
				tot_dy=tot_dy+l.dy

		if len(mesh_y.segments)==active_layers:
			pos=0
			for l in self.layers:
				if l.layer_type=="active":
					mesh_y.segments[pos].len=l.dy
					pos=pos+1
			return

		if len(mesh_y.segments)==1:
			mesh_y.segments[0].len=tot_dy

