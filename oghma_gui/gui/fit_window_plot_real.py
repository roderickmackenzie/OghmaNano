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

## @package fit_window_plot_real
#  Another fit plotting window?
#

import os
import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QMenuBar,QStatusBar, QMenu, QTableWidget, QAbstractItemView, QLabel
from PySide2.QtGui import QPainter,QIcon,QCursor

from open_save_dlg import open_as_filter
from icon_lib import icon_get
from cal_path import sim_paths
from plot_widget import plot_widget
from json_c import json_tree_c

class fit_window_plot_real(QWidget):

	def __init__(self,uid):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.uid=uid
		self.ax1=None
		self.show_key=True
		
		self.hbox=QVBoxLayout()

		self.label=QLabel()
		self.plot=plot_widget(enable_toolbar=False,widget_mode="graph")
		self.draw_graph()

		self.hbox.addWidget(self.plot)
		self.hbox.addWidget(self.label)
		self.setLayout(self.hbox)

	def update(self):
		self.draw_graph()

	def draw_graph(self):
		plot_labels=["Experimental"]
		json_path=self.refind_json_path()
		data_file=self.bin.get_token_value(json_path+".import_config","data_file")
		import_file_path=self.bin.get_token_value(json_path+".import_config","import_file_path")
		import_x_spin=self.bin.get_token_value(json_path+".import_config","import_x_spin")
		import_data_spin=self.bin.get_token_value(json_path+".import_config","import_data_spin")
		sim_data=self.bin.get_token_value(json_path+".config","sim_data")
		name=self.bin.get_token_value(json_path,"name")

		data_files=[os.path.join(sim_paths.get_sim_path(),data_file)]
		pre, ext = os.path.splitext(sim_data)
		sim_data_file=os.path.join(sim_paths.get_sim_path(),"sim",name,pre+".best")
		#print(sim_data_file)
		if os.path.isfile(sim_data_file)==True:
			plot_labels.append("Simulated")
			data_files.append(sim_data_file)

		self.plot.load_data(data_files)
		self.plot.set_labels(plot_labels)
		self.label.setText(_("Data imported from: ")+import_file_path+" col:"+str(import_x_spin)+" "+str(import_data_spin))
		self.plot.do_plot()

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid("fits.fits",self.uid)
		return ret

