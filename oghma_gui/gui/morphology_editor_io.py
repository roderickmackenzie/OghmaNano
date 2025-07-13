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

## @package shape_editor_io
#  This builds the images which are then used to generate shapes
#

import os

from server import server_get
from cal_path import sim_paths
from json_c import json_c

class morphology_editor_io():

	def __init__(self,path):
		self.path=path
		self.bin=json_c("morphology_db")
		self.bin.build_template()
	
	def load(self):
		self.bin.load(os.path.join(self.path,"data.json"))

	def save(self):
		self.bin.save()

	def add_job_to_server(self,sim_path,server):
		server.add_job(sim_path,"--simmode data@morphology_gen --path \""+self.path+"\"")

	def new_morphology(self,path,info=[]):
		from dlg_get_text2 import dlg_get_text2
		from clone_materials import clone_material
		new_sim_name=dlg_get_text2( _("New morphology name:"), _("New morphology name"),"add_morphology")
		if new_sim_name==None:
			return
		new_sim_name=new_sim_name.ret
	
		if new_sim_name!=None:
			new_morphology=os.path.join(path,new_sim_name)
			try:
				os.mkdir(new_morphology)
			except:
				pass

			self.bin.save_as(os.path.join(new_morphology,"data.json"))
			
			return new_morphology

		return None

