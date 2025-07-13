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

## @package tab_ml
#  ml tab widget
#

import i18n
_ = i18n.language.gettext

#qt
import os
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTabWidget
from PySide2.QtGui import QPainter,QIcon
from tab import tab_class
from tab_ml_random import tab_ml_random
from tab_ml_patch import tab_ml_patch
from tab_ml_sims import tab_ml_sims
from tab_ml_duplicate import tab_ml_duplicate
from oghma_QTabWidget import oghma_QTabWidget
from gQtCore import gSignal
from cal_path import sim_paths
from PySide2.QtWidgets import QMessageBox
from json_c import json_tree_c

class tab_ml(oghma_QTabWidget):

	tab_changed = gSignal(str)
	def __init__(self,json_path,uid):
		self.bin=json_tree_c()
		oghma_QTabWidget.__init__(self)
		self.last_page_index=0
		self.json_path=json_path
		self.uid=uid
		path=self.refind_json_path()
		self.setMovable(True)

		tab=tab_ml_sims(self.uid)
		self.addTab(tab,_("Simulations"))


		tab=tab_ml_random(self.uid)
		self.addTab(tab,_("Random variables"))

		tab=tab_ml_patch(self.uid)
		self.addTab(tab,_("Patch"))

		duplicate_id=self.bin.get_token_value(path+".duplicate","id")
		tab=tab_ml_duplicate(duplicate_id)
		self.addTab(tab,_("Duplicate"))

		from window_ml_networks import window_ml_networks
		ml_networks_id=self.bin.get_token_value(path+".ml_networks","id")
		self.net=window_ml_networks(ml_networks_id)
		self.addTab(self.net,_("Neural networks"))

		self.currentChanged.connect(self.callback_ribbon_changed)

	def rename(self,tab_name):
		self.data.name=tab_name
		self.bin.save()

	def get_json_obj(self):
		return self.data

	def compile_to_json(self):
		ret=self.bin.ml_make_nets_json(self.uid)
		msgBox = QMessageBox(self)
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Compiled to json:")
		
		if ret==None:
			msgBox.setInformativeText(_("Could not compile json."))
			
		else:
			msgBox.setInformativeText(_("Json compiled to: ")+ret)

		msgBox.setStandardButtons(QMessageBox.Ok )
		msgBox.setDefaultButton(QMessageBox.Ok)
		msgBox.setMinimumWidth(800)
		msgBox.exec_()

	def callback_ribbon_changed(self):
		index = self.currentIndex()
		if self.tabText(index)!=_("Neural networks"):
			self.last_page_index=index

		self.tab_changed.emit(self.tabText(index))

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid("ml",self.uid)
		return ret

