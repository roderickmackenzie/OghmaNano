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

## @package scan_tree
#  Logic to itterate though a scan tree.
#
import os
from cal_path import subtract_paths
import math
import random

def random_log(in_start,in_stop):
	start=math.log10(in_start)
	stop=math.log10(in_stop)

	r=random.uniform(start, stop)

	val=math.pow(10,r)

	ret="{:.8E}".format(val)
	return ret


def tree_load_flat_list(sim_dir):
	config=[]
	file_name=os.path.join(sim_dir,'flat_list.inp')

	if os.path.isfile(file_name)==False:
		return False

	f = open(file_name)
	lines = f.readlines()
	f.close()

	for i in range(0, len(lines)):
		lines[i]=lines[i].rstrip()

	number=int(lines[0])

	for i in range(1,number+1):
		lines[i]=os.path.join(sim_dir,lines[i])
		if os.path.isdir(lines[i]):
			config.append(lines[i])

	return config

def tree_save_flat_list(sim_dir,flat_list):
	config=[]
	file_name=os.path.join(sim_dir,'flat_list.inp')

	a = open(file_name, "w")
	a.write(str(len(flat_list))+"\n")
	for i in range(0,len(flat_list)):
		rel_dir=subtract_paths(sim_dir,flat_list[i])
		a.write(rel_dir+"\n")

	a.close()

	return config

def tree_gen_flat_list(dir_to_search,level=0):
	found_dirs=[]
	for root, dirs, files in os.walk(dir_to_search):
		for name in files:

			if name=="sim.oghma":
				full_name=os.path.join(root, name)
				f=subtract_paths(dir_to_search,full_name)
				f=os.path.dirname(f)
				if len(f.split("/"))>level:
					found_dirs.append(f)
	return found_dirs




