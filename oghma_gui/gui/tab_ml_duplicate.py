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

## @package duplicate
#  Window to configure duplicated variables for fitting.
#

from select_param import select_param
from icon_lib import icon_get
from g_select import g_select

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QAbstractItemView, QMenuBar, QTableWidgetItem
from PySide2.QtGui import QPainter,QIcon

from gtkswitch import gtkswitch

from g_tab2_bin import g_tab2_bin
from sim_name import sim_name

class tab_ml_duplicate(QWidget):

	def __init__(self,uid):
		QWidget.__init__(self)
		self.setWindowTitle(_("Fit variables duplicate window")+sim_name.web_window_title)   
		self.setWindowIcon(icon_get("duplicate"))

		self.vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(32, 32))

		self.vbox.addWidget(toolbar)

		self.tab = g_tab2_bin(toolbar=toolbar)
		self.tab.set_tokens(["duplicate_var_enabled","human_src","human_dest","multiplier","json_src","json_dest"])
		self.tab.set_labels([_("Enabled"),_("Source")+" (x)", _("Destination")+" (y)", _("Function")+" y=f(x)", _("Source (JSON)"), _("Destination (JSON)")])
		self.tab.json_root_path="ml"
		self.tab.uid=uid

		self.tab.fixup_new_row=self.fixup_new_row
		self.tab.populate()
		self.tab.changed.connect(self.callback_save)
		self.tab.callback_a=self.callback_show_list_a
		self.tab.callback_b=self.callback_show_list_b

		self.tab.setColumnWidth(0, 150)
		self.tab.setColumnWidth(1, 350)
		self.tab.setColumnWidth(2, 350)
		self.tab.setColumnWidth(3, 100)
		self.tab.setColumnWidth(4, 20)
		self.tab.setColumnWidth(5, 20)

		self.vbox.addWidget(self.tab)

		self.select_param_window_a=select_param(self.tab)
		self.select_param_window_a.human_path_col=1
		self.select_param_window_a.json_path_col=4
		self.select_param_window_a.update()
		self.select_param_window_a.set_save_function(self.callback_save)

		self.select_param_window_b=select_param(self.tab)
		self.select_param_window_b.human_path_col=2
		self.select_param_window_b.json_path_col=5
		self.select_param_window_b.update()
		self.select_param_window_b.set_save_function(self.callback_save)

		self.setLayout(self.vbox)

	def callback_save(self):
		self.bin.save()

	def callback_show_list_a(self):
		self.select_param_window_a.show()

	def callback_show_list_b(self):
		self.select_param_window_b.show()

	def fixup_new_row(self,row):
		self.tab.cellWidget(row, 1).button.clicked.connect(self.callback_show_list_a)
		self.tab.cellWidget(row, 2).button.clicked.connect(self.callback_show_list_b)

