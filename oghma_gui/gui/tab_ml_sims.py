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

from g_tab2 import g_tab2
from select_param import select_param
from json_root import json_root
from json_ml import json_ml_sims_item
from tab_ml_patch import tab_ml_patch
from tab_ml_output_vectors import tab_ml_output_vectors

class tab_ml_sims(QWidget):

	def __init__(self,uid):
		QWidget.__init__(self)
		self.uid=uid

		self.vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(32, 32))

		self.vbox.addWidget(toolbar)


		self.tab2 = g_tab2(toolbar=toolbar)
		self.tab2.set_tokens(["ml_sim_enabled","sim_name","ml_edit_sim","ml_edit_vectors"])
		self.tab2.set_labels([_("Enabled"),_("Sim name"),_("Patch"),_("Vectors")])

		data=json_root().ml.find_object_by_id(self.uid)
		index=json_root().ml.segments.index(data)
		self.tab2.fixup_new_row=self.fixup_new_row
		self.tab2.json_search_path="json_root().ml.segments["+str(index)+"].ml_sims.segments"
		self.tab2.setColumnWidth(1, 400)
		self.tab2.setColumnWidth(2, 100)
		self.tab2.setColumnWidth(3, 100)
		self.tab2.setColumnWidth(4, 100)
		self.tab2.base_obj=json_ml_sims_item()
		self.tab2.populate()
		self.tab2.changed.connect(self.callback_save)

		self.vbox.addWidget(self.tab2)

		self.setLayout(self.vbox)


	def callback_save(self):
		json_root().save()

	def fixup_new_row(self,row):
		data=json_root().ml.find_object_by_id(self.uid)
		index=json_root().ml.segments.index(data)
		self.tab2.cellWidget(row, 2).uid=json_root().ml.segments[index].ml_sims.segments[row].id
		self.tab2.cellWidget(row, 2).changed.connect(self.callback_edit_clicked)

		self.tab2.cellWidget(row, 3).uid=json_root().ml.segments[index].ml_sims.segments[row].id
		self.tab2.cellWidget(row, 3).changed.connect(self.callback_edit_vectors_clicked)

	def callback_edit_clicked(self,uid):
		w=tab_ml_patch(uid)
		w.setMinimumSize(700,700)
		w.show()

	def callback_edit_vectors_clicked(self,uid):
		w=tab_ml_output_vectors(uid)
		w.setMinimumSize(700,700)
		w.show()
