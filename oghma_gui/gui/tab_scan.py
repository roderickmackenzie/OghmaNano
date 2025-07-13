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

## @package tab_scan
#  The scan tab widget rewritten to use json
#

import os
from plot import check_info_file
from dat_file import dat_file
from cmp_class import cmp_class
from token_lib import tokens

from scan_plot import scan_gen_plot_data

from g_open import g_open
from icon_lib import icon_get

#scan_io
from scan_io import scan_push_to_hpc
from scan_io import scan_plot_fits
from scan_io import scan_io
from token_lib import fast_lib

#qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QDialog,QAction,QStatusBar, QTabWidget

#window
from plot_dlg import plot_dlg_class
from select_param import select_param
from error_dlg import error_dlg
from g_tab2_bin import g_tab2_bin

import i18n
_ = i18n.language.gettext

from help import help_window
from cal_path import sim_paths
from scan_io import scan_archive
from win_lin import desktop_open

import datetime

from decode_inode import decode_inode
from css import css_apply
from dir_viewer import dir_viewer
from server import server_get

from scan_tab_ribbon import scan_tab_ribbon

from multiplot import multiplot
import platform
from config_window import class_config_window
from json_c import json_tree_c
from plot_window import plot_window

class tab_scan(QWidget):
	def __init__(self,json_path,uid):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.notebook=QTabWidget()
		self.setWindowTitle(_("Parameter scan editor"))
		self.setWindowIcon(icon_get("scan"))

		self.main_vbox = QVBoxLayout()

		self.scan_tab_vbox = QVBoxLayout()

		self.tokens=tokens()
		self.myserver=server_get()
		self.status_bar=QStatusBar()
		
		self.uid=uid
		json_path=self.refind_json_path()
		name=self.bin.get_token_value(json_path,"name")
		optimizer_enabled=self.bin.get_token_value(json_path+".scan_optimizer","enabled")

		self.scan_io=scan_io()
		self.scan_io.parent_window=self
		self.scan_io.load(sim_paths.get_sim_path(),name)

		toolbar=QToolBar()

		self.scan_tab_vbox.addWidget(toolbar)

		self.tab2 = g_tab2_bin(toolbar=toolbar)

		css_apply(self.notebook,"tab_default.css")
		self.notebook.setMovable(True)

		self.tab2.set_tokens(["human_var","values","opp","token_json","token_json1"])
		self.tab2.set_labels([_("Parameter to scan"),_("Values"), _("Opperation"),_("JSON Variable 0"),_("JSON Variable 1")])

		self.tab2.json_root_path=json_path
		self.tab2.uid=self.uid

		self.tab2.fixup_new_row=self.fixup_new_row
		self.tab2.setColumnWidth(0, 300)
		self.tab2.setColumnWidth(1, 300)
		self.tab2.setColumnWidth(2, 300)
		self.tab2.setColumnWidth(3, 20)
		self.tab2.setColumnWidth(4, 20)
		self.tab2.populate()
		self.tab2.changed.connect(self.cell_changed)
		self.tab2.callback_a=self.callback_show_list

		self.scan_tab_vbox.addWidget(self.tab2)

		self.notebook.setMinimumSize(1000,500)
				
		self.program_widget=QWidget()
		self.program_widget.setLayout(self.scan_tab_vbox)
		self.notebook.addTab(self.program_widget,"Commands")
		if os.path.isdir(self.scan_io.scan_dir)==False:
				os.mkdir(self.scan_io.scan_dir)

		self.viewer=dir_viewer(self.scan_io.scan_dir)
		self.viewer.data.show_back_arrow=True
		self.notebook.addTab(self.viewer,"Output")

		self.ribbon=scan_tab_ribbon()
		self.ribbon.tb_simulate.start_sim.connect(self.callback_run_simulation)
		self.ribbon.tb_clean.triggered.connect(self.clean_scan_dir)
		self.ribbon.tb_plot.triggered.connect(self.callback_gen_plot_command)
		self.ribbon.tb_notes.triggered.connect(self.callback_notes)
		self.ribbon.tb_optimizer.triggered.connect(self.callback_optimizer)
		self.ribbon.menu_tb_optimizer_configure_item.triggered.connect(self.callback_menu_tb_optimizer)
		self.tab2.new_row_clicked.connect(self.add_line)
		self.main_vbox.addWidget(self.ribbon)
		self.main_vbox.addWidget(self.notebook)

		self.main_vbox.addWidget(self.status_bar)		
		self.setLayout(self.main_vbox)

		self.select_param_window=select_param(self.tab2)
		self.select_param_window.human_path_col=0
		self.select_param_window.json_path_col=3

		self.select_param_window.update()

		self.select_param_window.set_save_function(self.callback_save)
		self.rebuild_op_type_widgets()
		self.ribbon.tb_optimizer.setChecked(optimizer_enabled)
		self.plot_windows=[]

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid("scans",self.uid)
		return ret

	def add_line(self,data):
		help_window().help_set_help("list-add.png",_("<big><b>The scan window</b></big><br> Now using the drop down menu in the prameter to change 'column', select the device parameter you wish to vary, an example may be dos0/Electron Mobility. Now enter the values you would like it to scan oveer in the  'Values', an example could be '1e-3 1e-4 1e-5 1e-6'.  And hit the double arrorw to run the simulation."))
		self.rebuild_op_type_widgets()

	def plot_results(self,data_file):
		data_file.key_units=self.get_units()
		plot_files, plot_labels, config_file = scan_gen_plot_data(data_file,self.scan_io.scan_dir)
		plot_win=plot_window()
		plot_win.init(plot_files,plot_labels)
		self.plot_windows.append(plot_win)
		plot_win.closed.connect(self.remove_plot_window)

		self.last_plot_data=data_file
		return

	def remove_plot_window(self, window):
		if window in self.plot_windows:
			self.plot_windows.remove(window)

	def get_units(self):
		token=""
		return ""
		for i in range(0,self.tab2.rowCount()):
			if self.tab2.get_value(i,2)=="scan":
				for ii in range(0,len(self.param_list)):
					if self.tab2.get_value(i,0)==self.param_list[ii].human_label:
						token=self.param_list[ii].token
				break
		if token!="":
			found_token=self.tokens.find(token)
			if type(found_token)!=bool:
				return found_token.units

		return ""


	def clean_scan_dir(self):
		self.scan_io.clean_dir()

	def plot_fits(self):
		scan_plot_fits(self.scan_io.scan_dir)

	def push_to_hpc(self):
		scan_push_to_hpc(self.scan_io.scan_dir,False)

	def push_unconverged_to_hpc(self):
		scan_push_to_hpc(self.scan_io.scan_dir,True)

	def scan_archive(self):
		scan_archive(self.scan_io.scan_dir)

	def build_scan(self):
		self.scan_io.set_base_dir(sim_paths.get_sim_path())
		self.scan_io.build_scan()


	def callback_plot_results(self):
		self.plot_results(self.last_plot_data)

	def callback_last_menu_click(self, widget, data):
		#print("here one!")
		self.plot_results(data)

	def callback_reopen_xy_window(self):
		if len(self.plotted_graphs)>0:
			pos=len(self.plotted_graphs)-1
			plot_data=dat_file()
			plot_data.file0=self.plotted_graphs[pos].file0
			plot_xy_window=plot_dlg_class(plot_data)
			plot_xy_window.run()
			plot_now=plot_xy_window.ret

			if plot_now==True:
				self.plot_results(plot_data)
				self.plotted_graphs.refresh()

	def callback_gen_plot_command(self):
		dialog=g_open(self.scan_io.scan_dir,act_as_browser=False)
		ret=dialog.exec_()

		if ret==QDialog.Accepted:
			full_file_name=dialog.get_filename()

			dir_type=decode_inode(full_file_name)
			if dir_type!=None:
				if dir_type.type=="snapshots":
					self.snapshot_window=cmp_class(full_file_name)
					self.snapshot_window.show()
					return

			file_name=os.path.basename(full_file_name)

			plot_data=dat_file()
			plot_data.path=self.scan_io.scan_dir
			plot_data.example_file0=full_file_name
			plot_data.example_file1=full_file_name

			plot_now=False
			if check_info_file(file_name)==True:
				plot_data.file0=file_name
				plot_xy_window=plot_dlg_class(plot_data)
				plot_xy_window.run()
				plot_now=plot_xy_window.ret
			else:
				plot_data.file0=file_name
				plot_data.tag0=""
				plot_data.file1=""
				plot_data.tag1=""
				plot_now=True

			if plot_now==True:
				self.plot_results(plot_data)

				#self.plotted_graphs.refresh()

	def cell_changed(self):
		self.rebuild_op_type_widgets()
		self.callback_save()

	def callback_combo_changed(self):
		combobox = self.sender()
		ix = self.tab2.indexAt(combobox.pos())
		y=ix.row()
		value=self.tab2.get_value(y,2)
		if value == "constant":
			self.tab2.set_value(y,1,"0.0",None)
			self.tab2.set_value(y,4,"",None)
		elif value == "scan":
			self.tab2.set_value(y,1,"1e-5 1e-6 1e-7 1e-8",None)
			self.tab2.set_value(y,4,"",None)
		elif value == "none":
			self.tab2.set_value(y,4,"none",None)
		else:
			self.tab2.set_value(y,1,"duplicate",None)
			json_path=self.bin.human_path_to_json(fast_lib,value)
			self.tab2.set_value(y,4,json_path,None)
		self.callback_save()


	def rebuild_op_type_widgets(self):
		self.tab2.blockSignals(True)
		items=[]
		items.append("scan")
		items.append("constant")
		items.append("none")

		json_path=self.refind_json_path()
		segments=self.bin.get_token_value(json_path,"segments")

		for n in range(0,segments):
			human_var=self.bin.get_token_value(json_path+".segment"+str(n),"human_var")
			items.append(human_var)
		
		for i in range(0,self.tab2.rowCount()):
			combobox=self.tab2.cellWidget(i,2)
			combobox.blockSignals(True)			
			combobox.clear()
			

			for a in items:
				combobox.addItem(a)
			opp=self.bin.get_token_value(json_path+".segment"+str(i),"opp")
			uid=self.bin.get_token_value(json_path+".segment"+str(i),"id")

			self.tab2.set_value(i,2,opp,uid)
			combobox.blockSignals(False)

		self.tab2.blockSignals(False)


	def callback_run_simulation(self):
		if self.tab2.rowCount() == 0:
			error_dlg(self,_("You have not selected any parameters to scan through.  Use the add button."))
			return

		json_path=self.refind_json_path()
		name=self.bin.get_token_value(json_path,"name")
		optimizer_enabled=self.bin.get_token_value(json_path+".scan_optimizer","enabled")

		if optimizer_enabled==False:
			self.scan_io.load(sim_paths.get_sim_path(),name)
			self.scan_io.myserver=server_get()
			self.scan_io.myserver.callback=self.callback_build_plots
			self.scan_io.set_base_dir(sim_paths.get_sim_path())
			self.scan_io.run()
		else:
			self.myserver.add_job(sim_paths.get_sim_path(),"--optimizer "+name+" --path "+sim_paths.get_sim_path())
			self.myserver.start()


	def callback_build_plots(self):
		a=multiplot(gnuplot=True)
		a.find_files(self.scan_io.scan_dir)
		a.save(gnuplot=True,multi_plot=True)

	def callback_notes(self):
		notes_path=os.path.join(self.scan_io.scan_dir,"notes.txt")
		if os.path.isfile(notes_path)==False:
			out = open(notes_path, 'w')
			out.write("Notes on the simulation: "+self.scan_io.scan_dir+"\n")
			out.write("Date: "+datetime.datetime.today().strftime('%Y-%m-%d')+"\n")
			out.write("Generated by: "+" ".join(platform.uname())+"\n")
			out.write("\n")
			out.close()
		else:
			out = open(notes_path, 'a')
			out.write("\n"+datetime.datetime.today().strftime('%Y-%m-%d')+":\n")
			out.close()


		desktop_open(notes_path)

	def fixup_new_row(self,row):
		self.tab2.cellWidget(row, 0).button.clicked.connect(self.callback_show_list)
		json_path=self.refind_json_path()
		name=self.bin.get_token_value(json_path,"name")
		self.status_bar.showMessage(sim_paths.get_sim_path()+"("+name+")")
		self.tab2.cellWidget(row, 2).currentIndexChanged.connect(self.callback_combo_changed)

	def callback_save(self):
		self.bin.save()

	def callback_show_list(self):
		self.select_param_window.show()

	def callback_optimizer(self):
		help_window().help_set_help("optimizer.png",_("<big><b>Fast optimizer</b></big><br>When the fast optimizer is enabled simulation results are not written to disk and instead only key paramters are saved in a csv file. Using a spreadsheet you can then search/sort for the desired device parameters. This enables very fast parameter optimization of layer thicknesses."))
		json_path=self.refind_json_path()
		self.bin.set_token_value(json_path+".scan_optimizer","enabled",self.ribbon.tb_optimizer.isChecked())
		self.bin.save()

	def callback_menu_tb_optimizer(self):
		json_path=self.refind_json_path()
		self.mesh_config=class_config_window([path+".scan_optimizer"],[_("Optimizer")],title=_("Scan - Configure Optimizer"),icon="optimizer")
		self.mesh_config.show()

