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

## @package ribbon_database
#  The database ribbon.
#


import os
from icon_lib import icon_get

from cal_path import get_css_path

#qt
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget

from doping import doping_window
from contacts import contacts_window
from cal_path import get_materials_path
from g_open import g_open
from g_open import g_open_window

from help import help_window
from cost import cost


from parasitic import parasitic

from util import wrap_text
from dlg_get_text2 import dlg_get_text2

from error_dlg import error_dlg

from QAction_lock import QAction_lock
from cal_path import get_user_data_path
import webbrowser
from cal_path import sim_paths

from lock import get_lock
from ribbon_page import ribbon_page
from json_root import json_root
from json_base import json_base
from QWidgetSavePos import QWidgetSavePos
from sim_name import sim_name

class ribbon_database(ribbon_page):
	def __init__(self):
		ribbon_page.__init__(self)
	
		self.materials = QAction_lock("organic_material", _("Materials\ndatabase"), self,"ribbion_db_materials")
		self.materials.clicked.connect(self.callback_view_materials)
		self.addAction(self.materials)

		self.spectra_file = QAction_lock("spectra_file", _("Optical\ndatabase"), self,"ribbion_db_spectra")
		self.spectra_file.clicked.connect(self.callback_view_optical)
		self.addAction(self.spectra_file)

		self.user = QAction_lock("folder", _("User\ndata"), self,"ribbion_db_user_data")
		self.user.clicked.connect(self.callback_configure_user_data)
		self.addAction(self.user)

		self.shape = QAction_lock("shape", _("Shape\ndatabase"), self,"ribbion_db_shape")
		self.shape.clicked.connect(self.callback_configure_shape)
		self.addAction(self.shape)

		self.filters = QAction_lock("filter_wheel", _("Filters\ndatabase"), self,"ribbion_db_materials")
		self.filters.clicked.connect(self.callback_view_filters)
		self.addAction(self.filters)

		self.home_backup = QAction_lock("backup", _("Backup\nSimulaion"), self,"ribbion_db_backup")
		self.home_backup.clicked.connect(self.callback_home_backup)
		self.addAction(self.home_backup)

		self.solar = QAction_lock("weather-few-clouds", _("Solar spectrum\ngenerator"), self,"solar_spectrum_tool")
		self.solar.clicked.connect(self.callback_solar)
		self.addAction(self.solar)

	def update(self):
		pass


	def setEnabled(self,val):
		self.materials.setEnabled(val)
		self.spectra_file.setEnabled(val)
		self.user.setEnabled(val)
		self.shape.setEnabled(val)
		self.home_backup.setEnabled(val)


	def on_new_shape_clicked(self):
		self.dialog.vbox.viewer.new_shape()

	def callback_view_materials(self):
		self.dialog=g_open_window(get_materials_path(),big_toolbar=True)
		self.new_materials = QAction_lock("add_material", wrap_text(_("Add Material"),8), self,"add_material")
		self.new_materials.clicked.connect(self.dialog.vbox.viewer.new_material)
		self.dialog.vbox.toolbar.addAction(self.new_materials)

		self.dialog.vbox.menu_new_material_enabled=True
		self.dialog.show()

	def callback_view_filters(self):
		self.dialog=g_open_window(sim_paths.get_filters_path(),big_toolbar=True)
		self.new_materials = QAction_lock("add_filter", wrap_text(_("Add Filter"),8), self,"add_filter")
		self.new_materials.clicked.connect(self.dialog.vbox.viewer.new_filter)
		self.dialog.vbox.toolbar.addAction(self.new_materials)

		self.dialog.vbox.menu_new_material_enabled=True
		self.dialog.show()

	def callback_view_optical(self):
		self.dialog=g_open_window(sim_paths.get_spectra_path(),big_toolbar=True)
		self.new_materials = QAction_lock("add_spectra", wrap_text(_("Add Spectra"),8), self,"add_spectra")
		self.new_materials.clicked.connect(self.dialog.vbox.viewer.new_spectra)
		self.dialog.vbox.toolbar.addAction(self.new_materials)
		self.dialog.show()

	def callback_update_window(self):
		webbrowser.open(sim_name.web+"/download_materials.php")

	def callback_configure_shape(self):
		self.dialog=g_open_window(sim_paths.get_shape_path(),big_toolbar=True)
		self.new_shape = QAction_lock("add_shape", wrap_text(_("Add Shape"),8), self,"add_shape")
		self.new_shape.clicked.connect(self.on_new_shape_clicked)
		self.dialog.vbox.toolbar.addAction(self.new_shape)
		self.dialog.show()

	def callback_configure_user_data(self):
		self.dialog=g_open_window(get_user_data_path(),big_toolbar=True)
		self.dialog.show()

	def callback_solar(self):
		from solar_spectrum_gen_window import solar_spectrum_gen_window
		self.solar_window=solar_spectrum_gen_window()

		self.solar_window.show()

	def callback_home_backup(self):
		backup_path=sim_paths.get_backup_path()
		if os.path.isdir(backup_path)==False:
			os.makedirs(backup_path)

		data=json_base("backup")
		data.include_name=False
		data.var_list.append(["icon","backup"])
		data.var_list.append(["item_type","backup_main"])
		data.var_list.append(["hidden","True"])
		data.var_list_build()

		data.save_as(os.path.join(backup_path,"data.json"))

		self.dialog=g_open(backup_path,big_toolbar=True)
		self.new_backup = QAction_lock("add_backup", wrap_text(_("New backup"),2), self,"add_backup")
		self.new_backup.clicked.connect(self.on_new_backup)
		self.dialog.vbox.toolbar.addAction(self.new_backup)

		self.dialog.exec_()

	def on_new_backup(self):
		from backup import backup
		new_backup_name=dlg_get_text2( _("New backup:"), _("New backup name"),"add_backup")
		new_backup_name=new_backup_name.ret
		if new_backup_name!=None:
			new_backup=os.path.join(self.dialog.viewer.path,new_backup_name)
			backup(new_backup,get_sim_path())
			self.dialog.viewer.fill_store()
