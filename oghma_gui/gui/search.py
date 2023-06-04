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

## @package search
#  General search functions.
#

import os, fnmatch
import glob

def find_sims(search_path):
	sims=[]
	for root, dirs, files in os.walk(search_path):
		for name in files:
			full_name=os.path.join(root, name)
			if full_name.endswith("sim.oghma") or full_name.endswith("sim.json"):
				if os.path.dirname(os.path.dirname(full_name)).endswith("sim")==0:		
					sims.append(os.path.dirname(full_name))
	return sims

def search_simulations(path):
	ret=[]
	for root, dirs, files in os.walk(path):
		for name in files:
			if name=="sim.oghma":
				ret.append(os.path.dirname(os.path.join(root, name)))
	return ret

def find_fit_log(out_file,path):
	pattern='fitlog_time_error.dat'
	fitlog = []
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				fitlog.append(os.path.join(root, name))

	pattern='fitlog_time_speed.dat'
	fitlog_time_speed = []
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				fitlog_time_speed.append(os.path.join(root, name))

	string="plot "
	for my_file in fitlog:
		 string=string+"'"+my_file+"' using ($1):($2) with lp,"

	#for my_file in fitlog_time_speed:
		# string=string+"'"+my_file+"' using ($2) axis x1y2 with lp,"

	string = string[:-1]
	text_file = open(out_file, "w")
	text_file.write(string)
	text_file.close()


def return_file_list(result,start_dir,file_name):
	#print(start_dir, file_name)
	pattern=file_name
	path=start_dir
	for root, dirs, files in os.walk(path, followlinks=True):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				result.append(os.path.join(root, name))

	for i in range(0, len(result)):
		result[i]=result[i].rstrip()




def find_shapshots(path):
	out=[]
	for root, dirs, files in os.walk(path):
		for name in files:
			if name.endswith("json.dat")==True:
				sub_snapshot_dir=os.path.dirname(os.path.join(root, name))
				snapshot_dir=os.path.dirname(sub_snapshot_dir)
				if os.path.basename(snapshot_dir)=="snapshots":
					if snapshot_dir not in out:
						out.append(snapshot_dir)

	print(out)
	return out
