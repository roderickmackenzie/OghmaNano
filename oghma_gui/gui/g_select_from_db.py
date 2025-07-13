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

## @package g_select_from_db
#  A widget for the tab widget which allows the user to select material files.
#



from PySide2.QtWidgets import QMessageBox, QDialog
from PySide2.QtWidgets import QLineEdit,QWidget,QHBoxLayout,QPushButton
from gQtCore import gSignal
from cal_path import subtract_paths
from g_select_base import g_select_base
from cal_path import sim_paths

import i18n
_ = i18n.language.gettext


class g_select_from_db(g_select_base):

	changed = gSignal()

	def __init__(self,path,file_box=True):
		g_select_base.__init__(self)
		self.path=path

		self.button.clicked.connect(self.callback_button_click)
		self.edit.textChanged.connect(self.text_changed)

	def text_changed(self):
		self.changed.emit()

	def callback_button_click(self):
		from g_open import g_open
		dialog=g_open(self.path,act_as_browser=False)

		ret=dialog.exec_()
		if ret==QDialog.Accepted:
			file_name=dialog.get_filename()
			rel_path=subtract_paths(self.path,file_name)
			rel_path=rel_path.replace("\\", "/")
			self.set_value(rel_path)
			self.changed.emit()
		

class g_select_filter(g_select_from_db):
	def __init__(self):
		g_select_from_db.__init__(self,sim_paths.get_filters_path())

class g_select_shape(g_select_from_db):
	def __init__(self):
		g_select_from_db.__init__(self,sim_paths.get_shape_path())

class g_select_material(g_select_from_db):
	def __init__(self):
		g_select_from_db.__init__(self,sim_paths.get_materials_path())

class g_select_morphology(g_select_from_db):
	def __init__(self):
		g_select_from_db.__init__(self,sim_paths.get_morphology_path())

class g_select_cache(g_select_from_db):
	def __init__(self):
		self.internal_value="none_none_none_default"
		g_select_from_db.__init__(self,sim_paths.get_home_path())
		self.edit.setEnabled(False)
		self.button.setEnabled(False)

	def set_value(self,value):
		self.edit.blockSignals(True)
		if value=="none_none_none_default":
			self.edit.setText(sim_paths.get_newton_cache_path())
		else:
			self.edit.setText(value)

		self.internal_value=value
		self.edit.blockSignals(False)

	def get_value(self):
		return self.internal_value

