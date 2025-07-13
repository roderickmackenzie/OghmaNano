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

## @package jv_experiment
#  JV experiment editor
#



import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar
from PySide2.QtGui import QPainter,QIcon

#window
from experiment_bin import experiment_bin
from play import play
from server import server_get
from cal_path import sim_paths
from icon_lib import icon_get
from json_c import json_tree_c

class window_light_src(experiment_bin):

	def __init__(self,data=None):
		experiment_bin.__init__(self,window_save_name="window_light_src", window_title=_("Light source editor"),name_of_tab_class="tab_light_src",json_search_path="optical.light_sources.lights")
		self.bin=json_tree_c()

		self.notebook.currentChanged.connect(self.switch_page)

		self.run = play(self,"optics_ribbon_run",run_text=_("Rebuild"))
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.run)
		self.run.start_sim.connect(self.callback_run)

		self.switch_page()

	def switch_page(self):
		self.notebook.currentWidget()
		#self.tb_lasers.update(tab.data)


	def callback_run(self):
		self.dump_verbosity=self.bin.get_token_value("optical.light","dump_verbosity")
		self.bin.set_token_value("optical.light","dump_verbosity",1)
		self.bin.save()

		self.my_server=server_get()
		self.my_server.clear_cache()
		self.my_server.add_job(sim_paths.get_sim_path(),"--simmode opticalmodel@optics")
		self.my_server.sim_finished.connect(self.callback_sim_finished)
		self.my_server.start()

	def callback_sim_finished(self):
		self.bin.set_token_value("optical.light","dump_verbosity",self.dump_verbosity)
		self.bin.save()
		self.update()
