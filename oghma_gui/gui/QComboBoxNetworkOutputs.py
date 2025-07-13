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

## @package QComboBoxNewtonSelect
#  This combobox is used to select the newton solver to use.
#
import i18n
_ = i18n.language.gettext

#qt
import os
from gQtCore import QSize, Qt 
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QPushButton,QDialog, QWidget, QLineEdit, QHBoxLayout, QMenu
from cal_path import sim_paths
from g_select_base import g_select_base
from json_c import json_tree_c
from error_dlg import error_dlg

class QComboBoxNetworkOutputs(g_select_base):

	def __init__(self):
		g_select_base.__init__(self)
		self.button.clicked.connect(self.callback_button_click)
		self.uid=None
		self.bin=json_tree_c()

	def contextMenuEvent(self, event):
		self.menu.popup(QCursor.pos())

	def callback_button_click(self):
		path=self.bin.find_path_by_uid("ml",self.uid)
		dataset_name=self.bin.get_token_value(path.split(".ml_networks")[0],"name")
		self.dataset_path=os.path.join(sim_paths.get_sim_path(),dataset_name)

		file_name=os.path.join(self.dataset_path,"targets.txt")
		if os.path.isfile(file_name)==False:
			error_dlg(self,"no file: "+file_name)
			return

		self.blockSignals(True)
		#self.clear()

		file1 = open(file_name, 'r')
		all_inputs = file1.readlines()
		file1.close()

		self.menu = QMenu(self)

		l=[]
		lm=[]
		for item in all_inputs:
			path=item.strip()
			if item.startswith("params"):
				s=path.split(".",1)
			else:
				s=path.rsplit(".",1)
			if s[0] not in l:
				l.append(s[0])
				lm.append(self.menu.addMenu(s[0]))
			submenu=lm[l.index(s[0])].addAction(s[1],self.callback_menu)

		self.blockSignals(False)

		self.menu.popup(QCursor.pos())

	def callback_menu(self):
		action = self.sender()
		path=action.parent().title()+"."+action.text()
		self.edit.setText(path)
		self.changed.emit()		


