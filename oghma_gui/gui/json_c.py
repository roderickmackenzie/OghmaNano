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

import os
import ctypes
from cal_path import sim_paths
from bytes2str import str2bytes,bytes2str
from str2bool import str2bool
from util import is_number
import json
import re

JSON_INT=0x00
JSON_BOOL=0x01
JSON_DOUBLE=0x02
JSON_STRING=0x03
JSON_NODE=0x04
JSON_TEMPLATE=0x05
JSON_RANDOM_ID=0x06
JSON_STRING_HEX=0x07
JSON_DAT_FILE=0x08

def convert_string(value,data_type):
	def clean_numeric_value(val):
		ret=re.sub(r'[^\d\.\-eE]', '', val)
		if ret=="":
			ret=0.0
		return ret
	json_type = data_type
	if json_type == JSON_INT:
		return int(float(value))
	elif json_type == JSON_BOOL:
		return str2bool(value)
	elif json_type == JSON_DOUBLE:
		try:
			return float(value)
		except:
			return float(clean_numeric_value(value))
	elif json_type == JSON_STRING:
		return str(value)
	else:
		return str(value)

class json_string(ctypes.Structure):
	_fields_ = [('data', ctypes.c_void_p),
				('len', ctypes.c_int),
				('pos', ctypes.c_int),
				('compact', ctypes.c_int)]

	def __init__(self):
		self.lib=sim_paths.get_dll_py()
		self.lib.json_string_init(ctypes.byref(self))

	def free(self):
		self.lib.json_string_free(ctypes.byref(self))

	def get_data(self):
		return bytes2str(ctypes.cast(self.data, ctypes.c_char_p).value)

class json_obj_c(ctypes.Structure):
	_fields_ = [('name', ctypes.c_char * 40),
				('len', ctypes.c_int),
				('max_len', ctypes.c_int),
				('objs', ctypes.c_void_p),
				('data', ctypes.c_char_p),
				('data_len', ctypes.c_int),
				('data_type', ctypes.c_char),
				('data_flags', ctypes.c_ubyte),
				('json_template', ctypes.c_void_p)]

class json_c(ctypes.Structure):
	_fields_ = [('raw_data', ctypes.c_char_p),
				('raw_data_len', ctypes.c_long),
				('pos', ctypes.c_long),
				('level', ctypes.c_int),
				('path', ctypes.c_char * 4096),
				('obj', json_obj_c),
				('compact', ctypes.c_int),
				('file_path', ctypes.c_char * 4096),
				('is_template', ctypes.c_int),
				('bib_template', json_obj_c),
				('triangles_loaded', ctypes.c_int),
				('bib_file', ctypes.c_int),
				('yml_file', ctypes.c_int)]

	def __init__(self,template_type):
		self.template_type=template_type
		self.lib=sim_paths.get_dll_py()
		self.lib.json_obj_find_by_path.restype = ctypes.POINTER(json_obj_c)
		self.lib.json_init(ctypes.byref(self))
		self.init_rand()
		self.last_time=-1
		self.call_backs=[]
		self.loaded=False

	def __del__(self):
		self.free()

	def free(self):
		self.lib.json_free(ctypes.byref(self))

	def json_obj_find_by_path(self,json_path):
		obj=self.lib.json_obj_find_by_path(ctypes.byref(self.obj),ctypes.c_char_p(str2bytes(json_path)))
		return obj

	def build_template(self):
		if self.template_type=="oghma_save_file":
			self.lib.json_build_template_from_file(ctypes.byref(self))
		elif self.template_type=="oghma_local":
			self.lib.json_local(ctypes.byref(self))
		elif self.template_type=="json_data_view_gui_configs":
			self.lib.json_data_view_gui_configs(ctypes.byref(self))
		elif self.template_type=="material_db":
			self.lib.json_db_materials(ctypes.byref(self))
		elif self.template_type=="spectra_db":
			self.lib.json_db_spectra(ctypes.byref(self))
		elif self.template_type=="filter_db":
			self.lib.json_db_filter(ctypes.byref(self))
		elif self.template_type=="shape_db":
			self.lib.json_db_shape(ctypes.byref(self))
		elif self.template_type=="morphology_db":
			self.lib.json_db_morphology(ctypes.byref(self))
		elif self.template_type=="folder_material":
			self.lib.json_folder_material(ctypes.byref(self))
		elif self.template_type=="folder_backup":
			self.lib.json_folder_backup(ctypes.byref(self))
		elif self.template_type=="folder_backup_main":
			self.lib.json_folder_backup_main(ctypes.byref(self))
		elif self.template_type=="folder_multi_plot_dir":
			self.lib.json_folder_multi_plot_dir(ctypes.byref(self))
		elif self.template_type=="snapshots":
			self.lib.json_folder_snapshots(ctypes.byref(self))
		elif self.template_type=="file_defined":
			pass

	def load(self,file_name):
		self.build_template()
		ret=self.lib.json_load(None,ctypes.byref(self),ctypes.c_char_p(str2bytes(file_name)))
		if ret==0:
			self.loaded=True
			self.last_time=self.file_time()
			return True

		return False

		

	def reload(self):
		self.load(self.file_path)

	def save(self):
		ret=self.lib.json_save(ctypes.byref(self))
		self.last_time=self.file_time()
		return ret

	def save_as(self,file_name):
		self.file_path=str2bytes(file_name)
		self.save()

	def dump(self):
		#print("dump")
		self.lib.json_dump_all(ctypes.byref(self))

	def gen_json(self,path):
		#print("from_path")
		a=json_string()
		self.lib.json_dump_obj_string_from_path(ctypes.byref(a),ctypes.byref(self), ctypes.c_char_p(str2bytes(path)))
		ret=a.get_data()
		a.free()
		return ret.split("\n")

	def get_tokens_from_path(self,path):
		a=json_string()
		ret_code=self.lib.json_dump_tokens_from_path(ctypes.byref(a),ctypes.byref(self), ctypes.c_char_p(str2bytes(path)))
		ret=a.get_data()
		a.free()
		if ret_code!=0:
			return None
		return ret.split("\n")

	def get_token_value(self,path,token):
		a=json_string()
		ret_type = ctypes.c_int()
		if token.count(".")>0:
			mini_path,token=token.rsplit(".",1)
			path=path+"."+mini_path
		status=self.lib.json_get_token_value_from_path(ctypes.byref(a),ctypes.pointer(ret_type), ctypes.byref(self), ctypes.c_char_p(str2bytes(path)), ctypes.c_char_p(str2bytes(token)))
		ret=a.get_data()
		a.free()
		if status==-1:
			return None

		return convert_string(ret,ret_type.value)

	def set_token_value(self,path,token,value):
		#print("here")
		value=str(value)
		self.lib.json_set_token_value_using_path(ctypes.byref(self), ctypes.c_char_p(str2bytes(path)), ctypes.c_char_p(str2bytes(token)), ctypes.c_char_p(str2bytes(value)))

	def get_all_sim_modes(self):
		a=json_string()
		ret=self.lib.json_get_all_sim_modes(ctypes.byref(a),ctypes.byref(self))
		if ret==-1:
			return None
		ret=a.get_data()
		a.free()
		ret=ret.split("*")
		return ret

	def is_token(self,path,token):
		ret=self.lib.json_is_token_from_path(ctypes.byref(self), ctypes.c_char_p(str2bytes(path)), ctypes.c_char_p(str2bytes(token)))
		if ret==0:
			return True
		return False

	def json_delete_token_using_path(self,path,token):
		ret=self.lib.json_delete_token_using_path(ctypes.byref(self), ctypes.c_char_p(str2bytes(path)), ctypes.c_char_p(str2bytes(token)))
		if ret==0:
			return True
		return False

	def add_bib_item(self,path,token):
		self.lib.json_add_bib_item_at_path(ctypes.byref(self), ctypes.c_char_p(str2bytes(path)), ctypes.c_char_p(str2bytes(token)))

	def find_path_by_uid(self,path,uid):
		data = ctypes.create_string_buffer(4000)
		data.value = path.encode('utf-8')
		ret=self.lib.json_search_for_token_value_in_path(data, ctypes.byref(self), ctypes.c_char_p(str2bytes("id")), ctypes.c_char_p(str2bytes(uid)))
		if ret!=0:
			return None
		return data.value.decode('utf-8')

	def bib_cite(self,token):
		a=json_string()
		self.lib.json_py_bib_short_cite(ctypes.byref(a),ctypes.byref(self), ctypes.c_char_p(str2bytes(token)))
		ret=a.get_data()
		a.free()
		return ret

	def json_py_bib_enforce_citation(self,token):
		ret=self.lib.json_py_bib_enforce_citation(ctypes.byref(self), ctypes.c_char_p(str2bytes(token)))
		return ret

	def import_json_to_obj(self,path,json_text):
		return self.lib.json_py_import_json_to_obj(ctypes.byref(self),ctypes.c_char_p(str2bytes(path)), ctypes.c_char_p(str2bytes(json_text)));

	def init_rand(self):
		return self.lib.json_py_init_rand()

	def dump_as_latex(self,path,token_lib):
		a=json_string()
		ret=self.lib.json_py_to_latex(ctypes.byref(a),ctypes.byref(self), ctypes.c_char_p(str2bytes(path)),ctypes.byref(token_lib))
		if ret==-1:
			return None
		ret=a.get_data()
		a.free()
		return ret

	def is_node(self,path):
		if self.lib.json_py_isnode(ctypes.byref(self), ctypes.c_char_p(str2bytes(path)))==0:
			return True
		return False

	def ml_make_nets_json(self,uid):
		new_file_path = ctypes.create_string_buffer(4000)
		ret=self.lib.ml_make_nets_json(new_file_path,ctypes.c_char_p(str2bytes(sim_paths.get_sim_path())), ctypes.byref(self), ctypes.c_char_p(str2bytes(uid)))
		if ret!=0:
			return None

		return new_file_path.value.decode('utf-8')

	def import_old_oghma_file(self,file_name):
		edited=self.lib.json_import_old_oghma_file(ctypes.byref(self), ctypes.c_char_p(str2bytes(file_name)))
		return edited

	def oghma_file_fixup(self):
		self.lib.json_compat_fixup(ctypes.byref(self))

	#segments

	def clear_segments(self,json_path):
		return self.lib.json_py_clear_segments(ctypes.byref(self),ctypes.c_char_p(str2bytes(json_path)))

	def make_new_segment(self,path,human_name,pos):
		data = ctypes.create_string_buffer(4000)
		data.value = path.encode('utf-8')
		self.lib.json_py_add_segment(data, ctypes.c_char_p(str2bytes(path)), ctypes.byref(self), ctypes.c_char_p(str2bytes(human_name)),ctypes.c_int(pos))
		return data.value.decode('utf-8')

	def delete_segment(self,path,segment_name):
		ret=self.lib.json_delete_segment_by_path(ctypes.byref(self), ctypes.c_char_p(str2bytes(path)),  ctypes.c_char_p(str2bytes(segment_name)))
		return ret

	def clone_segment(self,root_path,src_segment,new_segment_name):
		new_segment_path = ctypes.create_string_buffer(4000)
		ret=self.lib.json_clone_segment(new_segment_path, ctypes.c_char_p(str2bytes(root_path)), ctypes.c_char_p(str2bytes(src_segment)), ctypes.byref(self),ctypes.c_char_p(str2bytes(new_segment_name)))
		return new_segment_path.value.decode('utf-8')

	def segments_swap(self,path,i0,i1):
		return self.lib.json_py_segments_swap(ctypes.byref(self), ctypes.c_char_p(str2bytes(path)),ctypes.c_int(i0), ctypes.c_int(i1))

	def segments_move_up_down(self,path,direction,row):
		rows=self.get_token_value(path,"segments")
		a=row
		if direction=="up":
			b=a-1
			if b<0:
				return None, None
		else:
			b=a+1
			if b>rows-1:
				return None, None

		self.segments_swap(path,a,b)
		return a,b

	def clipboard_copy(self,path,paste_object_type,row_numbers=[]):
		from PySide2.QtWidgets import QApplication
		a=json_string()
		c_array=None
		if row_numbers!=[]:
			array_type = ctypes.c_int * len(row_numbers)
			c_array = array_type(*row_numbers)

		ret=self.lib.json_copy_to_clipboard(ctypes.byref(self), ctypes.byref(a), ctypes.c_char_p(str2bytes(path)), ctypes.c_char_p(str2bytes(paste_object_type)), c_array, ctypes.c_int(len(row_numbers)))
		if ret==-1:
			return None
		ret=a.get_data()
		a.free()

		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(ret, mode=cb.Clipboard)

	def paste_append_segments_from_clipboard(self,root_path,paste_object_type, row, text):
		root_path=ctypes.c_char_p(str2bytes(root_path))
		paste_object_type=ctypes.c_char_p(str2bytes(paste_object_type))
		row=ctypes.c_int(row)
		text_send=ctypes.c_char_p(str2bytes(text))
		text_len=ctypes.c_int(len(text))
		ret=self.lib.json_clip_segments_append_at_path( ctypes.byref(self), root_path, paste_object_type , row, text_send, text_len)
		return ret

	#groups
	def groups_get_all_linked_uids(self,uid):
		a=json_string()
		self.lib.json_groups_get_all_linked_uids(ctypes.byref(a), ctypes.byref(self), ctypes.c_char_p(str2bytes(uid)))
		ret=a.get_data()
		a.free()
		ret=ret.split("\n")
		return ret

	def json_world_size(self,my_min,my_max):
		self.lib.json_world_size(ctypes.byref(self), ctypes.byref(my_min), ctypes.byref(my_max))


	def project_epi_value_to_mesh(self,x,y,sub_path,token0,token1):
		print("remove me")
		array_type_x = ctypes.c_double * len(x)
		array_type_y = ctypes.c_double * len(y)

		x_c = array_type_x(*x)
		y_c = array_type_y(*y)

		self.lib.json_epitaxy_project_values_to_mesh(
			ctypes.cast(x_c, ctypes.POINTER(ctypes.c_double)),
			ctypes.cast(y_c, ctypes.POINTER(ctypes.c_double)),
			ctypes.c_int(len(x)), ctypes.c_char_p(str2bytes(token0)), ctypes.c_char_p(str2bytes(token1)),
			ctypes.c_char_p(str2bytes(sub_path)),
			ctypes.byref(json_tree_c())
		)

		x = list(x_c)
		y = list(y_c)

		return x,y

	def file_time(self):
		ret=-1
		if self.loaded==True:
			ret=self.lib.zip_get_file_modification_date(ctypes.c_char_p(self.file_path))
		return ret

	def check_reload(self):
		if self.last_time!=-1:
			if self.loaded==True:
				#print("check",self.last_time,self.f.time())
				if self.last_time!=self.file_time():
					self.reload()
					for f in self.call_backs:
						try:
							f()
						except:
							pass

	def add_call_back(self,function):
		if function not in self.call_backs:
			self.call_backs.append(function)

	def remove_call_back(self,function):
		if function in self.call_backs:
			self.call_backs.remove(function)

	def human_path_to_json(self,token_lib,human_path):
		json_path = ctypes.create_string_buffer(4000)
		self.lib.json_human_path_to_json(ctypes.byref(self), ctypes.byref(token_lib), json_path, ctypes.c_char_p(str2bytes(human_path)))
		return json_path.value.decode('utf-8')

	def json_path_to_human_path(self,token_lib,json_path):
		human_path = ctypes.create_string_buffer(4000)
		self.lib.json_path_to_human_path(ctypes.byref(self), ctypes.byref(token_lib), human_path, ctypes.c_char_p(str2bytes(json_path)))
		return human_path.value.decode('utf-8')
	
	def json_py_add_obj_double(self,json_path, token, value):
		self.lib.json_py_add_obj_double(ctypes.byref(self), ctypes.c_char_p(str2bytes(json_path)),ctypes.c_char_p(str2bytes(token)), ctypes.c_double(value))

	def json_py_add_obj_int(self,json_path, token, value):
		self.lib.json_py_add_obj_int(ctypes.byref(self), ctypes.c_char_p(str2bytes(json_path)),ctypes.c_char_p(str2bytes(token)), ctypes.c_int(value))

	def json_py_add_obj_bool(self,json_path, token, value):
		self.lib.json_py_add_obj_bool(ctypes.byref(self), ctypes.c_char_p(str2bytes(json_path)),ctypes.c_char_p(str2bytes(token)), ctypes.c_int(value))

	def json_py_add_obj_string(self,json_path, token, value):
		self.lib.json_py_add_obj_string(ctypes.byref(self), ctypes.c_char_p(str2bytes(json_path)),ctypes.c_char_p(str2bytes(token)), ctypes.c_char_p(str2bytes(value)))

	def format_float(self,number):
		out = ctypes.create_string_buffer(200)
		self.lib.format_float(out,ctypes.c_double(number))
		return out.value.decode('utf-8')

json_bin=json_c("oghma_save_file")

def json_tree_c():
	global json_bin
	return json_bin

json_bin_local=json_c("oghma_local")
json_bin_local.load(os.path.join(sim_paths.get_user_settings_dir(),"data.json"))

def json_local_root():
	global json_bin_local
	return json_bin_local

json_files_gui_config=json_c("json_data_view_gui_configs")

def json_files_gui_config_load(file_path):
	global json_files_gui_config
	json_files_gui_config.lib.json_free(ctypes.byref(json_files_gui_config))
	json_files_gui_config.load(file_path)
	json_files_gui_config.lib.json_data_view_gui_3d_fixup(ctypes.byref(json_files_gui_config))
	json_files_gui_config.save()

