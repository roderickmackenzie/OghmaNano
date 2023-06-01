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

## @package json_mesh
#  Store the fx domain json data
#

from json_base import json_base

class json_mesh_segment(json_base):

	def __init__(self):
		json_base.__init__(self,"json_mesh_segment")
		self.var_list=[]
		self.var_list.append(["len",0.0032249])
		self.var_list.append(["points",1.0])
		self.var_list.append(["mul",1.0])
		self.var_list.append(["left_right","left"])
		self.var_list_build()

		self.start=0.0
		self.end=0.0

class json_mesh_thermal(json_base):

	def __init__(self):
		json_base.__init__(self,"json_mesh_thermal")
		self.var_list=[]
		self.var_list.append(["start",220])
		self.var_list.append(["stop",300])
		self.var_list.append(["points",7])
		self.var_list.append(["mul",1.0])
		self.var_list.append(["left_right","left"])
		self.var_list_build()

class json_mesh_lambda(json_base):

	def __init__(self):
		json_base.__init__(self,"json_mesh_lambda")
		self.var_list=[]
		self.var_list.append(["start",300e-9])
		self.var_list.append(["stop",1.4e-6])
		self.var_list.append(["points",150.0])
		self.var_list.append(["mul",1.0])
		self.var_list.append(["left_right","left"])
		self.var_list_build()

class json_mesh_xyz(json_base):

	def __init__(self,direction="x",segment_example=json_mesh_segment()):
		self.direction=direction
		json_base.__init__(self,"mesh_"+direction,segment_class=True,segment_example=segment_example)
		self.var_list.append(["enabled",True])
		self.var_list.append(["auto",True])
		self.var_list_build()
		self.mesh_pos=[]
		self.mesh_val=[]

	def get_len(self):
		tot=0.0
		for l in self.segments:
			tot=tot+l.len

		return tot

	def get_points(self):
		tot=0.0
		for l in self.segments:
			tot=tot+l.points

		return tot

	def set_len(self,value):
		if len(self.segments)==1:
			self.segments[0].len=value
			return True
		else:
			return False

	def load_from_json(self,data):
		#compat added in 18/05/2022 remove later
		super(json_mesh_xyz, self).load_from_json(data)
		if self.get_points()==1:
			if self.direction!="y":
				self.enabled=False

		if self.direction=="l":
			if len(self.segments)==1:

				if self.segments[0].points==10.0:
					if self.segments[0].stop==9e-07:
						self.segments[0].points=150
						self.segments[0].start=300e-9
						self.segments[0].stop=1.4e-6

	def calculate_points(self,root_data=None):
		points=[]
		self.tot_points=0
		pos=0.0
		self.mesh_pos=[]
		self.mesh_val=[]
		done=False

		if root_data!=None:
			if self.direction=="y" and root_data.electrical_solver.solver_type=="circuit":
				for l in root_data.epi.layers:
					if l.layer_type=="active" or l.layer_type=="contact":
						self.mesh_pos.append(pos)
						self.mesh_val.append(1.0)
						pos=pos+l.dy/2
						self.mesh_pos.append(pos)
						self.mesh_val.append(1.0)
						pos=pos+l.dy/2
						#print(self.mesh_pos)
				self.mesh_pos.append(pos)
				self.mesh_val.append(1.0)
				
				done=True

		if self.direction=="l" or self.direction=="t":
			for l in self.segments:
				pos=0.0
				if l.points!=0:
					seg_length=l.stop-l.start
					dx=seg_length/l.points
					temp_x=[]
					if seg_length==0.0 and l.points>0:
						self.tot_points=self.tot_points+1
						temp_x.append(0)
					else:
						while(pos<seg_length):
							if pos+dx/2>seg_length:
								break
							pos=pos+dx/2
							temp_x.append(pos)
							pos=pos+dx/2

							dx=dx*l.mul
							self.tot_points=self.tot_points+1
							if dx==0 or self.tot_points>2000:
								break

					l.mesh=[]
					for i in range(0,len(temp_x)):
						if l.left_right=="left":
							l.mesh.append((temp_x[i]))
						else:
							l.mesh.append((l.len-temp_x[i]))

					l.mesh.sort()

			for l in self.segments:
				for p in l.mesh:
					self.mesh_pos.append(l.start+p)
					self.mesh_val.append(1.0)
			done=True

		if done==False:
			for l in self.segments:
				pos=0.0
				if l.points!=0:
					dx=l.len/l.points
					temp_x=[]
					while(pos<l.len):
						if pos+dx/2>l.len:
							break
						pos=pos+dx/2
						temp_x.append(pos)
						pos=pos+dx/2

						dx=dx*l.mul
						self.tot_points=self.tot_points+1
						if dx==0 or self.tot_points>2000:
							break

					l.mesh=[]
					for i in range(0,len(temp_x)):
						if l.left_right=="left":
							l.mesh.append((temp_x[i]))
						else:
							l.mesh.append((l.len-temp_x[i]))

					l.mesh.sort()


			last_l=0.0
			for l in self.segments:
				#print(l.mesh,last_l)
				for p in l.mesh:
					self.mesh_pos.append(p+last_l)
					self.mesh_val.append(1.0)

				last_l=last_l+l.len
		return self.mesh_pos,self.mesh_val

class json_mesh_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["remesh_x",True])
		self.var_list.append(["remesh_y",True])
		self.var_list.append(["remesh_z",True])
		self.var_list_build()


class json_mesh(json_base):

	def __init__(self,optical=False,x=True,y=True,z=True,t=False):
		json_base.__init__(self,"mesh")
		self.var_list=[]
		self.var_list.append(["config",json_mesh_config()])
		if x==True:
			self.var_list.append(["mesh_x",json_mesh_xyz(direction="x")])
		else:
			self.mesh_x=None

		if y==True:
			self.var_list.append(["mesh_y",json_mesh_xyz(direction="y")])
		else:
			self.mesh_y=None

		if z==True:
			self.var_list.append(["mesh_z",json_mesh_xyz(direction="z")])
		else:
			self.mesh_z=None

		if t==True:
			self.var_list.append(["mesh_t",json_mesh_xyz(direction="t",segment_example=json_mesh_thermal())])
		else:
			self.mesh_t=None

		if optical==True:
			self.var_list.append(["mesh_l",json_mesh_xyz(direction="l",segment_example=json_mesh_lambda())])
		else:
			self.mesh_l=None
			
		self.var_list_build()



