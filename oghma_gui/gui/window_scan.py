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

## @package window_scan
#  Scan experiment editor
#

import i18n
_ = i18n.language.gettext
from jvexperiment_tab import jvexperiment_tab
from experiment import experiment
from tab_scan import tab_scan
from cal_path import sim_paths
from PySide2.QtWidgets import QAction
from scans_io import scans_io
from icon_lib import icon_get
from util import wrap_text
from server import server_get
from play import play
from scan_io import scan_io
from json_root import json_root

class window_scan(experiment):


	def __init__(self,data=None):
		experiment.__init__(self,"tab_scan",window_save_name="window_scan", window_title=_("Parameter scan window"),json_search_path="json_root().scans",min_y=500,style="list")
		self.sim_dir=sim_paths.get_sim_path()
		self.scans_io=scans_io(self.sim_dir)
		self.scans_io.parent_window=self
		self.tb_clean = QAction(icon_get("clean"), wrap_text(_("Clean all"),4), self)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_clean)
		self.tb_clean.triggered.connect(self.callback_clean_all)

		self.tb_run_all =  play(self,"scan_play_all",play_icon="forward2",run_text=wrap_text(_("Run all scans"),5))
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_run_all)
		self.tb_run_all.start_sim.connect(self.callback_run_all_simulations)

		self.delete_item.connect(self.callback_delete_item)
		self.rename_item.connect(self.callback_rename_item)

		self.removeAction(self.ribbon.tb_rename)
		self.ribbon.file.insertAction(self.tb_clean,self.ribbon.tb_rename)

		self.ribbon.setTabText(0, _("Scan"))

	def callback_clean_all(self):
		self.scans_io.clean_all()

	def callback_run_all_simulations(self):
		for obj in json_root().scans.segments:
			if obj.scan_optimizer.enabled==False:
				s=scan_io()
				s.load(sim_paths.get_sim_path(),obj.name,obj)
				s.parent_window=self
				s.myserver=server_get()
				s.set_base_dir(sim_paths.get_sim_path())
				s.run()
			else:
				server_get().add_job(sim_paths.get_sim_path(),"--optimizer "+obj.name+" --path "+sim_paths.get_sim_path())
				server_get().start()


	def callback_delete_item(self,item):
		pass
		#disabled due to paranoya
		#s=scans_io(self.sim_dir)
		#s.delete(item)

	def callback_rename_item(self,old_name,new_name):
		s=scan_io()
		s.load(sim_paths.get_sim_path(),old_name,None)
		s.rename(new_name)

