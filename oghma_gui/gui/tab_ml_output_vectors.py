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
from json_root import json_root
from json_ml import json_ml_output_vector_item

class tab_ml_output_vectors(QWidget):


	def __init__(self,uid):
		QWidget.__init__(self)
		self.uid=uid
		self.vbox=QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(32, 32))

		self.vbox.addWidget(toolbar)


		self.tab2 = g_tab2(toolbar=toolbar)

		self.tab2.set_tokens(["ml_output_vector_item_enabled","file_name","ml_token_name","vectors"])
		self.tab2.set_labels([_("Enabled"),_("File name"), _("ML Token"),_("Vectors")])

		self.tab2.json_search_path="json_root().ml"
		self.tab2.uid=uid
		self.tab2.postfix="ml_output_vectors.segments"

		self.tab2.fixup_new_row=self.fixup_new_row
		self.tab2.setColumnWidth(1, 100)
		self.tab2.setColumnWidth(2, 100)
		self.tab2.setColumnWidth(3, 400)
		self.tab2.setColumnWidth(4, 20)
		self.tab2.base_obj=json_ml_output_vector_item()
		self.tab2.populate()
		self.tab2.changed.connect(self.callback_save)
		#self.tab2.callback_a=self.callback_show_list

		self.vbox.addWidget(self.tab2)

		self.setLayout(self.vbox)

	def fixup_new_row(self,row):
		return


	def callback_save(self):
		json_root().save()

