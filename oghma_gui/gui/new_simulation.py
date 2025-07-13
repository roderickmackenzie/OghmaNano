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

## @package new_simulation
#  A new simulation window, shows the user which simulation he/she can make.
#

import os
from copy_device import copy_device
from open_save_dlg import save_as_simfile

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QPushButton,QCheckBox,QHBoxLayout, QListView, QLabel,QWidget,QDialog,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QMenu
from PySide2.QtGui import QIcon

#calpath
from icon_lib import icon_get
from error_dlg import error_dlg

from help import help_window

from dlg_get_text2 import dlg_get_text2

from dir_viewer import dir_viewer

from util import peek_data
from cal_path import sim_paths
from lock import get_lock
from util_zip import archive_make_empty
from sim_name import sim_name
import ctypes
from bytes2str import str2bytes

class new_simulation(QDialog):


	def callback_close(self):
		self.reject()

	def callback_next(self):
		self.lib=sim_paths.get_dll_py()
		self.lib.lock_decrypt_file.restype = ctypes.c_int
		help_window().help_set_help("document-save-as.png",_("<big><b>Now save the simulation</b></big><br>Now select where you would like to save the simulation directory."))

		if len(self.viewer.selectedItems())>0:
			device_lib_sim_file=self.viewer.file_path
			decrypted_file=os.path.join(sim_paths.get_tmp_path(),"tmp.oghma")
			if peek_data(device_lib_sim_file).startswith(b"oghmaenc")==True:
				pw_dlg=dlg_get_text2( _("password:"), "","gnome-dialog-password")
				if self.lib.lock_decrypt_file(ctypes.c_char_p(str2bytes(decrypted_file)),ctypes.c_char_p(str2bytes(device_lib_sim_file)),ctypes.c_char_p(str2bytes(pw_dlg.ret),None))==-1:
					error_dlg(self,_("Wrong password"))
					return
				else:
					device_lib_sim_file=decrypted_file

			if os.path.isdir(device_lib_sim_file)==True:
				temp_file=os.path.join(device_lib_sim_file,"sim.json")
				if os.path.isfile(temp_file)==True:
					device_lib_sim_file=temp_file

			file_path=save_as_simfile(self)
			#print(file_path,sim_paths.get_exe_path())
			if file_path!=None:
				if file_path.startswith(sim_paths.get_exe_path())==True:
					error_dlg(self,_("It's not a good idea to save the simulation in the installation directory.  Try saving it somewhere else, such as your desktop or home directory."))
					return

				if file_path.count("oghma_local")>0:
					error_dlg(self,_("It's not a good idea to save the simulation in the oghma_local directory."))
					return

				if os.path.isdir(file_path)==True:
					error_dlg(self,_("That directory already exists.  Pick another name or delete the old one."))
					return

				if not os.path.exists(file_path):
					os.makedirs(file_path)

				self.ret_path=file_path

				os.chdir(self.ret_path)
				new_archive=os.path.join(self.ret_path,"sim.oghma")
				archive_make_empty(new_archive)
				copy_device(device_lib_sim_file,self.ret_path,setup_sim_to_run=True)

				self.close()
		else:
			error_dlg(self,_("Please select a device before clicking next"))


	def get_return_path(self):
		return self.ret_path

		return
		print(_("Organic LED"))
		print(_("Crystalline silicon solar cell"))
		print(_("a-Si solar cell "))
		print(_("polycrystalline silicon "))
		print(_("OFET "))
		print(_("Perovskite solar cell"))
		print(_("CIGS Solar cell"))

	def callback_toggle_hidden(self):
		self.viewer.data.show_hidden=self.show_hidden.isChecked()
		self.viewer.fill_store()
	
	def __init__(self):
		QDialog.__init__(self)
		self.main_vbox=QVBoxLayout()
		self.setMinimumSize(900,580) 
		self.setWindowTitle(_("New simulation")+sim_name.web_window_title)
		self.setWindowIcon(icon_get("si"))
		self.title=QLabel("<big><b>"+_("Which type of device would you like to simulate?")+" ("+_("Double click to open")+")</b></big>")

		self.viewer=dir_viewer(sim_paths.get_device_lib_path())
		self.viewer.open_own_files=False
		self.viewer.data.show_back_arrow=True
		self.viewer.set_enable_menu(False)
		self.viewer.setViewMode(QListView.IconMode)
		self.viewer.setSpacing(8)
		self.viewer.setWordWrap(True)
		gridsize=self.size()
		gridsize.setWidth(100)
		gridsize.setHeight(140)
		self.viewer.setGridSize(gridsize)

		self.viewer.setTextElideMode ( Qt.ElideNone)
		#gridsize=self.size()
		#gridsize.setWidth(100)
		#gridsize.setHeight(90)
		#self.setGridSize(gridsize)
		self.main_vbox.addWidget(self.title)
		self.main_vbox.addWidget(self.viewer)

		self.hwidget=QWidget()

		#self.nextButton = QPushButton(_("Next"))
		self.cancelButton = QPushButton(_("Close"))

		self.files=[]

		hbox = QHBoxLayout()
		self.show_hidden=QCheckBox(_("Show hidden"))
		self.show_hidden.clicked.connect(self.callback_toggle_hidden)
		#if get_lock().is_next()==True:
		hbox.addWidget(self.show_hidden)
		self.show_hidden.setChecked(True)
		self.viewer.data.show_hidden=True

		hbox.addStretch(1)
		hbox.addWidget(self.cancelButton)
		#hbox.addWidget(self.nextButton)
		self.hwidget.setLayout(hbox)

		self.main_vbox.addWidget(self.hwidget)

		self.setLayout(self.main_vbox)
		self.viewer.fill_store()
		self.show()

		self.ret_path=None
		# Create a new window

		
		self.viewer.accept.connect(self.callback_next)
		#self.nextButton.clicked.connect(self.callback_next)
		self.cancelButton.clicked.connect(self.callback_close)



