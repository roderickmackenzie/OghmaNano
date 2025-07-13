# -*- coding: utf-8 -*-
#
#   OghmaNano - Organic and hybrid Material Nano Simulation tool
#   Copyright (C) 2008-2022 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
#
#   https://www.oghma-nano.com
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitationfit
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

## @package fit_window
#  Main fit window
#

import os
from global_objects import global_object_get
from icon_lib import icon_get

from global_objects import global_object_register
from server import server_get
from help import help_window

from fit_configure_window import fit_configure_window

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar, QTableWidget, QAbstractItemView,QFileDialog,QDialog
from PySide2.QtGui import QPainter,QIcon,QCursor

#windows
from gui_util import yes_no_dlg
from tab_fit import tab_fit
from QHTabBar import QHTabBar
from dlg_get_text2 import dlg_get_text2
from fit_progress import fit_progress
from util import wrap_text
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos
from css import css_apply
from fit_ribbon import fit_ribbon
import copy
from shutil import copyfile
from global_objects import global_object_run
import zipfile
from util_zip import extract_file_from_archive
from experiment_bin import experiment_bin

import i18n
_ = i18n.language.gettext

class fit_window(experiment_bin):

	def __init__(self):
		experiment_bin.__init__(self,"tab_fit",window_save_name="window_scan", window_title=_("Fit the simulation to experimental data"),json_search_path="fits.fits",min_y=500,icon="fit",custon_ribbon=fit_ribbon(), add_notebook_in_tab=True)
		#return
		self.fixup_new=self.callback_fixup_new
		self.ribbon.play.start_sim.connect(self.callback_do_fit)
		self.ribbon.play_one.start_sim.connect(self.callback_one_fit)

		self.ribbon.import_data.triggered.connect(self.callback_import)

		self.ribbon.tb_duplicate.triggered.connect(self.callback_duplicate)
		self.ribbon.tb_vars.triggered.connect(self.callback_vars)
		self.ribbon.tb_rules.triggered.connect(self.callback_rules)
		self.ribbon.tb_configure.triggered.connect(self.callback_configure)

		self.tb_vars= QAction(icon_get("vars"), wrap_text(_("Fitting\nvariables"),4), self)

		self.ribbon.export_zip.triggered.connect(self.callback_export)

		self.ribbon.tb_refresh.triggered.connect(self.callback_update_plots)

		self.fit_progress=fit_progress()
		self.h_notebook.addTab(self.fit_progress,"Fit progress")

		self.fit_configure_window=None
		self.ribbon.enable.changed.connect(self.callback_enable)

		self.update_interface()
		self.notebook.currentChanged.connect(self.update_interface)

		fit_method=self.bin.get_token_value("fits.fit_config","fit_method")
		self.ribbon.combobox.setValue_using_english(fit_method)
		self.ribbon.combobox.currentIndexChanged.connect(self.callback_combobox_changed)
		self.bin.add_call_back(self.callback_update_values)
		self.destroyed.connect(self.doSomeDestruction)

	def get_new_data_file(self):
		files=[]
		segments=self.bin.get_token_value("fits.fits","segments")
		for i in range(0,segments):
			data_file=self.bin.get_token_value("fits.fits.segment"+str(i)+".import_config","data_file")
			files.append(data_file)

		for i in range(0,100):
			name="fit_data"+str(i)+".inp"
			if name not in files:
				return  name
		return False

	def callback_fixup_new(self,path_of_new_tab):
		value=self.get_new_data_file()
		self.bin.set_token_value(path_of_new_tab+".import_config","data_file",value)

	def callback_combobox_changed(self):
		value=self.ribbon.combobox.currentText_english()
		self.bin.set_token_value("fits.fit_config","fit_method",value)
		if self.fit_configure_window!=None:
			self.fit_configure_window.config_tab.tab.hide_show_widgets()
		self.bin.save()

	def callback_update_plots(self):
		for i in range(0,self.notebook.count()):
			tab = self.notebook.widget(i)
			tab.update_graphs()

		self.fit_progress.update()

	def callback_update_values(self):
		for i in range(0,self.notebook.count()):
			tab = self.notebook.widget(i)
			tab.update_values()

		#global_object_run("clear_terminal")

	def callback_configure(self):
		self.configure_show(3)

	def callback_duplicate(self):
		self.configure_show(0)

	def callback_vars(self):
		self.configure_show(1)

	def callback_rules(self):
		self.configure_show(2)

	def configure_show(self,tab_number):
		if self.fit_configure_window==None:
			self.fit_configure_window=fit_configure_window("fit_config")

		help_window().help_set_help("vars.png",_("<big><b>The fitting variables window</b></big><br> Use this window to select the variables use to perform the fit."))
		self.fit_configure_window.show()
		if tab_number!=None:
			self.fit_configure_window.notebook.setCurrentIndex(tab_number)

	def remove_invalid(self,input_name):
		return input_name.replace (" ", "_")

	def callback_import(self):
		tab = self.notebook.currentWidget()
		tab.import_data()

	def callback_one_fit(self):
		if os.path.isfile(os.path.join(sim_paths.get_sim_path(),"sim.json"))==False:
			extract_file_from_archive(sim_paths.get_sim_path(),os.path.join(sim_paths.get_sim_path(),"sim.oghma"),"sim.json")
		my_server=server_get()
		my_server.clear_cache()
		my_server.clear_jobs()
		my_server.set_fit_update_function(self.callback_update_plots)
		my_server.add_job(sim_paths.get_sim_path(),"--1fit")
		#print(my_server.print_jobs())
		my_server.start()

	def callback_do_fit(self):
		if os.path.isfile(os.path.join(sim_paths.get_sim_path(),"sim.json"))==False:
			extract_file_from_archive(sim_paths.get_sim_path(),os.path.join(sim_paths.get_sim_path(),"sim.oghma"),"sim.json")
		my_server=server_get()
		my_server.clear_jobs()
		my_server.clear_cache()
		my_server.set_fit_update_function(self.callback_update_plots)
		my_server.add_job(sim_paths.get_sim_path(),"--fit")
		#print(my_server.print_jobs())
		my_server.start()

	def callback_enable(self):
		tab = self.notebook.currentWidget()
		json_path=self.bin.find_path_by_uid("fits.fits",tab.uid)
		self.bin.set_token_value(json_path+".config","enabled",str(self.ribbon.enable.enabled))
		index=self.notebook.currentIndex()
		self.notebook.setTabText(index, tab.get_tab_text())
		self.bin.save()

	def update_interface(self):
		super().update_interface()
		tab = self.notebook.currentWidget()
	
		if type(tab)==tab_fit:
			found, tab_path = self.get_current_item()
			json_path=self.bin.find_path_by_uid("fits.fits",tab.uid)
			name=self.bin.get_token_value(tab_path,"name")
			uid=self.bin.get_token_value(tab_path,"id")
			enabled=self.bin.get_token_value(tab_path+".config","enabled")
			imported_exp_data_file=self.bin.get_token_value(tab_path+".import_config","data_file")

			self.status_bar.showMessage("name="+name+", json_path="+tab_path+", data_file="+imported_exp_data_file)
			self.ribbon.enable.setState(enabled)
			self.ribbon.enable.setEnabled(True)
			self.ribbon.import_data.setEnabled(True)
	
		elif type(tab)==fit_progress:
			self.ribbon.enable.setEnabled(False)
			self.ribbon.import_data.setEnabled(False)

		#self.status_bar.showMessage("ROD")

	def doSomeDestruction(self):
		self.bin.remove_call_back(self.callback_update_values)

	def __del__(self):
		my_server=server_get()
		my_server.set_fit_update_function(None)

	def callback_export(self):
		types=[]
		dialog = QFileDialog(self)
		dialog.setDirectory(sim_paths.get_sim_path())
		dialog.selectFile(os.path.basename(sim_paths.get_sim_path()))
		dialog.setWindowTitle(_("Export the simulation"))
		dialog.setAcceptMode(QFileDialog.AcceptSave)
		types.append(_("Zip file")+" (*.zip)")

		dialog.setNameFilters(types)
		dialog.setFileMode(QFileDialog.ExistingFile)
		dialog.setAcceptMode(QFileDialog.AcceptSave)

		if dialog.exec_() == QDialog.Accepted:
			file_name = dialog.selectedFiles()[0]
			if file_name.endswith(".zip")==False:
				file_name=file_name+".zip"

			zf = zipfile.ZipFile(file_name, 'a',zipfile.ZIP_DEFLATED)

			segments=self.bin.get_token_value("fits.fits","segments")
			for n in range(0,segments):
				segment_path="fits.fits.segment"+str(n)
				name=self.bin.get_token_value(segment_path,"name")
				enabled=self.bin.get_token_value(segment_path+".config","enabled")
				sim_data=self.bin.get_token_value(segment_path+".config","sim_data")
				data_file=self.bin.get_token_value(segment_path+".import_config","data_file")
				if enabled==True:
					file_name=os.path.join(os.getcwd(), "sim",name,sim_data)
					if os.path.isfile(file_name):
						f=open(file_name, mode='rb')
						lines = f.read()
						f.close()

						zf.writestr(os.path.join(name,sim_data), lines)

					file_name=os.path.join(os.getcwd(), data_file)
					if os.path.isfile(file_name):
						f=open(file_name, mode='rb')
						lines = f.read()
						f.close()

						zf.writestr(os.path.join(name,data_file), lines)

			zf.close()

