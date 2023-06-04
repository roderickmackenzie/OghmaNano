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

## @package ribbon_electrical
#  The configure ribbon.
#


from icon_lib import icon_get

from cal_path import get_css_path

#qt
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

from config_window import class_config_window

from help import help_window

from global_objects import global_object_register

from g_open import g_open
from QAction_lock import QAction_lock
from lock import get_lock
from json_root import json_root
from cal_path import sim_paths
from ribbon_page import ribbon_page
from ribbon_electrical import ribbon_page2
from fx_selector import fx_selector
from util import wrap_text
from tb_item_sun import tb_item_sun

class ribbon_optical(ribbon_page2):
	def __init__(self):
		ribbon_page2.__init__(self)
		self.enabled=False
		self.light_sources_window=None
		self.ray_trace_window=None
		self.detectors_window=None
		self.fdtd_window=None
		self.mode_window=None
		self.optical_mesh=None
		self.transfer_matrix_window=None
		pan=self.add_panel()
		self.light_sources = QAction_lock("lighthouse", _("Light\nSources"), self,"ribbon_home_light_sources")
		self.light_sources.clicked.connect(self.callback_light_sources)
		pan.addAction(self.light_sources)


		self.lasers = QAction_lock("lasers", _("Lasers\n(fs)"), self,"ribbion_db_lasers")
		self.lasers.clicked.connect(self.callback_configure_lasers)
		pan.addAction(self.lasers)

		if pan.iconSize().width()>24:
			self.sun=tb_item_sun()
		else:
			self.sun=tb_item_sun(layout=QHBoxLayout())

		pan.addWidget(self.sun)


		pan.addSeparator()

		self.transfer_matrix = QAction_lock("optics", _("Transfer\nMatrix"), self,"ribbon_home_optics")
		self.transfer_matrix.clicked.connect(self.callback_transfer_matrix)
		pan.addAction(self.transfer_matrix)

		self.ray_trace = QAction_lock("ray", wrap_text(_("Ray tracing\neditor"),8), self,"ribbon_simulations_ray")
		self.ray_trace.clicked.connect(self.callback_ray_tracing_window)
		if sim_paths.is_plugin("trace")==True:
			pan.addAction(self.ray_trace)

		self.detector = QAction_lock("ccd", _("Optical\nDetectors"), self,"ribbon_home_optics")
		self.detector.clicked.connect(self.callback_detector)
		pan.addAction(self.detector)

		self.fdtd = QAction_lock("fdtd", _("FDTD\nSimulation"), self,"ribbon_simulations_fdtd")
		self.fdtd.clicked.connect(self.callback_fdtd)
		pan.addAction(self.fdtd)

		self.mode = QAction_lock("mode_fiber", _("Mode\nCalculator"), self,"ribbon_simulations_mode")
		self.mode.clicked.connect(self.callback_mode)
		pan.addAction(self.mode)

		if pan.iconSize().width()>24:
			self.fx_box=fx_selector()
		else:
			self.fx_box=fx_selector(layout=QHBoxLayout())
		
		self.fx_box.update()
		global_object_register("main_fx_box",self.fx_box)

		pan.addWidget(self.fx_box)

		self.mesh = QAction_lock("mesh", _("Optical\nmesh"), self,"ribbon_config_mesh")
		self.mesh.triggered.connect(self.callback_edit_mesh)
		pan.addAction(self.mesh)

		self.boundary = QAction_lock("boundary", _("Boundary\nConditions"), self,"ribbon_optical_boundary")
		self.boundary.clicked.connect(self.callback_boundary)
		pan.addAction(self.boundary)

		self.lasers_window=None

	def update(self):
		if self.light_sources_window!=None:
			del self.light_sources_window
			self.light_sources_window=None

		if self.lasers_window!=None:
			del self.lasers_window
			self.lasers_window=None

		if self.transfer_matrix_window!=None:
			del self.transfer_matrix_window
			self.transfer_matrix_window=None

		self.sun.update()
		self.fx_box.update()

	def setEnabled(self,val):
		self.light_sources.setEnabled(val)
		self.lasers.setEnabled(val)
		self.sun.setEnabled(val)
		self.ray_trace.setEnabled(val)
		self.detector.setEnabled(val)
		self.fdtd.setEnabled(val)
		self.mode.setEnabled(val)
		self.fx_box.setEnabled(val)
		self.boundary.setEnabled(val)
		self.mesh.setEnabled(val)
		self.transfer_matrix.setEnabled(val)

	def callback_configure_lasers(self):
		from lasers import lasers
		data=json_root()
		if self.lasers_window==None:
			self.lasers_window=lasers(data.optical.lasers)

		help_window().help_set_help(["lasers.png",_("<big><b>Laser setup</b></big><br> Use this window to set up your lasers.")])
		if self.lasers_window.isVisible()==True:
			self.lasers_window.hide()
		else:
			self.lasers_window.show()

	def callback_light_sources(self):
		help_window().help_set_help(["lighthouse.png",_("<big><b>The light sources window</b></big><br>Use this window to setup optical sources for the transfer matrix, ray tracing and FDTD simulations.")])


		if self.light_sources_window==None:
			from window_light_src import window_light_src
			self.light_sources_window=window_light_src()
			#self.notebook.changed.connect(self.optics_window.update)

		if self.light_sources_window.isVisible()==True:
			self.light_sources_window.hide()
		else:
			self.light_sources_window.show()

	def callback_ray_tracing_window(self):

		if self.ray_trace_window==None:
			from ray_trace_editor import ray_trace_editor
			self.ray_trace_window=ray_trace_editor()

		help_window().help_set_help(["ray.png",_("<big><b>The ray tracing editor</b></big><br> Use this window to configure ray tracing.")])
		if self.ray_trace_window.isVisible()==True:
			self.ray_trace_window.hide()
		else:
			self.ray_trace_window.show()

	def callback_detector(self):
		help_window().help_set_help(["ccd.png",_("<big><b>The detectors window</b></big><br>Use this window to setup optical detectors.  These can be used for the ray tracing simulations.")])


		if self.detectors_window==None:
			from detectors_editor import detectors_editor
			self.detectors_window=detectors_editor()

		if self.detectors_window.isVisible()==True:
			self.detectors_window.hide()
		else:
			self.detectors_window.ribbon.update()
			self.detectors_window.show()

	def callback_fdtd(self):
		from window_fdtd import window_fdtd
		if self.fdtd_window==None:
			self.fdtd_window=window_fdtd()

		help_window().help_set_help(["fdtd.png",_("<big><b>FDTD</b></big><br> Use this window to setup a finite difference time domain simulation.")])
		if self.fdtd_window.isVisible()==True:
			self.fdtd_window.hide()
		else:
			self.fdtd_window.show()

	def callback_mode(self):
		from window_mode import window_mode
		if self.mode_window==None:
			self.mode_window=window_mode()

		help_window().help_set_help(["mode_fiber.png",_("<big><b>Mode calculator</b></big><br> Use this window to setup a the optical mode calculator.")])
		if self.mode_window.isVisible()==True:
			self.mode_window.hide()
		else:
			self.mode_window.show()

	def callback_edit_mesh(self):
		from window_mesh_editor import window_mesh_editor
		help_window().help_set_help(["mesh.png",_("<big><b>Mesh editor</b></big>\nUse this window to setup the mesh, the window can also be used to change the dimensionality of the simulation.")])

		if self.optical_mesh==None:
			self.optical_mesh=window_mesh_editor(json_path_to_mesh="json_root().optical.mesh",window_title=_("Optical Mesh Editor"))
		if self.optical_mesh.isVisible()==True:
			self.optical_mesh.hide()
		else:
			self.optical_mesh.show()

	def callback_boundary(self):
		data=json_root()
		self.config_window=class_config_window([data.optical.boundary],[_("Boundary conditions")],title=_("Boundary conditions"),icon="electrical")
		self.config_window.show()

	def callback_transfer_matrix(self):
		help_window().help_set_help(["optics.png",_("<big><b>The optical simulation window</b></big><br>Use this window to perform optical simulations.  Click on the play button to run a simulation."),"media-playback-start",_("Click on the play button to run an optical simulation.  The results will be displayed in the tabs to the right."),"youtube",_("<big><b><a href=\"https://www.youtube.com/watch?v=A_3meKTBuWk\">Tutorial video</b></big><br>Designing optical filters and reflective coatings.")])


		if self.transfer_matrix_window==None:
			from optics import class_optical
			self.transfer_matrix_window=class_optical()
			global_object_register("optics_force_redraw",self.transfer_matrix_window.force_redraw)
			self.transfer_matrix_window.ribbon.update()

		self.show_window(self.transfer_matrix_window)
