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

## @package pl_experiment
#  PL simulation set up, for PL spectra.
#


from global_objects import global_object_get
from icon_lib import icon_get
from global_objects import global_object_register

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar
from PySide2.QtGui import QPainter,QIcon

#window
from tb_lasers import tb_lasers
from QWidgetSavePos import QWidgetSavePos
from jvexperiment_tab import jvexperiment_tab
from experiment import experiment

class pl_experiment(experiment):

	def ribbon_simulation(self):
		toolbar = QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(42, 42))

		self.tb_lasers=tb_lasers()
		toolbar.addWidget(self.tb_lasers)

		return toolbar

	def __init__(self,data=None):
		experiment.__init__(self,"jvexperiment_tab",window_save_name="plexperiment_editor", window_title=_("PL experiment window"),json_search_path="json_root().sims.pl_ss")


		self.notebook.currentChanged.connect(self.switch_page)
		w=self.ribbon_simulation()
		self.ribbon.addTab(w,_("Simulation"))

		self.switch_page()

	def switch_page(self):
		tab = self.notebook.currentWidget()
		if tab!=None:
			self.tb_lasers.update(tab.data)



