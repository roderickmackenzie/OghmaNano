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

## @package g_select
#  A widget for the tab widget which allows the user to select files.
#


#qt
import os
from PySide2.QtWidgets import QTextEdit, QAction, QListView,QLineEdit,QWidget,QHBoxLayout,QPushButton
from PySide2.QtGui import QPixmap
from gQtCore import QSize, Qt, QTimer, QPersistentModelIndex
from QComboBoxLang import QComboBoxLang
from PySide2.QtGui import QIcon
from g_select_base import g_select_base
from cal_path import sim_paths
from open_save_dlg import open_as_filter
from json_c import json_tree_c
import i18n
_ = i18n.language.gettext

class g_select(g_select_base):

	def __init__(self):
		g_select_base.__init__(self)
		self.button.clicked.connect(self.callback_button_click)

	def callback_button_click(self):
		file_name=open_as_filter(self,"dat (*.dat);;csv (*.csv);;txt (*.txt)")
		if file_name!=None:
			self.setText(file_name)

	def text(self):
		return self.get_value()

	def setText(self,value):
		self.set_value(value)

class g_select_import(g_select_base):

	def __init__(self):
		g_select_base.__init__(self)
		self.bin=json_tree_c()
		self.button.clicked.connect(self.callback_button_click)
		self.uid_main_sim=None
		self.uid_sub_sim=None
		self.uid_vector=None

	def callback_button_click(self):
		from import_data_json import import_data_json
		output_vector_path=self.bin.find_path_by_uid("ml",self.uid_vector)
		sub_sim_path=self.bin.find_path_by_uid("ml",self.uid_sub_sim)
		main_sim_path=self.bin.find_path_by_uid("ml",self.uid_main_sim)

		main_sim_name=self.bin.get_token_value(main_sim_path,"name")
		sim_name=self.bin.get_token_value(sub_sim_path,"sim_name")
		ml_token_name=self.bin.get_token_value(output_vector_path,"ml_token_name")
		data_file=sim_name+"_"+ml_token_name+".csv"
		self.bin.set_token_value(output_vector_path+".import_config","data_file",data_file)


		exp_path=os.path.join(sim_paths.get_sim_path(),main_sim_name,"experimental")
		if os.path.isdir(exp_path)==False:
			os.makedirs(exp_path)

		self.im=import_data_json(self.bin,output_vector_path+".import_config",export_path=exp_path)
		self.im.run()

		import_file_path=self.bin.get_token_value(output_vector_path+".import_config","import_file_path")
		self.set_value(import_file_path)

class g_select_electrical_edit(g_select_base):

	def __init__(self,uid):
		self.uid=uid
		self.bin=json_tree_c()
		g_select_base.__init__(self)
		self.button.clicked.connect(self.callback_button_click)

	def callback_button_click(self):
		from dos_main import dos_main
		self.electrical_editor=dos_main()
		self.electrical_editor.show()
		self.electrical_editor.show_tab_by_uid(self.uid)
		
	def text(self):
		return

	def setText(self,value):
		return

