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

## @package dos_main
#  The main DoS dialog.
#

import os
from tab_base import tab_base
from tab import tab_class
from epitaxy import get_epi

#qt5
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QTabWidget,QStatusBar, QAction, QMenu

#windows
from QHTabBar import QHTabBar
from global_objects import global_object_register
from icon_lib import icon_get

from css import css_apply

from json_root import json_root
from help import QAction_help
from lock import get_lock
from json_dialog import json_dialog
from json_base import json_base
from dlg_get_text2 import dlg_get_text2
from sim_name import sim_name
from ribbon_page import ribbon_page
from cal_path import sim_paths

class dos_main(QWidget,tab_base):

	def __init__(self):
		QWidget.__init__(self)
		self.setMinimumSize(1000, 600)

		self.main_vbox = QVBoxLayout()

		self.setWindowIcon(icon_get("preferences-system"))

		self.setWindowTitle(_("Electrical parameter editor")+sim_name.web_window_title) 

		toolbar=ribbon_page()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self.dd_enabled = QAction(icon_get("drift_diffusion"), _("Enable\nDrift Diff."), self)
		self.dd_enabled.setCheckable(True)
		self.dd_enabled.triggered.connect(self.callback_dd)
		toolbar.addAction(self.dd_enabled)

		self.auger = QAction(icon_get("auger"), _("Enable\nAuger"), self)
		self.auger.setCheckable(True)
		self.auger.triggered.connect(self.callback_auger)
		toolbar.addAction(self.auger)

		self.traps = QAction(icon_get("traps"), _("Dynamic\nSRH traps"), self)
		self.traps.setCheckable(True)
		self.traps.triggered.connect(self.callback_traps)


		self.menu_srh_traps = QMenu(self)

		configure_item=QAction(icon_get("electrical"),_("Max trap depth"), self)
		self.menu_srh_traps.addAction(configure_item)
		configure_item.triggered.connect(self.callback_trap_depth)

		configure_item=QAction(icon_get("fermi"),_("Min Fermi level"), self)
		self.menu_srh_traps.addAction(configure_item)
		configure_item.triggered.connect(self.callback_fermi_min_max)


		self.traps.setMenu(self.menu_srh_traps)

		toolbar.addAction(self.traps)

		self.steady_state_srh = QAction(icon_get("srh"), _("Equilibrium\nSRH traps"), self)
		self.steady_state_srh.setCheckable(True)
		self.steady_state_srh.triggered.connect(self.callback_srh)
		toolbar.addAction(self.steady_state_srh)

		self.exciton = QAction(icon_get("exciton"), _("Excitons"), self)
		self.exciton.setCheckable(True)
		self.exciton.triggered.connect(self.callback_exciton)
		toolbar.addAction(self.exciton)

		self.singlet = QAction(icon_get("singlet"), _("Excited\nstates"), self)
		self.singlet.setCheckable(True)
		self.singlet.triggered.connect(self.callback_singlet)
		if get_lock().is_next()==True:
			toolbar.addAction(self.singlet)

		toolbar.addWidget(spacer)

		self.configure = QAction(icon_get("cog"), _("Configure"), self)
		self.configure.triggered.connect(self.callback_configure)
		toolbar.addAction(self.configure)

		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)

		self.notebook = QTabWidget()
		self.tabs_top=False

		if len(json_root().epi.layers)>8:
			self.tab_bar=QHTabBar()
			css_apply(self.notebook,"style_h.css")
			self.notebook.setTabBar(self.tab_bar)
			self.notebook.setTabPosition(QTabWidget.West)
		else:
			css_apply(self,"tab_default.css")



		self.main_vbox.addWidget(self.notebook)
		self.setLayout(self.main_vbox)

		global_object_register("dos_update",self.update)
		self.status_bar=QStatusBar()
		self.notebook.currentChanged.connect(self.changed_click)

		self.main_vbox.addWidget(self.status_bar)	
		self.update()

		json_root().add_call_back(self.update_values)
		self.destroyed.connect(self.doSomeDestruction)

	def doSomeDestruction(self):
		json_root().remove_call_back(self.update_values)

	def update_values(self):
		for i in range(0,self.notebook.count()):
			tab=self.notebook.widget(i)
			tab.tab.refind_template_widget()
			tab.tab.hide_show_widgets()
			tab.tab.update_values()

	def update(self):
		self.notebook.blockSignals(True)
		self.notebook.clear()
		data=json_root()
		for l in data.epi.layers:
			if data.electrical_solver.solver_type!="circuit":
				if l.shape_dos.enabled==True and l.enabled==True:
						#print(l.shape_dos)
						db_json_file=os.path.join(sim_paths.get_materials_path(),l.optical_material,"data.json")
						widget=tab_class(None,json_path="json_root().epi", uid=l.shape_dos.id, db_json_file=db_json_file, db_json_db_path="electrical_constants")
						self.notebook.addTab(widget,l.name)

						for s in l.segments:
							if s.shape_dos.enabled==True and s.enabled==True:
								widget=tab_class(None,json_path="json_root().epi",uid=s.shape_dos.id)
								widget.tab.json_human_path=""
								self.notebook.addTab(widget,s.name)
			else:
				if l.layer_type=="active":
					name="Electrical "+l.name
					widget=tab_class(l.shape_electrical)

					self.notebook.addTab(widget,name)

		self.changed_click()
		self.notebook.blockSignals(False)

	def callback_trap_depth(self):
		data=json_root()
		w=self.notebook.currentWidget()
		dos_data=data.epi.find_object_by_id(w.tab.template_widget.id)
		ret=dlg_get_text2( _("Maximum trap depth (eV):"), str(dos_data.srh_start),"electrical.png")
		if ret.ret!=None:
			depth=0.0
			try:
				depth=-abs(float(ret.ret))
			except:
				error_dlg(self,_("That's not a number.."))
				return
			dos_data.srh_start=float(depth)
			data.save()
			#self.update_graph()

	def callback_fermi_min_max(self):
		data=json_root()
		w=self.notebook.currentWidget()
		dos_data=data.epi.find_object_by_id(w.tab.template_widget.id)
		ret=dlg_get_text2( _("Minimum fermi level (eV):"), str(dos_data.nstart),"fermi.png")
		if ret.ret!=None:
			depth=0.0
			try:
				depth=-abs(float(ret.ret))
			except:
				error_dlg(self,_("That's not a number.."))
				return
			dos_data.nstart=float(depth)
			dos_data.pstart=float(depth)
			data.save()

	def help(self):
		help_window().help_set_help(["tab.png","<big><b>Density of States</b></big>\nThis tab contains the electrical model parameters, such as mobility, tail slope energy, and band gap."])

	def changed_click(self):
		data=json_root()
		if data.electrical_solver.solver_type!="circuit":
			self.dd_enabled.setEnabled(True)
			self.auger.setEnabled(True)
			self.traps.setEnabled(True)
			self.singlet.setEnabled(True)
			self.steady_state_srh.setEnabled(True)
			self.configure.setEnabled(True)

			tab = self.notebook.currentWidget()
			if tab==None:
				return
			tab.tab.refind_template_widget()
			self.dd_enabled.setChecked(tab.tab.template_widget.dd_enabled)
			self.auger.setChecked(tab.tab.template_widget.dos_enable_auger)
			self.steady_state_srh.setChecked(tab.tab.template_widget.ss_srh_enabled)
			self.exciton.setChecked(tab.tab.template_widget.exciton_enabled)
			self.singlet.setChecked(tab.tab.template_widget.singlet_enabled)

			if tab.tab.template_widget.srh_bands>0:
				self.traps.setChecked(True)
			else:
				self.traps.setChecked(False)

		else:
			self.dd_enabled.setEnabled(False)
			self.auger.setEnabled(False)
			self.traps.setEnabled(False)
			self.steady_state_srh.setEnabled(False)
			self.singlet.setEnabled(False)

	def callback_auger(self):
		data=json_root()
		if data.electrical_solver.solver_type!="circuit":
			tab = self.notebook.currentWidget()
			tab.tab.refind_template_widget()
			tab.tab.template_widget.dos_enable_auger=self.auger.isChecked()
			tab.tab.hide_show_widgets()
			data.save()

	def callback_dd(self):
		data=json_root()
		tab = self.notebook.currentWidget()
		tab.tab.refind_template_widget()
		tab.tab.template_widget.dd_enabled=self.dd_enabled.isChecked()
		tab.tab.hide_show_widgets()
		data.save()

	def callback_srh(self):
		data=json_root()
		if data.electrical_solver.solver_type!="circuit":
			tab = self.notebook.currentWidget()
			tab.tab.refind_template_widget()
			tab.tab.template_widget.ss_srh_enabled=self.steady_state_srh.isChecked()
			tab.tab.hide_show_widgets()
			data.save()

	def callback_exciton(self):
		data=json_root()
		if data.electrical_solver.solver_type!="circuit":
			tab = self.notebook.currentWidget()
			tab.tab.refind_template_widget()

			for l in data.epi.layers:
				l.shape_dos.exciton_enabled=self.exciton.isChecked()
				for s in l.segments:
					s.shape_dos.exciton_enabled=self.exciton.isChecked()

			self.update_values()

			data.exciton.exciton_enabled=self.exciton.isChecked()

			tab.tab.hide_show_widgets()
			data.save()

	def callback_singlet(self):
		data=json_root()
		if data.electrical_solver.solver_type!="circuit":
			tab = self.notebook.currentWidget()
			tab.tab.refind_template_widget()

			for l in data.epi.layers:
				l.shape_dos.singlet_enabled=self.singlet.isChecked()
				for s in l.segments:
					s.shape_dos.singlet_enabled=self.singlet.isChecked()

			self.update_values()

			data.singlet.singlet_enabled=self.singlet.isChecked()

			tab.tab.hide_show_widgets()
			data.save()

	def callback_configure(self):
		from config_window import class_config_window
		tab = self.notebook.currentWidget()
		if tab!=None:
			tab.tab.refind_template_widget()
			self.config=class_config_window([tab.tab.template_widget.config],[_("DoS Config")],title=_("Dos Config"),icon="electrical")
			self.config.changed.connect(self.update_values)
			self.config.show()

	def callback_traps(self):
		data=json_root()
		tab = self.notebook.currentWidget()
		tab.tab.refind_template_widget()

		if self.traps.isChecked()==True:
			tab.tab.template_widget.srh_bands=5
		else:
			tab.tab.template_widget.srh_bands=0

		tab.tab.hide_show_widgets()
		data.save()

		self.update_values()

