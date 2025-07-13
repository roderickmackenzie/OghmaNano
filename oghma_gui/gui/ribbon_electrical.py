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

#qt
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

from help import help_window

from global_objects import global_object_register

from g_open import g_open
from QAction_lock import QAction_lock

from lock import get_lock
from cal_path import sim_paths
from tb_item_solvers import tb_item_solvers
from ribbon_page import ribbon_page
from config_window import class_config_window
from lock import get_lock
from ribbon_page import ribbon_page2
from json_c import json_tree_c

class ribbon_electrical(ribbon_page2):
	def __init__(self):
		ribbon_page2.__init__(self)
		self.bin=json_tree_c()
		self.enabled=False
		self.config_window=None
		self.electrical_mesh=None
		self.electrical_interfaces=None
		self.doping_window=None
		self.parasitic_window=None
		self.gradients_window=None
		self.window_code_editor=None
		self.window_exciton_config=None
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

		self.exciton = QAction_lock("exciton", _("Exciton\nsolver"), self,"ribbon_device_exciton")
		self.exciton.clicked.connect(self.callback_exciton)
		self.exciton.setCheckable(True)

		self.menu_exciton = QMenu(self)
		self.exciton.setMenu(self.menu_exciton)
		pan.addAction(self.exciton)
		button = pan.widgetForAction(self.exciton)
		button.setMinimumWidth(80)

		configure_item=QAction(_("Configure"), self)
		self.menu_exciton.addAction(configure_item)
		configure_item.triggered.connect(self.callback_configure_exciton)

		micro_code=QAction(_("Edit microcode"), self)
		self.menu_exciton.addAction(micro_code)
		micro_code.triggered.connect(self.callback_exciton_micro_code)

		self.mesh = QAction_lock("mesh", _("Electrical\nmesh"), self,"ribbon_config_mesh")
		self.mesh.triggered.connect(self.callback_edit_mesh)
		pan.addAction(self.mesh)

		self.boundary = QAction_lock("boundary", _("Boundary\nConditions"), self,"ribbon_electrical_boundary")
		self.boundary.clicked.connect(self.callback_boundary)
		pan.addAction(self.boundary)
		global_object_register("ribon_electrical_update_buttons",self.update_buttons)

	def update(self):
		self.close_window(self.electrical_mesh)
		self.close_window(self.config_window)
		self.close_window(self.doping_window)
		self.close_window(self.gradients_window)
		self.close_window(self.parasitic_window)
		self.close_window(self.electrical_interfaces)
		self.close_window(self.window_code_editor)
		self.close_window(self.window_exciton_config)
		self.tb_solvers.update()
		self.update_buttons()


	def update_buttons(self):
		solver_type=self.bin.get_token_value("electrical_solver","solver_type")
		perovskite_enabled=self.bin.get_token_value("perovskite","perovskite_enabled")
		exciton_enabled=self.bin.get_token_value("exciton","exciton_enabled")
		if self.enabled==True:
			if solver_type=="drift-diffusion":
				self.mesh.setEnabled(True)
				self.doping.setEnabled(True)
				self.gradients.setEnabled(True)
				self.interfaces.setEnabled(True)
				self.parasitic.setEnabled(True)
				self.boundary.setEnabled(True)
				self.perovskite.setEnabled(True)
				self.perovskite.setChecked(perovskite_enabled)
				self.exciton.setEnabled(True)
				self.exciton.setChecked(exciton_enabled)
			elif solver_type=="poisson":
				self.mesh.setEnabled(True)
				self.doping.setEnabled(True)
				self.gradients.setEnabled(True)
				self.interfaces.setEnabled(False)
				self.parasitic.setEnabled(False)
				self.boundary.setEnabled(True)
				self.perovskite.setEnabled(False)
				self.perovskite.setChecked(perovskite_enabled)
				self.exciton.setEnabled(False)
				self.exciton.setChecked(exciton_enabled)
			elif solver_type=="circuit":
				self.mesh.setEnabled(True)
				self.doping.setEnabled(False)
				self.gradients.setEnabled(False)
				self.interfaces.setEnabled(False)
				self.parasitic.setEnabled(False)
				self.boundary.setEnabled(False)
				self.perovskite.setEnabled(False)
				self.perovskite.setChecked(perovskite_enabled)
				self.exciton.setEnabled(False)
				self.exciton.setChecked(exciton_enabled)
			else:
				self.mesh.setEnabled(False)
				self.doping.setEnabled(False)
				self.gradients.setEnabled(False)
				self.interfaces.setEnabled(False)
				self.parasitic.setEnabled(False)
				self.boundary.setEnabled(False)
				self.perovskite.setEnabled(False)
				self.perovskite.setChecked(False)		
				self.exciton.setEnabled(False)
				self.exciton.setChecked(False)	
		

	def callback_perovskite(self):
		self.bin.set_token_value("perovskite","perovskite_enabled",self.perovskite.isChecked())
		self.bin.save()

	def callback_exciton(self):
		self.bin.set_token_value("exciton","exciton_enabled",self.exciton.isChecked())
		self.bin.save()

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
		self.exciton.setEnabled(val)
		self.update_buttons()

	def callback_edit_mesh(self):
		from window_mesh_editor import window_mesh_editor
		help_window().help_set_help("mesh.png",_("<big><b>Mesh editor</b></big>\nUse this window to setup the mesh, the window can also be used to change the dimensionality of the simulation."))
		self.close_window(self.electrical_mesh)
		self.electrical_mesh=window_mesh_editor(json_path_to_mesh="electrical_solver.mesh")

		self.show_window(self.electrical_mesh)

	def callback_interfaces(self):
		from interface_editor import interface_editor
		help_window().help_set_help("interfaces.png",_("<big><b>Interface editor</b></big>\nUse this window to edit how electrical interfaces behave."))

		self.close_window(self.electrical_interfaces)
		self.electrical_interfaces=interface_editor()

		self.electrical_interfaces.show()
		self.electrical_interfaces.setWindowState(Qt.WindowNoState)

	def callback_boundary(self):
		self.config_window=class_config_window(["electrical_solver.boundary","exciton.exciton_boundary"],[_("Electrical boundary conditions"),_("Excitonic boundary conditions")],title=_("Electrical boundary conditions"),icon="electrical")
		self.show_window(self.config_window)

	def callback_doping(self):
		from doping import doping_window
		help_window().help_set_help("doping.png",_("<big><b>Doping window</b></big>\nUse this window to add doping to the simulation"))

		self.close_window(self.doping_window)
		self.doping_window=doping_window()

		self.show_window(self.doping_window)

	def callback_gradients(self):
		from window_material_gradients import window_material_gradients
		help_window().help_set_help("gradients.png",_("<big><b>Gradients window</b></big>\nUse this window to add doping to the simulation"))

		self.close_window(self.gradients_window)
		self.gradients_window=window_material_gradients()

		self.show_window(self.gradients_window)


	def callback_parasitic(self):
		from parasitic import parasitic
		help_window().help_set_help("parasitic.png",_("<big><b>Parasitic components</b></big>\nUse this window to edit the shunt and series resistance."))

		self.close_window(self.parasitic_window)
		self.parasitic_window=parasitic()

		self.show_window(self.parasitic_window)


	def callback_configure_exciton(self):
		self.window_exciton_config=class_config_window(["exciton"],[_("Exciton solver")],title=_("Exciton configuration"),icon="exciton")
		self.window_exciton_config.show()

	def callback_exciton_micro_code(self):
		from window_code_editor import window_code_editor
		self.window_code_editor=window_code_editor()
		self.window_code_editor.show()

