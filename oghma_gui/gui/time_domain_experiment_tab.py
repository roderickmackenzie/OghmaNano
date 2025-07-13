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

## @package time_domain_experiment_tab
#  A tab to hold time domain experiments.
#


from time_domain_mesh_tab import tab_time_mesh
from circuit import circuit
from tab import tab_class


import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTabWidget
from PySide2.QtGui import QPainter,QIcon
from cal_path import sim_paths
from css import css_apply
from json_c import json_tree_c

class time_domain_experiment_tab(QTabWidget):

	def __init__(self,json_search_path,uid):
		QTabWidget.__init__(self)
		self.bin=json_tree_c()
		css_apply(self ,"tab_default.css")
		self.json_search_path=json_search_path
		self.uid=uid
		self.setMovable(True)

		self.tmesh = tab_time_mesh(uid)
		self.addTab(self.tmesh,_("time mesh"))

		if self.bin.get_token_value("electrical_solver","solver_type")!="circuit":
			self.circuit=circuit(json_search_path,uid)
			self.addTab(self.circuit,_("Circuit"))

		tab=tab_class(json_search_path,uid=uid, json_postfix="config")
		self.addTab(tab,_("Configure"))

	def update(self):
		self.tmesh.update()

	def image_save(self):
		self.tmesh.image_save()

	def rename(self,tab_name):
		self.data.name=tab_name
		self.bin.save()

	def get_json_obj(self):
		return self.data

