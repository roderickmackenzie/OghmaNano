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

## @package util
#  General helper functions.
#



import os
import shutil
import sys
from cal_path import sim_paths
from win_lin import get_platform

def can_i_delete(file_name):
	if os.path.samefile(str(sim_paths.get_home_path()),str(file_name))==True:
		return False
	elif file_name.startswith(sim_paths.get_sim_path()):
		return True
	elif file_name.startswith(sim_paths.get_shape_path()):
		return True
	elif file_name.startswith(sim_paths.get_materials_path()):
		return True
	elif file_name.startswith(sim_paths.get_filters_path()):
		return True
	elif file_name.startswith(sim_paths.get_spectra_path()):
		return True
	elif file_name.startswith(sim_paths.get_backup_path()):
		return True
	return False

def safe_delete(path,allow_dir_removal=False):
	#Paranoia
	if can_i_delete(path)==False:
		return

	#Paranoia
	if os.path.samefile(str(sim_paths.get_home_path()),str(path))==True:
		sys.exit('I can not delete this dir')
		return

	#Paranoia
	if os.path.samefile(str(os.getcwd()),str(path))==True:
		sys.exit('I can not delete this dir2')
		return

	if os.path.isdir(path)==True:
		if allow_dir_removal==False:
			print("I am not allwed to delete:", path)
			return
		try:
			shutil.rmtree(path)
		except IOError:
			print("Could not delete the dir:", path)

	elif os.path.isfile(path)==True:
		print("Delete",path)
		try:
			os.remove(path)
		except IOError:
			print("Could not delete the file:", path)
	else:
		print("This should not be run")


