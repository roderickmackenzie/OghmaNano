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

## @package clone_materials
#  Clone a materials
#
#import sys
import os
#import glob
from shutil import copyfile
from cal_path import subtract_paths
from materials_io import find_db_items
from win_lin import get_platform
from process_events import process_events
from json_c import json_c

def clone_material(dest_material_dir,src_material_dir):
	if os.path.isdir(dest_material_dir)==False:
		try:
			os.makedirs(dest_material_dir)
		except:
			return False

	files=os.listdir(src_material_dir)
	all_files=["alpha.csv","n.csv","emission.csv"]
	all_files.append("spectra.csv")
	all_files.append("shape.inp")
	all_files.append("filter.csv")
	all_files.append("shape_import.inp")
	all_files.append("data.json")
	all_files.append("image.png")
	all_files.append("image_original.png")


	for i in range(0,len(files)):
		if files[i] in all_files:
			src_mat_file=os.path.join(src_material_dir,files[i])
			if os.path.isfile(src_mat_file)==True:
				copyfile(src_mat_file,os.path.join(dest_material_dir,files[i]))
	return True

def clone_materials(dest,src_dir,file_type,just_count=False,total=0,progress_window=None,all_files=100,sim_link=False):
	db_folder=json_c("folder_material")
	db_folder.build_template()
	

	cur_ver=db_folder.get_token_value("","ver")
	do_copy=False
	
	if db_folder.load(os.path.join(dest,"data.json"))==False:
		do_copy=True

	if db_folder.get_token_value("","ver")!=cur_ver:
		do_copy=True
	
	if do_copy==False:
		return 0

	if sim_link==False:
		if just_count==False:
			if os.path.isdir(dest)==False:
				os.makedirs(dest)
			db_folder.save_as(os.path.join(dest,"data.json"))

		files=find_db_items(mat_path=src_dir,file_type=file_type)
		for i in range(0,len(files)):

			if just_count==False:
				src_file=os.path.join(src_dir,files[i])
				dest_file=os.path.join(dest,files[i])
				clone_material(dest_file,src_file)


				if progress_window!=None:
					progress_window.set_fraction(float(total)/float(all_files))
					progress_window.set_text(files[i])
					
					process_events()

			total=total+1
	print(dest,do_copy,sim_link,just_count)
	if sim_link==True:
		if os.path.isdir(dest)==False:
			if just_count==False:
				os.symlink(src_dir, dest)
			total=total+1

	return total
