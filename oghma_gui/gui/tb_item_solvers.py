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

## @package tb_item_solvers
#  A toolbar item to select the solver type
#


#inp

import i18n
_ = i18n.language.gettext

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QMenu
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QLabel,QComboBox
from gQtCore import gSignal

from global_objects import global_object_run
from QAction_lock import QAction_lock
from config_window import class_config_window
from json_c import json_tree_c

class tb_item_solvers(QToolBar):

	changed = gSignal()
	
	def __init__(self,orientation=Qt.Vertical):
		QToolBar.__init__(self)
		self.bin=json_tree_c()
		self.setOrientation(orientation)
		self.setToolButtonStyle( Qt.ToolButtonTextBesideIcon)
		self.setStyleSheet(" QToolButton { padding-left: 0px; padding-right: 0px; padding-top: 0px;padding-bottom: 0px; width: 200px;} QToolButton:checked {background-color: LightBlue; }")

		self.tb_item_poisson = QAction_lock("poisson", _("Electrostatic solver"), self,"ribbon_thermal_joule")
		self.tb_item_poisson.clicked.connect(self.callback_solver_poisson_click)
		self.tb_item_poisson.setCheckable(True)

		self.menu_poisson = QMenu(self)
		configure_item=QAction(_("Configure"), self)
		self.menu_poisson.addAction(configure_item)
		self.tb_item_poisson.setMenu(self.menu_poisson)
		configure_item.triggered.connect(self.callback_poisson)
		self.addAction(self.tb_item_poisson)

		self.tb_item_newton = QAction_lock("newton", _("Drift diffusion"), self,"ribbon_thermal_optical")
		self.tb_item_newton.clicked.connect(self.callback_solver_newton_click)
		self.tb_item_newton.setCheckable(True)

		self.menu_newton = QMenu(self)
		self.tb_item_newton.setMenu(self.menu_newton)
		self.addAction(self.tb_item_newton)

		configure_item=QAction(_("Configure"), self)
		self.menu_newton.addAction(configure_item)
		configure_item.triggered.connect(self.callback_newton)

		micro_code=QAction(_("Edit microcode"), self)
		self.menu_newton.addAction(micro_code)
		micro_code.triggered.connect(self.callback_micro_code)


		self.tb_item_circuit = QAction_lock("kirchhoff", _("Simple circuit solver"), self,"ribbon_thermal_recombination")
		self.tb_item_circuit.clicked.connect(self.callback_circuit_clicked)
		self.tb_item_circuit.setCheckable(True)

		self.menu_circuit_config = QMenu(self)
		configure_item=QAction(_("Configure"), self)
		self.menu_circuit_config.addAction(configure_item)
		self.tb_item_circuit.setMenu(self.menu_circuit_config)
		configure_item.triggered.connect(self.callback_circuit_config)
		self.addAction(self.tb_item_circuit)
		self.update()

	def update(self):

		self.tb_item_newton.blockSignals(True)
		self.tb_item_poisson.blockSignals(True)
		self.tb_item_circuit.blockSignals(True)
		solver_type=self.bin.get_token_value("electrical_solver","solver_type")
		if solver_type=="drift-diffusion":
			self.tb_item_poisson.setChecked(True)
			self.tb_item_newton.setChecked(True)
			self.tb_item_circuit.setChecked(False)
		elif solver_type=="poisson":
			self.tb_item_poisson.setChecked(True)
			self.tb_item_newton.setChecked(False)
			self.tb_item_circuit.setChecked(False)
		elif solver_type=="circuit":
			self.tb_item_poisson.setChecked(False)
			self.tb_item_newton.setChecked(False)
			self.tb_item_circuit.setChecked(True)
		elif solver_type=="none":
			self.tb_item_poisson.setChecked(False)
			self.tb_item_newton.setChecked(False)
			self.tb_item_circuit.setChecked(False)
		self.tb_item_newton.blockSignals(False)
		self.tb_item_poisson.blockSignals(False)
		self.tb_item_circuit.blockSignals(False)

	def callback_poisson(self):
		self.mesh_config=class_config_window(["electrical_solver.poisson"],[_("Poission solver")],title=_("Poission solver configuration"),icon="poisson")
		self.mesh_config.show()

	def callback_newton(self):
		self.mesh_config=class_config_window(["math","singlet"],[_("Newton solver"),_("Singlet solver")],title=_("Newton solver configuration"),icon="newton")
		self.mesh_config.show()

	def callback_micro_code(self):
		from window_code_editor import window_code_editor
		self.a=window_code_editor()
		self.a.show()

	def callback_circuit_config(self):
		self.mesh_config=class_config_window(["circuit.config"],[_("Configuration")],title=_("Circuit solver configuration"),icon="newton")

		self.mesh_config.show()

	def callback_solver_poisson_click(self):
		pos=self.tb_item_poisson.isChecked()
		self.tb_item_newton.isChecked()
		self.tb_item_circuit.isChecked()
		if pos==True:
			self.bin.set_token_value("electrical_solver","solver_type","poisson")
		else:
			self.bin.set_token_value("electrical_solver","solver_type","none")
		self.bin.save()
		self.update()
		self.changed.emit()

	def callback_solver_newton_click(self):
		self.tb_item_poisson.isChecked()
		dd=self.tb_item_newton.isChecked()
		self.tb_item_circuit.isChecked()
		if dd==True:
			self.bin.set_token_value("electrical_solver","solver_type","drift-diffusion")
		else:
			self.bin.set_token_value("electrical_solver","solver_type","none")
		self.bin.save()
		self.update()
		self.changed.emit()

	def callback_circuit_clicked(self):
		self.tb_item_poisson.isChecked()
		self.tb_item_newton.isChecked()
		cir=self.tb_item_circuit.isChecked()
		if cir==True:
			self.bin.set_token_value("electrical_solver","solver_type","circuit")
		else:
			self.bin.set_token_value("electrical_solver","solver_type","none")
		self.bin.save()
		self.update()
		self.changed.emit()
		
	def setEnabled(self,val):
		self.tb_item_poisson.setEnabled(val)
		self.tb_item_newton.setEnabled(val)
		self.tb_item_circuit.setEnabled(val)

