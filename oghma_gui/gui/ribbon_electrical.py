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
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget

from help import help_window

from global_objects import global_object_register

from g_open import g_open
from QAction_lock import QAction_lock

from lock import get_lock
from json_root import json_root
from cal_path import sim_paths
from tb_item_solvers import tb_item_solvers
from ribbon_page import ribbon_page
from config_window import class_config_window
from lock import get_lock
from ribbon_page import ribbon_page2

class ribbon_electrical(ribbon_page2):
	def __init__(self):
		ribbon_page2.__init__(self)
		self.enabled=False
		self.config_window=None
		self.electrical_mesh=None
		self.electrical_interfaces=None
		self.doping_window=None
		self.parasitic_window=None
		self.gradients_window=None

		
		pan=self.add_panel()

		self.doping = QAction_lock("doping", _("Doping/\nIons"), self,"ribbon_device_doping")
		self.doping.clicked.connect(self.callback_doping)
		pan.addAction(self.doping)

		self.gradients = QAction_lock("gradients", _("Material\nGradients"), self,"gradients")
		self.gradients.clicked.connect(self.callback_gradients)
		pan.addAction(self.gradients)

		self.interfaces = QAction_lock("interfaces", _("Interfaces"), self,"ribbon_config_interfaces")
		self.interfaces.triggered.connect(self.callback_interfaces)
		pan.addAction(self.interfaces)

		self.parasitic = QAction_lock("parasitic", _("Parasitic\n components"), self,"ribbon_device_parasitic")
		self.parasitic.clicked.connect(self.callback_parasitic)
		pan.addAction(self.parasitic)

		if pan.iconSize().width()>24:
			self.tb_solvers=tb_item_solvers()
		else:
			self.tb_solvers=tb_item_solvers(orientation=Qt.Horizontal)

		pan.addWidget(self.tb_solvers)
		self.tb_solvers.changed.connect(self.update_buttons)

		self.perovskite = QAction_lock("perovskite", _("Mobile\nIon solver"), self,"ribbon_device_mobile_ion")
		self.perovskite.clicked.connect(self.callback_perovskite)
		self.perovskite.setCheckable(True)
		pan.addAction(self.perovskite)

		self.singlet = QAction_lock("singlet", _("Excited\nstates"), self,"ribbon_device_mobile_singlet")
		self.singlet.clicked.connect(self.callback_singlet)
		self.singlet.setCheckable(True)
		if get_lock().is_next()==True:
			pan.addAction(self.singlet)

		self.mesh = QAction_lock("mesh", _("Electrical\nmesh"), self,"ribbon_config_mesh")
		self.mesh.triggered.connect(self.callback_edit_mesh)
		pan.addAction(self.mesh)

		self.boundary = QAction_lock("boundary", _("Boundary\nConditions"), self,"ribbon_electrical_boundary")
		self.boundary.clicked.connect(self.callback_boundary)
		pan.addAction(self.boundary)

		#a.setStyleSheet("QToolBar {margin-top: 0px;margin-bottom: 0px; padding 0px;}")
#		spacer = QWidget()
#		spacer.setMinimumSize(100,20)
#		self.addWidget(spacer)


	def update(self):
		if self.electrical_mesh!=None:
			self.electrical_mesh.hide()
			del self.electrical_mesh
			self.electrical_mesh=None

		if self.config_window!=None:
			self.config_window.hide()
			del self.config_window
			self.config_window=None

		if self.doping_window!=None:
			self.doping_window.hide()
			del self.doping_window
			self.doping_window=None

		if self.gradients_window!=None:
			self.gradients_window.hide()
			del self.gradients_window
			self.gradients_window=None

		if self.parasitic_window!=None:
			self.parasitic_window.hide()
			del self.parasitic_window
			self.parasitic_window=None

		if self.electrical_interfaces!=None:
			self.electrical_interfaces.hide()
			del self.electrical_interfaces
			self.electrical_interfaces=None

		self.tb_solvers.update()
		self.update_buttons()


	def update_buttons(self):
		data=json_root()
		if self.enabled==True:
			if data.electrical_solver.solver_type=="drift-diffusion":
				self.mesh.setEnabled(True)
				self.doping.setEnabled(True)
				self.gradients.setEnabled(True)
				self.interfaces.setEnabled(True)
				self.parasitic.setEnabled(True)
				self.boundary.setEnabled(True)
				self.perovskite.setEnabled(True)
				self.singlet.setEnabled(True)
			elif data.electrical_solver.solver_type=="poisson":
				self.mesh.setEnabled(True)
				self.doping.setEnabled(True)
				self.gradients.setEnabled(True)
				self.interfaces.setEnabled(False)
				self.parasitic.setEnabled(False)
				self.boundary.setEnabled(True)
				self.perovskite.setEnabled(False)
				self.singlet.setEnabled(False)
			elif data.electrical_solver.solver_type=="circuit":
				self.mesh.setEnabled(True)
				self.doping.setEnabled(False)
				self.gradients.setEnabled(False)
				self.interfaces.setEnabled(False)
				self.parasitic.setEnabled(False)
				self.boundary.setEnabled(False)
				self.perovskite.setEnabled(False)
				self.singlet.setEnabled(False)
			else:
				self.mesh.setEnabled(False)
				self.doping.setEnabled(False)
				self.gradients.setEnabled(False)
				self.interfaces.setEnabled(False)
				self.parasitic.setEnabled(False)
				self.boundary.setEnabled(False)
				self.perovskite.setEnabled(False)
				self.singlet.setEnabled(False)

		self.perovskite.setChecked(data.perovskite.perovskite_enabled)
		self.singlet.setChecked(data.singlet.singlet_enabled)

	def callback_perovskite(self):
		data=json_root()
		data.perovskite.perovskite_enabled=self.perovskite.isChecked()
		data.save()

	def callback_singlet(self):
		data=json_root()
		data.singlet.singlet_enabled=self.singlet.isChecked()
		data.save()

	def setEnabled(self,val):
		self.enabled=val
		self.mesh.setEnabled(val)
		self.doping.setEnabled(val)
		self.gradients.setEnabled(val)
		self.interfaces.setEnabled(val)
		self.parasitic.setEnabled(val)
		self.tb_solvers.setEnabled(val)
		self.boundary.setEnabled(val)
		self.perovskite.setEnabled(val)
		self.singlet.setEnabled(val)
		self.update_buttons()



	def callback_edit_mesh(self):
		from window_mesh_editor import window_mesh_editor
		help_window().help_set_help(["mesh.png",_("<big><b>Mesh editor</b></big>\nUse this window to setup the mesh, the window can also be used to change the dimensionality of the simulation.")])

		if self.electrical_mesh==None:
			self.electrical_mesh=window_mesh_editor(json_path_to_mesh="json_root().electrical_solver.mesh")

		self.show_window(self.electrical_mesh)

	def callback_interfaces(self):
		from interface_editor import interface_editor
		help_window().help_set_help(["interfaces.png",_("<big><b>Interface editor</b></big>\nUse this window to edit how electrical interfaces behave.")])

		if self.electrical_interfaces==None:
			self.electrical_interfaces=interface_editor()

		self.electrical_interfaces.show()
		self.electrical_interfaces.setWindowState(Qt.WindowNoState)

	def callback_boundary(self):
		data=json_root()
		self.config_window=class_config_window([data.electrical_solver.boundary,data.exciton.exciton_boundary],[_("Electrical boundary conditions"),_("Excitonic boundary conditions")],title=_("Electrical boundary conditions"),icon="electrical")
		self.show_window(self.config_window)

	def callback_doping(self):
		from doping import doping_window
		help_window().help_set_help(["doping.png",_("<big><b>Doping window</b></big>\nUse this window to add doping to the simulation")])

		if self.doping_window==None:
			self.doping_window=doping_window()

		self.show_window(self.doping_window)

	def callback_gradients(self):
		from window_material_gradients import window_material_gradients
		help_window().help_set_help(["gradients.png",_("<big><b>Gradients window</b></big>\nUse this window to add doping to the simulation")])

		if self.gradients_window==None:
			self.gradients_window=window_material_gradients()

		self.show_window(self.gradients_window)


	def callback_parasitic(self):
		from parasitic import parasitic
		help_window().help_set_help(["parasitic.png",_("<big><b>Parasitic components</b></big>\nUse this window to edit the shunt and series resistance.")])

		if self.parasitic_window==None:
			self.parasitic_window=parasitic()

		self.show_window(self.parasitic_window)

