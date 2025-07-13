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

## @package time_domain_experiment
#  The main experiment window, used for configuring time domain experiments.
#

from icon_lib import icon_get
import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QMenuBar,QStatusBar, QMenu
from PySide2.QtGui import QPainter,QIcon

from util import wrap_text

from experiment_bin import experiment_bin
from tb_lasers import tb_lasers
from config_window import class_config_window

class time_domain_experiment(experiment_bin):

	def __init__(self):
		experiment_bin.__init__(self,"time_domain_experiment_tab",window_save_name="time_domain_experiment", window_title=_("Time domain experiment window"),json_search_path="sims.time_domain")

		w=self.ribbon_simulation()
		self.ribbon.addTab(w,_("Simulation"))

		self.tb_laser_start_time.triggered.connect(self.callback_laser_start_time)

		self.tb_start.triggered.connect(self.callback_start_time)

		self.notebook.currentChanged.connect(self.switch_page)
		self.switch_page()

	def ribbon_simulation(self):
		toolbar = QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(42, 42))

		self.tb_laser_start_time = QAction(icon_get("laser"), wrap_text(_("Laser start time"),2), self)
		toolbar.addAction(self.tb_laser_start_time)

		self.tb_lasers=tb_lasers()
		toolbar.addWidget(self.tb_lasers)

		self.tb_start = QAction(icon_get("start"), _("Simulation start time"), self)
		toolbar.addAction(self.tb_start)

		self.tb_loop = QAction(icon_get("loop"), _("Loop"), self)
		self.tb_loop.setCheckable(True)

		self.menu_loop = QMenu(self)
		configure_item=QAction(_("Configure"), self)
		self.menu_loop.addAction(configure_item)
		self.tb_loop.setMenu(self.menu_loop)
		self.tb_loop.triggered.connect(self.callback_loop)
		self.menu_loop.triggered.connect(self.callback_loop_menu)

		toolbar.addAction(self.tb_loop)

		return toolbar

	def callback_laser_start_time(self):
		tab = self.notebook.currentWidget()
		tab.tmesh.callback_laser()

	def callback_start_time(self):
		tab = self.notebook.currentWidget()
		tab.tmesh.callback_start_time()

	def switch_page(self):
		tab = self.notebook.currentWidget()
		if tab!=None:
			json_path=self.bin.find_path_by_uid("sims.time_domain",tab.uid)
			laser_name=self.bin.get_token_value(json_path+".config","pump_laser")			
			self.tb_lasers.update(laser_name)

	def callback_loop(self):
		tab = self.notebook.currentWidget()
		if tab!=None:
			json_path=self.bin.find_path_by_uid("sims.time_domain",tab.uid)
			time_loop=self.bin.get_token_value(json_path+".mesh","time_loop")
			time_loop=not time_loop
			self.tb_loop.setChecked(time_loop)
			self.bin.save()

	def callback_loop_menu(self):
		tab = self.notebook.currentWidget()
		if tab!=None:
			json_path=self.bin.find_path_by_uid("sims.time_domain",tab.uid)
			self.mesh_config=class_config_window([json_path+".mesh"],[_("Config")],title=_("Loop configuration"),icon="loop")
			self.mesh_config.show()


