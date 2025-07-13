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

## @package server_base
#  The server module, used to run simulations across all CPUs, also has interface to the HPC class.
#

import os

import multiprocessing
import time
from win_lin import get_platform
from progress_class import progress_class
from stat import *

import i18n
_ = i18n.language.gettext
from cluster import cluster
from gui_enable import gui_get
import time
from cal_path import sim_paths
from datetime import datetime
import socket
from threading import Thread
import ctypes
from bytes2str import str2bytes
from bytes2str import bytes2str
from json_c import json_tree_c

if gui_get()==True:
	from process_events import process_events

class ipc_data(ctypes.Structure):
	_fields_ = [('connection', ctypes.c_void_p ),
				('buf', ctypes.c_char * 4096 ),
				('sock', ctypes.c_int64 ),
				('clients', ctypes.c_void_p ),
				('nclients', ctypes.c_int ),
				('port', ctypes.c_int ) ]

class job_class(ctypes.Structure):
	_fields_ = [('name', ctypes.c_char * 400),
				('status', ctypes.c_int),
				('batch_id', ctypes.c_int),
				('fun', ctypes.c_char *8),		#Will only work on 64 bit systems
				('sim', ctypes.c_void_p),
				('server', ctypes.c_void_p),
				('data0', ctypes.c_void_p),
				('data1', ctypes.c_void_p),
				('data2', ctypes.c_void_p),
				('data3', ctypes.c_void_p),
				('data4', ctypes.c_void_p),
				('data5', ctypes.c_void_p),
				('data_int0', ctypes.c_int),
				('data_int1', ctypes.c_int),
				('data_int2', ctypes.c_int),
				('data_int3', ctypes.c_int),
				('data_int4', ctypes.c_int),
				('data_int5', ctypes.c_int),
				('cpus', ctypes.c_int),
				('worker', ctypes.c_void_p),
				('process_type', ctypes.c_int),
				('next', ctypes.c_void_p),
				('micro_jobs_done', ctypes.c_int),
				('micro_jobs_tot', ctypes.c_int),
				('odes', ctypes.c_int),
				('tot_jobs', ctypes.c_int),
				('data_double0', ctypes.c_double),
				('start_time', ctypes.c_longlong),
				('end_time', ctypes.c_longlong),
				('path', ctypes.c_char * 4096),
				('args', ctypes.c_char * 4096),
				('full_command', ctypes.c_char * 4096),
				('ip', ctypes.c_char * 40),
				('lock_file_name', ctypes.c_char * 40)]

class server_class(ctypes.Structure):
	_fields_ = [('dbus_finish_signal', ctypes.c_char * 256),
				('lock_file', ctypes.c_char * 4096),
				('jobs', ctypes.c_int),
				('jobs_running', ctypes.c_int),
				('min_cpus', ctypes.c_int),
				('max_run_time', ctypes.c_int),
				('start_time', ctypes.c_longlong),
				('end_time', ctypes.c_longlong),
				('last_job_ended_at', ctypes.c_int),
				('allow_fake_forking_on_windows', ctypes.c_int),
				('max_threads', ctypes.c_int),
				('worker_max', ctypes.c_int),
				('steel', ctypes.c_int),
				('poll_time', ctypes.c_int),
				('worker', ctypes.c_void_p),
				('j', ctypes.c_void_p),
				('send_progress_to_gui', ctypes.c_int),
				('use_gpu', ctypes.c_int),
				('enable_micro_job_reporting', ctypes.c_int),
				('lock', ctypes.c_void_p),
				('batch_id', ctypes.c_int),
				('max_forks', ctypes.c_int),
				('quiet', ctypes.c_int),
				('tot_odes', ctypes.c_int),
				('tot_jobs', ctypes.c_int),
				('stats_start_time', ctypes.c_double),
				('stats_stop_time', ctypes.c_double),
				('server_jobs_per_s', ctypes.c_double),
				('server_odes_per_s', ctypes.c_double),
				('ipc',ipc_data)]

class server_base():

	def __init__(self):
		print("1")
		self.server=server_class()
		self.bin=json_tree_c()
		self.lib=sim_paths.get_dll_py()
		self.lib.server_get_next_job.restype = ctypes.POINTER(job_class)
		self.lib.server_jobs_find_by_lock_file_name.restype = ctypes.POINTER(job_class)
		self.lib.server_jobs_find_by_number.restype = ctypes.POINTER(job_class)
		self.lib.server_init(ctypes.byref(self.server))
		self.lib.server_init(ctypes.byref(self.server))
		self.lib.server2_malloc(None,ctypes.byref(self.server))
		self.running=False
		self.progress_window=progress_class()
		self.stop_work=False
		self.update_cpu_number()
		self.clear_jobs()
		self.callback=None
		self.max_job_time=None
		self.time_out=False
		self.quotes_around_windows_exe=False
		self.pipe_to_null=True
		self.enable_html_output=True

	def __del__(self):
		self.lib.server2_malloc(None,ctypes.byref(self.server))

	def get_exe_args(self):
		if self.enable_html_output==False:
			return ""

		if gui_get()==True:
			return "--gui --html"
		else:
			return ""

	def clear_jobs(self):
		self.lib.server_jobs_clear(ctypes.byref(self.server))
		self.start_time=0


	def server_base_init(self,sim_dir):
		self.sim_dir=sim_dir

	def update_cpu_number(self):
		self.cpus=multiprocessing.cpu_count()
		max=self.bin.get_token_value("server","max_core_instances")
		if max=="0" or max==None:
			self.cpus=1
			return

		if max=="all-div2":
			self.cpus=self.cpus/2

		if max=="all-2":
			self.cpus=self.cpus-2

		if max=="all":
			return

		max=int(max)
		self.cpus=max

	def add_job(self,path,args):
		self.lib.server_add_cmd_line_job(ctypes.byref(self.server),ctypes.c_char_p(str2bytes(sim_paths.get_exe_command())),ctypes.c_char_p(str2bytes(path)), ctypes.c_char_p(str2bytes(args)));

	def check_warnings(self):
		buf = (ctypes.c_char * 4096)()
		self.lib.server_jobs_check_warnings(ctypes.byref(self.server),buf,4096)
		message=bytes2str(ctypes.cast(buf, ctypes.c_char_p).value)
		return message

	def remove_debug_info(self):
		self.lib.server_remove_debug_info(ctypes.byref(self.server))

	def print_jobs(self):
		self.lib.server2_dump_jobs(ctypes.byref(self.server))

	def exe_command(self,job,background=True):
		if background==True:
			p = Thread(target=self.run_in_background,args=(job,))
			p.daemon = True
			p.start()
		else:
			self.lib.server_system_exe(ctypes.byref(self.server),job,ctypes.c_int(self.pipe_to_null))

	def run_in_background(self,job):
		self.lib.server_system_exe(ctypes.byref(self.server),job,ctypes.c_int(self.pipe_to_null))

	def server_base_process_jobs(self):
		path=True
		while(path!=False):
			#self.print_jobs()
			path,command,args,job=self.server_base_get_next_job_to_run(lock_file=True)
			if path!=False:
				self.exe_command(job)
				njobs=self.lib.server2_count_all_jobs(ctypes.byref(self.server))
				jobs_run=self.lib.server2_count_finished_jobs(ctypes.byref(self.server))
				if njobs>1:
					jobs_per_second="%.2f" % self.server.server_jobs_per_s
					self.progress_window.set_text(_("Running job ")+path+" jobs/s="+jobs_per_second)
					self.progress_window.set_fraction(float(jobs_run)/float(njobs))
					if gui_get()==True:
						process_events()
			else:
				return

	def remove_lock_files(self):
		ls=os.listdir(self.sim_dir)
		#print(">>>>>>",self.sim_dir,ls)
		for i in range(0, len(ls)):
			if ls[i][:4]=="lock" and ls[i][-4:]==".dat":
				del_file=os.path.join(self.sim_dir,ls[i])
				#print("delete file:",del_file)
				os.remove(del_file)

	def simple_run(self):
		self.start_time=time.time()
		self.stop_work=False
		self.remove_lock_files()
				
		self.server_base_process_jobs()
		dt=0.1
		n=0

		while(1):
			ls=os.listdir(self.sim_dir)
			#print(self.sim_dir,ls)
			for i in range(0, len(ls)):
				if ls[i][:4]=="lock" and ls[i][-4:]==".dat":
					n=0
					lock_file=ls[i]
					#print("rod",lock_file)
					os.remove(os.path.join(self.sim_dir,lock_file))
					job=lock_file[:-4]
					#print("rod",job)
					self.base_job_finished(job)

			self.server_base_process_jobs()
			time.sleep(dt)
			#self.print_jobs()
			self.server_base_check_for_crashed()
			#self.print_jobs()
			njobs=self.lib.server2_count_all_jobs(ctypes.byref(self.server))
			jobs_run=self.lib.server2_count_finished_jobs(ctypes.byref(self.server))
			if njobs==jobs_run:
				self.remove_lock_files()
				break

			if self.time_out!=False:
				if n>self.time_out/2:
					print(str(n)+"/"+str(self.time_out))

				if n>self.time_out:
					self.remove_lock_files()
					break
			n=n+dt
		

	def base_job_finished(self,job_lock_file_name):
		#print("SEARCH!!!!!!!!!!!!!",job_lock_file_name)
		#self.lib.server2_dump_jobs(ctypes.byref(self.server))
		njobs=self.lib.server2_count_all_jobs(ctypes.byref(self.server))
		jobs_run=self.lib.server2_count_finished_jobs(ctypes.byref(self.server))

		j=self.lib.server_jobs_find_by_lock_file_name(ctypes.byref(self.server), ctypes.c_char_p(str2bytes(job_lock_file_name)));
		if bool(j)!=False:
			self.lib.job_mark_as_finished(j)
			#
		jobs_running=self.lib.server_count_jobs_running(ctypes.byref(self.server),None)

		if jobs_running==0:
			if self.callback!=None:
				self.callback()
			self.callback=None

		self.progress_window.set_fraction(float(jobs_run)/float(njobs))

	def server_base_set_callback(self,callback):
		self.callback=callback

	def server_base_check_for_crashed(self):
		#print("server_base_check_for_crashed")
		if self.max_job_time==None:
			return

		self.lib.server_stop_crashed_jobs(ctypes.byref(self.server), ctypes.c_int(self.max_job_time))


	def server_base_get_next_job_to_run(self,lock_file=False):
		#print("server_base_get_next_job_to_run")
		njobs=self.lib.server2_count_all_jobs(ctypes.byref(self.server))
		jobs_running=self.lib.server_count_jobs_running(ctypes.byref(self.server),None)
		jobs_run=self.lib.server2_count_finished_jobs(ctypes.byref(self.server))

		if (njobs==0):
			return False,False,False,False

		j=self.lib.server_get_next_job(ctypes.byref(self.server), None)

		if bool(j)!=False:
			if (jobs_running<self.cpus):
				self.lib.job_mark_as_running(j)

				#set IP
				ip=socket.gethostbyname(socket.gethostname())
				self.lib.job_set_ip(j, ctypes.c_char_p(str2bytes(ip)));

				#lock file
				lock_name=bytes2str(j.contents.lock_file_name)
				if lock_file==True:
					lock_args=" --lockfile "+os.path.join(self.sim_dir,lock_name+".dat")
				else:
					lock_args=" --lock "+lock_name

				#build args
				args=bytes2str(j.contents.args)+" "+self.get_exe_args()+lock_args
				self.lib.job_set_args(j, ctypes.c_char_p(str2bytes(args)))
				#self.lib.server2_dump_jobs(ctypes.byref(self.server))

				#exe command
				command=sim_paths.get_exe_command()
				if get_platform()=="win":
					#The quotes are needed depending on how we are running this 
					if self.quotes_around_windows_exe==True:
						command="\""+command+"\""
				#
				self.lib.job_set_full_command(j, ctypes.c_char_p(str2bytes(command)));
				return bytes2str(j.contents.path),command,args,j

		return False,False,False,False

	def tx_to_core(self,data):
		path=os.path.join(sim_paths.get_sim_path(),"tx.dat")
		print("tx to core:"+path+" "+data)
		f=open(path,"w")
		f.write(data)
		f.close()

	def killall(self):
		self.stop_work=True
		if self.cluster==True:
			self.cluster_killall()
		#else:
		self.tx_to_core("terminate")
		#	if get_platform()=="linux":
		#		cmd = 'killall '+sim_paths.get_exe_name()
		#		os.system(cmd)
		#		print(cmd)
		#	else:
		#		cmd="taskkill /im "+sim_paths.get_exe_name()
		#		print(cmd)
		#		os.system(cmd)

		self.gui_sim_stop()


