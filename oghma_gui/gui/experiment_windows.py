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

## @package qe
#  The quantum efficiency window
#

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar
from PySide2.QtGui import QPainter,QIcon

import i18n
_ = i18n.language.gettext
from experiment_bin import experiment_bin
from tb_lasers import tb_lasers

class window_eqe(experiment_bin):

	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="eqe", window_title=_("Quantum efficiency editor"),json_search_path="sims.eqe",icon="qe")

class jv_experiment(experiment_bin):

	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="jvexperiment_editor", window_title=_("JV experiment window"),json_search_path="sims.jv",icon="jv",json_config_postfix="config")

class window_poly(experiment_bin):

	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="poly_editor", window_title=_("Polynomial data generator"),json_search_path="sims.poly",json_config_postfix="config")

class sunsvoc(experiment_bin):
	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="sunsvoc_editor", window_title=_("Suns v.s. Voc"),json_search_path="sims.suns_voc",icon="sunsvoc",json_config_postfix="config")

class sunsjsc(experiment_bin):
	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="sunsjsc_editor", window_title=_("Suns Jsc simulation editor"),json_search_path="sims.suns_jsc",icon="sunsjsc",json_config_postfix="config")

class window_ce(experiment_bin):
	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="ceexperiment_editor", window_title=_("Charge extraction experiment window"),json_search_path="sims.ce",json_config_postfix="config")

class pl_experiment(experiment_bin):

	def ribbon_simulation(self):
		toolbar = QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(42, 42))

		self.tb_lasers=tb_lasers()
		toolbar.addWidget(self.tb_lasers)

		return toolbar

	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="plexperiment_editor", window_title=_("PL experiment window"),json_search_path="sims.pl_ss",json_config_postfix="config")

		self.notebook.currentChanged.connect(self.switch_page)
		w=self.ribbon_simulation()
		self.ribbon.addTab(w,_("Simulation"))
		self.tb_lasers.laser_changed.connect(self.laser_changed)
		self.switch_page()
		
	def switch_page(self):
		tab = self.notebook.currentWidget()
		if tab!=None:
			json_path=self.bin.find_path_by_uid("sims.pl_ss",tab.uid)
			laser_name=self.bin.get_token_value(json_path+".config","pump_laser")
			self.tb_lasers.update(laser_name)

	def laser_changed(self,new_laser):
		tab = self.notebook.currentWidget()
		if tab!=None:
			json_path=self.bin.find_path_by_uid("sims.pl_ss",tab.uid)
			self.bin.set_token_value(json_path+".config","pump_laser",new_laser)
			self.bin.save()

class lasers(experiment_bin):
	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="laser_editor", window_title=_("Laser editor"),json_search_path="optical.lasers",json_config_postfix="config")

class spm_experiment(experiment_bin):
	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="spmexperiment_editor", window_title=_("Scanning probe microscopy editor"),json_search_path="sims.spm",icon="spm",json_config_postfix="config")

class window_fdtd(experiment_bin):
	def __init__(self):
		experiment_bin.__init__(self,"tab_fdtd",window_save_name="window_fdtd", window_title=_("FDTD Editor"),json_search_path="sims.fdtd",icon="fdtd")

class cv_experiment(experiment_bin):
	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="cvexperiment_editor", window_title=_("CV experiment window"),json_search_path="sims.cv",json_config_postfix="config")

class window_equilibrium(experiment_bin):
	def __init__(self):
		experiment_bin.__init__(self,"tab_jv",window_save_name="equilibrium", window_title=_("Electrical equilibrium solver"),json_search_path="sims.equilibrium",icon="equilibrium")

class window_mode(experiment_bin):
	def __init__(self,data=None):
		experiment_bin.__init__(self,"tab_jv",window_save_name="window_mode", window_title=_("mode Editor"),json_search_path="sims.mode",icon="mode",json_config_postfix="config")

class ray_trace_editor(experiment_bin):
	def __init__(self,data=None):
		experiment_bin.__init__(self,"tab_jv",window_save_name="window_ray", window_title=_("Ray trace editor"),json_search_path="sims.ray",icon="ray",json_config_postfix="config")

class fxexperiment(experiment_bin):

	def __init__(self):
		experiment_bin.__init__(self,"fxexperiment_tab",window_save_name="fx_domain_experiment", window_title=_("Frequency domain experiment window"),json_search_path="sims.fx_domain")

class window_probes(experiment_bin):

	def __init__(self):
		experiment_bin.__init__(self,window_save_name="window_probes", window_title=_("Probes"), name_of_tab_class="tab_probes",json_search_path="dump.probes",icon="map_pin")
		self.setMinimumWidth(900)



