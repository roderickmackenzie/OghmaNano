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

## @package fit_window_plot
#  Widget to plot the results of the fit.
#

import os
from plot_widget import plot_widget
import i18n
_ = i18n.language.gettext

#qt
from PySide2.QtWidgets import QWidget,QVBoxLayout

from open_save_dlg import save_as_jpg

from cal_path import sim_paths

class fit_window_plot(QWidget):

	def update(self):
		self.draw_graph()

	def draw_graph(self):
		error_sim=os.path.join(self.path,"fit_error_sim.csv")
		error_exp=os.path.join(self.path,"fit_error_exp.csv")
		delta=os.path.join(self.path,"fit_error_delta.csv")
		self.plot.load_data([error_sim,error_exp])
		self.plot.set_labels(["Simulation","Experiment"])
		self.plot.do_plot()

		self.plot_delta.load_data([delta])
		self.plot_delta.set_labels(["Delta"])
		self.plot_delta.do_plot()

	def export_image(self):
		self.plot.callback_save_image()

	def export_csv(self):
		self.plot.callback_save_csv()

	def export_xls(self):
		self.plot.callback_save_xls()

	def export_gnuplot(self):
		self.plot.callback_save_gnuplot()

	def __init__(self,path):
		QWidget.__init__(self)
		self.vbox=QVBoxLayout()
		self.path=path

		self.plot=plot_widget(enable_toolbar=False,widget_mode="pyqtgraph")
		self.vbox.addWidget(self.plot)
		self.plot_delta=plot_widget(enable_toolbar=False,widget_mode="pyqtgraph")
		self.vbox.addWidget(self.plot_delta)
		
		self.setLayout(self.vbox)
		
		self.draw_graph()
