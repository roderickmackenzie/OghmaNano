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

## @package json_root
#  Used to store json data
#


from inp import inp
from epitaxy_class import epitaxy
from json_base import json_base
from json_fit import json_fits
from json_math import json_math
from json_hard_limit import json_hard_limit
from json_perovskite import json_perovskite
from json_server import json_server
from json_thermal import json_thermal
from json_exciton import json_exciton_main
from json_electrical_solver import json_electrical_solver
from json_circuit import json_circuit
from json_opengl_config import json_opengl_config
from json_gl import json_gl
from json_world import json_world
from json_world_stats import json_world_stats
from json_ml import json_ml
from json_dump import json_dump
from json_singlet import json_singlet
from json_sims import json_sims
from json_optical import json_optical
from json_mesh import json_mesh_segment
from json_mesh import json_mesh_lambda
from json_scan import json_scans
from json_gui_config import json_gui_config

class json_parasitic(json_base):

	def __init__(self):
		json_base.__init__(self,"parasitic")
		self.var_list=[]
		self.var_list.append(["icon_","parasitic"])
		self.var_list.append(["Rshunt",1300.0])
		self.var_list.append(["Rcontact",1.439413e+01])
		self.var_list.append(["otherlayers",0.0])
		self.var_list.append(["Rshort",1.0])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()

class json_sim(json_base):
	def __init__(self):
		json_base.__init__(self,"sim")
		self.var_list=[]
		self.var_list.append(["simmode","jv@jv"])
		self.var_list.append(["version","v7.88.17"])
		self.var_list.append(["notes",""])
		self.var_list.append(["first_sim_message",""])
		self.var_list.append(["use_json_local_root",True])
		self.var_list.append(["opengl",json_opengl_config()])
		self.var_list_build()

class all_json_root(json_base,json_world_stats):
	def __init__(self):
		self.loaded=False
		json_base.__init__(self,"main")
		json_world_stats.__init__(self)
		self.var_list=[]
		self.var_list.append(["sim",json_sim()])
		self.var_list.append(["sims",json_sims()])
		self.var_list.append(["optical",json_optical()])
		self.var_list.append(["dump",json_dump()])
		self.var_list.append(["math",json_math()])
		self.var_list.append(["server",json_server()])
		self.var_list.append(["epitaxy",epitaxy()])
		self.var_list.append(["thermal",json_thermal()])
		self.var_list.append(["exciton",json_exciton_main()])
		self.var_list.append(["fits",json_fits()])
		self.var_list.append(["parasitic",json_parasitic()])
		self.var_list.append(["hard_limit",json_hard_limit()])
		self.var_list.append(["perovskite",json_perovskite()])
		self.var_list.append(["singlet",json_singlet()])
		self.var_list.append(["electrical_solver",json_electrical_solver()])
		self.var_list.append(["circuit",json_circuit()])
		self.var_list.append(["gl",json_gl()])
		self.var_list.append(["gui_config",json_gui_config()])
		self.var_list.append(["world",json_world()])
		self.var_list.append(["ml",json_ml()])
		self.var_list.append(["scans",json_scans()])
		self.var_list.append(["icon","icon"])
		self.var_list.append(["sub_icon",""])
		self.var_list.append(["name","Simulation"])
		self.var_list.append(["hidden",False])
		self.var_list.append(["password",""])
		self.var_list.append(["status","open"])

		#public
		#private

		self.var_list_build()

		#short hands
		self.epi=self.epitaxy
		self.include_name=False
		self.auto_reload=False
		self.last_time=-1
		self.call_backs=[]
		

	def check_reload(self):
		if self.last_time!=-1:
			if self.loaded==True:
				#print("check",self.last_time,self.f.time())
				if self.last_time!=self.f.time():
					#print("reloading")
					self.reload()
					for f in self.call_backs:
						f()

	def add_call_back(self,function):
		if function not in self.call_backs:
			self.call_backs.append(function)

	#this is a cut down version of find_object_by_id
	def find_thing_by_id(self,id):
		ret=self.epitaxy.find_object_by_id(id)
		if ret!=None:
			return ret

		ret=self.optical.find_object_by_id(id)
		if ret!=None:
			return ret

		ret=self.world.find_object_by_id(id)
		if ret!=None:
			return ret

	def remove_call_back(self,function):
		if function in self.call_backs:
			self.call_backs.remove(function)

	def rescale_world(self,rx,ry,rz):
		for d in self.world.world_data.segments:
			d.rescale(rx,ry,rz)

		for shape in self.optical.detectors.segments:
			shape.rescale(rx,ry,rz)

		for source in self.optical.light_sources.lights.segments:
			source.rescale(rx,ry,rz)

	def fix_up(self):
		if self.optical.mesh.mesh_x.segments==[]:
			if self.optical.mesh.mesh_y.segments==[]:
				if self.optical.mesh.mesh_z.segments==[]:
					m=json_mesh_segment()
					self.optical.mesh.mesh_y.segments.append(m)
					self.optical.mesh.mesh_y.segments[0].len=self.epi.ylen()
					self.optical.mesh.mesh_y.segments[0].points=200
					self.optical.mesh.mesh_x.enabled=False
					self.optical.mesh.mesh_z.enabled=False

		if self.optical.mesh.mesh_l.segments==[]:
			m=json_mesh_lambda()
			self.optical.mesh.mesh_l.segments.append(m)
			self.optical.mesh.mesh_l.segments[0].start=300e-9
			self.optical.mesh.mesh_l.segments[0].stop=900e-9
			self.optical.mesh.mesh_l.points=10
			self.optical.mesh.mesh_l.enabled=False

		if self.exciton.segments!=[]:
			self.sims.exciton.segments=self.exciton.segments
			self.exciton.segments=[]

my_data=all_json_root()

def json_root():
	return my_data

#
