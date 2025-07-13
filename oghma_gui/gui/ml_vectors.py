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

## @package scan_ml
#  ML framework.
#

import os

from safe_delete import safe_delete

from math import log10

import i18n
_ = i18n.language.gettext

from server import server_break
from util_zip import zip_lsdir
from util_zip import extract_dir_from_archive

import zipfile
import string
from dat_file import dat_file
from cal_path import sim_paths
import ctypes
from json_c import json_c
from bytes2str import str2bytes
import random
from json_c import json_tree_c

class ml_vectors(ctypes.Structure):
	_fields_ = [('j', json_c),
				('base_sim_path', ctypes.c_char * 4096),
				('search_path', ctypes.c_char * 4096),
				('ml_tab_name', ctypes.c_char * 4096),
				('output_file', ctypes.c_char * 4096),
				('errors_file', ctypes.c_char * 4096),
				('stats_file', ctypes.c_char * 4096),
				('json_obj_ml_sims', ctypes.c_void_p),
				('json_obj_ml_random', ctypes.c_void_p),
				('json_obj_config', ctypes.c_void_p),
				('ml_sims_n', ctypes.c_int),
				('ml_random_n', ctypes.c_int),
				('done', ctypes.c_int),
				('total', ctypes.c_int),
				('finished_building', ctypes.c_int),
				('errors', ctypes.c_int)]

	def __init__(self):
		self.bin=json_tree_c()
		self.lib=sim_paths.get_dll_py()
		self.lib.ml_vectors_init(ctypes.byref(self))

	def make_tmp_dir(self):
		rnd = [random.choice(string.ascii_letters + string.digits) for n in range(0,32)]
		rnd = "".join(rnd)
		tmp_dir=os.path.join(sim_paths.get_tmp_path_fast(),"oghma_"+rnd)
		if os.path.isdir(tmp_dir)==True:
			safe_delete(tmp_dir,allow_dir_removal=True)

		os.mkdir(tmp_dir)

		return tmp_dir

	def build_vector(self,scan_dir,json_path):
		output_file=self.bin.get_token_value(json_path+".ml_config","ml_vector_file_name")
		name=self.bin.get_token_value(json_path,"name")

		archives=[]
		for archive_name in os.listdir(scan_dir):
			if archive_name.startswith("archive")==True and archive_name.endswith(".zip")==True:
				archives.append(archive_name)

		main_tmp_dir=self.make_tmp_dir()
		sim_dir=ctypes.c_char_p(str2bytes(sim_paths.get_sim_path()))
		
		self.lib.ml_vectors_load(ctypes.byref(self),sim_dir,ctypes.c_char_p(str2bytes(main_tmp_dir)),ctypes.c_char_p(str2bytes(scan_dir)), ctypes.c_char_p(str2bytes(name) ))
		self.lib.ml_vectors_write_header_to_output_file(ctypes.byref(self))
		
		for archive_name in archives:

			if archive_name.startswith("archive")==True and archive_name.endswith(".zip")==True:

				archive_path=os.path.join(scan_dir,archive_name)

				zf = zipfile.ZipFile(archive_path, 'r')
				simulations=zip_lsdir(archive_path,zf=zf,sub_dir="/")
				self.total=len(simulations)*len(archives)

				for simulation in simulations:

					tmp_dir=os.path.join(main_tmp_dir,simulation)

					extract_dir_from_archive(tmp_dir,"",simulation,zf=zf)

				self.lib.ml_vectors_gen(ctypes.byref(self))

				for simulation in simulations:
					tmp_dir=os.path.join(main_tmp_dir,simulation)
					safe_delete(tmp_dir,allow_dir_removal=True)
					print("del:",tmp_dir,main_tmp_dir)

		self.lib.ml_vectors_write_tail_to_output_file(ctypes.byref(self))

		print("del:",main_tmp_dir)
		safe_delete(main_tmp_dir,allow_dir_removal=True)

		os.chdir(sim_paths.get_sim_path())
		self.lib.ml_vectors_free(ctypes.byref(self))
		self.finished_building=True;
