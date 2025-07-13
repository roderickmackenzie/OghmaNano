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
from tab import tab_class

#qt5
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QTabWidget,QStatusBar, QAction, QMenu

#windows
from QHTabBar import QHTabBar
from global_objects import global_object_register
from global_objects import global_object_delete
from icon_lib import icon_get

from css import css_apply

from help import QAction_help
from lock import get_lock
from json_dialog import json_dialog
from dlg_get_text2 import dlg_get_text2
from sim_name import sim_name
from ribbon_page import ribbon_page
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos
from json_c import json_tree_c
from global_objects import global_object_run

class dos_main(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"dos_main")
		self.bin=json_tree_c()
		self.setMinimumSize(1000, 600)

		self.main_vbox = QVBoxLayout()

		self.setWindowIcon(icon_get("preferences-system"))

		self.setWindowTitle(_("Electrical parameter editor")+sim_name.web_window_title) 

		toolbar=ribbon_page()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self.dd_enabled = QAction(icon_get("drift_diffusion"), _("Enable\nDrift Diff."), self)
		self.dd_enabled.setCheckable(True)
		self.dd_enabled.triggered.connect(self.callback_buttons)
		toolbar.addAction(self.dd_enabled)


		self.traps = QAction(icon_get("traps"), _("Dynamic\nSRH traps"), self)
		self.traps.setCheckable(True)
		self.traps.triggered.connect(self.callback_buttons)

		self.menu_srh_traps = QMenu(self)

		self.min_trap_depth=QAction(icon_get("electrical"),_("Min trap depth"), self)
		self.menu_srh_traps.addAction(self.min_trap_depth)
		self.min_trap_depth.triggered.connect(self.callback_min_trap_depth)

		self.max_trap_depth=QAction(icon_get("electrical"),_("Max trap depth"), self)
		self.menu_srh_traps.addAction(self.max_trap_depth)
		self.max_trap_depth.triggered.connect(self.callback_max_trap_depth)

		self.fermi=QAction(icon_get("fermi"),_("Min Fermi level"), self)
		self.menu_srh_traps.addAction(self.fermi)
		self.fermi.triggered.connect(self.callback_fermi_min_max)

		self.fermi_n=QAction(icon_get("mesh"),_("Fn points"), self)
		self.menu_srh_traps.addAction(self.fermi_n)
		self.fermi_n.triggered.connect(self.callback_fermi_n)

		self.fermi_i=QAction(icon_get("mesh"),_("Fermi integral points"), self)
		self.menu_srh_traps.addAction(self.fermi_i)
		self.fermi_i.triggered.connect(self.callback_fermi_i)

		self.traps.setMenu(self.menu_srh_traps)

		toolbar.addAction(self.traps)

		self.auger = QAction(icon_get("auger"), _("Enable\nAuger"), self)
		self.auger.setCheckable(True)
		self.auger.triggered.connect(self.callback_buttons)
		toolbar.addAction(self.auger)

		self.steady_state_srh = QAction(icon_get("srh"), _("Equilibrium\nSRH traps"), self)
		self.steady_state_srh.setCheckable(True)
		self.steady_state_srh.triggered.connect(self.callback_buttons)
		toolbar.addAction(self.steady_state_srh)

		self.exciton = QAction(icon_get("exciton"), _("Excitons"), self)
		self.exciton.setCheckable(True)
		self.exciton.triggered.connect(self.callback_buttons)
		toolbar.addAction(self.exciton)

		self.singlet = QAction(icon_get("singlet"), _("Excited\nstates laser"), self)
		self.singlet.setCheckable(True)
		self.singlet.triggered.connect(self.callback_buttons)


		self.menu_singlet_traps = QMenu(self)

		self.menu_singlet_photon_rate=QAction(_("Photon rate equation"), self)
		self.menu_singlet_photon_rate.setCheckable(True)
		self.menu_singlet_photon_rate.triggered.connect(self.callback_menu_singlet)
		self.menu_singlet_traps.addAction(self.menu_singlet_photon_rate)

		self.singlet.setMenu(self.menu_singlet_traps)

		self.singlet_opv = QAction(icon_get("singlet_opv"), _("Excited\nstates OPV"), self)
		self.singlet_opv.setCheckable(True)
		self.singlet_opv.triggered.connect(self.callback_buttons)

		if get_lock().is_next()==True:
			toolbar.addAction(self.singlet)
			button = toolbar.widgetForAction(self.singlet)
			button.setMinimumWidth(80)

			toolbar.addAction(self.singlet_opv)
			button = toolbar.widgetForAction(self.singlet_opv)
			button.setMinimumWidth(80)

		toolbar.addWidget(spacer)

		self.configure = QAction(icon_get("cog"), _("Configure"), self)
		self.configure.triggered.connect(self.callback_buttons)
		toolbar.addAction(self.configure)

		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)

		self.notebook = QTabWidget()
		self.tabs_top=False

		segments=self.bin.get_token_value("epitaxy","segments")
		if segments>8:
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

		self.bin.add_call_back(self.update_values)
		self.destroyed.connect(self.doSomeDestruction)
		self.update_menus()
		self.buttons_update()

	def get_json_path(self,uid):
		json_path=self.bin.find_path_by_uid("epitaxy",uid)
		if json_path==None:
			json_path=self.bin.find_path_by_uid("world.world_data",uid)
		return json_path

	def update_menus(self):
		w=self.notebook.currentWidget()
		if w!=None:
			uid=w.tab.uid
			json_path=self.get_json_path(uid)
			json_path=json_path+".shape_dos"
			srh_stop=self.bin.get_token_value(json_path,"srh_stop")
			srh_start=self.bin.get_token_value(json_path,"srh_start")
			nstart=self.bin.get_token_value(json_path,"nstart")
			npoints=self.bin.get_token_value(json_path,"npoints")
			Esteps=self.bin.get_token_value(json_path,"Esteps")
			singlet_photon_enabled=self.bin.get_token_value(json_path,"singlet_photon_enabled")
			self.min_trap_depth.setText(_("Min trap depth")+" "+str(srh_stop)+"eV")
			self.max_trap_depth.setText(_("Max trap depth")+" "+str(srh_start)+"eV")
			self.fermi.setText(_("Min Fermi level")+" "+str(nstart)+"eV")

			self.fermi_n.setText(_("Carrier density points")+" "+str(npoints))
			self.fermi_i.setText(_("Fermi-dirac integral steps")+" "+str(Esteps))

			self.menu_singlet_photon_rate.setChecked(singlet_photon_enabled)

	def callback_menu_singlet(self):
		action = self.sender()
		text=action.text()
		w=self.notebook.currentWidget()
		if w!=None:
			json_path=self.get_json_path(w.tab.uid)
			self.bin.set_token_value(json_path,singlet_photon_enabled,self.menu_singlet_photon_rate.isChecked())
			self.bin.save()
			self.update_values()

	def doSomeDestruction(self):
		self.bin.remove_call_back(self.update_values)

	def update_values(self):
		for i in range(0,self.notebook.count()):
			tab=self.notebook.widget(i)
			tab.tab.hide_show_widgets()
			tab.tab.update_values()

	def show_tab_by_uid(self,uid):
		for i in range(0,self.notebook.count()):
			tab=self.notebook.widget(i)
			if uid==tab.tab.uid:
				self.notebook.setCurrentIndex(i)
				break

	def update(self):
		self.notebook.blockSignals(True)
		self.notebook.clear()
		electrical_solver=self.bin.get_token_value("electrical_solver","solver_type")
		layers=self.bin.get_token_value("epitaxy","segments")
		if electrical_solver=="drift-diffusion":
			for l in range(0,layers):
				path="epitaxy.segment"+str(l)
				enabled=self.bin.get_token_value(path,"enabled")
				obj_type=self.bin.get_token_value(path,"obj_type")
				name=self.bin.get_token_value(path,"name")
				optical_material=self.bin.get_token_value(path,"optical_material")
				uid=self.bin.get_token_value(path,"id")
				
				if (obj_type=="active" or obj_type=="bhj") and enabled==True:
						db_json_file=os.path.join(sim_paths.get_materials_path(),optical_material,"data.json")
						
						if obj_type!="bhj":
							widget=tab_class("epitaxy", uid=uid, json_postfix="shape_dos", db_json_file=db_json_file, db_json_db_path="electrical_constants")
							self.notebook.addTab(widget,name)

						shapes=self.bin.get_token_value(path,"segments")
						for s in range(0,shapes):
							s_path=path+".segment"+str(s)
							
							s_enabled=self.bin.get_token_value(s_path,"enabled")
							
							s_name=self.bin.get_token_value(s_path,"name")
							s_obj_type=self.bin.get_token_value(s_path,"obj_type")
							s_shape_dos_uid=self.bin.get_token_value(s_path,"id")
							show_dos=False
							if s_enabled==True:
								if s_obj_type=="active":
									show_dos=True
								if s_obj_type=="bhj":
									show_dos=True

							if show_dos==True:
								widget=tab_class("epitaxy",uid=s_shape_dos_uid, json_postfix="shape_dos")
								widget.tab.json_human_path=""
								self.notebook.addTab(widget,s_name)
		
		if electrical_solver=="circuit":
			for l in range(0,layers):
				path="epitaxy.segment"+str(l)
				obj_type=self.bin.get_token_value(path,"obj_type")
				name=self.bin.get_token_value(path,"name")
				uid=self.bin.get_token_value(path,"id")
				if obj_type=="active":
					name="Electrical "+name
					widget=tab_class("epitaxy",uid=uid, json_postfix="shape_electrical")
					self.notebook.addTab(widget,name)

			world_segments=self.bin.get_token_value("world.world_data","segments")
			for s in range(0,world_segments):
				path="world.world_data.segment"+str(s)
				enabled=self.bin.get_token_value(path,"enabled")
				name=self.bin.get_token_value(path,"name")
				uid=self.bin.get_token_value(path,"id")
				obj_type=self.bin.get_token_value(path,"obj_type")
				if enabled==True:
					if obj_type=="active":
						name="Electrical "+name
						widget=tab_class("world.world_data",uid=uid, json_postfix="shape_electrical")
						self.notebook.addTab(widget,name)

		self.changed_click()
		self.notebook.blockSignals(False)

	def show_dialog(self,token,icon, text,duplicate_to_token=None):
		w=self.notebook.currentWidget()
		uid=w.tab.uid
		json_path=self.get_json_path(uid)
		value=self.bin.get_token_value(json_path+".shape_dos",token)

		ret=dlg_get_text2( text, str(value),icon)
		if ret.ret!=None:
			depth=0.0
			try:
				value=-abs(float(ret.ret))
			except:
				error_dlg(self,_("That's not a number.."))
				return
			self.bin.set_token_value(json_path+".shape_dos",token,float(value))
			if duplicate_to_token!=None:
				self.bin.set_token_value(json_path+".shape_dos",duplicate_to_token,float(value))
			self.bin.save()
			self.update_menus()


	def callback_min_trap_depth(self):
		self.show_dialog("srh_stop", "electrical.png", _("Minimum trap depth (eV):"))

	def callback_max_trap_depth(self):
		self.show_dialog("srh_start", "electrical.png", _("Maximum trap depth (eV):"))

	def callback_fermi_min_max(self):
		self.show_dialog("nstart", "electrical.png", _("Minimum fermi level (eV):"),duplicate_to_token="pstart")

	def callback_fermi_n(self):
		self.show_dialog("npoints","mesh.png", _("Number of carrier density points to calculate:"),duplicate_to_token="ppoints")

	def callback_fermi_i(self):
		self.show_dialog("Esteps","mesh.png", _("Number of steps in the Fermi-dirac integral:"))

	def help(self):
		help_window().help_set_help("tab.png","<big><b>Density of States</b></big>\nThis tab contains the electrical model parameters, such as mobility, tail slope energy, and band gap.")

	def changed_click(self):
		self.buttons_update()
		self.update_menus()

	def callback_buttons(self):
		text=self.sender().text()
		tab = self.notebook.currentWidget()
		if tab==None:
			return

		uid=tab.tab.uid
		json_path=self.get_json_path(uid)
		json_path=json_path+".shape_dos"
		segments=self.bin.get_token_value("epitaxy","segments")

		if text==_("Enable\nDrift Diff."):
			dd_enabled=self.dd_enabled.isChecked()
			self.bin.set_token_value(json_path,"dd_enabled",dd_enabled)

			if dd_enabled==False:
				self.bin.set_token_value(json_path,"dos_enable_auger",False)
				self.bin.set_token_value(json_path,"ss_srh_enabled",False)
				self.bin.set_token_value(json_path,"srh_bands",0)
				self.singlet.setChecked(False)

		elif text==_("Enable\nAuger"):
			self.bin.set_token_value(json_path,"dos_enable_auger",self.auger.isChecked())
		elif text==_("Dynamic\nSRH traps"):
			if self.traps.isChecked()==True:
				self.bin.set_token_value(json_path,"srh_bands",5)
			else:
				self.bin.set_token_value(json_path,"srh_bands",0)
		elif text==_("Equilibrium\nSRH traps"):
			self.bin.set_token_value(json_path,"ss_srh_enabled",self.steady_state_srh.isChecked())
		elif text==_("Excitons"):
			self.bin.set_token_value(json_path,"exciton_enabled",self.exciton.isChecked())
		elif text==_("Excited\nstates laser"):
			self.bin.set_token_value(json_path,"singlet_enabled",self.singlet.isChecked())
			#self.singlet_opv.setChecked(False)
		elif text==_("Excited\nstates OPV"):
			self.bin.set_token_value(json_path,"singlet_opv_enabled",self.singlet_opv.isChecked())
		elif text==_("Configure"):
			from config_window import class_config_window
			self.config=class_config_window([json_path+".config"],[_("DoS Config")],title=_("Dos Config"),icon="electrical")
			self.config.changed.connect(self.update_values)
			self.config.show()

		tab.tab.hide_show_widgets()
		self.bin.save()
		self.buttons_update()
		self.update_values()
		global_object_run("ribon_electrical_update_buttons")

	def buttons_update(self):
		if self.bin.get_token_value("electrical_solver","solver_type")=="circuit":
			self.dd_enabled.setVisible(False)
			self.auger.setVisible(False)
			self.traps.setVisible(False)
			self.steady_state_srh.setVisible(False)
			self.exciton.setVisible(False)
			self.singlet.setVisible(False)
			return

		tab = self.notebook.currentWidget()
		if tab==None:
			return
		uid=tab.tab.uid
		json_path=self.get_json_path(uid)
		json_path=json_path+".shape_dos"
		dd_enabled=self.bin.get_token_value(json_path,"dd_enabled")
		dos_enable_auger=self.bin.get_token_value(json_path,"dos_enable_auger")
		ss_srh_enabled=self.bin.get_token_value(json_path,"ss_srh_enabled")
		exciton_enabled=self.bin.get_token_value(json_path,"exciton_enabled")
		singlet_enabled=self.bin.get_token_value(json_path,"singlet_enabled")
		singlet_opv_enabled=self.bin.get_token_value(json_path,"singlet_opv_enabled")
		srh_bands=self.bin.get_token_value(json_path,"srh_bands")

		if dd_enabled==True:
			self.auger.setEnabled(True)
			self.traps.setEnabled(True)
			self.singlet.setEnabled(True)
			self.steady_state_srh.setEnabled(True)
		else:
			self.auger.setEnabled(False)
			self.traps.setEnabled(False)
			self.singlet.setEnabled(False)
			self.steady_state_srh.setEnabled(False)

		self.configure.setEnabled(True)

		self.dd_enabled.setChecked(dd_enabled)
		self.auger.setChecked(dos_enable_auger)
		self.steady_state_srh.setChecked(ss_srh_enabled)
		self.exciton.setChecked(exciton_enabled)
		self.singlet.setChecked(singlet_enabled)
		self.singlet_opv.setChecked(singlet_opv_enabled)

		if srh_bands>0:
			self.traps.setChecked(True)
		else:
			self.traps.setChecked(False)

	def closeEvent(self, event):
		global_object_delete("dos_update")
		event.accept()
