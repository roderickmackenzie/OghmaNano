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

## @package cal_path
#  Calculate the where files are, and if you can't find them look harder.
#

import sys
import os
from win_lin import get_platform
from win_lin import set_oghma_core_path
from gui_enable import gui_get
from str2bool import str2bool
import json
from sim_name import sim_name
import ctypes
from bytes2str import str2bytes
from bytes2str import bytes2str

li_path=None
sim_paths=None

class c_paths(ctypes.Structure):
	_fields_ = [('html_path', ctypes.c_char_p),
				('user_home_dir', ctypes.c_char_p),
				('user_desktop_dir', ctypes.c_char_p),
				('user_music_dir', ctypes.c_char_p),
				('user_downloads_dir', ctypes.c_char_p),
				('python_script_path', ctypes.c_char_p),
				('shape_base_path', ctypes.c_char_p),
				('morphology_base_path', ctypes.c_char_p),
				('filters_base_path', ctypes.c_char_p),
				('scripts_base_path', ctypes.c_char_p),
				('atmosphere_path', ctypes.c_char_p),
				('device_lib_path', ctypes.c_char_p),
				('plugins_path', ctypes.c_char_p),
				('image_path', ctypes.c_char_p),
				('css_path', ctypes.c_char_p),
				('flag_path', ctypes.c_char_p),
				('lang_path', ctypes.c_char_p),
				('spectra_base_path', ctypes.c_char_p),
				('cluster_path', ctypes.c_char_p),
				('cluster_libs_path', ctypes.c_char_p),
				('bib_path', ctypes.c_char_p),
				('fonts_path', ctypes.c_char_p),
				('video_path', ctypes.c_char_p),
				('components_path', ctypes.c_char_p),
				('inp_template_path', ctypes.c_char_p),
				('guess_of_main_oghma_dir', ctypes.c_char_p),
				('materials_base_path', ctypes.c_char_p),
				('exe_command', ctypes.c_char_p),
				('src_path', ctypes.c_char_p),
				('li_path', ctypes.c_char_p),
				('text_dump', ctypes.c_char_p),
				('materials', ctypes.c_char_p),
				('filter_path', ctypes.c_char_p),
				('cie_color_path', ctypes.c_char_p),
				('shape_path', ctypes.c_char_p),
				('morphology_path', ctypes.c_char_p),
				('spectra_path', ctypes.c_char_p),
				('tmp_path', ctypes.c_char_p),
				('tmp_path_fast', ctypes.c_char_p),
				('updates', ctypes.c_char_p),
				('oghma_local', ctypes.c_char_p),
				('newton_cache_path', ctypes.c_char_p),
				('external_solver_path', ctypes.c_char_p),
				('root_simulation_path', ctypes.c_char_p),
				('dirs', ctypes.c_int),
				('files', ctypes.c_int),
				('search_oghma_local', ctypes.c_int),
				('installed_from_deb', ctypes.c_int)]

	def __init__(self):
		self.lib = None
		self.dll_path=None
		if self.find_the_dll()==False:
			print("I can't find liboghma_py.dll or liboghma_py.so")
			sys.exit(0)
		self.lib = ctypes.CDLL(self.dll_path)
		if self.lib==None:
			print("Error loading  liboghma_py.dll or liboghma_py.so")
			sys.exit(0)
		self.lib.init_lang()
		self.lib.paths_init(ctypes.byref(self))
		self.lib.color_map_build_index()
		self.lib.paths_set_python_script_path(ctypes.byref(self),ctypes.c_char_p(str2bytes(os.path.dirname(os.path.realpath(__file__)))))
		self.lib.paths_do_search(ctypes.byref(self))
		self.lib.get_compile_time.restype = ctypes.c_char_p
		self.lib.token_lib_find.restype = ctypes.c_void_p
		self.lib.token_lib_rfind.restype = ctypes.c_void_p
		self.lib.server_get_next_job.restype = ctypes.c_void_p
		self.lib.json_epitaxy_get_layer_start.restype = ctypes.c_double
		self.lib.json_epitaxy_get_layer_stop.restype = ctypes.c_double
		self.lib.json_epitaxy_get_len.restype = ctypes.c_double
		self.lib.json_epitaxy_get_device_start.restype = ctypes.c_double
		self.lib.zip_get_file_modification_date.restype = ctypes.c_long

		#self.lib.json_epitaxy_project_doping.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.byref]
		#self.lib.paths_dump(ctypes.byref(self))

	def find_the_dll(self):
		if get_platform()=="linux":
			ex=".so"
		elif get_platform()=="wine":
			ex=".so"
		else:
			ex=".dll"
		paths=[]
		paths.append(os.getcwd())
		#chk cwd and in the oghma_* directories
		paths.append(os.path.join(os.getcwd(),"oghma_local"))
		paths.append(os.path.join(os.getcwd(),"oghma_gui"))
		paths.append(os.path.join(os.getcwd(),"oghma_core"))

		#check where the root directory for a normal install
		script_dir=os.path.dirname(os.path.realpath(__file__))
		script_dir_dot_dot=os.path.dirname(script_dir)
		script_dir_dot_dot_dot_dot=os.path.dirname(script_dir_dot_dot)
		paths.append(script_dir)
		paths.append(os.path.dirname(script_dir))

		paths.append(os.path.join(script_dir_dot_dot,"oghma_local"))
		paths.append(os.path.join(script_dir_dot_dot,"oghma_gui"))
		paths.append(os.path.join(script_dir_dot_dot,"oghma_core"))

		paths.append(os.path.join(script_dir_dot_dot_dot_dot,"oghma_local"))
		paths.append(os.path.join(script_dir_dot_dot_dot_dot,"oghma_gui"))
		paths.append(os.path.join(script_dir_dot_dot_dot_dot,"oghma_core"))

		paths.append(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir))))

		if get_platform()=="linux":
			paths.append("/usr/lib/oghma_core/")
			paths.append("/usr/lib/")
			paths.append("/usr/bin/")		#libs should not be in here but it is easy
		else:
			paths.append(os.path.join("C:\\Program Files","OghmaNano"))
			paths.append(os.path.join("D:\\Program Files","OghmaNano"))
			paths.append(os.path.join("C:\\Program Files (x86)","OghmaNano"))
			paths.append(os.path.join("D:\\Program Files (x86)","OghmaNano"))

		for path in paths:
			test_file=os.path.join(path,"liboghma_py.so")
			if os.path.isfile(test_file)==True:
				self.dll_path=test_file
				return True

			test_file=os.path.join(path,"liboghma_py.dll")
			if os.path.isfile(test_file)==True:
				self.dll_path=test_file
				return True

		return False

	def get_paths_as_debug_info(self):
		self.lib.paths_dump_to_text(ctypes.byref(self))
		text=bytes2str(ctypes.cast(self.text_dump, ctypes.c_char_p).value)
		text="<b>"+text.replace("\n","<br><b>")
		text=text.replace(":","</b>")
		return text

	def get_html_path(self):
		return bytes2str(ctypes.cast(self.html_path, ctypes.c_char_p).value)

	def get_inp_template_path(self):
		return bytes2str(ctypes.cast(self.inp_template_path, ctypes.c_char_p).value)

	def is_plugin(self,name):
		if os.path.isfile(os.path.join(bytes2str(ctypes.cast(self.plugins_path, ctypes.c_char_p).value),name+".dll"))==True:
			return True

		if os.path.isfile(os.path.join(bytes2str(ctypes.cast(self.plugins_path, ctypes.c_char_p).value),name+".so"))==True:
			return True

		return False

	def get_newton_cache_path(self):
		return bytes2str(ctypes.cast(self.newton_cache_path, ctypes.c_char_p).value)

	def get_bib_path(self):
		return bytes2str(ctypes.cast(self.bib_path, ctypes.c_char_p).value)

	def get_tmp_path(self):
		ret=bytes2str(ctypes.cast(self.tmp_path, ctypes.c_char_p).value)

		if os.path.isdir(ret)==False:
			os.makedirs(ret)

		return ret

	def get_tmp_path_fast(self):
		ret=bytes2str(ctypes.cast(self.tmp_path_fast, ctypes.c_char_p).value)

		if os.path.isdir(ret)==False:
			os.makedirs(ret)

		return ret

	def get_materials_path(self):
		return os.path.join(self.get_user_settings_dir(),"materials")

	def get_sim_path(self):
		return bytes2str(sim_paths.root_simulation_path)

	##############################################################
	#get_xxx_path(self): in self.get_user_settings_dir()

	def get_filters_path(self):
		return os.path.join(self.get_user_settings_dir(),"filters")

	def get_shape_path(self):
		return os.path.join(self.get_user_settings_dir(),"shape")

	def get_spectra_path(self):
		return os.path.join(self.get_user_settings_dir(),"spectra")

	def get_scripts_path(self):
		return os.path.join(self.get_user_settings_dir(),"scripts")

	def get_morphology_path(self):
		return os.path.join(self.get_user_settings_dir(),"morphology")

	##############################################################
	#get_base_xxx_path(self):

	def get_base_filters_path(self):
		return bytes2str(ctypes.cast(self.filters_base_path, ctypes.c_char_p).value)

	def get_base_morphology_path(self):
		return bytes2str(ctypes.cast(self.morphology_base_path, ctypes.c_char_p).value)

	def get_base_shape_path(self):
		return bytes2str(ctypes.cast(self.shape_base_path, ctypes.c_char_p).value)

	def get_base_scripts_path(self):
		return bytes2str(ctypes.cast(self.scripts_base_path, ctypes.c_char_p).value)

	def get_base_spectra_path(self):
		return bytes2str(ctypes.cast(self.spectra_base_path, ctypes.c_char_p).value)

	def get_base_material_path(self):
		return bytes2str(ctypes.cast(self.materials_base_path, ctypes.c_char_p).value)

	##############################################################
	def am_i_rod(self):
		path=os.path.join(self.get_home_path(),"oghma_rod")
		if os.path.isfile(path):
			return True
		return False

	def get_wine_home_dir(self):
		path=os.path.join(self.get_home_path(),".wine","drive_c","users",os.path.basename(self.get_home_path()))
		if os.path.isdir(path):
			return path
		return False

	def get_li_path(self):
		global li_path
		
		#If settings.json is in the exe path default to that
		test_path=os.path.join(os.path.dirname(bytes2str(ctypes.cast(self.exe_command, ctypes.c_char_p).value)),"settings.json")
		if os.path.isfile(test_path)==True:
			return test_path

		return li_path

	def get_backup_path(self):
		global sim_paths
		path=os.getcwd()
		if sim_paths.root_simulation_path!=None:
			path=bytes2str(sim_paths.root_simulation_path)

		backup_path=os.path.join(path,"backup")
		return backup_path

	def get_home_path(self):
		return bytes2str(ctypes.cast(self.user_home_dir, ctypes.c_char_p).value)

	def get_shape_template_path(self):
		return os.path.join(bytes2str(ctypes.cast(self.inp_template_path, ctypes.c_char_p).value),"shape")

	def get_exe_path(self):
		ret=os.path.dirname(bytes2str(ctypes.cast(self.exe_command, ctypes.c_char_p).value))
		return ret

	def get_dll_py(self):
		return self.lib

	def get_fonts_path(self):
		return bytes2str(ctypes.cast(self.fonts_path, ctypes.c_char_p).value)

	def get_user_settings_dir(self):
		ret=bytes2str(ctypes.cast(self.oghma_local, ctypes.c_char_p).value)
		if os.path.isdir(ret)==False:
			os.makedirs(ret)
		return ret

	def get_device_lib_path(self):
		return bytes2str(ctypes.cast(self.device_lib_path, ctypes.c_char_p).value)

	def get_plugins_path(self):
		return bytes2str(ctypes.cast(self.plugins_path, ctypes.c_char_p).value)

	def get_exe_command(self):
		return bytes2str(ctypes.cast(self.exe_command, ctypes.c_char_p).value)

	def get_exe_name(self):
		return os.path.basename(bytes2str(ctypes.cast(self.exe_command, ctypes.c_char_p).value))

	def get_components_path(self):
		return bytes2str(ctypes.cast(self.components_path, ctypes.c_char_p).value)

	def get_image_file_path(self):
		return bytes2str(ctypes.cast(self.image_path, ctypes.c_char_p).value)

	def get_css_path(self):
		return bytes2str(ctypes.cast(self.css_path, ctypes.c_char_p).value)

	def get_flag_file_path(self):
		return bytes2str(ctypes.cast(self.flag_path, ctypes.c_char_p).value)

	def get_lang_path(self):
		return bytes2str(ctypes.cast(self.lang_path, ctypes.c_char_p).value)

	def get_video_path(self):
		return bytes2str(ctypes.cast(self.video_path, ctypes.c_char_p).value)

	def get_atmosphere_path(self):
		return bytes2str(ctypes.cast(self.atmosphere_path, ctypes.c_char_p).value)

	def get_cluster_path(self):
		return bytes2str(ctypes.cast(self.cluster_path, ctypes.c_char_p).value)

	def get_cluster_libs_path(self):
		return bytes2str(ctypes.cast(self.cluster_libs_path, ctypes.c_char_p).value)

	def get_src_path(self):
		return bytes2str(ctypes.cast(self.src_path, ctypes.c_char_p).value)

	def get_web_cache_path(self):
		ret=os.path.join(sim_paths.get_user_settings_dir(),"web_cache")

		if os.path.isdir(ret)==False:
			os.makedirs(ret)

		return ret

	def get_user_data_path(self):
		ret=os.path.join(sim_paths.get_user_settings_dir(),"user_data")
		if os.path.isdir(ret)==False:
			os.makedirs(ret)
		return ret

	def __del__(self):
		if self.lib!=None:
			self.lib.paths_free(ctypes.byref(self))

def subtract_paths(root,b_in):		#There is a functon in C that is untestedm, in a release or two replce this with the C function
	a=root.replace("/","\\")
	b=b_in.replace("/","\\")
	a=a.split("\\")
	b=b.split("\\")
	a_len=len(a)
	b_len=len(b)
	m=a_len
	if b_len<m:
		m=b_len
	pos=0

	for i in range(0,m):
		if a[i]!=b[i]:
			break
		pos=pos+1

	ret=[]
	for i in range(pos,b_len):
		ret.append(b[i])

	return "/".join(ret)

def to_native_path(path):
	ret=path
	if get_platform()=="win":
		ret=ret.replace("/","\\")
		ret=ret.lower()
	return ret

def remove_cwdfrompath(path):
	tmp=path
	if tmp.startswith(os.getcwd()):
		tmp=tmp[len(os.getcwd())+1:]
	return tmp

def remove_simpathfrompath(path):
	tmp=path
	if tmp.startswith(sim_paths.get_sim_path()):
		tmp=tmp[len(sim_paths.get_sim_path())+1:]
	return tmp

def test_arg_for_sim_file():
	if len(sys.argv)>1:
		f=os.path.realpath(sys.argv[1])
		if os.path.isfile(f)==True and f.endswith("sim"+sim_name.file_ext):
			return os.path.dirname(f)
		elif os.path.isdir(f)==True and os.path.isfile(os.path.join(f,"sim"+sim_name.file_ext))==True:
			return f
	return False

def calculate_paths():
	global li_path
	global sim_paths
	sim_paths=c_paths()

	#A bit of sticking plaster
	if ctypes.cast(sim_paths.li_path, ctypes.c_char_p).value==None:
		li_path=None
	else:
		li_path=bytes2str(ctypes.cast(sim_paths.li_path, ctypes.c_char_p).value)

	set_oghma_core_path(bytes2str(ctypes.cast(sim_paths.exe_command, ctypes.c_char_p).value))

def get_sim_paths():
	global sim_paths
	return sim_paths

def set_sim_path(path):
	global sim_paths
	sim_paths.root_simulation_path=bytes(path, encoding='utf8') 

def multiplatform_exe_command(command,port=None):
	if get_platform()!="linux":
		if command.count(".exe")>0:
			if get_platform()=="wine":
				command="/bin/wine \""+command
			else:
				command="\""+command
			command=command.replace(".exe",".exe\"",1)

	if port!=None:
		command=command+" --port "+str(port)

	return command


