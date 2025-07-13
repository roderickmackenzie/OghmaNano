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
from PySide2.QtGui import QIcon, QPixmap, QFontMetrics
from gQtCore import QSize, Qt, QTimer, gSignal, QTimer, QRect
from PySide2.QtWidgets import QMenu,QAbstractItemView,QListWidgetItem,QPushButton,QListView,QWidget,QListWidget,QAction,QDialog, QVBoxLayout
from PySide2.QtWidgets import QLabel, QApplication, QStyledItemDelegate, QStyle

#cal_path
from icon_lib import icon_get

from help import help_window

from error_dlg import error_dlg

from dlg_get_text2 import dlg_get_text2
from gui_util import yes_no_dlg

from util import isfiletype
from win_lin import desktop_open

from plot_window import plot_window

import webbrowser
from config_window import class_config_window

from cal_path import sim_paths

from win_lin import get_platform
from decode_inode import decode_inode

from progress_class import progress_class
from process_events import process_events
import shutil
from bytes2str import bytes2str
from bytes2str import str2bytes
import ctypes

import i18n
_ = i18n.language.gettext

#util
from util import latex_to_html
from util import peek_data
import operator
from search import find_shapshots
from dir_viewer_new import dir_viewer_new
from inode import inode
from dir_viewer_menu import dir_viewer_menu
from bytes2str import bytes2str
from g_io import g_io
from json_c import json_c
from json_c import json_tree_c
import ctypes

class FileItemDelegate(QStyledItemDelegate):
	def __init__(self, parent=None):
		super().__init__(parent)

	def break_filename(self, text, interval=10):
		# Insert zero-width space every `interval` characters to force wrap
		return '\u200b'.join(text[i:i+interval] for i in range(0, len(text), interval))

	def paint(self, painter, option, index):
		icon = index.data(Qt.DecorationRole)
		text = index.data(Qt.DisplayRole)

		view = self.parent()
		list_mode = getattr(view, "viewMode", lambda: QListView.IconMode)()

		rect = option.rect
		icon_size = 64
		spacing = 8

		# Draw selection background
		if option.state & QStyle.State_Selected:
			painter.fillRect(rect, option.palette.highlight())

		painter.setPen(option.palette.text().color())
		wrapped_text = self.break_filename(text)

		if list_mode == QListView.ListMode:
			# Icon on the left, text on the right
			icon_rect = QRect(
				rect.x(),
				rect.y() + (rect.height() - icon_size) // 2,
				icon_size,
				icon_size
			)
			text_rect = QRect(
				rect.x() + icon_size + spacing,
				rect.y(),
				rect.width() - icon_size - spacing,
				rect.height()
			)
			painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap, wrapped_text)
		else:
			# Icon above, text below (default IconMode)
			icon_rect = QRect(
				rect.x() + (rect.width() - icon_size) // 2,
				rect.y(),
				icon_size,
				icon_size
			)
			text_rect = QRect(
				rect.x(),
				rect.y() + icon_size + spacing,
				rect.width(),
				rect.height() - icon_size - spacing
			)
			painter.drawText(text_rect, Qt.AlignHCenter | Qt.TextWordWrap, wrapped_text)

		if icon:
			icon.paint(painter, icon_rect)


	def sizeHint(self, option, index):
		view = self.parent()
		list_mode = getattr(view, "viewMode", lambda: QListView.IconMode)()

		text = index.data(Qt.DisplayRole)
		icon_size = 64
		spacing = 4
		text_line_height = 16

		if list_mode == QListView.ListMode:
			# Estimate number of lines (optional: remove wrapping in ListMode for better control)
			font_metrics = option.fontMetrics
			text_width = 150  # assume 150px width for text
			line_count = max(1, font_metrics.boundingRect(QRect(0, 0, text_width, 1000), Qt.TextWordWrap, text).height() // text_line_height)

			height = max(icon_size, line_count * text_line_height) + spacing * 2
			width = icon_size + spacing + text_width
			return QSize(width, height)
		else:
			line_count = (len(text) // 10) + 1
			height = icon_size + spacing + (line_count * text_line_height) + spacing
			return QSize(100, height)


class dir_viewer_c(ctypes.Structure):

	_fields_ = [('data_type', ctypes.c_int),
				('this_dir', inode),
				('files', ctypes.POINTER(inode)),
				('nfiles', ctypes.c_int),
				('nfiles_max', ctypes.c_int),
				('path', ctypes.c_char * 4096),
				('last_dir_sum', ctypes.c_char * 256),
				('show_hidden', ctypes.c_int),
				('show_back_arrow', ctypes.c_int),
				('root_dir', ctypes.c_char * 4096),
				('allow_navigation', ctypes.c_int),
				('json_data', ctypes.POINTER(json_c))
				]

	def __init__(self):
		self.bin=json_tree_c()
		self.bin.lib.dir_viewer_init(ctypes.byref(self))


	def __del__(self):
		self.bin.lib.dir_viewer_free(ctypes.byref(self))

class dir_viewer( QListWidget,dir_viewer_new,dir_viewer_menu):
	accept = gSignal()
	reject = gSignal()
	path_changed = gSignal()
	selection_changed = gSignal()

	def __init__(self,path,open_own_files=True,fake_dir_structure=None):
		QListWidget.__init__(self)
		self.g_io=g_io()
		self.bin=json_tree_c()
		self.data=dir_viewer_c()
		self.data.path= str2bytes(path)
		self.data.root_dir= str2bytes(path)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDragDropMode(QAbstractItemView.DragDrop)
		self.icon_cache = {}
		self.setItemDelegate(FileItemDelegate(self))
		self.open_own_files=open_own_files
		self.menu_new_material_enabled=False
		self.menu_new_spectra_enabled=False
		self.show_directories=True
		self.fake_dir_structure=fake_dir_structure
		self.file_path=""

		self.setStyleSheet("""QListWidget::item {margin: 0px;padding: 0px;}QListWidget::item:selected { background: lightblue; }""")

		self.enable_menu=True
		self.windows=[]
		self.setIconSize(QSize(64,64))
		#self.fill_store()

		self.itemDoubleClicked.connect(self.on_item_activated)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.itemSelectionChanged.connect(self.on_selection_changed)
		self.customContextMenuRequested.connect(self.callback_menu)
		self.selected=[]
		self.snapshot_window=[]

		self.check_for_changes=QTimer()
		self.check_for_changes.timeout.connect(self.callback_timer_check_for_changes)
		self.check_for_changes.start(2000)

		self.plot_windows = []

		#self.bin.lib.dir_viewer_dump(ctypes.byref(self.data))

	def keyPressEvent(self, ev):
		if ev.key() in (Qt.Key_Enter, Qt.Key_Return):
			self.on_item_activated(self.currentItem())
			ev.accept()
		else:
			return QListWidget.keyPressEvent(self, ev)

	def dragEnterEvent(self, event):
		#self.setText("<drop content>")
		#self.setBackgroundRole(QtGui.QPalette.Highlight)
		event.acceptProposedAction()
		#self.changed.emit(event.mimeData())

	def dragMoveEvent(self, event):
		event.acceptProposedAction()

	def dropEvent(self, event):
		mimeData = event.mimeData()

		if mimeData.hasUrls():
			a=[url.path() for url in mimeData.urls()]

#		self.setBackgroundRole(QtGui.QPalette.Dark)
		event.acceptProposedAction()

	def callback_timer_check_for_changes(self):
		if str(self.data.path).startswith("/oghma_root"):
			return

		if self.bin.lib.dir_viwer_update_needed(ctypes.byref(self.data))==0:
			self.fill_store()

	def set_multi_select(self):
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)

	def set_enable_menu(self,data):
		self.enable_menu=data

	def set_grid_view(self,height=90):
		icon_size = 64
		padding = 12  # Extra space below the text
		lines_of_text = 2  # Number of lines you expect for wrapping

		font_metrics = QFontMetrics(self.font())
		text_height = font_metrics.lineSpacing() * lines_of_text

		total_height = icon_size + text_height + padding

		#self.setIconSize(QSize(icon_size, icon_size))
		self.setViewMode(QListView.IconMode)
		self.setResizeMode(QListView.Adjust)
		self.setUniformItemSizes(False)
		self.setWordWrap(True)
		self.setSpacing(8)
		self.setTextElideMode(Qt.ElideNone)

		grid_size = QSize(100, total_height)
		self.setGridSize(grid_size)

	def set_list_view(self):
		self.setViewMode(QListView.ListMode)
		self.setIconSize(QSize(64, 64))

		delegate = self.itemDelegate()
		if delegate:
			model = self.model()
			if model.rowCount() > 0:
				hint = delegate.sizeHint(self.viewOptions(), model.index(0, 0))
				self.setGridSize(hint)
			else:
				self.setGridSize(QSize(200, 72))

	def set_directory_view(self,data):
		if data==True:
			self.set_grid_view()

	def get_selected(self):
		ret=[]
		for obj in self.selectedItems():
			decode=self.decode_name(obj.text())
			ret.append(decode)
		return ret

	def icon_get_cached(self,icon_name, sub_icon=None):
		key = (icon_name, sub_icon)
		if key in self.icon_cache:
			return self.icon_cache[key]

		result = icon_get(icon_name, sub_icon=sub_icon).pixmap(64, 64)
		if result==False:
			print("icon not found:",bytes2str(icon_name))
			result=icon_get("dat_file")
		self.icon_cache[key] = result
		return result

	def get_filename(self):
		return self.file_path

	def set_path(self,path):
		self.data.path=str2bytes(path)		
		self.path_changed.emit()

	def fill_store(self):
		#print("fill_store")
		#self.bin.lib.dir_viewer_dump(ctypes.byref(self.data))
		self.blockSignals(True)
		self.bin.lib.dir_viwer_build_inode_list(ctypes.byref(self.data),ctypes.byref(sim_paths))
		self.bin.lib.dir_viwer_update_needed(ctypes.byref(self.data))
		if self.data.this_dir.view_type==b"list":
	 		self.set_list_view()
		else:
			if str(self.data.path).endswith("device_lib")==True:
				self.set_grid_view(height=120)
			else:
				self.set_grid_view()

		self.paint()
		self.blockSignals(False)

	def paint(self):

		self.clear()
		QApplication.processEvents()

		for i in range(0,self.data.nfiles):
			inode_i = self.data.files[i]
			a=self.icon_get_cached(bytes2str(inode_i.icon),sub_icon=bytes2str(inode_i.sub_icon))
			self.add_icon(a,bytes2str(bytes2str(inode_i.display_name)))
				
	def add_icon(self,icon,text):
		item = QListWidgetItem()
		item.setIcon(icon)
		item.setText(text)
		item.setSizeHint(QSize(100, 100))
		self.addItem(item)

	def decode_name(self,display_name):
		for i in range(0,self.data.nfiles):
			if bytes2str(self.data.files[i].display_name)==display_name:
				return self.data.files[i]
		return None

	def on_item_activated(self,item):
		text=item.text()
		if self.bin.lib.dir_viwer_on_item_activated(ctypes.byref(self.data), ctypes.byref(sim_paths), ctypes.c_char_p(str2bytes(text)))==0:
			self.fill_store()
			return

		decode=self.decode_name(text)
		if decode.type==b"scan_dir":
			from scan_tab import scan_vbox
			self.scan_window=scan_vbox(full_path)
			self.scan_window.show()
			return

		if bytes2str(decode.file_name).startswith("http"):
			webbrowser.open(decode)
			return

		full_path=os.path.join(bytes2str(self.data.path),bytes2str(decode.file_name))
		if decode!=None:

			if self.open_own_files==True:
				self.file_path=bytes2str(full_path)

				if decode.type==b"spectra":
					from spectra_main import spectra_main
					self.mat_window=spectra_main(full_path)
					self.mat_window.show()
					return
				if decode.type==b"shape":
					from shape_editor import shape_editor
					self.windows.append(shape_editor(full_path))
					self.windows[-1].show()
					return
				if decode.type==b"transfer_matrix_output":
					from optics import class_optical 
					self.optics_window=class_optical()
					self.optics_window.show()

				if decode.type==b"material":
					from materials_main import materials_main
					self.mat_window=materials_main(full_path)
					self.mat_window.show()
					return
				if decode.type==b"morphology":
					from morphology_editor import morphology_editor
					self.windows.append(morphology_editor(full_path))
					self.windows[-1].show()
					return

				if decode.type==b"filter":
					from filter_main import filter_main
					self.filter_window=filter_main(full_path)
					self.filter_window.show()
					return
				if decode.type==b"transfer_matrix_snapshots":
					from cmp_class import cmp_class

					help_window().help_set_help("plot_time.png",_("<big><b>Examine the results in time domain</b></big><br> After you have run a simulation in time domain, if is often nice to be able to step through the simulation and look at the results.  This is what this window does.  Use the slider bar to move through the simulation.  When you are simulating a JV curve, the slider sill step through voltage points rather than time points."))

					self.snapshot_window.append(cmp_class(full_path,widget_mode="band_graph"))
					self.snapshot_window[-1].show()
					return

				if decode.type==b"snapshots":
					from cmp_class import cmp_class

					help_window().help_set_help("plot_time.png",_("<big><b>Examine the results in time domain</b></big><br> After you have run a simulation in time domain, if is often nice to be able to step through the simulation and look at the results.  This is what this window does.  Use the slider bar to move through the simulation.  When you are simulating a JV curve, the slider sill step through voltage points rather than time points."))
					self.snapshot_window.append(cmp_class(full_path))
					self.snapshot_window[-1].show()
					return
				if decode.type==b"folder":
					self.set_path(full_path)
					self.fill_store()
					return
				if decode.type==b"backup":
					ret=yes_no_dlg(self,_("Are you sure you want restore this file from the backup, it will overwrite all files in the simulation directory?")+"\n\n"+full_path)
					if ret==True:
						from backup import backup_restore
						backup_restore(sim_paths.get_sim_path(),full_path)


				if decode.type==b"file":
					self.file_path=bytes2str(full_path)
					if os.path.basename(full_path)=="sim_info.dat":
						self.sim_info_window=class_config_window([""],[_("Simulation information")],data=full_path,icon="json_file",ro=True)
						self.sim_info_window.show()
						return

					if isfiletype(full_path,"csv")==True:
						text=peek_data(full_path)
						if text.startswith(b"#oghma_csv") or text.startswith(b"#multiplot"):
							plot_win=plot_window()
							plot_win.init([full_path],[])
							self.plot_windows.append(plot_win)
							plot_win.closed.connect(self.remove_plot_window)
							return						

					if  isfiletype(full_path,"oghma")==True:
						return

					desktop_open(full_path)
					return

		self.accept.emit()

	def remove_plot_window(self, window):
		if window in self.plot_windows:
			self.plot_windows.remove(window)

	def on_selection_changed(self):
		self.selected=[]

		if len(self.selectedItems())>0:
			item=self.selectedItems()[0]
			if type(item)!=None:
				obj=self.decode_name(item.text())
				if obj==None:
					return

				file_name=bytes2str(obj.file_name)

				self.file_path=os.path.join(bytes2str(self.data.path), file_name)
	
			for item in self.selectedItems():
				obj_decode=self.decode_name(item.text())
				if obj_decode!=None:
					self.selected.append(obj_decode)

			full_path=bytes2str(self.file_path)

			if file_name.endswith(".dat")==True:
				state=dat_file()
				state.load_only_info(full_path)
				summary="<big><b>"+file_name+"</b></big><br><br>"+_("title")+": "+bytes2str(state.title)+"<br>"+_("x axis")+": "+bytes2str(state.y_label)+" ("+latex_to_html(bytes2str(state.y_units))+")<br>"+_("y axis")+": "+bytes2str(state.data_label)+" ("+latex_to_html(bytes2str(state.data_units))+")<br><br><big><b>"+_("Double click to open")+"</b></big>"
				help_window().help_set_help("dat_file.png",summary)
			elif file_name.endswith(".csv")==True:
				state=dat_file()
				state.load_only_info(full_path)
				summary="<big><b>"+file_name+"</b></big><br><br>"+_("title")+": "+bytes2str(state.title)+"<br>"+_("x axis")+": "+bytes2str(state.y_label)+" ("+latex_to_html(state.y_units)+")<br>"+_("y axis")+": "+bytes2str(state.data_label)+" ("+latex_to_html(bytes2str(state.data_units))+")<br><br><big><b>"+_("Double click to open")+"</b></big>"
				help_window().help_set_help("csv.png",summary)
			if file_name.endswith("equilibrium"):
				state=dat_file()
				state.load_only_info(full_path)
				summary="<big><b>"+_("equilibrium")+"</b></big><br><br>"+_("This contains the simulation output at 0V in the dark.")
				help_window().help_set_help("folder.png",summary)

			#if os.path.isdir(full_path)==True:
			dir_info=decode_inode(full_path)
			if dir_info!=None:
				if dir_info.type=="material":

					summary="<b><big>"+file_name+"</b></big><br>"
					ref_path=os.path.join(full_path,"mat.bib")
					b=json_c("file_defined")
					
					if b.load(ref_path)!=False:
						summary=summary+b.bib_cite("")
					help_window().help_set_help("organic_material",summary)
					b.free()

		self.selection_changed.emit()
