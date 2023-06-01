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

## @package json_local_root
#  Store the cv domain json data
#


import os
from json_base import json_base
from cal_path import sim_paths
from json_cluster import json_cluster

class json_save_window(json_base):

	def __init__(self):
		json_base.__init__(self,"save_window")
		self.var_list=[]
		self.var_list.append(["name","none"])
		self.var_list.append(["x",-1])
		self.var_list.append(["y",-1])
		self.var_list_build()

class json_save_windows(json_base):

	def __init__(self):
		json_base.__init__(self,"windows",segment_class=True,segment_example=json_save_window())

class json_icon_lib(json_base):

	def __init__(self):
		json_base.__init__(self,"json_icon_lib")
		self.var_list=[]
		self.var_list.append(["text-x-generic","text-x-generic"])
		self.var_list.append(["wps-office-xls","wps-office-xls"])
		self.var_list.append(["info","info_file"])
		self.var_list.append(["text-x-generic","text-x-generic"])
		self.var_list.append(["wps-office-xls","wps-office-xls"])
		self.var_list.append(["spectra","spectra_file"])
		self.var_list.append(["organic_material","organic_material"])
		self.var_list.append([".png","image-png"])
		self.var_list.append([".oghma","si"])
		self.var_list.append([".xlsx","wps-office-xls"])
		self.var_list.append([".pdf","pdf"])
		self.var_list.append(["desktop","folder"])
		self.var_list.append(["constraints","dat_file"])
		self.var_list_build()

class json_gui_config(json_base):

	def __init__(self):
		json_base.__init__(self,"gui_config")
		self.var_list=[]
		self.var_list.append(["enable_opengl",True])
		self.var_list.append(["gui_use_icon_theme",False])
		self.var_list.append(["matlab_interpreter","octave"])
		self.var_list.append(["enable_webbrowser",False])
		self.var_list.append(["enable_betafeatures",False])
		self.var_list.append(["toolbar_icon_size",48])
		self.var_list_build()

class json_os(json_base):

	def __init__(self):
		json_base.__init__(self,"os")
		self.var_list=[]
		self.var_list.append(["use_wine","False"])
		self.var_list_build()

class json_international(json_base):

	def __init__(self):
		json_base.__init__(self,"international")
		self.var_list=[]
		self.var_list.append(["lang","auto"])
		self.var_list_build()

class json_opencl(json_base):

	def __init__(self):
		json_base.__init__(self,"opencl")
		self.var_list=[]
		self.var_list.append(["device","none"])
		self.var_list_build()

class json_local(json_base):

	def __init__(self):
		json_base.__init__(self,"local")
		self.var_list=[]
		self.var_list.append(["international",json_international()])
		self.var_list.append(["opencl",json_opencl()])
		self.var_list.append(["gui_config",json_gui_config()])
		self.var_list.append(["icon_lib",json_icon_lib()])
		self.var_list.append(["cluster",json_cluster()])
		self.var_list.append(["windows",json_save_windows()])
		self.var_list.append(["os",json_os()])
		self.var_list_build()
		self.include_name=False

my_data=json_local()
my_data.load(os.path.join(sim_paths.get_user_settings_dir(),"data.json"))
if my_data.loaded==True:
	my_data.save()

my_data.loaded=True

def json_local_root():
	return my_data
