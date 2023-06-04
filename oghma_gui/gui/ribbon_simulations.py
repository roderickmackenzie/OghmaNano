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

## @package ribbon_simulations
#  The main time domain ribbon.
#


from icon_lib import icon_get

from cal_path import get_css_path

#qt

from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

from help import help_window

#experiments
from sunsvoc import sunsvoc
from sunsjsc import sunsjsc

from util import wrap_text
from global_objects import global_object_run
from gQtCore import gSignal
from QAction_lock import QAction_lock
from cal_path import sim_paths
from lock import get_lock
from json_root import json_root
from ribbon_page import ribbon_page

class ribbon_simulations(ribbon_page):
	experiments_changed = gSignal()

	def __init__(self):
		ribbon_page.__init__(self)

		self.jvexperiment_window=None
		self.exciton_window=None
		self.experiment_window=None
		self.fxexperiment_window=None
		self.capacitance_voltage_window=None

		self.sunsvocexperiment_window=None
		self.sunsjsc_experiment_window=None
		self.ce_experiment_window=None

		self.qe_window=None
		self.solar_spectrum_window=None
		self.cost_window=None

		self.plexperiment_window=None
		self.spm_window=None
		self.server_config_window=None
		self.equilibrium_window=None
		self.window_output_files=None

		self.jv = QAction_lock("jv", _("JV\neditor"), self,"ribbon_simulations_jv")
		self.jv.clicked.connect(self.callback_jv_window)
		if sim_paths.is_plugin("jv")==True:
			self.addAction(self.jv)

		self.time = QAction_lock("time", _("Time domain\neditor."), self,"ribbon_simulations_time")
		self.time.clicked.connect(self.callback_edit_experiment_window)
		if sim_paths.is_plugin("time_domain")==True:
			self.addAction(self.time )

		self.fx = QAction_lock("spectrum", _("FX domain\neditor"), self,"ribbon_simulations_spectrum")
		self.fx.clicked.connect(self.callback_fxexperiment_window)
		if sim_paths.is_plugin("fx_domain")==True:
			self.addAction(self.fx)

		self.capacitance_voltage = QAction_lock("cv", _("CV\neditor"), self,"ribbon_capacitance_voltage")
		self.capacitance_voltage.clicked.connect(self.callback_capacitance_voltage)
		if sim_paths.is_plugin("cv")==True:
			self.addAction(self.capacitance_voltage)

		self.sunsvoc = QAction_lock("sunsvoc", _("Suns Voc\neditor"), self,"ribbon_simulations_sunsvoc")
		self.sunsvoc.clicked.connect(self.callback_sunsvoc_window)
		if sim_paths.is_plugin("suns_voc")==True:
			self.addAction(self.sunsvoc)

		self.sunsjsc = QAction_lock("sunsjsc", _("Suns Jsc\neditor"), self,"ribbon_simulations_sunsjsc")
		self.sunsjsc.clicked.connect(self.callback_sunsjsc_window)
		if sim_paths.is_plugin("suns_jsc")==True:
			self.addAction(self.sunsjsc)

		self.ce = QAction_lock("ce", _("CE\neditor"), self,"ribbon_simulations_ce")
		self.ce.clicked.connect(self.callback_ce_window)
		if sim_paths.is_plugin("ce")==True:
			self.addAction(self.ce)


		self.pl = QAction_lock("pl", _("PL\neditor"), self,"ribbon_simulations_pl")
		self.pl.clicked.connect(self.callback_pl_window)
		if sim_paths.is_plugin("pl_ss")==True:
			self.addAction(self.pl)

		self.exciton = QAction_lock("exciton", _("Exciton\neditor"), self,"ribbon_simulations_exciton")
		self.exciton.clicked.connect(self.callback_exciton_window)
		if sim_paths.is_plugin("exciton")==True:
			self.addAction(self.exciton)

		self.qe = QAction_lock("qe", _("Quantum\nefficiency"), self,"ribbon_simulations_qe")
		self.qe.clicked.connect(self.callback_qe_window)
		if sim_paths.is_plugin("eqe")==True:
			self.addAction(self.qe)

		self.equilibrium = QAction_lock("equilibrium", _("Electrical\nequilibrium"), self,"ribbon_simulations_equilibrium")
		self.equilibrium.clicked.connect(self.callback_equilibrium_window)
		if sim_paths.is_plugin("equilibrium")==True:
			self.addAction(self.equilibrium)

		#self.qe.setVisible(False)

		self.addSeparator()

		self.tb_cost = QAction_lock("cost", _("Calculate\nthe cost"), self,"ribbon_simulations_cost")
		self.tb_cost.clicked.connect(self.callback_cost)
		self.addAction(self.tb_cost)

		self.addSeparator()

		self.spm = QAction_lock("spm", _("scanning probe\nmicroscopy"), self,"ribbon_simulations_spm")
		self.spm.clicked.connect(self.callback_spm_window)
		if sim_paths.is_plugin("spm")==True:
			self.addAction(self.spm)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.addWidget(spacer)

		self.tb_output = QAction_lock("hdd_custom", _("Output\nFiles"), self,"output_files")
		self.tb_output.clicked.connect(self.callback_output)
		self.addAction(self.tb_output)

		self.server_config = QAction_lock("cpu", _("Simulation\nHardware"), self,"server_config")
		self.server_config.clicked.connect(self.callback_server_config)
		self.addAction(self.server_config)

	def callback_experiments_changed(self):
		self.experiments_changed.emit()

	def update(self):
		if self.qe_window!=None:
			del self.qe_window
			self.qe_window=None

		if self.experiment_window!=None:
			del self.experiment_window
			self.experiment_window=None

		if self.fxexperiment_window!=None:
			del self.fxexperiment_window
			self.fxexperiment_window=None

		if self.capacitance_voltage_window!=None:
			del self.capacitance_voltage_window
			self.capacitance_voltage_window=None

		if self.solar_spectrum_window!=None:
			del self.solar_spectrum_window
			self.solar_spectrum_window=None

		if self.cost_window!=None:
			del self.cost_window
			self.cost_window=None

		if self.spm_window!=None:
			del self.spm_window
			self.spm_window=None

		if self.jvexperiment_window!=None:
			del self.jvexperiment_window
			self.jvexperiment_window=None

		if self.exciton_window!=None:
			del self.exciton_window
			self.exciton_window=None

		if self.window_output_files!=None:
			del self.window_output_files
			self.window_output_files=None

		#self.mode.update()

	def setEnabled(self,val):

		self.time.setEnabled(val)
		self.fx.setEnabled(val)
		self.capacitance_voltage.setEnabled(val)

		self.qe.setEnabled(val)
		#self.mode.setEnabled(val)
		self.tb_cost.setEnabled(val)
		self.sunsvoc.setEnabled(val)
		self.sunsjsc.setEnabled(val)
		self.ce.setEnabled(val)
		self.pl.setEnabled(val)
		self.spm.setEnabled(val)
		self.jv.setEnabled(val)
		self.exciton.setEnabled(val)
		self.server_config.setEnabled(val)
		self.tb_output.setEnabled(val)

	def callback_edit_experiment_window(self):
		from time_domain_experiment import time_domain_experiment
		if self.experiment_window==None:
			self.experiment_window=time_domain_experiment()
			self.experiment_window.changed.connect(self.callback_experiments_changed)
			
		help_window().help_set_help(["time.png",_("<big><b>The time mesh editor</b></big><br> To do time domain simulations one must define how voltage the light vary as a function of time.  This can be done in this window.  Also use this window to define the simulation length and time step.")])
		self.show_window(self.experiment_window)
 
	def callback_fxexperiment_window(self):
		from fxexperiment import fxexperiment
		if self.fxexperiment_window==None:
			self.fxexperiment_window=fxexperiment()

		help_window().help_set_help(["spectrum.png",_("<big><b>Frequency domain mesh editor</b></big><br> Some times it is useful to do frequency domain simulations such as when simulating impedance spectroscopy.  This window will allow you to choose which frequencies will be simulated.")])
		self.show_window(self.fxexperiment_window)
		
	def callback_capacitance_voltage(self):
		from cv_experiment import cv_experiment
		if self.capacitance_voltage_window==None:
			self.capacitance_voltage_window=cv_experiment()
			
		help_window().help_set_help(["cv.png",_("<big><b>Capacitance voltage editor</b></big><br> Use this editor to change serup capacitance voltage simulation.")])
		self.show_window(self.capacitance_voltage_window)


	def callback_spm_window(self):
		from spm_experiment import spm_experiment
		if self.spm_window==None:
			self.spm_window=spm_experiment()

		help_window().help_set_help(["spm.png",_("<big><b>Scanning probe microscopy</b></big><br> Use this window to configure the scanning probe microscopy simulations.")])
		self.show_window(self.spm_window)


	def callback_pl_window(self):
		from pl_experiment import pl_experiment
		if self.plexperiment_window==None:
			self.plexperiment_window=pl_experiment()
			#self.experiment_window.changed.connect(self.callback_experiments_changed)

		help_window().help_set_help(["pl.png",_("<big><b>PL simulation editor</b></big><br> Use this window to configure the steady state photoluminescence simulation."),"youtube",_("<big><b><a href=\"https://www.youtube.com/watch?v=pgaJg6dErP4\">Watch the youtube video</a></b></big><br>Watch the video on perfomring PL simulation.")])
		self.show_window(self.plexperiment_window)


	def callback_sunsvoc_window(self):

		if self.sunsvocexperiment_window==None:
			self.sunsvocexperiment_window=sunsvoc()

		help_window().help_set_help(["jv.png",_("<big><b>Suns voc simulation editor</b></big><br> Use this window to select the step size and parameters of the JV simulations.")])
		self.show_window(self.sunsvocexperiment_window)


	def callback_sunsjsc_window(self):

		if self.sunsjsc_experiment_window==None:
			self.sunsjsc_experiment_window=sunsjsc()

		help_window().help_set_help(["jv.png",_("<big><b>Suns Jsc simulation editor</b></big><br> Use this window to select the step size and parameters of the JV simulations.")])
		self.show_window(self.sunsjsc_experiment_window)

	def callback_ce_window(self):
		from window_ce import window_ce
		if self.ce_experiment_window==None:
			self.ce_experiment_window=window_ce()

		help_window().help_set_help(["ce.png",_("<big><b>Charge Extraction editor</b></big><br> This performs charge extraction experiments in time domain, accounting for recombination losses.  If you don’t mind about accounting for recombination losses on extraction just run a JV curve or a Suns-Voc simulation and use the charge.dat file.")])

		self.show_window(self.ce_experiment_window)
	
	def callback_qe_window(self, widget):
		from window_eqe import window_eqe
		if self.qe_window==None:
			self.qe_window=window_eqe()

		self.show_window(self.qe_window)

	def callback_equilibrium_window(self, widget):
		from window_equilibrium import window_equilibrium
		if self.equilibrium_window==None:
			self.equilibrium_window=window_equilibrium()

		self.show_window(self.equilibrium_window)

	def callback_cost(self):
		from cost import cost
		help_window().help_set_help(["cost.png",_("<big><b>Costs window</b></big>\nUse this window to calculate the cost of the solar cell and the energy payback time.")])

		if self.cost_window==None:
			self.cost_window=cost()

		self.show_window(self.cost_window)

	def callback_jv_window(self):
		from jv_experiment import jv_experiment
		if self.jvexperiment_window==None:
			self.jvexperiment_window=jv_experiment()
			#self.experiment_window.changed.connect(self.callback_experiments_changed)

		help_window().help_set_help(["jv.png",_("<big><b>JV simulation editor</b></big><br> Use this window to configure JV simulations.")])

		self.show_window(self.jvexperiment_window)

	def callback_exciton_window(self):
		from window_exciton import window_exciton
		if self.exciton_window==None:
			self.exciton_window=window_exciton()
			#self.experiment_window.changed.connect(self.callback_experiments_changed)

		help_window().help_set_help(["exciton.png",_("<big><b>Exciton simulation editor</b></big><br> Use this window to configure exciton simulations.")])
		self.show_window(self.exciton_window)

	def callback_server_config(self):
		help_window().help_set_help(["cpu.png",_("<big><b>Simulation hardware</b></big><br>Use this window to change how the model uses the computer's hardware.")])


		if self.server_config_window==None:
			from server_config import server_config
			self.server_config_window=server_config()

		self.show_window(self.server_config_window)

	def callback_output(self):
		from tab_banned_files import tab_banned_files
		from config_window import class_config_window
		data=json_root()
		self.window_output_files=class_config_window([data.dump],[_("Output files")],title=_("Output files"),icon="newton")

		tab=tab_banned_files()
		self.window_output_files.notebook.addTab(tab,_("Banned files and tokens"))
		self.window_output_files.show()
