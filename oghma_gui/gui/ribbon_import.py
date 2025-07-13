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

## @package ribbon_import
#  The ribbon for importaing data files.
#


import os

from cal_path import sim_paths

#qt
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

#windows
from help import help_window

from icon_lib import icon_get

from util import wrap_text

from ribbon_base import ribbon_base
from help import QAction_help

class ribbon_import(ribbon_base):
	def main_toolbar(self):
		toolbar = QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(42, 42))

		self.open_data= QAction(icon_get("document-open"), wrap_text(_("Open data file"),4), self)
		toolbar.addAction(self.open_data)

		self.import_data= QAction(icon_get("document-save-as"), wrap_text(_("Import data"),4), self)
		self.import_data.setEnabled(False)
		toolbar.addAction(self.import_data)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		self.tb_help = QAction_help()
		toolbar.addAction(self.tb_help)

		return toolbar


	def __init__(self):
		ribbon_base.__init__(self)
		self.setMaximumHeight(140)
		w=self.main_toolbar()
		self.addTab(w,_("Load/Import"))

		sheet=self.readStyleSheet(os.path.join(sim_paths.get_css_path(),"style.css"))
		if sheet!=None:
			sheet=str(sheet,'utf-8')
			self.setStyleSheet(sheet)

