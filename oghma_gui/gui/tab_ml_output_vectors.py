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
from json_c import json_tree_c

class tab_ml_output_vectors(QWidget):


	def __init__(self,uid_main_sim,uid_sub_sim):
		QWidget.__init__(self)
		self.bin=json_tree_c()

		sub_sim_path=self.bin.find_path_by_uid("ml",uid_sub_sim)
		sim_name=self.bin.get_token_value(sub_sim_path,"sim_name")
		self.setWindowTitle(_("Output vectors for ")+sim_name)

		self.uid_main_sim=uid_main_sim
		self.uid_sub_sim=uid_sub_sim

		self.vbox=QVBoxLayout()
		self.setMinimumSize(1100,700)
		toolbar=QToolBar()
		toolbar.setIconSize(QSize(32, 32))

		self.vbox.addWidget(toolbar)


		self.tab2 = g_tab2_bin(toolbar=toolbar)

		self.tab2.set_tokens(["ml_output_vector_item_enabled","file_name","ml_token_name","vectors","import_config.import_file_path"])
		self.tab2.set_labels([_("Enabled"),_("File name"), _("ML Token"),_("Vectors"),_("Experimental file")])

		self.tab2.json_root_path="ml"
		self.tab2.uid=self.uid_sub_sim
		self.tab2.json_postfix="ml_output_vectors"

		self.tab2.fixup_new_row=self.fixup_new_row
		self.tab2.setColumnWidth(1, 100)
		self.tab2.setColumnWidth(2, 100)
		self.tab2.setColumnWidth(3, 400)
		self.tab2.setColumnWidth(4, 300)
		self.tab2.populate()
		self.tab2.changed.connect(self.callback_save)
		#self.tab2.callback_a=self.callback_show_list

		self.vbox.addWidget(self.tab2)

		self.setLayout(self.vbox)

	def fixup_new_row(self,row):
		path=self.tab2.refind_json_path()
		path=path+".segment"+str(row)
		uid=self.bin.get_token_value(path,"id")
		self.tab2.cellWidget(row, 4).uid_vector=uid
		self.tab2.cellWidget(row, 4).uid_sub_sim=self.uid_sub_sim
		self.tab2.cellWidget(row, 4).uid_main_sim=self.uid_main_sim


	def callback_save(self,uid):
		#print(self.uid_main_sim)
		self.bin.save()

