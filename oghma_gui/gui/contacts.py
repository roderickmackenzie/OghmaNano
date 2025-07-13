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

import i18n
_ = i18n.language.gettext


#qt
from PySide2.QtWidgets import  QAction
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QToolBar, QMessageBox, QVBoxLayout, QHBoxLayout,QTableWidget,QAbstractItemView, QTableWidgetItem, QToolButton

from gQtCore import gSignal

from error_dlg import error_dlg
from global_objects import global_object_run

from QWidgetSavePos import QWidgetSavePos
from g_tab2_bin import g_tab2_bin
from energy_to_charge import energy_to_charge
from help import QAction_help
from mesh_math import mesh_math
from json_c import json_tree_c
from QLabel_click import QLabel_click
from bytes2str import str2bytes
import ctypes

class expander_widget(QWidget):
	def __init__(self, label_text, tab,state,save_state=False):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.save_state=save_state
		self.main_layout = QVBoxLayout()
		self.setLayout(self.main_layout)

		# Create a horizontal layout for the label and arrow button
		header_layout = QHBoxLayout()

		# Label on the left (clickable)
		self.label = QLabel_click(label_text)
		self.label.clicked.connect(self.on_label_clicked)
		header_layout.addWidget(self.label)

		# Arrow toggle button on the right
		self.toggle_button = QToolButton()
		self.toggle_button.setStyleSheet("border: none;")
		if state==False:
			self.toggle_button.setArrowType(Qt.RightArrow)
		else:
			self.toggle_button.setArrowType(Qt.DownArrow)

		self.toggle_button.setCheckable(True)
		self.toggle_button.setChecked(state)
		self.toggle_button.clicked.connect(self.on_toggle)
		header_layout.addWidget(self.toggle_button)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		header_layout.addWidget(spacer)


		self.main_layout.addLayout(header_layout)

		# Create the table widget
		self.tab = tab
		self.main_layout.addWidget(self.tab)
		self.tab.setVisible(state)

	def on_toggle(self):
		is_expanded = self.toggle_button.isChecked()
		self.tab.setVisible(is_expanded)
		if is_expanded:
			self.toggle_button.setArrowType(Qt.DownArrow)
		else:
			self.toggle_button.setArrowType(Qt.RightArrow)
		if self.save_state==True:
			self.bin.set_token_value("epitaxy.contacts","show_minority",is_expanded)
			self.bin.save()

	def on_label_clicked(self):
		self.toggle_button.click()

class contacts_window(QWidgetSavePos):

	changed = gSignal()

	def __init__(self):
		QWidgetSavePos.__init__(self,"contacts")
		self.bin=json_tree_c()
		self.mesh_z=mesh_math("electrical_solver.mesh.mesh_z")
		self.mesh_x=mesh_math("electrical_solver.mesh.mesh_x")
		self.setMinimumSize(1200, 400)

		self.setWindowIcon(icon_get("contact"))

		self.setWindowTitle2(_("Edit contacts")) 
		
		self.main_vbox = QVBoxLayout()

		self.toolbar=QToolBar()
		self.toolbar.setIconSize(QSize(48, 48))
		self.main_vbox.addWidget(self.toolbar)

		if self.bin.get_token_value("electrical_solver","solver_type")=="circuit":
			self.tab_majority=self.make_tab_majority()
			self.tab_majority.changed.connect(self.emit_structure_changed)
			self.main_vbox.addWidget(self.tab_majority)
			self.tab_minority=None
		else:
			self.tab_majority=self.make_tab_majority()
			self.tab_majority.changed.connect(self.emit_structure_changed)
			self.expander_majority = expander_widget("Majority carrier", self.tab_majority,True)
			self.main_vbox.addWidget(self.expander_majority)

			self.tab_minority=self.make_tab_minority()
			self.tab_minority.changed.connect(self.emit_structure_changed)
			show_minority=self.bin.get_token_value("epitaxy.contacts","show_minority")
			self.expander_minority = expander_widget("Minority carrier", self.tab_minority,show_minority,save_state=True)
			self.main_vbox.addWidget(self.expander_minority)

			self.tab_majority.itemSelectionChanged.connect(self.sync_selection_from_majority)
			self.tab_minority.itemSelectionChanged.connect(self.sync_selection_from_minority)

			spacer = QWidget()
			spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
			self.main_vbox.addWidget(spacer)

		self.update()

		self.setLayout(self.main_vbox)

		self.bin.add_call_back(self.update)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

		self.help = QAction_help()
		self.toolbar.addAction(self.help)

	def sync_selection_from_majority(self):
		self.tab_majority.sync_selection(self.tab_minority)

	def sync_selection_from_minority(self):
		self.tab_minority.sync_selection(self.tab_majority)

	def make_tab_majority(self):
		tab = g_tab2_bin(toolbar=self.toolbar)
		tab.set_tokens(["name","contact.position","contact.applied_voltage","x0","dx","contact.contact_resistance_sq","contact.shunt_resistance_sq", "np", "contact.majority" ,"contact.majority_model","id"])
		tab.set_labels([_("Name"),_("Top/Bottom"),_("Applied\nvoltage"),_("Start")+" (m)", _("Width")+" (m)" , _("Contact resistance\n")+" (Ohms m^2)", _("Shunt resistance")+"\n(Ohms m^2)", _("Charge density/\nFermi-offset"), _("Majority\ncarrier"), _("Physical\nmodel"),_("ID")])

		tab.json_root_path="epitaxy.contacts"
		tab.set_col_width("name", 120)
		tab.set_col_width("contact.position", 120)
		tab.setColumnWidth(2, 200)		#applied_voltage
		tab.setColumnWidth(3, 120)		#x0
		tab.setColumnWidth(4, 120)		#dx
		tab.setColumnWidth(5, 120)		#contact_resistance_sq
		tab.setColumnWidth(6, 120)		#
		tab.setColumnWidth(7, 200)		#majority density
		tab.setColumnWidth(8, 100)		#carrier type
		tab.set_col_width("contact.majority_model", 250)
		tab.set_col_width("id", 10)
		tab.set_col_hidden("contact.shunt_resistance_sq",True)
		tab.set_col_hidden("contact.contact_resistance_sq",True)
		tab.new_row_clicked.connect(self.callback_new_row_clicked)
		tab.populate()
		return tab

	def make_tab_minority(self):
		tab = g_tab2_bin()
		tab.set_tokens(["name","contact.minority","contact.minority_model", "id"])
		tab.set_labels([_("Name"), _("Minority\ncarrier"),_("Minority\ncarrier"), _("ID")])

		tab.setColumnWidth(0, 120)		#name
		tab.setColumnWidth(1, 120)		#minority
		tab.setColumnWidth(2, 200)		#Carrier density
		tab.set_col_width("id", 10)

		tab.json_root_path="epitaxy.contacts"
		tab.setColumnWidth(1, 120)

		tab.populate()
		return tab

	def show_hide_cols(self):

		if self.bin.get_token_value("electrical_solver","solver_type")=="circuit":
			self.tab_majority.set_col_hidden("contact.majority",True)
			self.tab_majority.set_col_hidden("contact.majority_model",True)
			self.tab_majority.set_col_hidden("contact.majority",True)
			self.tab_majority.set_col_hidden("np",True)
			if self.tab_minority!=None:
				self.tab_minority.set_col_hidden("contact.minority_model",True)

		else:
			self.tab_majority.set_col_hidden("contact.majority",False)
			self.tab_majority.set_col_hidden("contact.physical_model",False)
			self.tab_majority.set_col_hidden("contact.majority",False)

		if self.mesh_z.get_points()!=1 or self.mesh_x.get_points()!=1: 
			self.tab_majority.set_col_hidden("dx",False)
			self.tab_majority.set_col_hidden("x0",False)
		else:
			self.tab_majority.set_col_hidden("dx",True)
			self.tab_majority.set_col_hidden("x0",True)

		#Expand majority model type col
		expand=False
		for y in range(self.tab_majority.rowCount()):
			model_type=self.bin.get_token_value("epitaxy.contacts.segment"+str(y)+".contact","majority_model")
			if model_type=="ohmic_barrier":
				expand=True
			if model_type=="schottky":
				expand=True

		if expand==False:
			self.tab_majority.set_col_width("contact.majority_model", 120)
		else:
			self.tab_majority.set_col_width("contact.majority_model", 250)

		#Expand minority model type col
		if self.tab_minority!=None:
			expand=False
			for y in range(self.tab_minority.rowCount()):
				model_type=self.bin.get_token_value("epitaxy.contacts.segment"+str(y)+".contact","minority_model")
				if model_type=="ohmic_barrier":
					expand=True
				if model_type=="schottky":
					expand=True

			if expand==False:
				self.tab_minority.set_col_width("contact.minority_model", 120)
			else:
				self.tab_minority.set_col_width("contact.minority_model", 250)

	def update(self):
		self.show_hide_cols()
		changed=False
		pos=self.tab_majority.get_col_by_token("x0")
		dx=self.tab_majority.get_col_by_token("dx")
		for y in range(self.tab_majority.rowCount()):
			if str(self.tab_majority.get_value(y,1))=="left" or str(self.tab_majority.get_value(y,1))=="right":
				if self.tab_majority.cellWidget(y, dx).token!="dy":
					self.tab_majority.cellWidget(y, dx).token="dy"
					changed=True

				if self.tab_majority.cellWidget(y, pos).token!="y0":
					self.tab_majority.cellWidget(y, pos).token="y0"
					changed=True
			else:
				if self.tab_majority.cellWidget(y, dx).token!="dx":
					self.tab_majority.cellWidget(y, dx).token="dx"
					changed=True

				if self.tab_majority.cellWidget(y, pos).token!="x0":
					self.tab_majority.cellWidget(y, pos).token="x0"
					changed=True

		if changed==True:
			self.tab_majority.update()

	def emit_structure_changed(self,token):
		sender = self.sender()
		self.tab_majority.blockSignals(True)

		#Translate one tab to another
		if self.tab_minority!=None:
			self.tab_minority.blockSignals(True)

			if sender==self.tab_majority:
				if self.tab_majority.rowCount()!=self.tab_minority.rowCount():
					self.tab_minority.remove_all_rows()
					self.tab_minority.populate()
				else:
					if token=="majority":
						src_col=self.tab_majority.get_col_by_token("contact.majority")
						for y in range(0,self.tab_majority.rowCount()):
							if self.tab_majority.get_value(y,src_col)=="electron":
								self.bin.set_token_value("epitaxy.contacts.segment"+str(y)+".contact","minority","hole")
							else:
								self.bin.set_token_value("epitaxy.contacts.segment"+str(y)+".contact","minority","electron")

					self.tab_minority.update()

				self.tab_majority.sync_selection(self.tab_minority)
			elif sender==self.tab_minority:
				if self.tab_majority.rowCount()!=self.tab_minority.rowCount():
					self.tab_majority.remove_all_rows()
					self.tab_majority.populate()
				else:
					src_col=self.tab_minority.get_col_by_token("contact.minority")
					for y in range(0,self.tab_minority.rowCount()):
						if self.tab_majority.get_value(y,src_col)=="electron":
							self.bin.set_token_value("epitaxy.contacts.segment"+str(y)+".contact","majority","hole")
						else:
							self.bin.set_token_value("epitaxy.contacts.segment"+str(y)+".contact","majority","electron")

					self.tab_majority.update()
				self.tab_minority.sync_selection(self.tab_majority)

		self.bin.lib.json_fixup_contacts(ctypes.byref(json_tree_c()))
		self.show_hide_cols()
		self.bin.save()
		self.tab_majority.blockSignals(False)

		if self.tab_minority!=None:
			self.tab_minority.blockSignals(False)

		self.changed.emit()

		global_object_run("gl_force_redraw_hard")


	def callback_new_row_clicked(self,row):
		self.bin.lib.json_fixup_new_contact_size(ctypes.byref(json_tree_c()),ctypes.c_char_p(str2bytes("epitaxy.contacts.segment"+str(row))))
		self.tab_majority.update()
