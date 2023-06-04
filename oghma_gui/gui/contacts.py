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

## @package contacts
#  Window to configure the contacts
#

from icon_lib import icon_get
from epitaxy import get_epi

import i18n
_ = i18n.language.gettext


#qt
from PySide2.QtWidgets import  QAction
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QToolBar, QMessageBox, QVBoxLayout, QTableWidget,QAbstractItemView, QTableWidgetItem

from gQtCore import gSignal

from error_dlg import error_dlg
from global_objects import global_object_run

from QWidgetSavePos import QWidgetSavePos
from g_tab2 import g_tab2
from energy_to_charge import energy_to_charge
from json_root import json_root
from json_contacts import contact
from help import QAction_help

class contacts_window(QWidgetSavePos):

	changed = gSignal()

	def show_hide_cols(self):
		schottky=False
		for c in json_root().epi.contacts.segments:
			if c.physical_model=="schottky":
				schottky=True
				break

		if schottky==True:
			self.tab.setColumnHidden(9,False)
			self.tab.setColumnHidden(10,False)
		else:
			self.tab.setColumnHidden(9,True)
			self.tab.setColumnHidden(10,True)

		if json_root().electrical_solver.solver_type=="circuit":
			self.tab.setColumnHidden(7,True)
			self.tab.setColumnHidden(8,True)
			self.tab.setColumnHidden(11,True)
		else:
			self.tab.setColumnHidden(7,False)
			self.tab.setColumnHidden(8,False)
			self.tab.setColumnHidden(11,False)

		if json_root().electrical_solver.mesh.mesh_z.get_points()!=1 or json_root().electrical_solver.mesh.mesh_x.get_points()!=1: 
			self.hide_cols(False)
		else:
			self.hide_cols(True)


	def save_and_redraw(self):
		self.changed.emit()
		json_root().save()
		global_object_run("gl_force_redraw")

	def update(self):
		#self.tab.clear()
		#self.tab.populate()
		self.show_hide_cols()

	def hide_cols(self,val):
		self.tab.setColumnHidden(3,val)
		self.tab.setColumnHidden(4,val)
		#self.tab.setColumnHidden(5,val)


	def __init__(self):
		QWidgetSavePos.__init__(self,"contacts")
		self.epi=get_epi()

		self.setMinimumSize(1000, 400)

		self.setWindowIcon(icon_get("contact"))

		self.setWindowTitle2(_("Edit contacts")) 
		
		self.main_vbox = QVBoxLayout()

		self.toolbar=QToolBar()
		self.toolbar.setIconSize(QSize(48, 48))
		self.main_vbox.addWidget(self.toolbar)

		self.tab = g_tab2(toolbar=self.toolbar)
		self.tab.set_tokens(["name","position","applied_voltage","x0","dx","contact_resistance_sq","shunt_resistance_sq","np","charge_type", "ve0", "vh0", "physical_model","id"])
		self.tab.set_labels([_("Name"),_("Top/Bottom"),_("Applied\nvoltage"),_("Start")+" (m)", _("Width")+" (m)" , _("Contact resistance\n")+" (Ohms m^2)",_("Shunt resistance")+"\n(Ohms m^2)",_("Charge density/\nFermi-offset"),_("Majority\ncarrier"),_("ve0 (m/s)"),_("vh0 (m/s)"),_("Physical\nmodel"),_("ID")])

		self.tab.json_search_path="json_root().epitaxy.contacts.segments"
		self.tab.setColumnWidth(2, 200)
		self.tab.setColumnWidth(7, 200)
		self.tab.setColumnHidden(5,True)
		self.tab.setColumnHidden(6,True)
		self.tab.setColumnWidth(12, 10)

		self.tab.base_obj=contact()
		self.tab.populate()
		#self.tab.new_row_clicked.connect(self.callback_new_row_clicked)
		self.tab.changed.connect(self.emit_structure_changed)
		#self.tab.itemSelectionChanged.connect(self.save_and_redraw)



		self.main_vbox.addWidget(self.tab)

		self.update()

		self.setLayout(self.main_vbox)

		json_root().add_call_back(self.update)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

		self.help = QAction_help()
		self.toolbar.addAction(self.help)

		#get_contactsio().changed.connect(self.update)

	def emit_structure_changed(self):
		self.show_hide_cols()
		json_root().save()
		self.changed.emit()
		global_object_run("gl_force_redraw")

