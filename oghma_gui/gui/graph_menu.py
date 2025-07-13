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

## @package dat_file
#  Load and dump a dat file into a dat class
#

import os
import ctypes
from gQtCore import QSize, Qt
from cal_path import sim_paths
from PySide2.QtWidgets import QWidget,QMenu,QApplication
from PySide2.QtGui import QImage, QPainter
from dat_file import dat_file
from gl_main import text_lib
from json_c import json_c
from plot_ribbon import plot_ribbon
from icon_lib import icon_get
from lock import get_lock
from open_save_dlg import save_as_image
from bytes2str import str2bytes
from open_save_dlg import save_as_filter
from json_c import json_string

class graph_menu():

	def build_menu(self):
		sub_icon=None
		if get_lock().encode_output==True:
			sub_icon="lock"

		self.menu = QMenu(self)

		self.menu_show_labels=self.menu.addAction(_("Show labels"))
		#self.menu_show_labels.triggered.connect(self.menu_toggle)
		self.menu_show_labels.setCheckable(True)
		self.menu_show_labels.setChecked(True)

		self.menu_normalize_x_axis=self.menu.addAction(_("Normalize layer width"))
		#self.menu_normalize_x_axis.triggered.connect(self.menu_toggle)
		self.menu_normalize_x_axis.setCheckable(True)
		self.menu_normalize_x_axis.setChecked(False)

		clipboard=self.menu.addMenu(icon_get("edit-copy"),_("Copy"))

		action=clipboard.addAction(icon_get("image-x-generic"),_("Image"))
		action.triggered.connect(self.callback_copy_image)

		action=clipboard.addAction(icon_get("file_path"),_("Image path"))
		action.triggered.connect(self.callback_copy_path)

		save_as=self.menu.addMenu(_("Save as"))
		action=save_as.addAction(icon_get("edit-copy"),_("Image"))
		action.triggered.connect(self.callback_save_image)

		#export
		action=save_as.addAction(icon_get("export_gnuplot",sub_icon=sub_icon),_("Gnuplot"))
		action.triggered.connect(self.callback_save_gnuplot)

		action=save_as.addAction(icon_get("export_csv",sub_icon=sub_icon),_("Csv"))
		action.triggered.connect(self.callback_save_csv)

		action=save_as.addAction(icon_get("text-x-generic",sub_icon=sub_icon),_("Text file (txt)"))
		action.triggered.connect(self.callback_save_txt)

		action=save_as.addAction(icon_get("wps-office-xls",sub_icon=sub_icon),_("MS Excel (xlsx)"))
		action.triggered.connect(self.callback_save_xlsx)

		graph=self.menu.addMenu(_("Graph"))
		self.menu_show_title=graph.addAction(_("Show title"))
		self.menu_show_title.setCheckable(True)
		self.menu_show_title.setChecked(self.graph.show_title)
		self.menu_show_title.triggered.connect(self.callback_hide_show_title)

		self.menu_show_key=graph.addAction(_("Show key"))
		self.menu_show_key.setCheckable(True)
		self.menu_show_key.setChecked(True)
		#self.menu_show_key.triggered.connect(self.callback_hide_show_key)

		self.menu_show_axis=graph.addAction(_("Show axis"))
		self.menu_show_axis.triggered.connect(self.callback_hide_show_axis)
		self.menu_show_axis.setCheckable(True)
		self.menu_show_axis.setChecked(True)

		self.menu_show_data=graph.addAction(_("Show data"))
		self.menu_show_data.triggered.connect(self.callback_hide_data)
		self.menu_show_data.setCheckable(True)
		self.menu_show_data.setChecked(True)

		self.menu_show_free_carriers=graph.addAction(_("Show free carriers"))
		self.menu_show_free_carriers.triggered.connect(self.callback_menu_click)
		self.menu_show_free_carriers.setCheckable(True)

		self.menu_show_trapped_carriers=graph.addAction(_("Show trapped carriers"))
		self.menu_show_trapped_carriers.triggered.connect(self.callback_menu_click)
		self.menu_show_trapped_carriers.setCheckable(True)

	def callback_show_free_carriers(self):
		print("callback_show_free_carriers")

	def callback_copy_image(self):
		self.do_clip()

	def callback_copy_path(self):
		a=json_string()
		self.graph.lib.ui_graph_get_paths(ctypes.byref(a),ctypes.byref(self.graph))
		ret=a.get_data()
		QApplication.clipboard().setText(ret)
		a.free()

	def callback_hide_show_title(self):
		self.graph.show_title=self.menu_show_title.isChecked()
		self.update()

	def callback_hide_show_axis(self):
		show_hide=self.menu_show_axis.isChecked()
		self.graph.axis_y.hidden= not show_hide
		self.graph.axis_x.hidden= not show_hide
		self.graph.axis_z.hidden= not show_hide
		self.update()

	def callback_hide_show_key(self):
		self.show_key=self.menu_show_key.isChecked()
		self.do_plot()

	def callback_save_image(self):
		file_name=save_as_image(self)
		if file_name != None:
			self.do_clip(file_name=file_name)

	def callback_save_csv(self):
		file_name=save_as_filter(self,"CSV (*.csv)")
		if file_name != None:
			self.graph.lib.dat_files_save_as_csv(ctypes.c_char_p(str2bytes(file_name)), self.graph.data, ctypes.c_int(self.graph.ndata))

	def callback_save_xlsx(self):
		file_name=save_as_filter(self,"Excel (*.xlsx)")
		if file_name != None:
			self.graph.lib.dat_files_save_as_xlsx(ctypes.c_char_p(str2bytes(file_name)), self.graph.data, ctypes.c_int(self.graph.ndata))

	def callback_save_txt(self):
		file_name=save_as_filter(self,"Text file (*.txt)")
		if file_name != None:
			self.graph.lib.dat_files_save_as_csv(ctypes.c_char_p(str2bytes(file_name)), self.graph.data, ctypes.c_int(self.graph.ndata))

	def callback_save_gnuplot(self):
		file_name=save_as_filter(self,"gnuplot (*.)")
		if file_name != None:
			self.graph.lib.dat_files_save_as_gnuplot(ctypes.c_char_p(str2bytes(file_name)), self.graph.data, ctypes.c_int(self.graph.ndata))

	def callback_hide_data(self):
		self.graph.lib.ui_graph_hide_data(ctypes.byref(self.graph),ctypes.c_int(not self.menu_show_data.isChecked()))
		self.update()

	def callback_menu_click(self):
		sender = self.sender()
		text=sender.text()
		
		if text==_("Log x"):
			self.graph.axis_x.log_scale_auto=False
			self.graph.axis_x.log_scale= self.plot_ribbon.tb_scale_log_x.isChecked()
		elif text==_("Log y"):
			self.graph.axis_y.log_scale_auto=False
			self.graph.axis_y.log_scale= self.plot_ribbon.tb_scale_log_y.isChecked()
		elif text==_("Log z"):
			self.graph.axis_z.log_scale_auto=False
			self.graph.axis_z.log_scale= self.plot_ribbon.tb_scale_log_z.isChecked()
		elif text==_("Transpose"):
			self.graph.lib.graph_transpose_data(ctypes.byref(self.graph),ctypes.c_int(self.plot_ribbon.tb_transpose.isChecked()))
		elif text==_("Flip z"):
			self.graph.lib.graph_axis_flip_z(ctypes.byref(self.graph),ctypes.c_int(self.plot_ribbon.tb_flip_z.isChecked()))
		elif text==_("Flip x"):
			self.graph.lib.graph_axis_flip_x(ctypes.byref(self.graph),ctypes.c_int(self.plot_ribbon.tb_flip_x.isChecked()))
		elif text==_("Flip y"):
			self.graph.lib.graph_axis_flip_y(ctypes.byref(self.graph),ctypes.c_int(self.plot_ribbon.tb_flip_y.isChecked()))
		elif text==_("Show free carriers"):
			self.graph.show_free_carriers=self.menu_show_free_carriers.isChecked()
		elif text==_("Show trapped carriers"):
			self.graph.show_trapped_carriers=self.menu_show_trapped_carriers.isChecked()

		self.graph.lib.graph_load_set_up_axies(ctypes.byref(self.graph))
		self.update()

	def show_menu(self,event):
		if self.graph.plot_type==b'trap_map':
			self.menu_show_free_carriers.setVisible(True)
			self.menu_show_free_carriers.setChecked(self.graph.show_free_carriers)

			self.menu_show_trapped_carriers.setVisible(True)
			self.menu_show_trapped_carriers.setChecked(self.graph.show_trapped_carriers)
		else:
			self.menu_show_free_carriers.setVisible(False)
			self.menu_show_trapped_carriers.setVisible(False)
		self.menu.exec_(event.globalPos())



