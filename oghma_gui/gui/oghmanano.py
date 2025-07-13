#!/usr/bin/env python3
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

## @package oghma
#  The main gui code
#

import os
import sys

from sim_name import sim_name

#paths
sys.path.append('./gui/')
sys.path.append('./gui/base/')
sys.path.append('./base/')
sys.path.append("/usr/lib/"+sim_name.install_dir+"/")
sys.path.append("/usr/lib64/"+sim_name.install_dir+"/")
sys.path.append("/usr/share/"+sim_name.install_dir+"/")	#debian


from gui_enable import gui_test
gui_test()

from win_lin import get_platform
from cal_path import calculate_paths
from cal_path import set_sim_path

calculate_paths()

from inp import inp

print(sim_name.name + " (" +sim_name.long_name+")")
print("loading.... please wait...")

import i18n
_ = i18n.language.gettext

#undo
from undo import undo_list_class

from command_args import command_args
from cal_path import sim_paths

command_args(len(sys.argv),sys.argv)


from help import help_window
from help import help_init
from help import language_advert

from QWidgetSavePos import resize_window_to_be_sane

from main_notebook import main_notebook

#server
from server import server_init
from server import server_get

from splash import splash_window
from process_events import process_events
from error_han import error_han
#########bad

#qt
from PySide2.QtWidgets import QMainWindow,QApplication, QWidget, QSizePolicy, QVBoxLayout,QDialog, QFileDialog, QLineEdit
from PySide2.QtGui import QIcon
from gQtCore import Qt, QTimer

from used_files import used_files_add

from icon_lib import icon_init_db
from check_lib_in_bash_rc import check_lib_in_bash_rc
from msg_dlg import msg_dlg
from lock_gui import lock_gui
from lock import get_lock
import webbrowser

from gui_util import yes_no_dlg
from util import isfiletype
from ribbon import ribbon
from error_dlg import error_dlg

from cal_path import to_native_path
from global_objects import global_object_run
#from check_sim_exists import check_sim_exists
from cal_path import sim_paths

from const_ver import const_ver
from json_c import json_local_root
from oghma_local import oghma_local
from oghma_ipc import oghma_ipc
from json_c import json_c
from json_c import json_tree_c
from json_c import json_files_gui_config_load
import ctypes

import faulthandler
faulthandler.enable()
import locale

if get_platform()=="linux" or get_platform()=="wine":
	if os.geteuid() == 0:
		exit(_("Don't run me as root!!"))


class main_window(QMainWindow,oghma_local):

	def __init__(self):
		super(main_window,self).__init__()
		icon_init_db()
		set_sim_path(os.getcwd())
		self.oghma_local_setup()
		self.splash=splash_window()
		self.splash.inc_value()

		process_events()
		process_events()
		if os.path.isdir(os.path.dirname(sys.argv[0]))==False:
			error_dlg(self,_("I can't run from inside a zip file!"))
			sys.exit()

		self.splash.inc_value()
		self.splash.inc_value()

		server_init()
		self.splash.inc_value()
		#self.check_sim_exists=check_sim_exists()
		#self.splash.inc_value()

		#self.check_sim_exists.start_thread()
		#self.splash.inc_value()
		
		#self.check_sim_exists.sim_gone.connect(self.sim_gone)
		self.bin=json_tree_c()

		self.splash.inc_value()
		self.my_server=server_get()
		self.my_server.init(sim_paths.get_sim_path())
		self.splash.inc_value()
		

		self.undo_list=undo_list_class()
		self.splash.inc_value()

		self.ribbon=ribbon()
		self.splash.inc_value()

		self.notebook_active_page=None
		self.setAcceptDrops(True)
		#self.setGeometry(200, 100, 1300, 600)
		self.setWindowTitle(sim_name.long_name+sim_name.web_window_title)

		self.l=lock_gui()

		self.my_server.sim_started.connect(self.gui_sim_start)
		self.splash.inc_value()

		self.my_server.sim_finished.connect(self.gui_sim_stop)
		self.splash.inc_value()

		help_init()
		self.splash.inc_value()

		self.ipc_pipe=oghma_ipc(self.my_server.server.ipc)
		self.ipc_pipe.new_data.connect(self.callback_new_data)
		self.ipc_pipe.start()

		self.notebook=main_notebook()
		vbox=QVBoxLayout()
		self.splash.inc_value()

		vbox.addWidget(self.ribbon)
		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		vbox.addWidget(self.notebook)
		wvbox=QWidget()
		self.splash.inc_value()

		wvbox.setLayout(vbox)
		self.setCentralWidget(wvbox)

		self.splash.inc_value()

		self.statusBar()

		self.setWindowIcon(QIcon(os.path.join(sim_paths.get_image_file_path(),"image.jpg")))		
		self.splash.inc_value()

		self.show_tabs = True
		self.show_border = True

		self.ribbon.file.home_new.clicked.connect(self.callback_new)
		self.ribbon.file.home_open.clicked.connect(self.callback_open)
		self.ribbon.file.home_export.clicked.connect(self.callback_export)

		self.ribbon.file.used_files_click.connect(self.load_sim)
		#self.ribbon.home.undo.triggered.connect(self.callback_undo)
		self.ribbon.file.run.start_sim.connect(self.callback_simulate)
		from PySide2.QtGui import QKeySequence
		from PySide2.QtWidgets import QShortcut
		self.shortcut_run = QShortcut(QKeySequence('F9'), self)
		self.shortcut_run.activated.connect(self.callback_simulate)

		self.splash.inc_value()

		#self.ribbon.home.stop.setEnabled(False)

		self.ribbon.optical.setEnabled(False)
		self.ribbon.thermal.setEnabled(False)
		
		#self.ribbon.home.help.triggered.connect(self.callback_on_line_help)

		resize_window_to_be_sane(self,0.7,0.75)

		print(">>>>",sim_paths.get_sim_path())
		self.change_dir_and_refresh_interface(sim_paths.get_sim_path())
		self.splash.inc_value()


		#self.ribbon.home.sun.changed.connect(self.notebook.update)
		self.ribbon.setAutoFillBackground(True)
		self.splash.inc_value()
		self.show()

		help_window().show()


		self.enable_disable_buttons()

		check_lib_in_bash_rc()

		self.timer=QTimer()

		self.timer.timeout.connect(self.callback_check_reload)
		self.timer.start(1000)

		#from window_ml import window_ml
		#self.window_ml=window_ml()
		#self.showFullScreen()
		#self.timer=QTimer()		
		#self.timer.timeout.connect(self.callback_exit)
		#self.timer.start(2000)

		#print("here")
		#from cmp_class import cmp_class
		#self.plot_win=cmp_class("/home/rod/oghma/oghma8.0/snapshots/")
		#self.plot_win.show()
		#from plot_widget import plot_widget
		#self.g=plot_widget(enable_toolbar=True,force_2d3d=True)
		#self.g.set_labels([_("Spectra")])
		#self.g.load_data(["exciton_output/G.csv","exciton_output/Gn.csv","exciton_output/Gp.csv"])
		#self.g.show()

		#from graph import graph_widget
		#self.g=graph_widget()
		#self.g.load(["charge.csv","fit_data0.inp"])
		#self.g.graph.load_bands(self.bin)
		#self.g.graph.axis_y.hidden=True;
		#self.g.graph.points=True;
		#self.g.graph.lines=False;
		#self.g.graph.info[0].color_map_within_line=True
		#self.g.show()

		#from plot_window import plot_window
		#self.p=plot_window()
		#self.p.init(["Jp.csv"])
		#self.p.show()
		#from morphology_editor import morphology_editor
		#self.p=morphology_editor("/home/rod/oghma_local/morphology/default")
		#self.p.show()
		#from window_mesh_editor import window_mesh_editor
		#self.electrical_mesh=window_mesh_editor(json_path_to_mesh="electrical_solver.mesh")
		#self.electrical_mesh.show()

		#from fit_window import fit_window
		#self.fit_window=fit_window()
		#self.fit_window.show()
		#self.experiment_window.changed.connect(self.callback_experiments_changed)

		#from dir_viewer import dir_viewer,dir_viewer_c
		#self.viewer=dir_viewer("")
		#self.viewer.data.json_data=ctypes.pointer(self.bin)
		#self.viewer.data.data_type=1
		#self.viewer.data.allow_navigation=True
		#self.viewer.set_directory_view(True)
		#self.viewer.data.show_back_arrow=True
		#self.viewer.set_multi_select()
		#self.viewer.setMinimumSize(1000, 600)
		#print(ctypes.sizeof(self.viewer.data))
		#self.viewer.fill_store()
		#self.viewer.show()
		get_lock().lock_ping_server()


	def callback_exit(self):
		exit()

	def callback_check_reload(self):
		self.bin.check_reload()

	def callback_new_data(self,data):
		if data!=None:
			self.my_server.callback_dbus(data)

	def gui_sim_start(self):
		self.notebook_active_page=self.notebook.get_current_page()
		self.notebook.goto_page(_("Terminal"))

	def gui_sim_stop(self):
		if self.notebook_active_page!=None:
			self.notebook.goto_page(self.notebook_active_page)
		global_object_run("display_recalculate")

	def callback_simulate(self):
		self.my_server.clear_cache()
		self.my_server.clear_jobs()
		self.my_server.add_job(sim_paths.get_sim_path(),"")
		self.my_server.start()

	def close_now(self):
		QApplication.quit()
		
	def closeEvent(self, event):
		print("closing")
		self.close_now()
		event.accept()

	def callback_new(self):
		from new_simulation import new_simulation
		help_window().help_set_help("p3ht_pcbm.png",_("<big><b>New simulation!</b></big><br> Now selected the type of device you would like to simulate."))

		dialog=new_simulation()
		dialog.exec_()
		ret=dialog.ret_path

		if ret!=None:
			self.change_dir_and_refresh_interface(dialog.ret_path)
			first_sim_message=self.bin.get_token_value("sim","first_sim_message")
			if first_sim_message!="":
				msgBox = msg_dlg(title=sim_name.web)
				msgBox.setText(first_sim_message.replace("%DIR",dialog.ret_path))
				msgBox.exec_()

	def update_interface(self):
		enable_betafeatures=json_local_root().get_token_value("gui_config","enable_betafeatures")
		if self.notebook.is_loaded()==True:
			#self.check_sim_exists.set_dir(sim_paths.get_sim_path())

			help_window().help_set_help("media-playback-start",_("<big><b>Now run the simulation</b></big><br> Click on the play icon to start a simulation."))

			if enable_betafeatures==True:
				self.ribbon.simulations.qe.setVisible(True)
		else:
			#self.check_sim_exists.set_dir("")
			help_window().help_set_help("icon",_("<big><b>Hi!</b></big><br> I'm the on-line help system :).  If you have any questions or find any bugs please post them to the OghmaNano User forum <a href=\"https://www.oghma-nano.com/forum/\">https://www.oghma-nano.com/forum/</a>."))
			help_window().help_append("document-new",_("Click on the new icon to make a new simulation directory."))
			language_advert()

			if enable_betafeatures==True:
				self.ribbon.simulations.qe.setVisible(True)

	def disable_interface(self):
		self.ribbon.file.setEnabled(False,do_all=True)

		self.ribbon.simulations.setEnabled(False)
		self.ribbon.database.setEnabled(False)
		#self.ribbon.device.setEnabled(False)
		self.ribbon.goto_page(_("File"))

		self.ribbon.electrical.setEnabled(False)
		self.ribbon.optical.setEnabled(False)
		self.ribbon.thermal.setEnabled(False)
		self.notebook.setEnabled(False)


	def enable_disable_buttons(self):
		self.ribbon.file.setEnabled(True)
		self.notebook.setEnabled(True)

		if self.notebook.is_loaded()==True:
			self.ribbon.file.setEnabled_other(True)
			self.ribbon.simulations.setEnabled(True)
			self.ribbon.database.setEnabled(True)
			#self.save_sim.setEnabled(True)
			#self.ribbon.device.setEnabled(True)

			#self.menu_import_lib.setEnabled(True)
			self.ribbon.electrical.setEnabled(True)
			self.ribbon.optical.setEnabled(True)
			self.ribbon.automation.setEnabled(True)
			self.ribbon.thermal.setEnabled(True)
			self.ribbon.goto_page(_("Home"))

		else:
			self.ribbon.file.setEnabled_other(False)

			self.ribbon.simulations.setEnabled(False)
			self.ribbon.database.setEnabled(False)
			#self.ribbon.device.setEnabled(False)
			self.ribbon.goto_page(_("File"))
			self.ribbon.optical.setEnabled(False)
			self.ribbon.automation.setEnabled(False)
			self.ribbon.thermal.setEnabled(False)
			self.ribbon.electrical.setEnabled(False)


	def change_dir_and_refresh_interface(self,new_dir):
		#import time
		#t=time.time()
		edited=False
		loaded=False
		set_sim_path(new_dir)
		file_name=os.path.join(new_dir,"sim.json")
		gui_config_file=os.path.join(new_dir,"gui_config.json")
		alt_file_name=os.path.join(new_dir,"json.inp")

		if inp().isfile(file_name)==True:
			self.bin.load(file_name)
			edited=self.bin.import_old_oghma_file(file_name)
			self.bin.oghma_file_fixup()
			loaded=True
		elif inp().isfile(alt_file_name)==True:
			self.bin.load(alt_file_name)
			self.bin.f.file_name="sim.json"
			self.bin.oghma_file_fixup()
			loaded=True
		#sys.exit(0)

		if loaded==True:
			used_files_add(os.path.join(new_dir,"sim.oghma"))
			self.bin.set_token_value("sim","version",const_ver())
			self.bin.set_token_value("","status","public")
			print(edited)
			if edited==True:
				self.bin.save()
				self.bin.free()
				self.bin.load(file_name)
				self.bin.oghma_file_fixup()
				#msgBox = msg_dlg(title="OghmaNano")
				#msgBox.setText("I have had to repair this file because it was quite old. If simulations do not work, I recommend closing OghmaNano and re-opening the file.")
				#msgBox.exec_()
			else:
				self.bin.save()

		self.splash.inc_value()

		json_files_gui_config_load(gui_config_file)

		
		self.splash.inc_value()

		#calculate_paths()
		self.statusBar().showMessage(sim_paths.get_sim_path())
		self.splash.inc_value()

		self.notebook.load()

		self.update_interface()
		self.enable_disable_buttons()

		self.splash.inc_value()

		if self.notebook.terminal!=None:
			self.my_server.set_terminal(self.notebook.terminal)

		if self.notebook.update_display_function!=None:
			self.my_server.set_display_function(self.notebook.update_display_function)

		self.ribbon.update()
		self.splash.inc_value()

		if self.notebook.is_loaded()==True:
			self.l.run()
			self.notebook.tab_main.three_d.update()

		self.ribbon.electrical.tb_solvers.changed.connect(self.notebook.update_circuit_window)
		try:
			self.ribbon.electrical.tb_solvers.changed.connect(self.notebook.tab_main.ribbon.callback_circuit_diagram)
		except:
			pass


	def load_sim(self,filename):
		new_path=os.path.dirname(filename)
		self.change_dir_and_refresh_interface(new_path)

	def callback_open(self):
		dialog = QFileDialog(self)
		dialog.setWindowTitle(_("Open an existing simulation"))
		dialog.setNameFilter("Simulations - OghmaNano file (*.oghma *.gpvdm)")
		dialog.setFileMode(QFileDialog.ExistingFile)
		if dialog.exec_() == QDialog.Accepted:
			filename = dialog.selectedFiles()[0]
			if filename.endswith(".gpvdm"):
				new_file_name=filename[:-6]+".oghma"
				ret=yes_no_dlg(self,_("To open this file I need to rename it to have a .oghma extention. Do you want me to do that?. I would rename the file: "+filename+" to "+new_file_name))
				if ret==True:
					
					os.rename(filename, new_file_name)
					filename=new_file_name
				else:
					return

			filename=to_native_path(filename)
			self.load_sim(filename)

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
			from util_zip import archive_add_dir
			if file_name.endswith(".zip")==False:
				file_name=file_name+".zip"
			archive_add_dir(file_name,sim_paths.get_sim_path(),sim_paths.get_sim_path())

	def callback_on_line_help(self):
		webbrowser.open(sim_name.web)


	def callback_undo(self):
		l=self.undo_list.get_list()
		if len(l)>0:
			value=l[len(l)-1][2]
			w_type=l[len(l)-1][3]

			if type(w_type)==QLineEdit:
				self.undo_list.disable()
				w_type.setText(value)
				self.undo_list.enable()

			l.pop()

	def sim_gone(self):
		error_dlg(self,_("The simulation directory has been deleted."))
		self.update_interface()
		self.enable_disable_buttons()


	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls:
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasUrls:
			event.setDropAction(Qt.CopyAction)
			event.accept()
			links = []
			for url in event.mimeData().urls():
				links.append(str(url.toLocalFile()))
			if len(links)==1:
				file_name=links[0]
				if isfiletype(file_name,"gpvdm")==True:
					self.load_sim(file_name)
				elif os.path.isdir(file_name)==True:
					file_name=os.path.join(file_name,"sim.oghma")
					if os.path.isfile(file_name)==True:
						self.load_sim(file_name)
		else:
			event.ignore()
            
if __name__ == '__main__':
	#QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
	app = QApplication(sys.argv)
	locale.setlocale(locale.LC_NUMERIC, "C")			#sets the decimal point to a . not a ,
	sys.excepthook = error_han
	#from pycallgraph import PyCallGraph
	#from pycallgraph.output import GraphvizOutput
	#output=GraphvizOutput()
	#output.output_file = 'output.svg'
	#output.output_type = 'svg'
	#with PyCallGraph(output=output):
	ex = main_window()
	sys.exit(app.exec_())

