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

## @package tab_homo
#  A tab to draw the analytical HOMO/LUMO.
#

import os

from open_save_dlg import save_as_image

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView, QMenuBar,QGroupBox,QHBoxLayout, QTableWidgetItem, QStatusBar, QDialog
from PySide2.QtGui import QPainter,QIcon

from gQtCore import gSignal

from icon_lib import icon_get

from ribbon_complex_dos import ribbon_complex_dos 
from g_tab2_bin import g_tab2_bin
from cal_path import sim_paths
from dat_file import dat_file

from graph import graph_widget

from QComboBoxLang import QComboBoxLang

from error_dlg import error_dlg
from str2bool import str2bool
from sim_name import sim_name
from bytes2str import str2bytes
from json_c import json_tree_c
import ctypes

class equation_editor(QGroupBox):

	changed = gSignal()

	def __init__(self,name,uid):
		QGroupBox.__init__(self)
		self.bin=json_tree_c()
		self.setTitle(name)
		self.name=name
		self.setStyleSheet("QGroupBox {  border: 1px solid gray;}")
		vbox=QVBoxLayout()
		self.setLayout(vbox)

		self.toolbar=QToolBar()
		vbox.addWidget(self.toolbar)

		self.tab2 = g_tab2_bin(toolbar=self.toolbar)
		self.tab2.set_tokens(["function","function_enable","function_a","function_b","function_c"])
		self.tab2.set_labels([_("Function"),_("Enabled"), _("a"), _("b"), _("c")])
		self.tab2.json_root_path="epitaxy"
		self.tab2.uid=uid
		self.tab2.fixup_new_row=self.fixup_new_row
		self.tab2.populate()
		self.tab2.setColumnWidth(0, 250)
		self.tab2.setColumnWidth(1, 80)
		self.tab2.setColumnWidth(2, 100)
		self.tab2.setColumnWidth(3, 100)
		self.tab2.setColumnWidth(4, 100)

		#self.tab2.resizeColumnsToContents()
		self.tab2.verticalHeader().setVisible(False)

		self.tab2.changed.connect(self.callback_changed)
		
		vbox.addWidget(self.tab2)
		
	def callback_changed(self):
		self.bin.save()
		self.changed.emit()		

	def fixup_new_row(self,row):
		if self.name=="LUMO":
			self.tab2.cellWidget(row, 0).is_lumo=True
		else:
			self.tab2.cellWidget(row, 0).is_lumo=False

class dos_editor(QWidget):

	def __init__(self,search_path,uid):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.uid=uid
		self.search_path=search_path
		self.lib=sim_paths.get_dll_py()

		self.data_lumo=dat_file()
		self.data_homo=dat_file()
		self.data_numerical_lumo=dat_file()
		self.data_numerical_homo=dat_file()

		self.setWindowTitle(_("Complex Density of states editor")+sim_name.web_window_title)
		self.setWindowIcon(icon_get("electrical"))
		self.setMinimumSize(1400,500)

		edit_boxes=QWidget()
		vbox=QVBoxLayout()

		json_path=self.bin.find_path_by_uid("epitaxy",self.uid)
		uid=self.bin.get_token_value(json_path+".shape_dos.complex_lumo","id")

		self.lumo=equation_editor("LUMO",uid)
		vbox.addWidget(self.lumo)

		uid=self.bin.get_token_value(json_path+".shape_dos.complex_homo","id")
		self.homo=equation_editor("HOMO",uid)
		vbox.addWidget(self.homo)
		
		self.plot=graph_widget()
		self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.status_bar=QStatusBar()

		self.gen_mesh()

		edit_boxes.setLayout(vbox)

		hbox=QHBoxLayout()

		hbox.addWidget(self.plot)

		hbox.addWidget(edit_boxes)
		
		self.ribbon=ribbon_complex_dos()

		self.main_layout_widget=QWidget()
		self.main_layout_widget.setLayout(hbox)

		self.big_vbox=QVBoxLayout()

		self.big_vbox.addWidget(self.ribbon)
		self.big_vbox.addWidget(self.main_layout_widget)

		self.setLayout(self.big_vbox)

		self.lumo.changed.connect(self.update_graph)
		self.homo.changed.connect(self.update_graph)
		

		self.big_vbox.addWidget(self.status_bar)
		self.bin.add_call_back(self.update)

	def update_graph(self):
		self.gen_mesh()
		self.plot.update()

	def callback_save(self):
		file_name=save_as_image(self)
		if file_name!=False:
			self.canvas_lumo.figure.savefig(file_name)


	def gen_mesh(self):
		json_path=self.bin.find_path_by_uid("epitaxy",self.uid)
		json_path=json_path+".shape_dos"

		tot_lumo = ctypes.c_double(0.0)
		tot_homo = ctypes.c_double(0.0)

		self.bin.lib.draw_all_traps(ctypes.byref(tot_lumo),
							ctypes.byref(tot_homo),
							ctypes.byref(self.data_lumo),
							ctypes.byref(self.data_homo),
							ctypes.byref(self.data_numerical_lumo),
							ctypes.byref(self.data_numerical_homo),
							ctypes.byref(json_tree_c()),ctypes.c_char_p(str2bytes(json_path)));

		self.data_lumo.convert_from_C_to_python()
		self.data_homo.convert_from_C_to_python()
		self.data_numerical_lumo.convert_from_C_to_python()
		self.data_numerical_homo.convert_from_C_to_python()

		self.data_numerical_lumo.file_name=str2bytes(os.path.join(os.getcwd(),"lumo_numberical.csv"))
		self.data_numerical_homo.file_name=str2bytes(os.path.join(os.getcwd(),"homo_numberical.csv"))
		self.data_lumo.file_name=str2bytes(os.path.join(os.getcwd(),"lumo.csv"))
		self.data_homo.file_name=str2bytes(os.path.join(os.getcwd(),"homo.csv"))

		#self.data_numerical_lumo.save(self.data_numerical_lumo.file_name)
		#self.data_numerical_homo.save(self.data_numerical_homo.file_name)
		#self.data_lumo.save(self.data_lumo.file_name)
		#self.data_homo.save(self.data_homo.file_name)

		self.plot.graph.axis_y.log_scale_auto=False
		self.plot.graph.axis_y.log_scale=True
		self.plot.load([self.data_lumo,self.data_homo,self.data_numerical_lumo,self.data_numerical_homo])
		self.plot.set_key_text([_("LUMO"),_("HOMO"),_("LUMO numerical"),_("HOMO numerical")])
		tot_lumo_str="{:.2e}".format(tot_lumo.value)
		tot_homo_str="{:.2e}".format(tot_homo.value)

		self.status_bar.showMessage("Trap density: LUMO="+tot_lumo_str+" m-3,  HOMO="+tot_homo_str+" m-3")

		self.bin.lib.dat_file_free_only(ctypes.byref(self.data_lumo))
		self.bin.lib.dat_file_free_only(ctypes.byref(self.data_homo))
		self.bin.lib.dat_file_free_only(ctypes.byref(self.data_numerical_lumo))
		self.bin.lib.dat_file_free_only(ctypes.byref(self.data_numerical_homo))

	def update(self):
		self.lumo.tab2.update()
		self.homo.tab2.update()

