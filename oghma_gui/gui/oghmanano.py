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
from cal_path import get_image_file_path
from cal_path import calculate_paths
from cal_path import calculate_paths_init
from cal_path import get_share_path
from cal_path import set_sim_path

calculate_paths_init()
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

#qt
from PySide2.QtWidgets import QMainWindow,QApplication, QWidget, QSizePolicy, QVBoxLayout,QDialog, QFileDialog, QLineEdit
from PySide2.QtGui import QIcon
from gQtCore import Qt, QTimer

from used_files import used_files_add

from epitaxy import get_epi
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

from json_root import json_root
from const_ver import const_ver
from json_local_root import json_local_root
from oghma_local import oghma_local
from oghma_ipc import oghma_ipc

if get_platform()=="linux" or get_platform()=="wine":
	if os.geteuid() == 0:
		exit(_("Don't run me as root!!"))


class main_window(QMainWindow,oghma_local):

	def __init__(self):
		super(main_window,self).__init__()
		icon_init_db()

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

		self.ipc_pipe=oghma_ipc()
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

		self.setWindowIcon(QIcon(os.path.join(get_image_file_path(),"image.jpg")))		
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
		self.timer.timeout.connect(json_root().check_reload)
		self.timer.start(1000)

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
		help_window().help_set_help(["p3ht_pcbm.png",_("<big><b>New simulation!</b></big><br> Now selected the type of device you would like to simulate.")])

		dialog=new_simulation()
		dialog.exec_()
		ret=dialog.ret_path

		if ret!=None:
			self.change_dir_and_refresh_interface(dialog.ret_path)
			if json_root().sim.first_sim_message!="":
				msgBox = msg_dlg(title=sim_name.web)
				msgBox.setText(json_root().sim.first_sim_message.replace("%DIR",dialog.ret_path))
				msgBox.exec_()

	def update_interface(self):
		if self.notebook.is_loaded()==True:
			#self.check_sim_exists.set_dir(sim_paths.get_sim_path())

			help_window().help_set_help(["media-playback-start",_("<big><b>Now run the simulation</b></big><br> Click on the play icon to start a simulation.")])

			if json_local_root().gui_config.enable_betafeatures==True:
				self.ribbon.simulations.qe.setVisible(True)
		else:
			#self.check_sim_exists.set_dir("")
			help_window().help_set_help(["icon.png",_("<big><b>Hi!</b></big><br> I'm the on-line help system :).  If you have any questions or find any bugs please send them to <a href=\"mailto:"+get_lock().my_email+"\">"+get_lock().my_email+"</a>."),"document-new.png",_("Click on the new icon to make a new simulation directory.")])
			language_advert()

			if json_local_root().gui_config.enable_betafeatures==True:
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

		used_files_add(os.path.join(new_dir,"sim.oghma"))
		a=json_root()
		if inp().isfile(os.path.join(new_dir,"sim.json"))==True:
			a.load(os.path.join(new_dir,"sim.json"))
			a.fix_up()
		elif inp().isfile(os.path.join(new_dir,"json.inp"))==True:
			a.load(os.path.join(new_dir,"json.inp"))
			a.f.file_name="sim.json"
			a.fix_up()

		a.sim.version=const_ver()
		a.save()
		#get_watch().reset()
		self.splash.inc_value()

		self.splash.inc_value()

		set_sim_path(new_dir)
		self.splash.inc_value()

		#calculate_paths()
		self.splash.inc_value()

		get_epi()

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
		if filename.startswith(get_share_path())==True:
			error_dlg(self,_("You should not try to open simulations in the root simulation directory."))
			return

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
	
	sys.excepthook = error_han
	#from pycallgraph import PyCallGraph
	#from pycallgraph.output import GraphvizOutput
	#output=GraphvizOutput()
	#output.output_file = 'output.svg'
	#output.output_type = 'svg'
	#with PyCallGraph(output=output):
	ex = main_window()
	sys.exit(app.exec_())

