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

## @package fit_patch
#  Patch the fit.
#


from select_param import select_param

from icon_lib import icon_get

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView, QMenuBar,QTableWidgetItem
from PySide2.QtGui import QPainter,QIcon

from g_select import g_select
from json_c import json_tree_c
from g_tab2_bin import g_tab2_bin

class fit_patch(QWidget):

	def __init__(self,uid):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(32, 32))

		self.vbox.addWidget(toolbar)

		self.tab2 = g_tab2_bin(toolbar=toolbar)
		self.tab2.set_tokens(["human_path","val","json_path"])
		self.tab2.set_labels([_("Variable"), _("Value"), _("JSON Variable")])
		self.tab2.json_root_path="fits.fits"
		self.tab2.uid=uid
		self.tab2.json_postfix="fit_patch"
		
		self.tab2.setColumnWidth(0, 300)
		self.tab2.setColumnWidth(1, 150)
		self.tab2.setColumnWidth(2, 10)
		self.tab2.fixup_new_row=self.fixup_new_row
		self.tab2.verticalHeader().setVisible(False)
		self.tab2.changed.connect(self.callback_changed)
		self.select_param_window=select_param(self.tab2)
		self.select_param_window.human_path_col=0
		self.select_param_window.json_path_col=2
		self.select_param_window.set_save_function(self.callback_changed)
		self.tab2.callback_a=self.callback_show_list

		self.tab2.populate()

		self.tab2.changed.connect(self.callback_changed)

		self.vbox.addWidget(self.tab2)


		self.setLayout(self.vbox)

	def callback_changed(self):
		self.bin.save()

	def fixup_new_row(self,row):
		self.tab2.cellWidget(row, 0).button.clicked.connect(self.callback_show_list)

	def callback_show_list(self):
		self.select_param_window.show()

