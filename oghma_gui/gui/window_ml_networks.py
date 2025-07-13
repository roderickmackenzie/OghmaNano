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

## @package window_ml_networks
#  Scan experiment editor
#

import i18n
_ = i18n.language.gettext
from experiment_bin import experiment_bin
from tab_ml_network import tab_ml_network
from cal_path import sim_paths
from PySide2.QtWidgets import QAction
from icon_lib import icon_get
from util import wrap_text
from server import server_get
from play import play

class window_ml_networks(experiment_bin):

	def __init__(self,uid):
		experiment_bin.__init__(self,"tab_ml_network",window_save_name="window_scan", window_title=_("Neural networks editor"),json_search_path="ml",min_y=500,style="list",display_the_toolbar=False,uid=uid)
		self.sim_dir=sim_paths.get_sim_path()
		self.tb_clean = QAction(icon_get("clean"), wrap_text(_("Clean all"),4), self)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_clean)
		self.tb_clean.triggered.connect(self.callback_clean_all)

		self.tb_run_all =  play(self,"scan_play_all",play_icon="json_file",run_text=_("Compile\nto json"))
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_run_all)
		self.tb_run_all.start_sim.connect(self.callback_compile)

		self.delete_item.connect(self.callback_delete_item)
		self.rename_item.connect(self.callback_rename_item)

		self.removeAction(self.ribbon.tb_rename)
		self.ribbon.file.insertAction(self.tb_clean,self.ribbon.tb_rename)

	def callback_clean_all(self):
		pass

	def callback_compile(self):
		print("compile")

	def callback_delete_item(self,item):
		pass

	def callback_rename_item(self,old_name,new_name):
		pass

