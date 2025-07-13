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

## @package window_ml
#  ML editor
#

import os

from icon_lib import icon_get

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt, QTimer
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar
from PySide2.QtGui import QPainter,QIcon

#window
from progress_class import progress_class
from process_events import process_events
from global_objects import global_object_run
from experiment_bin import experiment_bin
from play import play
from server import server_get
from cal_path import sim_paths
from QAction_lock import QAction_lock
from tab import tab_class
from config_window import class_config_window
import codecs
from clean_sim import clean_sim_dir
from search import find_sims
from clean_sim import ask_to_delete
from scan_tree import random_log
import random
from scan_io import scan_archive
from ml_vectors import ml_vectors
from process_events import process_events
from server_base import server_base
from util import wrap_text
from error_dlg import error_dlg
import ctypes
from json_c import json_c
from bytes2str import str2bytes
from threading import Thread
from ribbon_page import ribbon_page
from hash_list import hash_list
from json_c import json_tree_c

class rand_state(ctypes.Structure):
	_fields_ = [
		("rand_function", ctypes.c_int),
		("rand_seed", ctypes.c_int),
		("noise_source", ctypes.c_char * 100),
		("mt", ctypes.c_ulonglong * 624),
		("index", ctypes.c_int),
		("n2", ctypes.c_double),
		("n2_cached", ctypes.c_int)
	]

class  ml_vectors_obj(ctypes.Structure):
	_fields_ = [('hist', ctypes.c_void_p),
				('min', hash_list),
				('max', hash_list),
				('log', ctypes.c_void_p),
				('tokens', ctypes.c_void_p)]

class ml_stats(ctypes.Structure):
	_fields_ = [('j', json_c),

				('vec', ml_vectors_obj),
				('vec_norm', ml_vectors_obj),
				('vec_combined', ml_vectors_obj),
				('vec_combined_norm', ml_vectors_obj),

				('json_vectors_file', ctypes.c_char * 4096),
				('base_sim_path', ctypes.c_char * 4096),
				('build_path', ctypes.c_char * 4096),
				('main_hist_dir', ctypes.c_char * 4096),

				('ml_random_n', ctypes.c_int),

				('json_obj_ml_random', ctypes.c_void_p),
				('token_lib', hash_list),

				('last_device_id', ctypes.c_char * 4096),
				('csv_file', ctypes.c_void_p),
				('csv_file_name', ctypes.c_char * 4096),
				('csv_line', ctypes.c_long),

				('csv_col', ctypes.c_int),
				('done', ctypes.c_int),
				('total', ctypes.c_int),
				('finished_building', ctypes.c_int),
				('log', hash_list)]

class ml_build(ctypes.Structure):
	_fields_ = [('j', json_c),
				('base_sim_path', ctypes.c_char * 4096),
				('build_path', ctypes.c_char * 4096),
				('ml_tab_name', ctypes.c_char * 4096),
				('ml_number_of_archives', ctypes.c_int),
				('ml_sims_per_archive', ctypes.c_int),
				('done', ctypes.c_int),
				('total', ctypes.c_int),
				('finished_building', ctypes.c_int),
				('rand',rand_state)]

	def __init__(self):
		self.lib=sim_paths.get_dll_py()
		self.lib.ml_build_init(ctypes.byref(self))

class window_ml(experiment_bin):


	def __init__(self):
		experiment_bin.__init__(self,window_save_name="window_ml", window_title=_("Machine learning"),name_of_tab_class="tab_ml",json_search_path="ml")

		self.bin=json_tree_c()
		self.tb_configure= QAction_lock("cog", _("Configure"), self,"ribbon_configure")
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_configure)
		self.tb_configure.clicked.connect(self.callback_configure)

		self.tb_build_vectors= QAction_lock("matrix", _("Build\nvectors"), self,"ribbon_configure")
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_build_vectors)
		self.tb_build_vectors.clicked.connect(self.callback_build_vectors)

		self.tb_norm_vectors= QAction_lock("matrix_norm", _("Norm\nvectors"), self,"ribbon_configure")
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_norm_vectors)
		self.tb_norm_vectors.clicked.connect(self.callback_stats)

		self.run = play(self,"ml_ribbon_run",run_text=_("Run\nGenerator"),connect_to_server=False)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.run)
		self.run.start_sim.connect(self.callback_run)

		self.tb_clean = QAction(icon_get("clean"), wrap_text(_("Clean files"),4), self)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_clean)
		self.tb_clean.triggered.connect(self.callback_clean)
		self.ribbon.setTabText(0, _("Generator"))

		self.notebook.currentChanged.connect(self.switch_page)
		self.my_server=server_base()
		self.my_server.server_base_init(sim_paths.get_sim_path())
		self.my_server.pipe_to_null=True
		self.my_server.quotes_around_windows_exe=True
		self.my_server.enable_html_output=False
		#self.my_server.sim_finished.connect(self.callback_sim_finished)
		#self.my_server.server_base_set_callback(self.callback_sim_finished)
		self.switch_page()
		self.running=False
		self.vectors_running=False
		self.stats_running=False
		self.progress_window=progress_class()
		self.my_server.progress_window=self.progress_window
		self.lib=sim_paths.get_dll_py()

		self.ml_build=ml_build()

		self.ml_vectors=ml_vectors()
		self.lib.ml_vectors_init(ctypes.byref(self.ml_vectors))

		self.ml_stats=ml_stats()
		self.lib.ml_stats_init(ctypes.byref(self.ml_stats))

		self.ribbon_network=self.ribbon_networks()
		self.ribbon.addTab(self.ribbon_network,_("Neural networks"))
		self.ribbon.currentChanged.connect(self.callback_ribbon_changed)
		self.sub_tab_changed.connect(self.callback_notebook_sub_tab_changed)

	def callback_notebook_sub_tab_changed(self,tab_name):
		if tab_name==_("Neural networks"):
			self.ribbon.goto_page(_("Neural networks"))
		else:
			self.ribbon.goto_page(_("Generator"))

	def callback_ribbon_changed(self):
		index = self.ribbon.currentIndex()
		tab_ml=self.notebook.currentWidget()
		if self.ribbon.tabText(index)==_("Neural networks"):
			tab_ml.goto_page(_("Neural networks"))
		else:
			tab_ml.setCurrentIndex(tab_ml.last_page_index)
			
	def ribbon_networks(self):
		toolbar = ribbon_page()
		self.tb_ribbon_networks_new = QAction(icon_get("document-new"), wrap_text(_("New"),2), self)
		toolbar.addAction(self.tb_ribbon_networks_new)
		self.tb_ribbon_networks_new.triggered.connect(self.callback_networks_new)

		self.tb_ribbon_networks_delete = QAction(icon_get("edit-delete"), wrap_text(_("Delete"),3), self)
		toolbar.addAction(self.tb_ribbon_networks_delete)
		self.tb_ribbon_networks_delete.triggered.connect(self.callback_networks_delete)

		self.tb_ribbon_networks_clone = QAction(icon_get("clone"), wrap_text(_("Clone"),3), self)
		toolbar.addAction(self.tb_ribbon_networks_clone)
		self.tb_ribbon_networks_clone.triggered.connect(self.callback_networks_clone)

		self.tb_ribbon_networks_rename = QAction(icon_get("rename"), wrap_text(_("Rename"),3), self)
		toolbar.addAction(self.tb_ribbon_networks_rename)
		self.tb_ribbon_networks_rename.triggered.connect(self.callback_networks_rename)

		self.tb_ribbon_networks_json_compile = QAction(icon_get("compile_to_json"), _("Compile\nto json"), self)
		toolbar.addAction(self.tb_ribbon_networks_json_compile)
		self.tb_ribbon_networks_json_compile.triggered.connect(self.callback_json_compile)

		return toolbar

	def callback_json_compile(self):
		tab_ml=self.notebook.currentWidget()
		tab_ml.compile_to_json()

	def callback_networks_new(self):
		tab_ml=self.notebook.currentWidget()
		tab_ml.net.callback_add_page()

	def callback_networks_delete(self):
		tab_ml=self.notebook.currentWidget()
		tab_ml.net.callback_delete_page()

	def callback_networks_clone(self):
		tab_ml=self.notebook.currentWidget()
		tab_ml.net.callback_clone_page()

	def callback_networks_rename(self):
		tab_ml=self.notebook.currentWidget()
		tab_ml.net.callback_rename_page()

	def callback_clean(self):
		print("clean")

	def switch_page(self):
		self.notebook.currentWidget()
		#self.tb_lasers.update(tab.data)

	def find_json_path_of_tab(self):
		tab = self.notebook.currentWidget()
		if tab==None:
			return
		ret=self.bin.find_path_by_uid("ml",tab.uid)
		return ret

	def set_ml_dir(self):
		path=self.find_json_path_of_tab()
		self.timervectors_pass_json_path=path
		name=self.bin.get_token_value(path,"name")
		ml_archive_path=self.bin.get_token_value(path+".ml_config","ml_archive_path")
		if ml_archive_path=="cwd":
			self.ml_dir=os.path.join(sim_paths.get_sim_path(),name)
		else:
			one=sim_paths.get_sim_path().split(os.path.sep)[-2]
			two=sim_paths.get_sim_path().split(os.path.sep)[-1]
			
			self.ml_dir=os.path.join(ml_archive_path,one,two,name)

		try:
			os.mkdir(self.ml_dir)
		except:
			pass

		if os.path.isdir(self.ml_dir)==False:
			error_dlg(self,_("Could not make ml_dir: ")+self.ml_dir)
			return False

		return True

	def callback_run(self):
		path=self.find_json_path_of_tab()
		ml_crash_time=self.bin.get_token_value(path+".ml_config","ml_crash_time")
		self.n=0
		if self.set_ml_dir()==False:
			return
		self.my_server.time_out=60*ml_crash_time

		if os.path.isdir(self.ml_dir)==True:
			dirs_to_del=[]
			for dir_name in os.listdir(self.ml_dir):
				full_path=os.path.join(self.ml_dir,dir_name)
				if os.path.isdir(full_path):
					dirs_to_del.append(full_path)

			ask_to_delete(self,dirs_to_del,interactive=True)

		path=self.find_json_path_of_tab()
		name=self.bin.get_token_value(path,"name")

		sub_sim_dir=os.path.join(self.ml_dir)
		self.lib.ml_build_free(ctypes.byref(self.ml_build))
		self.lib.ml_build_load(ctypes.byref(self.ml_build), ctypes.c_char_p(str2bytes(sim_paths.get_sim_path())), ctypes.c_char_p(str2bytes(sub_sim_dir)), ctypes.c_char_p(str2bytes(name)))

		self.run.start()
		self.progress_window.show()
		self.progress_window.start()
		self.running=False
		self.timer=QTimer()
		self.timer.timeout.connect(self.callback_timer)
		self.timer.start(100)


	def build_sims(self):
		self.lib.ml_build_gen(ctypes.byref(self.ml_build))
		self.ml_build.finished_building=True


	def callback_timer(self):
		if self.running==False:
			self.running=True
			self.ml_build.finished_building=False
			p = Thread(target=self.build_sims)
			p.daemon = True
			p.start()

		#print(self.running,self.ml_build.finished_building,self.ml_build.done,self.ml_build.total)
		if self.running==True:
			if self.ml_build.finished_building==True:
				for root, dirs, files in os.walk(self.ml_dir):
					if "sim.json" in files:
						if root!=self.ml_dir:
							self.my_server.add_job(root,"")
				self.my_server.simple_run()
				self.callback_sim_finished()
		try:
			frac=float(self.ml_build.done)/float(self.ml_build.total)
		except:
			frac=0.0

		self.progress_window.set_fraction(frac)
		self.progress_window.set_text(_("Building simulations: ")+str(self.ml_build.done)+"/"+str(self.ml_build.total))

	def callback_timer_build_vectors(self):
		if self.vectors_running==False:
			self.vectors_running=True
			self.ml_vectors.finished_building=False;
			p = Thread(target=self.build_vectors)
			p.daemon = True
			p.start()

		if self.vectors_running==True:
			if self.ml_vectors.finished_building==True:
				self.timer_vectors.stop()
				self.progress_window.stop()
				self.progress_window.hide()
				os.chdir(sim_paths.get_sim_path())
				self.vectors_running=False

		if self.ml_vectors.total!=-1:
			try:
				frac=float(self.ml_vectors.done)/float(self.ml_vectors.total)
			except:
				frac=0.0
			self.progress_window.set_fraction(frac)
			text=_("Building vectors: ")
			text=text+str(self.ml_vectors.done)+"/"+str(self.ml_vectors.total)
			try:
				frac=round(100.0*self.ml_vectors.errors/self.ml_vectors.total,1)
			except:
				frac=0.0
			text=text+" errors: "+str(frac)+"%"
			self.progress_window.set_text(text)

	def callback_timer_stats(self):
		if self.stats_running==False:
			self.stats_running=True
			self.ml_stats.finished_building=False
			p = Thread(target=self.build_stats)
			p.daemon = True
			p.start()

		if self.stats_running==True:
			if self.ml_stats.finished_building==True:
				self.timer_stats.stop()
				self.progress_window.stop()
				self.progress_window.hide()
				os.chdir(sim_paths.get_sim_path())
				self.stats_running=False

		if self.ml_stats.total!=-1:
			try:
				frac=float(self.ml_stats.done)/float(self.ml_stats.total)
			except:
				frac=0.0
			self.progress_window.set_fraction(frac)
			text=_("Building vectors: ")
			text=text+str(self.ml_stats.done)+"/"+str(self.ml_stats.total)
			self.progress_window.set_text(text)

	def build_vectors(self):
		self.ml_vectors.finished_building=False
		self.ml_vectors.build_vector(self.ml_dir,self.timervectors_pass_json_path)

	def build_stats(self):
		name=self.bin.get_token_value(self.timervectors_pass_json_path,"name")
		self.lib.ml_stats_load(ctypes.byref(self.ml_stats), ctypes.c_char_p(str2bytes(sim_paths.get_sim_path())), ctypes.c_char_p(str2bytes(name)))
		self.lib.ml_stats_run(ctypes.byref(self.ml_stats))
		self.lib.ml_stats_free(ctypes.byref(self.ml_stats))

	def callback_sim_finished(self):
		if self.running==True: 
			self.timer.stop()
			self.running=False
			self.my_server.remove_debug_info()
			self.my_server.clear_jobs()
			scan_archive(self.ml_dir,progress_window=self.progress_window)
			ml_number_of_archives=self.bin.get_token_value(self.timervectors_pass_json_path+".ml_config","ml_number_of_archives")
			ml_build_vectors_when_done=self.bin.get_token_value(self.timervectors_pass_json_path+".ml_config","ml_build_vectors_when_done")

			self.n=self.n+1
			if self.n>ml_number_of_archives:
				self.lib.ml_build_free(ctypes.byref(self.ml_build))
				self.run.stop()
				self.progress_window.stop()
				self.progress_window.hide()
				os.chdir(sim_paths.get_sim_path())
				if ml_build_vectors_when_done==True:
					self.running=False
					print("Building vectors")
					self.callback_build_vectors()
			else:
				self.timer.start()

	def callback_configure(self):
		path=self.find_json_path_of_tab()
		self.config_window=class_config_window([path+".ml_config"],[_("Config")])
		self.config_window.show()

	def callback_build_vectors(self):
		if self.set_ml_dir()==False:
			return

		self.progress_window.show()
		self.progress_window.start()
		self.vectors_running=False
		self.timer_vectors=QTimer()
		self.timer_vectors.timeout.connect(self.callback_timer_build_vectors)
		self.timer_vectors.start(10)

	def callback_stats(self):
		if self.set_ml_dir()==False:
			return

		self.progress_window.show()
		self.progress_window.start()
		self.stats_running=False
		self.timer_stats=QTimer()
		self.timer_stats.timeout.connect(self.callback_timer_stats)
		self.timer_stats.start(10)


