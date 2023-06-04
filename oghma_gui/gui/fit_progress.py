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

## @package fit_progress
#  Widget to display the fit progress. 
#


import os

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QMenuBar,QStatusBar, QMenu, QTableWidget, QAbstractItemView
from PySide2.QtGui import QPainter,QIcon,QCursor

#windows
from open_save_dlg import save_as_filter
from plot_widget import plot_widget

from cal_path import sim_paths

class fit_progress(QTabWidget):

	def update(self):
		for widget in self.plot_widgets:
			widget.reload()
			widget.do_plot()
	
	def update_for_fit(self):
		self.update()

	def __init__(self):
		QTabWidget.__init__(self)

		self.setMovable(True)
		self.plot_widgets=[]
		for file_name in ["fitlog.csv"]:	#,"fitlog_time_error.dat","fitlog_time_odes.dat"
			f_name=os.path.join(sim_paths.get_sim_path(),file_name)
			self.plot_widgets.append(plot_widget(enable_toolbar=False,widget_mode="pyqtgraph"))
			self.plot_widgets[-1].set_labels([os.path.basename(f_name)])
			self.plot_widgets[-1].load_data([f_name])
			self.plot_widgets[-1].do_plot()

			self.addTab(self.plot_widgets[-1],file_name)
		

	def rename(self,tab_name):
		return
