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

## @package fit_vars
#  A window to define the fit variables.
#

from token_lib import tokens

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QAbstractItemView, QMenuBar, QTableWidgetItem
from PySide2.QtGui import QPainter,QIcon

from g_tab2_bin import g_tab2_bin
from select_param import select_param
from tab_ml_patch import tab_ml_patch
from tab_ml_output_vectors import tab_ml_output_vectors
from json_c import json_tree_c

class tab_ml_sims(QWidget):

	def __init__(self,main_ml_sim_uid):
		QWidget.__init__(self)
		self.main_ml_sim_uid=main_ml_sim_uid
		self.bin=json_tree_c()
		path=self.refind_json_path()
		print(path,self.main_ml_sim_uid)

		self.vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(32, 32))

		self.vbox.addWidget(toolbar)


		self.tab2 = g_tab2_bin(toolbar=toolbar)
		self.tab2.set_tokens(["ml_sim_enabled","sim_name","ml_edit_sim","ml_edit_vectors"])
		self.tab2.set_labels([_("Enabled"),_("Sim name"),_("Patch"),_("Vectors")])


		self.tab2.fixup_new_row=self.fixup_new_row
		self.tab2.json_root_path=path+".ml_sims"
		self.tab2.setColumnWidth(1, 200)
		self.tab2.setColumnWidth(2, 100)
		self.tab2.setColumnWidth(3, 100)
		self.tab2.setColumnWidth(4, 100)
		self.tab2.populate()
		self.tab2.changed.connect(self.callback_save)
		self.vbox.addWidget(self.tab2)
		self.setLayout(self.vbox)
		self.tab_ml_output_vectors=None

	def callback_save(self):
		self.bin.save()

	def fixup_new_row(self,row):
		path=self.refind_json_path()
		uid=self.bin.get_token_value(path+".ml_sims.segment"+str(row),"id")
		#print("FIXUP=",uid,path+".ml_sims.segments"+str(row))
		self.tab2.cellWidget(row, 2).uid=uid
		self.tab2.cellWidget(row, 2).changed.connect(self.callback_edit_clicked)

		self.tab2.cellWidget(row, 3).uid=uid
		self.tab2.cellWidget(row, 3).changed.connect(self.callback_edit_vectors_clicked)

	def callback_edit_clicked(self,uid):
		w=tab_ml_patch(uid)
		w.setMinimumSize(700,700)
		w.show()

	def callback_edit_vectors_clicked(self,uid_of_row):
		#print("a>",self.main_ml_sim_uid,uid_of_row)
		self.tab_ml_output_vectors=tab_ml_output_vectors(self.main_ml_sim_uid,uid_of_row)
		self.tab_ml_output_vectors.show()

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid("ml",self.main_ml_sim_uid)
		return ret
