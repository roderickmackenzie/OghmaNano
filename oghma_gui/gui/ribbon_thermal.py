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

## @package ribbon_thermal
#  The thermal ribbon.
#


from icon_lib import icon_get

#qt
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

from help import help_window

from dlg_get_text2 import dlg_get_text2

from QAction_lock import QAction_lock
from thermal_isothermal_button import thermal_isothermal_button
from config_window import class_config_window

from ribbon_page import ribbon_page
from json_c import json_tree_c

class ribbon_thermal(ribbon_page):
	def __init__(self):
		ribbon_page.__init__(self)
		self.bin=json_tree_c()
		self.enabled=False
		self.optical_mesh=None
		self.config_window=None
		self.thermal_isothermal_button=thermal_isothermal_button(self)
		self.thermal_isothermal_button.triggered.connect(self.callback_thermal_isothermal_button)
		self.addAction(self.thermal_isothermal_button)

		self.addSeparator()

		self.temperature = QAction_lock("thermal", _("Set\nTemperature"), self,"ribbon_thermal_settemp")
		self.temperature.clicked.connect(self.callback_thermal)
		self.addAction(self.temperature)
		self.addSeparator()

		self.boundary = QAction_lock("boundary", _("Boundary\nConditions"), self,"ribbon_thermal_boundary")
		self.boundary.clicked.connect(self.callback_boundary)
		self.addAction(self.boundary)

		self.configure = QAction_lock("cog", _("Configure\nModel"), self,"ribbon_thermal_configure")
		self.configure.clicked.connect(self.callback_configure)
		self.addAction(self.configure)

		self.addSeparator()

		self.joule_heating = QAction_lock("joule_heating", _("Joule\nHeating"), self,"ribbon_thermal_joule")
		self.joule_heating.clicked.connect(self.callback_heating_click)
		self.joule_heating.setCheckable(True)
		self.addAction(self.joule_heating)

		self.parasitic_heating = QAction_lock("parasitic_heating", _("Parasitic\nHeating"), self,"ribbon_thermal_joule")
		self.parasitic_heating.clicked.connect(self.callback_heating_click)
		self.parasitic_heating.setCheckable(True)
		self.addAction(self.parasitic_heating)

		self.optical_heating = QAction_lock("optical_heating", _("Optical\nHeating"), self,"ribbon_thermal_optical")
		self.optical_heating.clicked.connect(self.callback_heating_click)
		self.optical_heating.setCheckable(True)
		self.addAction(self.optical_heating)

		self.recombination_heating = QAction_lock("recombination_heating", _("Recombination\nheating"), self,"ribbon_thermal_recombination")
		self.recombination_heating.clicked.connect(self.callback_heating_click)
		self.recombination_heating.setCheckable(True)
		self.addAction(self.recombination_heating)

		self.thermal_parameters = QAction_lock("thermal_kappa", _("Thermal\nparameters"), self,"ribbon_thermal_parameters")
		self.thermal_parameters.clicked.connect(self.callback_thermal_parameters)
		self.addAction(self.thermal_parameters)

		self.mesh = QAction_lock("mesh", _("Thermal\nmesh"), self,"ribbon_config_mesh")
		self.mesh.triggered.connect(self.callback_edit_mesh)
		self.addAction(self.mesh)

	def callback_thermal_parameters(self):
		help_window().help_set_help("thermal_kappa.png",_("<big><b>Thermal parameters</b></big>\nUse this window to change the thermal parameters of each layer."))

		from thermal_main import thermal_main
		self.thermal_editor=thermal_main()
		self.thermal_editor.show()

	def callback_heating_click(self):

		self.bin.set_token_value("thermal","joule_heating",str(self.joule_heating.isChecked()))
		self.bin.set_token_value("thermal","parasitic_heating",str(self.parasitic_heating.isChecked()))
		self.bin.set_token_value("thermal","optical_heating",str(self.optical_heating.isChecked()))
		self.bin.set_token_value("thermal","recombination_heating",str(self.recombination_heating.isChecked()))
		self.bin.save()

	def callback_thermal_isothermal_button(self):
		self.update()

	def callback_thermal(self):
		
		temp=self.bin.get_token_value("thermal","set_point")

		new_temp=dlg_get_text2( _("Enter the new temperature"), str(temp),"thermal.png")
		if new_temp.ret!=None:
			new_temp=float(new_temp.ret)
			self.bin.set_token_value("thermal","set_point",str(new_temp))
			self.bin.set_token_value("thermal.thermal_boundary","Ty0",str(new_temp))
			self.bin.set_token_value("thermal.thermal_boundary","Ty1",str(new_temp))
			self.bin.set_token_value("thermal.thermal_boundary","Tx0",str(new_temp))
			self.bin.set_token_value("thermal.thermal_boundary","Tx1",str(new_temp))
			self.bin.set_token_value("thermal.thermal_boundary","Tz0",str(new_temp))
			self.bin.set_token_value("thermal.thermal_boundary","Tz1",str(new_temp))
			self.bin.save()

	def update(self):
		if self.enabled==True:

			self.thermal_isothermal_button.refresh()
			if 	self.thermal_isothermal_button.thermal==False:
				self.temperature.setEnabled(True)
				self.boundary.setEnabled(False)
				self.configure.setEnabled(False)
				self.joule_heating.setEnabled(False)
				self.parasitic_heating.setEnabled(False)
				self.optical_heating.setEnabled(False)
				self.recombination_heating.setEnabled(False)
				self.thermal_isothermal_button.setEnabled(True)
				self.thermal_parameters.setEnabled(False)
				self.mesh.setEnabled(True)
			else:
				self.temperature.setEnabled(False)
				self.boundary.setEnabled(True)
				self.configure.setEnabled(True)
				self.joule_heating.setEnabled(True)
				self.parasitic_heating.setEnabled(True)
				self.optical_heating.setEnabled(True)
				self.recombination_heating.setEnabled(True)
				self.thermal_isothermal_button.setEnabled(True)
				self.thermal_parameters.setEnabled(True)
				self.mesh.setEnabled(True)

			self.joule_heating.setChecked(self.bin.get_token_value("thermal","joule_heating"))
			self.parasitic_heating.setChecked(self.bin.get_token_value("thermal","parasitic_heating"))
			self.optical_heating.setChecked(self.bin.get_token_value("thermal","optical_heating"))
			self.recombination_heating.setChecked(self.bin.get_token_value("thermal","recombination_heating"))
		else:
			self.temperature.setEnabled(False)
			self.boundary.setEnabled(False)
			self.configure.setEnabled(False)
			self.joule_heating.setEnabled(False)
			self.parasitic_heating.setEnabled(False)
			self.optical_heating.setEnabled(False)
			self.recombination_heating.setEnabled(False)
			self.thermal_isothermal_button.setEnabled(False)
			self.thermal_parameters.setEnabled(False)
			self.mesh.setEnabled(False)

	def setEnabled(self,val):
		self.enabled=val
		self.update()

	def callback_boundary(self):
		self.close_window(self.config_window)
		self.config_window=class_config_window(["thermal.thermal_boundary"],[_("Thermal boundary conditions")],title=_("Thermal boundary conditions"),icon="thermal")
		self.config_window.show()

	def callback_configure(self):
		self.close_window(self.config_window)
		self.config_window=class_config_window(["thermal"],[_("Configure")],title=_("Configure thermal model"),icon="thermal")
		self.config_window.show()

	def callback_edit_mesh(self):
		from window_mesh_editor import window_mesh_editor
		help_window().help_set_help("mesh.png",_("<big><b>Mesh editor</b></big>\nUse this window to setup the mesh."))

		self.close_window(self.optical_mesh)

		self.optical_mesh=window_mesh_editor(json_path_to_mesh="thermal.mesh",window_title=_("Thermal Mesh Editor"))
		self.optical_mesh.show()

