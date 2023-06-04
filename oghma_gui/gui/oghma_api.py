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

## @package oghma_api
#  An api used to run gpvdm
#

#import sys
import os
from shutil import copyfile
from cal_path import calculate_paths
from cal_path import calculate_paths_init
from cal_path import set_sim_path

from server import server_base
from server import server_get
from cal_path import sim_paths
from progress_class import progress_class
from spctral2 import spctral2
from inp import inp

#scan
from scan_io import scan_io
from scans_io import scans_io

from cal_path import get_exe_command
from scan_tree import tree_load_flat_list
from gui_enable import set_gui
from ml_vectors import ml_vectors
from scan_io import scan_archive
from multiplot import multiplot
from multiplot_from_tokens import multiplot_from_tokens
from PIL import Image, ImageFilter,ImageOps
from epitaxy import get_epi
import codecs
from json_root import json_root
from math import log10
from scan_tree import random_log
import random
from clone import clone_sim_dir
from clean_sim import clean_sim_dir

class api_scan():

	def __init__(self,server):
		calculate_paths_init()
		calculate_paths()
		self.server=server

	def build(self,scan_dir_path,base_dir,interactive=True):
		scans=scans_io(base_dir)
		config_file=scans.find_path_by_name(os.path.basename(scan_dir_path))
		#print(config_file)
		s=scan_io()
		s.interactive=interactive
		s.load(config_file)
		s.set_path(scan_dir_path)
		s.set_base_dir(base_dir)
		s.build_scan()

	def add_jobs(self,scan_dir_path):
		get_exe_command()
		scans=scans_io(os.getcwd())
		scan_config_file=scans.find_path_by_name(os.path.basename(scan_dir_path))
		s=scan_io()
		s.load(scan_config_file)

		s.program_list

		watch_dir=os.path.join(os.getcwd(),scan_dir_path)

		commands=[]
		commands=tree_load_flat_list(scan_dir_path)
		print(commands)
		
		
		self.server.server_base_init(watch_dir)

		for i in range(0, len(commands)):
			self.server.add_job(commands[i],"")
			print("Adding job"+commands[i])

		#simple_run(exe_command)

	def build_ml_vectors(self,path):
		set_gui(False)
		scan=ml_vectors()
		scan.build_vector(path)

	def archive(self,path):
		scan_archive(path)

class oghma_api():
	def __init__(self,verbose=True):
		self.save_dir=os.getcwd()
		self.server=server_base()
		if verbose==True:
			self.server.pipe_to_null=False
		else:
			self.server.pipe_to_null=True

		#self.server.server_base_init(sim_paths.get_sim_path())
		if server_get()!=False:
			self.server=server_get()
			self.server.clear_cache()

		self.scan=api_scan(self.server)
		#image ops
		self.Image=Image
		self.ImageFilter=ImageFilter
		self.ImageOps=ImageOps
		self.path=""
		self.callback=None

	def run(self,callback=None):
		if callback!=None:
			self.server.server_base_set_callback(callback)
		self.server.start()

	def add_job(self,path="",args=""):
		if path=="":
			path=sim_paths.get_sim_path()
		else:
			path=os.path.join(sim_paths.get_sim_path(),path)
		print("add path>",path)
		self.server.add_job(path,args)

	def random_file_name(self):
		return codecs.encode(os.urandom(int(16 / 2)), 'hex').decode()

	def random_log(self,min,max):
		return float(random_log(min,max))

	def random(self,min,max):
		return random.uniform(min, max)

	def set_sim_path(self,path):
		set_sim_path(path)


	def set_save_dir(self,path):
		if os.path.isdir(path)==False:
			os.makedirs(path)

		self.save_dir=path


	def save(self,dest,src):
		copyfile(src, os.path.join(self.save_dir,dest))

	def json_load(self,file_name):
		a=json_root()
		a.load(file_name)
		return a

	def mkdir(self,file_name):
		if os.path.isdir(file_name)==False:
			os.makedirs(file_name)

	def clone(self,output_dir,input_dir):
		clone_sim_dir(output_dir,input_dir)

	def build_multiplot(self,path,gnuplot=False,exp_data=""):
		a=multiplot(gnuplot=gnuplot,exp_data=exp_data)
		a.find_files(os.path.join(sim_paths.get_sim_path(),path))
		a.save()

	def clean_dir(self,path):
		clean_sim_dir(path)

	def graph_from_tokens(self,output_file,path,file0,token0,file1,token1):
		output_file=os.path.join(sim_paths.get_sim_path(),path,output_file)
		multiplot_from_tokens()

	def log_range(self,start,stop,steps):
		lout=[]
		l_start=log10(start)
		l_stop=log10(stop)
		dl=(l_stop-l_start)/steps
		pos=l_start
		for i in range(0,steps+1):
			lout.append(pow(10,pos))
			pos=pos+dl

		return lout

	def load_snapshots(self,path):
		dirs=[]
		for root, dirs, files in os.walk(path):
			for name in files:
				if name.endswith("json.dat")==True:
					dirs.append(os.path.dirname(os.path.join(root, name)))
					
		print(dirs)

	def range(self,start,stop,steps):
		lout=[]
		dl=(stop-start)/steps
		pos=start
		for i in range(0,steps+1):
			lout.append(pos)
			pos=pos+dl

		return lout

	def find_simulations(self,path):
		ret=[]
		for root, dirs, files in os.walk(path):
			for name in files:
				full_name=os.path.join(root, name)
				if full_name.endswith("sim.oghma"):		
					ret.append(os.path.dirname(full_name))
		return ret


	def get_sim_path(self):
		return sim_paths.get_sim_path()

