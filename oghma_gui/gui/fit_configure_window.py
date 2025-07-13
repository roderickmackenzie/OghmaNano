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

## @package fit_configure_window
#  The main window used for configuring the fit.
#

from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget
from PySide2.QtGui import QPainter,QIcon

#windows
from tab import tab_class

from gQtCore import gSignal

from QWidgetSavePos import QWidgetSavePos
from help import QAction_help
from json_c import json_tree_c

class fit_configure_window(QWidgetSavePos):

	changed = gSignal()
	
	def callback_tab_changed(self):
		self.changed.emit()

	def __init__(self,name):
		from fit_duplicate import fit_duplicate
		from fit_vars import fit_vars
		from fit_rules import fit_rules

		QWidgetSavePos.__init__(self,name)
		self.bin=json_tree_c()
		self.setMinimumSize(900, 600)
		self.setWindowIcon(icon_get("preferences-system"))

		self.setWindowTitle2(_("Fit configure")) 
		

		self.main_vbox = QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)		

		self.notebook = QTabWidget()
		self.notebook.setMovable(True)
		self.main_vbox.addWidget(self.notebook)

		uid=self.bin.get_token_value("fits.duplicate","id")
		self.duplicate_window=fit_duplicate("fits.duplicate",uid)
		self.notebook.addTab(self.duplicate_window,_("Duplicate variables"))

		self.fit_vars_window=fit_vars()
		self.notebook.addTab(self.fit_vars_window,_("Fit variables"))

		self.fit_rules_window=fit_rules()
		self.notebook.addTab(self.fit_rules_window,_("Fit rules"))

		self.config_tab=tab_class("fits.fit_config")
		self.notebook.addTab(self.config_tab,_("Configure minimizer"))

		self.bin.add_call_back(self.update_values)

		self.setLayout(self.main_vbox)

	def update_values(self):
		self.dummy_tab.tab.template_widget=data.fits.dummy_vars
		self.dummy_tab.tab.update_values()


