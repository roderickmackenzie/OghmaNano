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

## @package ribbon_spectra
#  A ribbon for the materials window.
#

import os

#qt
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

from win_lin import desktop_open

from icon_lib import icon_get
from cal_path import sim_paths
from util import wrap_text
from ribbon_base import ribbon_base
from QAction_lock import QAction_lock


class ribbon_spectra(ribbon_base):
	def main_toolbar(self):
		self.main_toolbar = QToolBar()
		self.main_toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		self.main_toolbar.setIconSize(QSize(42, 42))

		self.import_data= QAction_lock("import", _("From\nFile"), self,"ribbon_spectra_import")
		self.main_toolbar.addAction(self.import_data)

		self.tb_ref= QAction(icon_get("ref"), wrap_text(_("Insert reference information"),8), self)
		self.main_toolbar.addAction(self.tb_ref)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.main_toolbar.addWidget(spacer)

		self.help = QAction(icon_get("internet-web-browser"), _("Help"), self)
		self.main_toolbar.addAction(self.help)

		self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		return self.main_toolbar


	def __init__(self):
		ribbon_base.__init__(self)

		w=self.main_toolbar()
		self.addTab(w,_("File"))

		sheet=self.readStyleSheet(os.path.join(sim_paths.get_css_path(),"style.css"))
		if sheet!=None:
			sheet=str(sheet,'utf-8')
			self.setStyleSheet(sheet)

