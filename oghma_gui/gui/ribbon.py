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

## @package ribbon
#  Main ribbon class for main window.
#



from json_local_root import json_local_root

#qt
from gQtCore import QSize, gSignal, Qt
from PySide2.QtWidgets import QWidget,QLabel,QHBoxLayout,QToolBar, QToolButton,QMenu, QAction
#from PySide2.QtWidgets import QTabWidget

from ribbon_database import ribbon_database
from ribbon_simulations import ribbon_simulations
from ribbon_electrical import ribbon_electrical
from ribbon_optical import ribbon_optical
from ribbon_information import ribbon_information
from ribbon_sim_mode import ribbon_sim_mode
from icon_lib import icon_get

from about import about_dlg

from ribbon_cluster import ribbon_cluster
from css import css_apply

from status_icon import status_icon_stop
from global_objects import global_object_get
from server import server_get

from connect_to_cluster import connect_to_cluster
from ribbon_base import ribbon_base
from error_dlg import error_dlg
from ribbon_file import ribbon_file
import webbrowser

from help import help_window
from lock import get_lock
from ribbon_thermal import ribbon_thermal
from ribbon_automation import ribbon_automation
from sim_name import sim_name
from json_root import json_root

class QLabel_click(QLabel):
	clicked=gSignal()
	def __init(self, parent):
		QLabel.__init__(self, QMouseEvent)

	def mousePressEvent(self, ev):
		self.clicked.emit()

class ribbon(ribbon_base):

	def callback_menu(self,event):
		self.main_menu.exec_(self.mapToGlobal(event))

	def update(self):
		self.file.update()
		self.database.update()
		self.simulations.update()
		self.electrical.update()
		self.optical.update()
		self.information.update()
		self.ribbon_sim_mode.update()
		self.thermal.update()
		self.automation.update()
		self.setup_tabs()
		self.menu_update()

	def callback_about_dialog(self):
		dlg=about_dlg()
		dlg.exec_()

	def callback_questions(self):
		webbrowser.open(sim_name.web+"/contact.html")

	def mouseReleaseEvent(self,event):
		if event.button()==Qt.RightButton:
			self.main_menu.exec_(event.globalPos())

	def __init__(self):
		ribbon_base.__init__(self)
		self.build_main_menu()
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		#self.customContextMenuRequested.connect(self.callback_menu)

		self.cluster_tab=None

		self.myserver=server_get()

		self.holder=QWidget()
		self.hbox=QHBoxLayout()
		self.holder.setLayout(self.hbox)
		self.toolbar=QToolBar()
		self.toolbar.setIconSize(QSize(32, 32))

		self.help_message=QLabel_click(_(get_lock().question+" <a href=\""+get_lock().my_email+"\">"+get_lock().my_email+"</a>"))
		self.help_message.clicked.connect(self.callback_questions)
		self.about = QToolButton(self)
		self.about.setText(_("About"))
		self.about.pressed.connect(self.callback_about_dialog)

		self.cluster_button = QAction(icon_get("not_connected"), _("Connect to cluster"), self)
		self.cluster_button.triggered.connect(self.callback_cluster_connect)
		self.toolbar.addAction(self.cluster_button)
		
		self.hbox.addWidget(self.help_message)
		self.hbox.addWidget(self.toolbar)
		self.hbox.addWidget(self.about)

		self.setCornerWidget(self.holder)

		self.file=ribbon_file()
		self.addTab(self.file,_("File"))
		
		self.ribbon_sim_mode=ribbon_sim_mode()
		
		self.simulations=ribbon_simulations()

		self.simulations.experiments_changed.connect(self.ribbon_sim_mode.update)

		self.automation=ribbon_automation()
		self.electrical=ribbon_electrical()
		self.optical=ribbon_optical()
		self.thermal=ribbon_thermal()
		self.database=ribbon_database()
		self.tb_cluster=ribbon_cluster()
		self.information=ribbon_information()


		css_apply(self,"style.css")

		self.currentChanged.connect(self.changed_click)
		self.setup_tabs()
		self.menu_update()

	def callback_cluster_connect(self):
		dialog=connect_to_cluster()
		if dialog.exec_():
			self.cluster_tab=global_object_get("cluster_tab")
			global_object_get("notebook_goto_page")(_("Terminal"))
			if self.myserver.cluster==False:
				if self.myserver.connect()==False:
					error_dlg(self,_("Can not connect to cluster."))
			else:
				self.myserver.cluster_disconnect()
				print("Disconnected")

		#print(self.myserver.cluster)

		self.tb_cluster.update()
		if self.myserver.cluster==True:
			self.cluster_button.setIcon(icon_get("connected"))
			status_icon_stop(True)
		else:
			status_icon_stop(False)
			self.cluster_button.setIcon(icon_get("not_connected"))

	def changed_click(self):

		if self.tabText(self.currentIndex()).strip()==_("Editors"):
			help_window().help_set_help(["sunsvoc.png",_("<big><b>Simulation Editors</b></big><br> Use this tab to edit the simulation you wish to perform, you can choose from steady state measurments such as JV curve/Suns-Voc, time domain or frequency domain.  You can also choose to use advanced optical models to understand your data.")])

		if self.tabText(self.currentIndex()).strip()==_("Configure"):
			help_window().help_set_help(["preferences-system.png",_("<big><b>Configure</b></big><br> Use this tab to control advanced features of the simulation, such as finite difference mesh, amount of data written to disk, and the configuration of the back end numerical solvers.")])
		if self.tabText(self.currentIndex()).strip()==_("Simulation type"):
			help_window().help_set_help(["jv.png",_("<big><b>Simulation type</b></big><br> Use this tab to select which simulation mode the model runs in, select between steady state, time domain, frequency domain and optical simulations.")])

		if self.tabText(self.currentIndex()).strip()==_("Databases"):
			help_window().help_set_help(["spectra_file.png",_("<big><b>Databases</b></big><br> Use this tab to explore the materials and optical data bases, you can add and download more materials/optical models using the tools here.")])

		if self.tabText(self.currentIndex()).strip()==_("Information"):
			help_window().help_set_help(["youtube.png",_("<big><b>Information</b></big><br> Access extra information about the model in this tab, there are lots of tutorial videos on YouTube, follow on Twitter for the latest updates.")])

	def build_main_menu(self):
		view_menu = QMenu(self)
		self.main_menu = QMenu(self)
		view=self.main_menu.addMenu(_("View"))

		#view
		self.menu_view_sim_mode=view.addAction(_("Simulation type"))
		self.menu_view_sim_mode.triggered.connect(self.menu_toggle_view)
		self.menu_view_sim_mode.setCheckable(True)

		self.menu_view_editors=view.addAction(_("Editors"))
		self.menu_view_editors.triggered.connect(self.menu_toggle_view)
		self.menu_view_editors.setCheckable(True)

		self.menu_view_automation=view.addAction(_("Automation"))
		self.menu_view_automation.triggered.connect(self.menu_toggle_view)
		self.menu_view_automation.setCheckable(True)

		self.menu_view_electrical=view.addAction(_("Electrical"))
		self.menu_view_electrical.triggered.connect(self.menu_toggle_view)
		self.menu_view_electrical.setCheckable(True)

		self.menu_view_optical=view.addAction(_("Optical"))
		self.menu_view_optical.triggered.connect(self.menu_toggle_view)
		self.menu_view_optical.setCheckable(True)

		self.menu_view_thermal=view.addAction(_("Thermal"))
		self.menu_view_thermal.triggered.connect(self.menu_toggle_view)
		self.menu_view_thermal.setCheckable(True)

		self.menu_view_database=view.addAction(_("Databases"))
		self.menu_view_database.triggered.connect(self.menu_toggle_view)
		self.menu_view_database.setCheckable(True)

		self.menu_view_cluster=view.addAction(_("Cluster"))
		self.menu_view_cluster.triggered.connect(self.menu_toggle_view)
		self.menu_view_cluster.setCheckable(True)

		self.menu_view_information=view.addAction(_("Information"))
		self.menu_view_information.triggered.connect(self.menu_toggle_view)
		self.menu_view_information.setCheckable(True)


	def setup_tabs(self):
		self.clear()
		self.addTab(self.file,_("File"))

		if json_root().gui_config.main_ribbon.sim_mode_visible==True:
			self.addTab(self.ribbon_sim_mode,_("Simulation type"))

		if json_root().gui_config.main_ribbon.editors_visible==True:
			self.addTab(self.simulations,_("Editors"))

		if json_root().gui_config.main_ribbon.automation_visible==True:
			self.addTab(self.automation,_("Automation"))

		if json_root().gui_config.main_ribbon.electrical_visible==True:
			self.addTab(self.electrical,_("Electrical"))

		if json_root().gui_config.main_ribbon.optical_visible==True:
			self.addTab(self.optical,_("Optical"))

		if json_root().gui_config.main_ribbon.thermal_visible==True:
			self.addTab(self.thermal,_("Thermal"))

		if json_root().gui_config.main_ribbon.database_visible==True:
			self.addTab(self.database,_("Databases"))

		if json_root().gui_config.main_ribbon.cluster_visible==True:
			self.addTab(self.tb_cluster,_("Cluster"))

		if json_root().gui_config.main_ribbon.information_visible==True:
			self.addTab(self.information,_("Information"))


	def menu_toggle_view(self):
		json_root().gui_config.main_ribbon.sim_mode_visible=self.menu_view_sim_mode.isChecked()
		json_root().gui_config.main_ribbon.editors_visible=self.menu_view_editors.isChecked()
		json_root().gui_config.main_ribbon.automation_visible=self.menu_view_automation.isChecked()
		json_root().gui_config.main_ribbon.electrical_visible=self.menu_view_electrical.isChecked()
		json_root().gui_config.main_ribbon.optical_visible=self.menu_view_optical.isChecked()
		json_root().gui_config.main_ribbon.thermal_visible=self.menu_view_thermal.isChecked()
		json_root().gui_config.main_ribbon.database_visible=self.menu_view_database.isChecked()
		json_root().gui_config.main_ribbon.cluster_visible=self.menu_view_cluster.isChecked()
		json_root().gui_config.main_ribbon.information_visible=self.menu_view_information.isChecked()

		self.setup_tabs()

		json_root().save()

	def menu_update(self):
		self.menu_view_sim_mode.setChecked(json_root().gui_config.main_ribbon.sim_mode_visible)
		self.menu_view_editors.setChecked(json_root().gui_config.main_ribbon.editors_visible)
		self.menu_view_automation.setChecked(json_root().gui_config.main_ribbon.automation_visible)
		self.menu_view_electrical.setChecked(json_root().gui_config.main_ribbon.electrical_visible)
		self.menu_view_optical.setChecked(json_root().gui_config.main_ribbon.optical_visible)
		self.menu_view_thermal.setChecked(json_root().gui_config.main_ribbon.thermal_visible)
		self.menu_view_database.setChecked(json_root().gui_config.main_ribbon.database_visible)
		self.menu_view_cluster.setChecked(json_root().gui_config.main_ribbon.cluster_visible)
		self.menu_view_information.setChecked(json_root().gui_config.main_ribbon.information_visible)


