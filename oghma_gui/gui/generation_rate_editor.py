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
from epitaxy import get_epi

from error_dlg import error_dlg
from inp import inp
from cal_path import sim_paths
from json_root import json_root

class generation_rate_editor(QWidgetSavePos):

	def cell_changed(self, y,x):
		data=json_root()
		epi=get_epi()

		for i in range(0,self.tab.rowCount()):
			uid=self.tab.get_value(i,2)
			obj=epi.find_object_by_id(uid)
			obj.Gnp=float(self.tab.get_value(i,1))

		data.save()

	def __init__(self):
		QWidgetSavePos.__init__(self,"generation_rate_editor")

		self.setWindowTitle2(_("Generaton rate editor"))
		self.setWindowIcon(icon_get("layers"))
		self.resize(400,250)

		self.main_vbox=QVBoxLayout()

		self.tab = g_tab2()

		self.tab.verticalHeader().setVisible(False)
		self.create_model()

		self.tab.cellChanged.connect(self.cell_changed)
		self.main_vbox.addWidget(self.tab)

		self.setLayout(self.main_vbox)

	def create_model(self):
		epi=get_epi()
		self.tab.blockSignals(True)
		self.tab.clear()
		self.tab.setColumnCount(3)

		self.tab.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tab.setHorizontalHeaderLabels([_("Layer name"), _("Generation rate (m^{-3}s^{-1})"), _("json id")])
		self.tab.setColumnWidth(1, 250)
		self.tab.setColumnWidth(2, 10)

		for l in epi.layers:
			self.add_row(l.name,l.Gnp,l.id)
			for s in l.segments:
				self.add_row(s.name,s.Gnp,s.id)


		self.tab.blockSignals(False)

	def add_row(self,name,Gnp,uid):

		self.tab.blockSignals(True)
		i=self.tab.rowCount()
		self.tab.insertRow ( i )
		item1 = QTableWidgetItem(str(name))
		self.tab.setItem(i,0,item1)

		item2 = QTableWidgetItem(str(Gnp))
		self.tab.setItem(i,1,item2)

		item2 = QTableWidgetItem(str(uid))
		self.tab.setItem(i,2,item2)

		self.tab.blockSignals(False)


