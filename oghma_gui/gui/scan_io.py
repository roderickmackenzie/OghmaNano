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

## @package scan_io
#  IO functions for the scanning simulation parameters.
#


import sys
import os
import shutil
import gc

from inp import inp_get_token_value

from scan_tree import tree_load_flat_list
from scan_tree import tree_gen_flat_list
from scan_tree import tree_save_flat_list


from server import server_break

from error_dlg import error_dlg
from process_events import process_events
from safe_delete import safe_delete

import i18n
_ = i18n.language.gettext


import zipfile
from util_zip import archive_add_dir
from inp import inp
from json_scan import json_scan_line
from clean_sim import ask_to_delete
from progress_class import progress_class
from decode_inode import decode_inode
import ctypes
from cal_path import sim_paths


def scan_next_archive(sim_dir):
	i=0
	while(1):
		name="archive"+str(i)+".zip"
		full_name=os.path.join(sim_dir,name)
		if os.path.isfile(full_name)==False:
			return name
		i=i+1

def scan_archive(sim_dir,progress_window=None):
	own_progress_window=False
	if progress_window==None:
		progress_window=progress_class()
		progress_window.show()
		progress_window.start()
		own_progress_window=True

	archive_path=os.path.join(sim_dir,"build_archive.zip")
	if os.path.isfile(archive_path)==True:
		os.remove(archive_path)
	zf = zipfile.ZipFile(archive_path, 'a',zipfile.ZIP_DEFLATED)

	l=os.listdir(sim_dir)
	for i in range(0,len(l)):
		dir_to_zip=os.path.join(sim_dir,l[i])
		if os.path.isdir(dir_to_zip)==True:
			archive_add_dir(archive_path,dir_to_zip,sim_dir,zf=zf,remove_src_dir=True,exclude=["gmon.out"])

		progress_window.set_fraction(float(i)/float(len(l)))
		progress_window.set_text(_("Adding: ")+l[i])

		#if server_break()==True:
		#	break
		process_events()
		
	zf.close()

	os.rename(archive_path, os.path.join(sim_dir,scan_next_archive(sim_dir)))

	if own_progress_window==True:
		progress_window.stop()



def scan_list_simulations(dir_to_search):
	found_dirs=[]
	for root, dirs, files in os.walk(dir_to_search):
		for name in files:
#			full_name=os.path.join(root, name)
			if name=="sim.oghma":
				found_dirs.append(root)
	return found_dirs

def scan_plot_fits(dir_to_search):
	files=os.listdir(dir_to_search)
	for i in range(0,len(files)):
		if files[i].endswith(".jpg"):
			safe_delete(os.path.join(dir_to_search,files[i]))
			#print("remove",os.path.join(dir_to_search,files[i]))

	sim_dirs=tree_load_flat_list(dir_to_search)
	
	for i in range(0,len(sim_dirs)):
		os.chdir(sim_dirs[i])
		name=sim_dirs[i].replace("/","_")
		
		os.system("gnuplot fit.plot >plot.eps")
		os.system("gs -dNOPAUSE -r600 -dEPSCrop -sDEVICE=jpeg -sOutputFile="+os.path.join(dir_to_search,name+".jpg")+" plot.eps -c quit")
	os.chdir(dir_to_search)

def scan_get_converged_status(fit_log_path):
	error=False

	if os.path.isfile(fit_log_path):
		f = open(fit_log_path, "r")
		lines = f.readlines()
		f.close()

		for l in range(0, len(lines)):
			lines[l]=lines[l].rstrip()

		if len(lines)>4:
			error=float(lines[len(lines)-2].split()[1])
	
	return error

def scan_list_unconverged_simulations(dir_to_search):
	found_dirs=[]
	sim_dirs=tree_load_flat_list(dir_to_search)
	
	for i in range(0,len(sim_dirs)):
		add=False
		fit_log=os.path.join(sim_dirs[i],'fitlog.dat')

		error=scan_get_converged_status(fit_log)

		if error==False:
			add=True
		elif error>0.1:
			add=True

		if add==True:
			found_dirs.append(sim_dirs[i])

	return found_dirs



class report_token():
	def __init__(self,file_name,token):
		self.file_name=file_name
		self.token=token
		self.values=[]

def scan_push_to_hpc(base_dir,only_unconverged):
	config_file=os.path.join(os.getcwd(),"server.inp")
	#print(config_file)
	hpc_path=inp_get_token_value(config_file, "#hpc_dir")
	hpc_path=os.path.abspath(hpc_path)

	if os.path.isdir(hpc_path)==True:
		hpc_files=[]
		hpc_files=scan_list_simulations(hpc_path)
		#print("hpc files=",hpc_files)
		safe_delete(hpc_files)
		files=[]

		if only_unconverged==True:
			files=scan_list_unconverged_simulations(base_dir)
		else:
			files=scan_list_simulations(base_dir)

		#print("copy files=",files)
		for i in range(0,len(files)):
			dest_path=os.path.join(hpc_path,files[i][len(base_dir)+1:])
			#print(dest_path)
			shutil.copytree(files[i], dest_path,symlinks=True)
	else:
		print("HPC dir not found",hpc_path)

class scan_io(ctypes.Structure):
	_fields_ = [('scan_items', ctypes.c_void_p),
				('nitems', ctypes.c_int),
				('optimizer_enabled', ctypes.c_int),
				('scan_optimizer_dump_at_end', ctypes.c_int),
				('scan_optimizer_dump_n_steps', ctypes.c_int),
				('name', ctypes.c_char * 4096),
				('last_error', ctypes.c_char * 4096)]

	def __init__(self):
		self.parent_window=None
		self.interactive=True
		self.scan_dir=None
		self.base_dir=None
		self.scan_name=None
		self.config_file=None
		self.program_list=[]
		self.myserver=None
		self.lib=sim_paths.get_dll_py()
		self.lib.scan_load_config_from_file.restype = ctypes.c_int
		self.lib.scan_make_dirs.restype = ctypes.c_int
		self.lib.scan_init(None,ctypes.byref(self))

	def load_config_from_file(self,path,json_path):
		return self.lib.scan_load_config_from_file(None,ctypes.byref(self), bytes(path, encoding='utf8') , bytes(json_path, encoding='utf8'))

	def scan_dump(self):
		self.lib.scan_dump(None,ctypes.byref(self))

	def scan_make_dirs(self,path):
		return self.lib.scan_make_dirs(None,ctypes.byref(self),bytes(path, encoding='utf8'))

	def scan_free(self):
		self.lib.scan_free(None,ctypes.byref(self))

	def __del__(self):
		self.lib.scan_free(None,ctypes.byref(self))


	def load(self,path,name,scan_obj):
		self.program_list=[]

		if name!=None:
			self.scan_name=name
		else:
			self.scan_name=os.path.basename(path)

		self.scan_dir=os.path.join(path,self.scan_name)

		if scan_obj!=None:
			for s in scan_obj.segments:
				self.program_list.append(s)

	def set_path(self,scan_dir):
		self.scan_dir=scan_dir

	def set_base_dir(self,base_dir):
		self.base_dir=base_dir

	def run(self,run_simulation=True,generate_simulations=True,args=""):
		f=inp()
		f.load(os.path.join(self.scan_dir,"scan_config.inp"))
		args=f.get_token("#scan_config_args")

		if args==False:
			args=""

		args=args+" --mindbustx"

		if self.scan_dir=="":
			error_dlg(self.parent_window,_("No sim dir name"))
			return

		if generate_simulations==True:
			self.build_scan()

		if run_simulation==True:
			commands=tree_load_flat_list(self.scan_dir)
			if commands==False:
				error_dlg(self.parent_window,_("I can't load flat_list.inp.  This usually means there is a problem with how you have set up your scan."))
				return

			for i in range(0, len(commands)):
				self.myserver.add_job(commands[i],args)
				#print("Adding job"+commands[i])

			#print("2.",os.listdir(self.scan_dir))
			self.myserver.start()

		gc.collect()

	def build_scan(self):
		self.clean_dir()

		if self.load_config_from_file(self.base_dir,self.scan_name)!=0:
			error_dlg(self.parent_window,_("Problem loading file."))

		if self.scan_make_dirs(self.base_dir)!=0:
			error_dlg(self.parent_window,_("Problem generating tree."))
			self.scan_free()
			return False

		flat_simulation_list=tree_gen_flat_list(self.scan_dir)
		tree_save_flat_list(self.scan_dir,flat_simulation_list)
		self.scan_free()

	def is_scan_dir(self,scan_name):
		ret=decode_inode(scan_name)
		if ret.type==b"scan":
			return True
		return False

	def clean_dir(self):
		dirs_to_del=[]
		if self.is_scan_dir(self.scan_dir)==False:
			return

		listing=os.listdir(self.scan_dir)

		for sub_sir in listing:
			full_path=os.path.join(self.scan_dir, sub_sir)
			if os.path.isdir(full_path)==True:
				dirs_to_del.append(full_path)

		ask_to_delete(self.parent_window,dirs_to_del,interactive=self.interactive)

	def rename(self,new_name):
		new_path=os.path.join(os.path.dirname(self.scan_dir),new_name)
		try:
			shutil.move(self.scan_dir, new_path)
			self.scan_dir=new_path
		except:
			pass
		
	def clone(self,new_human,new_config_file):
		self.scan_dir=os.path.join(os.path.dirname(self.scan_dir),new_name)
		print(self.config_file)

