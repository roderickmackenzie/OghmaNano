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

## @package thermal_isothermal_button
#  Select thermal/isothermal simulation
#


#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QMessageBox, QLineEdit

from icon_lib import icon_get
from help import help_window
from json_root import json_root

from cal_path import sim_paths

class thermal_isothermal_button(QAction):

	def set_state(self,val):
		data=json_root()
		data.thermal.thermal=val
		data.save()

	def update_ui(self,update_help):
		self.blockSignals(True)
		data=json_root()
		self.thermal=data.thermal.thermal

		if self.thermal==True:
			self.setIcon(icon_get("thermal-on"))
			self.setText(_("Thermal model\nenabled"))
			if update_help==True:
				help_window().help_set_help(["thermal-on.png",_("<big><b>Thermal solver switched on</b></big><br>The heat equation will be solved across the device")])

		if self.thermal==False:
			self.setIcon(icon_get("thermal-off"))
			self.setText(_("Iso-thermal\nmodel"))
			if update_help==True:
				help_window().help_set_help(["thermal-off.png",_("<big><b>Isothermal mode</b></big><br>A single temperature will be assumed across the entire device.")])
		self.blockSignals(False)

	def refresh(self):
		self.update_ui(False)

	def __init__(self,parent):
		self.thermal=False
		QAction.__init__(self,icon_get("thermal-off"), _("Isothermal"),parent)
		self.triggered.connect(self.callback_state_changed)
		self.update_ui(False)

	def callback_state_changed(self):
		if self.thermal==True:
			self.thermal=False
		else:
			self.thermal=True

		#print(self.thermal)
		self.set_state(self.thermal)
		self.update_ui(True)
