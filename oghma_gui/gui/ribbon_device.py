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

## @package ribbon_device
#  The device editor ribbon.
#


from icon_lib import icon_get

#qt
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget
from help import help_window

from global_objects import global_object_register
from pl_main import pl_main
from QAction_lock import QAction_lock
from ribbon_page import ribbon_page
from json_c import json_tree_c

class ribbon_device(ribbon_page):
	def __init__(self):
		ribbon_page.__init__(self)
		self.bin=json_tree_c()
		self.contacts_window=None
		self.layer_editor=None
		self.dim_editor=None
		self.electrical_editor=None
		self.emission_editor=None


		self.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		self.setOrientation(Qt.Vertical);
		self.setIconSize(QSize(42, 42))

		self.tb_layer_editor = QAction_lock("layers", _("Layer\neditor"), self,"ribbon_device_layers")
		self.tb_layer_editor.clicked.connect(self.callback_layer_editor)
		self.addAction(self.tb_layer_editor)
		global_object_register("show_layer_editor",self.callback_layer_editor)
		
		self.contacts = QAction_lock("contact", _("Contacts"), self,"ribbon_device_contacts")
		self.contacts.clicked.connect(self.callback_contacts)
		self.addAction(self.contacts)

		self.tb_electrical_editor = QAction_lock("electrical", _("Electrical\nparameters"), self,"ribbon_device_electrical")
		self.tb_electrical_editor.clicked.connect(self.callback_electrical_editor)
		self.addAction(self.tb_electrical_editor)

		self.tb_emission_editor = QAction_lock("emission", _("Emission\nparameters"), self,"ribbon_device_emission")
		self.tb_emission_editor.clicked.connect(self.callback_emission_editor)
		self.addAction(self.tb_emission_editor)

		self.tb_dimension_editor = QAction_lock("dimensions", _("Substrate\nxz-size"), self,"ribbon_device_dim")
		self.tb_dimension_editor.clicked.connect(self.callback_dimension_editor)
		self.addAction(self.tb_dimension_editor)

		self.callback_circuit_diagram()

	def callback_circuit_diagram(self):
		self.tb_electrical_editor.setEnabled(True)

		if self.bin.get_token_value("circuit","enabled")==True:
			if self.bin.get_token_value("electrical_solver","solver_type")=="circuit":
				self.tb_electrical_editor.setEnabled(False)
			

	def update(self):
		self.close_window(self.contacts_window)
		self.close_window(self.layer_editor)
		self.close_window(self.dim_editor)
		self.close_window(self.electrical_editor)

	def setEnabled(self,val):
		self.cost.setEnabled(val)
		self.contacts.setEnabled(val)
		self.tb_electrical_editor.setEnabled(val)

		
	def callback_contacts(self):		
		help_window().help_set_help("contact.png",_("<big><b>Contacts window</b></big>\nUse this window to change the layout of the contacts on the device"))

		self.close_window(self.contacts_window)

		from contacts import contacts_window
		self.contacts_window=contacts_window()
		self.show_window(self.contacts_window)


	def callback_layer_editor(self):
		help_window().help_set_help("layers.png",_("<big><b>Device layers</b></big>\nUse this window to configure the structure of the device."))

		if self.is_valid(self.layer_editor):
			self.layer_editor.close()

		from layer_widget import layer_widget
		self.layer_editor=layer_widget()
		self.layer_editor.setAttribute(Qt.WA_DeleteOnClose, True)
		self.show_window(self.layer_editor)

	def callback_dimension_editor(self):
		help_window().help_set_help("dimensions.png",_("<big><b>xz dimension editor</b></big>\nUse this window to configure the xz size of the device."))

		self.close_window(self.dim_editor)

		from dim_editor import dim_editor
		self.dim_editor=dim_editor()
		self.show_window(self.dim_editor)


	def callback_electrical_editor(self):
		help_window().help_set_help("electrical.png",_("<big><b>Electrical parameters</b></big>\nUse this window to change the electrical parameters of each layer."))
		self.close_window(self.electrical_editor)

		from dos_main import dos_main
		self.electrical_editor=dos_main()
		self.show_window(self.electrical_editor)

	def callback_emission_editor(self):
		help_window().help_set_help("emission.png",_("<big><b>Emission parameters</b></big>\nUse this window to set if a layer emits light or not.  You can choose between theoretically calculated emission spectra and imported experimental spectra."))

		self.close_window(self.emission_editor)

		self.emission_editor=pl_main()
		self.show_window(self.emission_editor)
