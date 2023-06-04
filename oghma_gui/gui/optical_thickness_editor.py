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

## @package generation_rate_editor
#  Editor to set the Generation rate in each layer
#

from icon_lib import icon_get
from global_objects import global_object_get

#inp
#windows
from g_tab2 import g_tab2
from error_dlg import error_dlg

#qt
from gQtCore import QSize
from PySide2.QtWidgets import QWidget, QVBoxLayout , QDialog,QToolBar,QAction, QSizePolicy, QTableWidget, QTableWidgetItem,QAbstractItemView

from global_objects import global_object_run
from global_objects import global_isobject
from global_objects import global_object_get
from QComboBoxLang import QComboBoxLang

import i18n
_ = i18n.language.gettext

from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos

from cal_path import sim_paths
from json_root import json_root

class optical_thickness_editor(QWidgetSavePos):

	def cell_changed(self):
		data=json_root()
		#for i in range(0,self.tab.rowCount()):
		#	uid=self.tab.get_value(i,2)
		#	obj=epi.find_object_by_id(uid)
		#	obj.Gnp=float(self.tab.get_value(i,1))

		data.save()

	def __init__(self):
		QWidgetSavePos.__init__(self,"generation_rate_editor")

		self.setWindowTitle2(_("Optical thickness editor"))
		self.setWindowIcon(icon_get("layers"))
		self.resize(500,250)

		self.main_vbox=QVBoxLayout()

		self.tab = g_tab2()

		self.tab.verticalHeader().setVisible(False)

		self.tab.blockSignals(True)
		self.tab.clear()
		#self.tab.setColumnCount(3)

		self.tab.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tab.set_tokens(["name","optical_thickness_enabled","optical_thickness","id"])
		self.tab.setHorizontalHeaderLabels([_("Layer name"), _("Enabled"), _("Optical thickness")+" (m)", _("json id")])
		self.tab.json_search_path="json_root().epitaxy.layers"
		self.tab.setColumnWidth(1, 100)
		self.tab.setColumnWidth(2, 250)
		self.tab.setColumnWidth(3, 10)
		self.tab.populate()
		self.tab.changed.connect(self.cell_changed)
		self.tab.blockSignals(False)

		#self.tab.cellChanged.connect(self.cell_changed)
		self.main_vbox.addWidget(self.tab)

		self.setLayout(self.main_vbox)




