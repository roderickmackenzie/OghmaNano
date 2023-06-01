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
from experiment import experiment
from play import play
from server import server_get
from cal_path import sim_paths
from QAction_lock import QAction_lock
from json_root import json_root
from tab import tab_class
from config_window import class_config_window
import codecs
from clone import clone_sim_dir
from clean_sim import clean_sim_dir
from search import find_sims
from clean_sim import ask_to_delete
from inp import inp
from scan_human_labels import set_json_from_human_path
from json_root import all_json_root
from scan_tree import random_log
import random
from scan_io import scan_archive
from ml_vectors import ml_vectors
from process_events import process_events
from server_base import server_base
from util import wrap_text
from error_dlg import error_dlg

class window_ml(experiment):


	def __init__(self):
		experiment.__init__(self,window_save_name="window_ml", window_title=_("Machine learning"),name_of_tab_class="tab_ml",json_search_path="json_root().ml")

		self.tb_configure= QAction_lock("cog", _("Configure"), self,"ribbon_configure")
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_configure)
		self.tb_configure.clicked.connect(self.callback_configure)

		self.tb_build_vectors= QAction_lock("matrix", _("Build\nvectors"), self,"ribbon_configure")
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_build_vectors)
		self.tb_build_vectors.clicked.connect(self.callback_build_vectors)

		self.run = play(self,"ml_ribbon_run",run_text=_("Run\nGenerator"),connect_to_server=False)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.run)
		self.run.start_sim.connect(self.callback_run)

		self.tb_clean = QAction(icon_get("clean"), wrap_text(_("Clean files"),4), self)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_clean)
		self.tb_clean.triggered.connect(self.callback_clean)

		self.notebook.currentChanged.connect(self.switch_page)
		self.my_server=server_base()
		self.my_server.time_out=60*7
		self.my_server.server_base_init(sim_paths.get_sim_path())
		self.my_server.pipe_to_null=True
		#self.my_server.sim_finished.connect(self.callback_sim_finished)
		#self.my_server.server_base_set_callback(self.callback_sim_finished)
		self.switch_page()
		self.running=False

		self.progress_window=progress_class()
		self.my_server.progress_window=self.progress_window

	def callback_clean(self):
		print("clean")

	def switch_page(self):
		self.notebook.currentWidget()
		#self.tb_lasers.update(tab.data)

	def set_ml_dir(self):
		tab = self.notebook.currentWidget()
		self.obj=json_root().ml.find_object_by_id(tab.uid)
		if self.obj.ml_config.ml_archive_path=="cwd":
			self.ml_dir=os.path.join(sim_paths.get_sim_path(),self.obj.name)
		else:
			one=sim_paths.get_sim_path().split(os.path.sep)[-2]
			two=sim_paths.get_sim_path().split(os.path.sep)[-1]
			
			self.ml_dir=os.path.join(self.obj.ml_config.ml_archive_path,one,two,self.obj.name)

	def callback_run(self):
		self.n=0
		self.notebook.currentWidget()
		self.set_ml_dir()

		if os.path.isdir(self.ml_dir)==True:
			dirs_to_del=[]
			for dir_name in os.listdir(self.ml_dir):
				full_path=os.path.join(self.ml_dir,dir_name)
				if os.path.isdir(full_path):
					dirs_to_del.append(full_path)


			ask_to_delete(self,dirs_to_del,interactive=True)

		self.run.start()
		self.progress_window.show()
		self.progress_window.start()
		self.running=False
		self.timer=QTimer()
		self.timer.timeout.connect(self.callback_timer)
		self.timer.start(10)

	def callback_timer(self):
		if self.running==False:
			self.running=True
			self.n=self.n+1

			for n in range(0,self.obj.ml_config.ml_sims_per_archive):
				random_file_name=codecs.encode(os.urandom(int(16 / 2)), 'hex').decode()
				cur_dir=os.path.join(self.ml_dir,random_file_name)

				#build random vars for all sims
				random_vars=[]
				for random_item in self.obj.ml_random.segments:
					if random_item.random_var_enabled:
						if random_item.random_distribution=="log":
							val=float(random_log(random_item.min,random_item.max))
						else:
							val=random.uniform(random_item.min, random_item.max)
						random_vars.append([random_item.json_var,val])

				for sim in self.obj.ml_sims.segments:
					if sim.ml_sim_enabled==True:
						sub_sim_dir=os.path.join(cur_dir,sim.sim_name)
						clone_sim_dir(sub_sim_dir,sim_paths.get_sim_path())
						clean_sim_dir(sub_sim_dir)

						data=all_json_root()
						data.load(os.path.join(sub_sim_dir,"sim.json"))

						for patch_item in self.obj.ml_patch.segments:
							if patch_item.ml_patch_enabled:
								data.set_val(patch_item.json_var,patch_item.ml_patch_val)

						for patch_item in sim.ml_patch.segments:
							if patch_item.ml_patch_enabled:
								data.set_val(patch_item.json_var,patch_item.ml_patch_val)

						for random_item in random_vars:
							data.set_val(random_item[0],random_item[1])

						for duplicate_item in self.obj.duplicate.segments:
							if duplicate_item.duplicate_var_enabled:
								val=data.get_val(duplicate_item.json_src)
								data.set_val(duplicate_item.json_dest,val)
								
						data.save(do_tab=False)
						self.my_server.add_job(sub_sim_dir,"")

				self.progress_window.set_fraction(float(n)/float(self.obj.ml_config.ml_sims_per_archive))
				self.progress_window.set_text(_("Building simulations: ")+str(n)+"/"+str(self.obj.ml_config.ml_sims_per_archive))
				process_events()

			self.my_server.simple_run()
			self.callback_sim_finished()

	def callback_sim_finished(self):
		if self.running==True:
			self.my_server.remove_debug_info()
			self.my_server.clear_jobs()
			scan_archive(self.ml_dir,progress_window=self.progress_window)
			if self.n>self.obj.ml_config.ml_number_of_archives:
				self.timer.stop()
				self.run.stop()
				self.progress_window.stop()
				self.progress_window.hide()
				os.chdir(sim_paths.get_sim_path())
			self.running=False

	def callback_configure(self):
		tab = self.notebook.currentWidget()
		obj=json_root().ml.find_object_by_id(tab.uid)

		self.config_window=class_config_window([obj.ml_config],[_("Config")])
		self.config_window.show()

	def callback_build_vectors(self):
		tab = self.notebook.currentWidget()
		obj=json_root().ml.find_object_by_id(tab.uid)

		self.set_ml_dir()
		if os.path.isdir(self.ml_dir):
			scan=ml_vectors()
			scan.build_vector(self.ml_dir,obj)
		else:
			error_dlg(self,_("The directory does not exist: ")+self.ml_dir)
