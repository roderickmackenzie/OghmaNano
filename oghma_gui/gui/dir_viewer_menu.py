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

## @package dir_viewer_new
#  Make new files/directories
#


import os

#qt
from PySide2.QtGui import QIcon, QPixmap
from gQtCore import QSize, Qt, QTimer, gSignal
from PySide2.QtWidgets import QMenu,QAbstractItemView,QListWidgetItem,QPushButton,QListView,QWidget,QListWidget,QAction,QDialog

import shutil
from dlg_get_text2 import dlg_get_text2
from cal_path import sim_paths
from util_zip import archive_decompress
from icon_lib import icon_get
from safe_delete import safe_delete
from gui_util import yes_no_dlg
from error_dlg import error_dlg
from safe_delete import can_i_delete
from bytes2str import bytes2str

class dir_viewer_menu():

	def callback_menu(self,event):
		if self.enable_menu==False:
			return
		menu = QMenu(self)
		selected=self.get_selected()
		if self.path!="/root":
			menu_new = menu.addMenu(_("New"))

			newdirAction = menu_new.addAction(icon_get("folder"),_("New directory"))
			newdirAction.triggered.connect(self.new_dir)

			menu_new.addSeparator()

			menu_new_material = menu_new.addAction(icon_get("organic_material"),_("New material"))
			menu_new_material.triggered.connect(self.new_material)

			menu_new_sepctra = menu_new.addAction(icon_get("spectra_file"),_("New spectra"))
			menu_new_sepctra.triggered.connect(self.new_spectra)

			menu_new_shape = menu_new.addAction(icon_get("shape"),_("New shape"))
			menu_new_shape.triggered.connect(self.new_shape)

			menu_new_filter = menu_new.addAction(icon_get("filter_wheel"),_("New filter"))
			menu_new_filter.triggered.connect(self.new_filter)

		if len(selected)>0:
			deleteAction = menu.addAction(icon_get("edit-delete"),_("Delete file"))
			deleteAction.triggered.connect(self.callback_delete)

			renameAction = menu.addAction(icon_get("rename"),_("Rename"))
			renameAction.triggered.connect(self.rename)

			cloneAction = menu.addAction(icon_get("edit-copy"),_("Copy"))
			cloneAction.triggered.connect(self.clone)

			cleanAction = menu.addAction(icon_get("clean"),_("Clean"))
			cleanAction.triggered.connect(self.clean)

			renameAction.setEnabled(False)
			deleteAction.setEnabled(False)
			cloneAction.setEnabled(False)
			cleanAction.setEnabled(False)

		if len(selected)==1:
			if selected[0].can_delete==True:
				if can_i_delete(self.path)==True:
					deleteAction.setEnabled(True)
					renameAction.setEnabled(True)
					cloneAction.setEnabled(True)
					cleanAction.setEnabled(True)
			
			if selected[0].type=="simulation_root":
				menu.addSeparator()

				#pack_action = menu.addAction(_("Pack archive"))
				unpack_action = menu.addAction(icon_get("package-x-generic"),_("Unpack archive"))
				unpack_action.triggered.connect(self.callback_unpack)
		action = menu.exec_(self.mapToGlobal(event))

			
		#self.fill_store()

	def clone(self):
		old_name=self.currentItem().text()
		decode=self.decode_name(old_name)
		if decode.type=="scan_dir":
			new_sim_name=dlg_get_text2( _("Clone the file to be called:"), old_name+"_new","clone.png")
			new_sim_name=new_sim_name.ret

			if new_sim_name!=None:
				scans=scans_io(self.path)
				if scans.clone(new_sim_name,old_name)==False:
					error_dlg(self,_("The file name already exists"))
		else:
			new_sim_name=dlg_get_text2( _("Clone the file to be called:"), old_name+"_new","clone.png")
			new_sim_name=new_sim_name.ret

			if new_sim_name!=None:
				if os.path.isdir(os.path.join(self.path,new_sim_name))==False:
					shutil.copytree(os.path.join(self.path,old_name), os.path.join(self.path,new_sim_name))

		self.fill_store()

	def rename(self):
		old_name=self.currentItem().text()
		decode=self.decode_name(old_name)
		if decode.type=="scan_dir":
			new_sim_name=dlg_get_text2( _("Rename the simulation to be called:"), old_name,"rename.png")
			new_sim_name=new_sim_name.ret

			if new_sim_name!=None:
				scan=scan_io()
				scan.load(os.path.join(self.path,decode.file_name))
				scan.rename(new_sim_name)
		else:
			new_sim_name=dlg_get_text2( _("Rename:"), self.currentItem().text(),"rename")
			new_sim_name=new_sim_name.ret

			if new_sim_name!=None:
				new_name=os.path.join(self.path,new_sim_name)
				old_name=os.path.join(self.path,old_name)
				os.rename(old_name, new_name)
		self.fill_store()

	def clean(self):
		progress_window=progress_class()
		progress_window.show()
		progress_window.start()

		process_events()

		print("searching")
		files=find_shapshots(self.path)
		if len(files)<20:
			disp="\n".join(files)
		else:
			disp="\n".join(files[:20])+"..."

		ret=yes_no_dlg(self,_("Are you sure you want to delete the files ?")+"\n\n"+disp)
		if ret==True:
			i=0
			for f in files:
				progress_window.set_fraction(float(i)/float(len(files)))
				progress_window.set_text("Deleting: "+f)
				process_events()

				safe_delete(f,allow_dir_removal=True)

				i=i+1

		progress_window.stop()
		self.fill_store()

	def callback_unpack(self):
		name=self.currentItem().text()
		decode=self.decode_name(name)
		if self.path=="/root" and decode.file_name=="sim.oghma":
			full_file_name=os.path.join(sim_paths.get_sim_path(),decode.file_name)
			archive_decompress(full_file_name)
			error_dlg(self,_("You should now have a sim.json file in: ")+ sim_paths.get_sim_path() + " " +_("Open this directory to see it."))
	def callback_delete(self):
		files=""
		for i in self.selectedItems():
			files=files+os.path.join(self.path,i.text())+"\n"
		ret=yes_no_dlg(self,_("Are you sure you want to delete the files ?")+"\n\n"+files)
		if ret==True:
			for i in self.selectedItems():
				decode=self.decode_name(i.text())
				if decode.type=="scan_dir":
					scans=scans_io(self.path)
					scans.delete(decode.display_name)
				else:
					file_to_remove=os.path.join(self.path,bytes2str(decode.file_name))
					safe_delete(file_to_remove,allow_dir_removal=True)
		self.fill_store()

