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

## @package dir_viewer
#  A directory/file browser
#


import os
from dat_file import dat_file

#qt
from PySide2.QtGui import QIcon, QPixmap
from gQtCore import QSize, Qt, QTimer, gSignal
from PySide2.QtWidgets import QMenu,QAbstractItemView,QListWidgetItem,QPushButton,QListView,QWidget,QListWidget,QAction,QDialog

#cal_path
from icon_lib import icon_get

from help import help_window

from error_dlg import error_dlg

from bibtex import bibtex
from dlg_get_text2 import dlg_get_text2
from gui_util import yes_no_dlg

from util import isfiletype
from win_lin import desktop_open

from plot_gen import plot_gen

import webbrowser
from window_json_ro_viewer import window_json_ro_viewer

from cal_path import sim_paths
from cal_path import get_videos_path
from cal_path import get_downloads_path
from cal_path import sim_paths

from win_lin import get_platform
from decode_inode import decode_inode

from progress_class import progress_class
from process_events import process_events
import shutil
from bytes2str import bytes2str
from bytes2str import str2bytes

import i18n
_ = i18n.language.gettext

#util
from util import latex_to_html
from util import peek_data
from multiplot import multiplot
import operator
from json_root import json_root
from search import find_shapshots
from dir_viewer_new import dir_viewer_new
from file_store import file_store
from dir_viewer_menu import dir_viewer_menu
from bytes2str import bytes2str
from g_io import g_io

class dir_viewer(QListWidget,dir_viewer_new,dir_viewer_menu):

	accept = gSignal()
	reject = gSignal()
	path_changed = gSignal()
	selection_changed = gSignal()

	def keyPressEvent(self, ev):
		if ev.key() in (Qt.Key_Enter, Qt.Key_Return):
			self.on_item_activated(self.currentItem())
			ev.accept()
		else:
			return QListWidget.keyPressEvent(self, ev)

	def dragEnterEvent(self, event):
		#self.setText("<drop content>")
	#	print("c")
		#self.setBackgroundRole(QtGui.QPalette.Highlight)
		event.acceptProposedAction()
		#self.changed.emit(event.mimeData())

	def dragMoveEvent(self, event):
		#print("b")
		event.acceptProposedAction()

	def dropEvent(self, event):
		mimeData = event.mimeData()

		if mimeData.hasUrls():
			a=[url.path() for url in mimeData.urls()]
			print("d",a)

#		self.setBackgroundRole(QtGui.QPalette.Dark)
		event.acceptProposedAction()


	def dropMimeData(self, data, action, row, column, parent):
		print()
#		print(data)

	def __init__(self,path,open_own_files=True):
		QListWidget.__init__(self)
		self.g_io=g_io()
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDragDropMode(QAbstractItemView.DragDrop)
		self.open_own_files=open_own_files
		self.file_list=[]
		self.menu_new_material_enabled=False
		self.menu_new_spectra_enabled=False
		self.show_directories=True
		self.file_path=""
		self.show_back_arrow=False

		self.setStyleSheet("margin: 0; padding: 0; ")

		self.show_hidden=False
		self.enable_menu=True
		self.path=""
		self.allow_navigation=False

		self.set_path(path)
		self.root_dir= self.path
		self.windows=[]
	
		self.show_only=[]

		self.setIconSize(QSize(64,64))

		
		self.fill_store()

		self.itemDoubleClicked.connect(self.on_item_activated)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.itemSelectionChanged.connect(self.on_selection_changed)
		self.customContextMenuRequested.connect(self.callback_menu)
		self.resizeEvent=self.resizeEvent
		self.selected=[]
		self.snapshot_window=[]
		self.this_dir=None
		#self.show()

	def set_back_arrow(self,data):
		self.show_back_arrow=data

	def set_show_hidden(self,data):
		self.show_hidden=data

	def set_multi_select(self):
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)

	def set_enable_menu(self,data):
		self.enable_menu=data

	def set_grid_view(self,height=90):
		self.setIconSize(QSize(64,64))
		self.setViewMode(QListView.IconMode)
		self.setSpacing(8)
		self.setWordWrap(True)
		self.setTextElideMode ( Qt.ElideNone)
		gridsize=self.size()
		gridsize.setWidth(100)
		gridsize.setHeight(height)
		self.setGridSize(gridsize)

	def set_list_view(self):
		self.setViewMode(QListView.ListMode)
		self.setIconSize(QSize(64,64))
		gridsize=self.size()
		gridsize.setHeight(64)
		self.setGridSize(gridsize)

	def set_directory_view(self,data):
		if data==True:
			self.set_grid_view()


	def get_selected(self):
		ret=[]		
		for obj in self.selectedItems():
			decode=self.decode_name(obj.text())
			ret.append(decode)
		return ret

	def resizeEvent(self,resizeEvent):
		self.fill_store()

	def get_icon(self, name):
		return icon_get(name+"_file")

	def get_filename(self):
		return self.file_path


	def set_path(self,path):
		self.path=bytes2str(path)		
		self.path_changed.emit()

	def add_back_arrow(self):
		if self.show_back_arrow==True:
			if self.path==self.root_dir and self.allow_navigation==False:
				return

			if self.path!="/root":
				itm = QListWidgetItem( ".." )
				itm.setIcon(icon_get('go-previous'))
				self.addItem(itm)

	#builds virtule list of files visible to user
	def listdir(self):
		ret=[]

		if self.path=="/root":
			itm=file_store()
			itm.file_name=b"sim.oghma"
			itm.icon=b"si"
			itm.type=b"simulation_root"
			itm.display_name=str2bytes(_("Simulation"))
			itm.can_delete=False
			ret.append(itm)

			itm=file_store()
			itm.file_name=b"home_dir"
			itm.icon=b"user-home"
			itm.display_name=str2bytes(_("Home"))
			itm.can_delete=False
			ret.append(itm)

			if sim_paths.get_desktop_path()!=False:
				itm=file_store()
				itm.file_name=b"desktop_dir"
				itm.icon=b"desktop"
				itm.display_name=str2bytes(_("Desktop"))
				itm.can_delete=False
				ret.append(itm)

			if get_downloads_path()!=False:
				itm=file_store()
				itm.file_name=b"downloads_dir"
				itm.icon=b"folder-download"
				itm.display_name=str2bytes(_("Downloads"))
				itm.can_delete=False
				ret.append(itm)

			itm=file_store()
			itm.file_name=b"configure"
			itm.icon=b"cog"
			itm.display_name=str2bytes(_("Configure"))
			itm.can_delete=False
			ret.append(itm)
			for name in self.g_io.g_get_mounts():
				full_name=name
				if get_platform()=="linux":
					name=os.path.basename(name)

				if name=="":
					name="/"
				itm=file_store()
				itm.file_name=str2bytes(full_name)
				itm.type=b"mount_point"
				itm.icon=b"drive-harddisk"
				itm.display_name=str2bytes(name)
				itm.can_delete=False
				ret.append(itm)

		elif self.path=="/root/icons/":
			from icon_lib import icon_get_db
			ilib=icon_get_db()
			for item in ilib.db:
				itm=file_store()
				itm.file_name=str2bytes(item.name[0])
				itm.icon=str2bytes(item.name[0])
				itm.display_name=str2bytes(item.name[0])
				itm.can_delete=False
				ret.append(itm)

		elif self.path=="/root/configure":
			pass


		else:
			self.this_dir=decode_inode(self.path)
			if os.path.isdir(self.path)==True:
				files=os.listdir(self.path)
				for f in files:
					itm=decode_inode(os.path.join(self.path,f))
					if itm!=None:
						add=True
						if sim_paths.get_sim_path()==self.path:
							if f=="sim.oghma":
								add=False
						if itm.type=="scan_dir":
							add=False

						if add==True:
							ret.append(itm)


		ret=sorted(ret, key=operator.attrgetter('display_name'))
		#files = sorted(files, key=operator.attrgetter('file_name'))
		return ret

	def fill_store(self):

		self.file_list=[]

		path=self.path

		all_files=self.listdir()
		#all_files.sort()
		if self.this_dir!=None:
			if self.this_dir.view_type==b"list":
				self.set_list_view()
			else:
				if path.endswith("device_lib")==True:
					self.set_grid_view(height=120)
				else:
					self.set_grid_view()

		for itm in all_files:
			#if it is a directory
			file_name=os.path.join(path, bytes2str(itm.file_name))

			if bytes2str(itm.file_name)=="data.json":
				itm.hidden=True

			if len(self.show_only)!=0:
				if itm.type not in self.show_only:
					itm.hidden=True

			if itm.hidden==False:
				self.file_list.append(itm)

		order=["bhj", "p3htpcbm.oghma","ofets","filter.json","OLED","perovskite","exciton_domain.json","simple_diode","morphology.json","large_area_diode.oghma","hexagonal_contact.oghma"]
		n=0
		if path.endswith("device_lib"):
			for o in order:
				for i in range(0,len(self.file_list)):
					if self.file_list[i].file_name==str2bytes(o):
						self.file_list.insert(n, self.file_list.pop(i))
						n=n+1

		self.paint()

	def paint(self):
		self.clear()

		self.add_back_arrow()

		for i in range(0,len(self.file_list)):
			draw=True
			if self.file_list[i].file_name==b"":
				draw=False

			if self.file_list[i].hidden==True and self.show_hidden==False:
				draw=False

			if bytes2str(self.file_list[i].file_name).endswith(".json"):
				if self.file_list[i].hide_this_json_file==True:
					draw=False

			if draw==True:
				itm = QListWidgetItem( bytes2str(self.file_list[i].display_name) )
				a=icon_get(bytes2str(self.file_list[i].icon),sub_icon=bytes2str(self.file_list[i].sub_icon))
				#print(self.file_list[i].sub_icon)
				if a==False:
					print("icon not found:",bytes2str(self.file_list[i].icon))
					a=icon_get("dat_file")
				itm.setIcon(a)

				self.addItem(itm)

	def decode_name(self,display_name):
		for i in range(0,len(self.file_list)):
			if bytes2str(self.file_list[i].display_name)==display_name:
				return self.file_list[i]
		return None

	def on_item_activated(self,item):
		text=item.text()
		if text=="..":
			if self.path==self.root_dir:
				self.set_path("/root")
			else:
				old_path=self.path
				self.set_path(os.path.dirname(self.path))
				#print(self.path,old_path,os.path.dirname(self.path))
				if old_path==self.path:
					self.set_path("/root")
			self.fill_store()
			return

		decode=self.decode_name(text)
		if decode==None:
			return

		full_path=os.path.join(self.path,bytes2str(decode.file_name))

		if bytes2str(decode.file_name).startswith("http"):
			webbrowser.open(decode)
			return
		elif decode.file_name==b"home_dir":
			self.set_path(sim_paths.get_home_path())
			self.fill_store()
			return
		elif decode.file_name==b"desktop_dir":
			self.set_path(sim_paths.get_desktop_path())
			self.fill_store()
			return
		elif decode.file_name==b"configure":
			self.set_path("/root/configure")
			self.fill_store()
			return

		elif decode.file_name==b"music_dir":
			self.set_path(get_music_path())
			self.fill_store()
			return
		elif decode.file_name==b"downloads_dir":
			self.set_path(get_downloads_path())
			self.fill_store()
			return
		elif decode.type==b"simulation_root":
			self.set_path(sim_paths.get_sim_path())
			self.fill_store()
			return			
		elif decode.type==b"mount_point":
			self.set_path(decode.file_name)
			self.fill_store()
			return
		elif decode.type==b"scan_dir":
			from scan_tab import scan_vbox
			#print(full_path) 
			self.scan_window=scan_vbox(full_path)
			self.scan_window.show()
			return
		elif decode.type==b"parameter_dir":
			self.set_path(full_path)
			self.fill_store()
			return
		
		dir_info=decode_inode(full_path)
		if dir_info!=None:
			if self.open_own_files==True:
				self.file_path=full_path

				if dir_info.type==b"spectra":
					from spectra_main import spectra_main
					self.mat_window=spectra_main(full_path)
					self.mat_window.show()
					return
				if dir_info.type==b"shape":
					from shape_editor import shape_editor
					self.windows.append(shape_editor(full_path))
					self.windows[-1].show()
					return
				if dir_info.type==b"transfer_matrix_output":
					from optics import class_optical 
					self.optics_window=class_optical()
					self.optics_window.show()

				if dir_info.type==b"material":
					from materials_main import materials_main
					self.mat_window=materials_main(full_path)
					self.mat_window.show()
					return

				if dir_info.type==b"filter":
					from filter_main import filter_main
					self.filter_window=filter_main(full_path)
					self.filter_window.show()
					return
				if dir_info.type==b"transfer_matrix_snapshots":
					from cmp_class import cmp_class

					help_window().help_set_help(["plot_time.png",_("<big><b>Examine the results in time domain</b></big><br> After you have run a simulation in time domain, if is often nice to be able to step through the simulation and look at the results.  This is what this window does.  Use the slider bar to move through the simulation.  When you are simulating a JV curve, the slider sill step through voltage points rather than time points.")])

					self.snapshot_window.append(cmp_class(full_path,widget_mode="band_graph"))
					self.snapshot_window[-1].show()
					return

				if dir_info.type==b"snapshots":
					from cmp_class import cmp_class

					help_window().help_set_help(["plot_time.png",_("<big><b>Examine the results in time domain</b></big><br> After you have run a simulation in time domain, if is often nice to be able to step through the simulation and look at the results.  This is what this window does.  Use the slider bar to move through the simulation.  When you are simulating a JV curve, the slider sill step through voltage points rather than time points.")])
					widget_mode="matplotlib"
					self.snapshot_window.append(cmp_class(full_path,widget_mode=widget_mode))
					self.snapshot_window[-1].show()
					#print("snapshots!!")
					return

				if dir_info.type==b"backup":
					ret=yes_no_dlg(self,_("Are you sure you want restore this file from the backup, it will overwrite all files in the simulation directory?")+"\n\n"+full_path)
					if ret==True:
						from backup import backup_restore
						backup_restore(sim_paths.get_sim_path(),full_path)


				if dir_info.type==b"file":
					self.file_path=full_path
					if os.path.basename(full_path)=="sim_info.dat":
						self.sim_info_window=window_json_ro_viewer(full_path)
						self.sim_info_window.show()
						return

					if isfiletype(full_path,"dat")==True or isfiletype(full_path,"csv")==True:
						text=peek_data(full_path)
						if text.startswith(b"#multiplot"):
							my_multiplot=multiplot()
							my_multiplot.plot(full_path)
						else:
							plot_gen([full_path],[],"auto")
						return

					if  isfiletype(full_path,"oghma")==True:
						return

					desktop_open(full_path)
					return

			if dir_info.type==b"dir" or dir_info.type==b"backup_main" or dir_info.type==b"multi_plot_dir" :
				self.file_path=full_path
				self.set_path(full_path)
				self.fill_store()
			else:
				self.accept.emit()


	def on_selection_changed(self):
		self.selected=[]

		if len(self.selectedItems())>0:
			item=self.selectedItems()[0]
			if type(item)!=None:
				obj=self.decode_name(item.text())
				if obj==None:
					return

				file_name=bytes2str(obj.file_name)

				self.file_path=os.path.join(self.path, file_name)
	
			for item in self.selectedItems():
				obj_decode=self.decode_name(item.text())
				if obj_decode!=None:
					self.selected.append(obj_decode)

			full_path=self.file_path

			if file_name.endswith(".dat")==True:
				state=dat_file()
				state.load_only_info(full_path)
				summary="<big><b>"+file_name+"</b></big><br><br>"+_("title")+": "+bytes2str(state.title)+"<br>"+_("x axis")+": "+bytes2str(state.y_label)+" ("+latex_to_html(bytes2str(state.y_units))+")<br>"+_("y axis")+": "+bytes2str(state.data_label)+" ("+latex_to_html(bytes2str(state.data_units))+")<br><br><big><b>"+_("Double click to open")+"</b></big>"
				help_window().help_set_help(["dat_file.png",summary])
			elif file_name.endswith(".csv")==True:
				state=dat_file()
				state.load_only_info(full_path)
				summary="<big><b>"+file_name+"</b></big><br><br>"+_("title")+": "+bytes2str(state.title)+"<br>"+_("x axis")+": "+bytes2str(state.y_label)+" ("+latex_to_html(state.y_units)+")<br>"+_("y axis")+": "+bytes2str(state.data_label)+" ("+latex_to_html(bytes2str(state.data_units))+")<br><br><big><b>"+_("Double click to open")+"</b></big>"
				help_window().help_set_help(["csv.png",summary])
			if file_name.endswith("equilibrium"):
				state=dat_file()
				state.load_only_info(full_path)
				summary="<big><b>"+_("equilibrium")+"</b></big><br><br>"+_("This contains the simulation output at 0V in the dark.")
				help_window().help_set_help(["folder.png",summary])

			#if os.path.isdir(full_path)==True:
			dir_info=decode_inode(full_path)
			if dir_info!=None:
				if dir_info.type=="material":

					summary="<b><big>"+file_name+"</b></big><br>"
					ref_path=os.path.join(full_path,"mat.bib")
					b=bibtex()
					
					if b.load(ref_path)!=False:
						summary=summary+b.get_text()
					help_window().help_set_help(["organic_material",summary])

		self.selection_changed.emit()
