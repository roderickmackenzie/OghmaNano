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

## @package tab_fit
#  A tab containing a fit. 
#

import os
from tab import tab_class
from fit_patch import fit_patch

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QMenuBar,QStatusBar, QMenu, QTableWidget, QAbstractItemView
from PySide2.QtGui import QPainter,QIcon,QCursor

#windows
from fit_window_plot import fit_window_plot
from fit_window_plot_real import fit_window_plot_real

from open_save_dlg import save_as_filter
from cal_path import sim_paths

from css import css_apply
from fit_duplicate import fit_duplicate
from json_c import json_tree_c

class tab_fit(QTabWidget):

	def __init__(self,json_path,uid):
		QTabWidget.__init__(self)
		self.json_path=json_path
		self.uid=uid
		self.bin=json_tree_c()
		path=self.refind_json_path()

		css_apply(self,"tab_default.css")

		self.tmesh_real = fit_window_plot_real(uid)
		self.addTab(self.tmesh_real,_("Experimental data"))

		self.tmesh = fit_window_plot(uid)
		self.addTab(self.tmesh,_("Delta=Experiment - Simulation"))

		self.config_tab=tab_class("fits.fits",uid=uid,json_postfix="config")
		self.addTab(self.config_tab,_("Configure fit"))

		self.fit_patch = fit_patch(uid)
		self.addTab(self.fit_patch, _("Fit patch"))

		duplicate_uid=self.bin.get_token_value(path+".duplicate","id")
		self.fit_duplicate = fit_duplicate("fits",duplicate_uid)
		self.addTab(self.fit_duplicate, _("Local duplicate"))

	def update_values(self):
		self.config_tab.tab.update_values()

	def update_graphs(self,force=False):
		json_path=self.bin.find_path_by_uid("fits.fits",self.uid)
		enabled=self.bin.get_token_value(json_path+".config","enabled")
		if enabled==True or force==True:
			self.tmesh_real.update()
			self.tmesh.update()

	def import_data(self):
		from import_data_json import import_data_json

		json_path=self.bin.find_path_by_uid("fits.fits",self.uid)

		self.im=import_data_json(self.bin,json_path+".import_config",export_path=sim_paths.get_sim_path())
		self.im.run()
		self.update_values()
		self.update_graphs(force=True)

	def get_tab_text(self):
		json_path=self.bin.find_path_by_uid("fits.fits",self.uid)
		enabled=self.bin.get_token_value(json_path+".config","enabled")
		name=self.bin.get_token_value(json_path,"name")

		if enabled==True:
			tick_cross="(\u2705)"
		else:
			tick_cross="(\u274C)"

		return name+" "+str(tick_cross)

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid("fits",self.uid)
		return ret
