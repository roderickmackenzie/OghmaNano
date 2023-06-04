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

## @package fit_window
#  Main fit window
#

import os
from global_objects import global_object_get
from icon_lib import icon_get

from global_objects import global_object_register
from server import server_get
from help import help_window

import i18n
_ = i18n.language.gettext

from fit_configure_window import fit_configure_window

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar, QTableWidget, QAbstractItemView,QFileDialog,QDialog
from PySide2.QtGui import QPainter,QIcon,QCursor

#windows
from gui_util import yes_no_dlg
from fit_tab import fit_tab
from QHTabBar import QHTabBar
from dlg_get_text2 import dlg_get_text2
from fit_progress import fit_progress
from util import wrap_text
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos
from css import css_apply
from fit_ribbon import fit_ribbon
from json_root import json_root
import copy
from shutil import copyfile
from global_objects import global_object_run
import zipfile
from util_zip import extract_file_from_archive

class fit_window(QWidgetSavePos):

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
		if self.fit_configure_window==None:
			self.fit_configure_window=fit_configure_window("fit_config")

		help_window().help_set_help(["vars.png",_("<big><b>The fitting variables window</b></big><br> Use this window to select the variables use to perform the fit.")])
		if self.fit_configure_window.isVisible()==True:
			self.fit_configure_window.hide()
		else:
			self.fit_configure_window.show()

	#def callback_add_page(self,file_name):
	#	new_tab=fit_tab(file_name)
	#	self.notebook.addTab(new_tab,new_tab.get_tab_text())

	def remove_invalid(self,input_name):
		return input_name.replace (" ", "_")

	def callback_import(self):
		tab = self.notebook.currentWidget()
		tab.import_data()

	def callback_view_toggle_tab(self):
		print("add code")
		#self.toggle_tab_visible(data)

	def get_new_data_file(self):
		files=[]
		data=json_root()
		for d in data.fits.fits.segments:
			files.append(d.import_config.data_file)
		#print(files)
		for i in range(0,100):
			name="fit_data"+str(i)+".inp"
			if name not in files:
				return  name
		return False

	def load_tabs(self):
		data=json_root()
		data.fits.fits.fix_identical_uids([])
		for fit in data.fits.fits.segments:
			if fit.import_config.data_file=="none":
				fit.import_config.data_file=self.get_new_data_file()
			new_tab=fit_tab(fit.id)
			self.notebook.addTab(new_tab,new_tab.get_tab_text())



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
		data=json_root()
		tab = self.notebook.currentWidget()
		data_obj=data.fits.fits.find_object_by_id(tab.uid)
		data_obj.config.enabled=self.ribbon.enable.enabled
		index=self.notebook.currentIndex()
		self.notebook.setTabText(index, tab.get_tab_text())
		data.save()

	def update_interface(self):
		tab = self.notebook.currentWidget()
		data=json_root()

		if type(tab)==fit_tab:
			data_obj=data.fits.fits.find_object_by_id(tab.uid)
			self.status_bar.showMessage(data_obj.config.fit_name+","+data_obj.import_config.data_file)
			self.ribbon.enable.setState(data_obj.config.enabled)
			self.ribbon.enable.setEnabled(True)
			self.ribbon.import_data.setEnabled(True)
			self.tab_bar.obj_search_path="json_root().fits.fits"
			self.tab_bar.obj_id=data_obj.id

		if type(tab)==fit_progress:
			self.ribbon.enable.setEnabled(False)
			self.ribbon.import_data.setEnabled(False)


	def __init__(self,name):
		QWidgetSavePos.__init__(self,name)
		json_root()
		#self.data=data.fits
		self.main_vbox = QVBoxLayout()

		#self.setFixedSize(900, 700)
		self.setWindowTitle2(_("Fit the simulation to experimental data"))
		self.setWindowIcon(icon_get("fit"))

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)


		self.tab_bar=QHTabBar()

		self.main_vbox.addWidget(toolbar)

		self.ribbon=fit_ribbon()

		self.ribbon.play.start_sim.connect(self.callback_do_fit)

		self.ribbon.play_one.start_sim.connect(self.callback_one_fit)

		self.ribbon.import_data.triggered.connect(self.callback_import)
		self.ribbon.tb_configure.triggered.connect(self.callback_configure)

		self.ribbon.tb_rename.triggered.connect(self.callback_rename_page)
		self.tab_bar.rename.connect(self.callback_rename_page)
		self.ribbon.tb_delete.triggered.connect(self.callback_delete_page)
		self.tab_bar.delete.connect(self.callback_delete_page)
		self.ribbon.tb_clone.triggered.connect(self.callback_clone_page)
		self.ribbon.tb_new.triggered.connect(self.callback_add_page)
		self.ribbon.export_zip.triggered.connect(self.callback_export)

		self.ribbon.tb_refresh.triggered.connect(self.callback_update_plots)
		self.main_vbox.addWidget(self.ribbon)

		self.notebook = QTabWidget()
		self.h_notebook = QTabWidget()

		self.ribbon.enable.changed.connect(self.callback_enable)
		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		css_apply(self.notebook,"style_h.css")

		#tab_bar.menu_click.connect(self.menu_click)
		self.notebook.setTabBar(self.tab_bar)
		self.notebook.setTabPosition(QTabWidget.West)


		self.notebook.setMovable(True)
		self.h_notebook.addTab(self.notebook,_("Data sets"))

		self.fit_progress=fit_progress()
		self.h_notebook.addTab(self.fit_progress,"Fit progress")

		self.load_tabs()


		self.main_vbox.addWidget(self.h_notebook)

		self.status_bar=QStatusBar()
		self.main_vbox.addWidget(self.status_bar)

		self.setLayout(self.main_vbox)

		self.fit_configure_window=None
		self.update_interface()
		self.notebook.currentChanged.connect(self.update_interface)

		json_root().add_call_back(self.callback_update_values)
		self.destroyed.connect(self.doSomeDestruction)

		#self.tab_bar.menu_click.connect(self.callback_tab_bar_menu_click)


		self.tab_bar.paste.connect(self.do_paste)
		self.tab_bar.tabMoved.connect(self.callback_tab_moved)

	def callback_tab_moved(self,from_pos,to_pos):
		data=json_root()
		data.fits.fits.segments.insert(to_pos, data.fits.fits.segments.pop(from_pos))
		data.save()
		#print("tab")

	def do_paste(self):
		data=json_root()
		tab = self.notebook.currentWidget()
		data_obj=data.fits.fits.find_object_by_id(tab.uid)
		a=copy.deepcopy(data_obj)
		a.load_from_json(self.tab_bar.paste_data)
		a.import_config.data_file=self.get_new_data_file()
		a.update_random_ids()
		data.fits.fits.segments.append(a)
		tab=fit_tab(data.fits.fits.segments[-1].id)
		self.notebook.addTab(tab,data_obj.config.fit_name)

	def doSomeDestruction(self):
		json_root().remove_call_back(self.callback_update_values)


	def callback_rename_page(self):
		tab = self.notebook.currentWidget()
		data=json_root()
		data_obj=data.fits.fits.find_object_by_id(tab.uid)
		new_sim_name=dlg_get_text2( _("Rename the fit:"), data_obj.config.fit_name,"rename.png")

		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:
			
			data_obj.config.fit_name=new_sim_name
			self.notebook.setTabText(self.notebook.currentIndex(), new_sim_name)
			data.save()

	def callback_clone_page(self):
		tab = self.notebook.currentWidget()
		data=json_root()
		data_obj=data.fits.fits.find_object_by_id(tab.uid)
		new_sim_name=dlg_get_text2( _("Clone the experiment:"), data_obj.config.fit_name+"_new","clone.png")

		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:
			
			a=copy.deepcopy(data_obj)
			a.config.fit_name=new_sim_name
			a.update_random_ids()
			#print(a.import_config.data_file)
			a.import_config.data_file=self.get_new_data_file()
			copyfile(os.path.join(sim_paths.get_sim_path(),data_obj.import_config.data_file),os.path.join(sim_paths.get_sim_path(),a.import_config.data_file))
			data.fits.fits.segments.append(a)
			tab=fit_tab(a.id)
			self.notebook.addTab(tab,new_sim_name)
			data.save()

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

			data=json_root()
			for fit in data.fits.fits.segments:
				if fit.config.enabled==True:
					file_name=os.path.join(os.getcwd(), "sim",fit.config.fit_name,fit.config.sim_data)
					if os.path.isfile(file_name):
						f=open(file_name, mode='rb')
						lines = f.read()
						f.close()

						zf.writestr(os.path.join(fit.config.fit_name,fit.config.sim_data), lines)

					file_name=os.path.join(os.getcwd(), fit.import_config.data_file)
					if os.path.isfile(file_name):
						f=open(file_name, mode='rb')
						lines = f.read()
						f.close()

						zf.writestr(os.path.join(fit.config.fit_name,fit.import_config.data_file), lines)

			zf.close()

	def callback_delete_page(self):
		data=json_root()
		if len(data.fits.fits.segments)>1:
			tab = self.notebook.currentWidget()
			#print(tab.uid)
			data_obj=data.fits.fits.find_object_by_id(tab.uid)
			response=yes_no_dlg(self,_("Are you sure you want to delete the experiment: ")+data_obj.config.fit_name)
			if response == True:
				index=self.notebook.currentIndex()
				data.fits.fits.segments.remove(data_obj)
				self.notebook.removeTab(index)
				data.save()

	def callback_add_page(self):
		tab = self.notebook.currentWidget()
		data=json_root()
		data_obj=data.fits.fits.find_object_by_id(tab.uid)
		new_sim_name=dlg_get_text2( _("Make a new fit:"), data_obj.config.fit_name+"_new","document-new.png")

		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:
			a=copy.deepcopy(data_obj)
			a.update_random_ids()
			a.config.fit_name=new_sim_name
			a.import_config.data_file=self.get_new_data_file()
			data.fits.fits.segments.append(a)
			tab=fit_tab(data.fits.fits.segments[-1].id)
			self.notebook.addTab(tab,new_sim_name)
			data.save()


