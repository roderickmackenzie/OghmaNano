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

## @package optics_filters_tab
#  A mesh editor for the time domain mesh.
#


import os

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QLabel,QToolBar,QSizePolicy,QAction

from g_tab2_bin import g_tab2_bin
from global_objects import global_object_run

from plot_widget import plot_widget
from cal_path import sim_paths

from icon_lib import icon_get
from tab import tab_class
import i18n
from json_c import json_tree_c

_ = i18n.language.gettext


class optics_filters_tab(QWidget):
 
	def __init__(self,search_path,uid,name):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.main_vbox_y0 = QVBoxLayout()
		self.serach_path=search_path
		self.uid=uid

		label_left=QLabel(name)
		self.main_vbox_y0.addWidget(label_left)
		toolbar2=QToolBar()
		toolbar2.setIconSize(QSize(32, 32))

		self.main_vbox_y0.addWidget(toolbar2)
	

		self.tab_filters = g_tab2_bin(toolbar=toolbar2)
		self.tab_filters.set_tokens(["filter_enabled","filter_material","filter_invert","filter_db"])
		self.tab_filters.set_labels([_("Enabled"),_("Filter"),_("Invert"),_("dB")])
		self.tab_filters.setColumnWidth(0, 100)
		self.tab_filters.setColumnWidth(1, 250)


		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar2.addWidget(spacer)

		self.tab_filters.json_root_path=search_path
		self.tab_filters.uid=uid
		self.tab_filters.json_postfix="virtual_spectra.light_filters"
		self.tab_filters.populate()

		self.tab_filters.new_row_clicked.connect(self.callback_new_row_clicked_filters)
		self.tab_filters.changed.connect(self.on_cell_edited)
		self.main_vbox_y0.addWidget(self.tab_filters)

		self.plot_widget=plot_widget(enable_toolbar=False,widget_mode="graph")
		self.plot_widget.set_labels([_("Attenuation")])
		plot_file=os.path.join(sim_paths.get_sim_path(),"optical_output","light_src_filter_"+self.uid+".csv")
		self.plot_widget.load_data([plot_file])
		self.plot_widget.canvas.x0_mul=0.2
		self.plot_widget.canvas.y_label="Transmission"
		self.plot_widget.canvas.x_label="Wavelength"
		self.plot_widget.canvas.enable_wavelength_to_rgb=True
		self.plot_widget.setMinimumHeight(250)

		self.update()

		self.main_vbox_y0.addWidget(self.plot_widget)
		self.setLayout(self.main_vbox_y0)

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid(self.serach_path,self.uid)
		return ret

	def callback_new_row_clicked_filters(self,row):
		self.plot_widget.do_plot()

	def on_cell_edited(self):
		self.bin.save()
		self.plot_widget.do_plot()
		global_object_run("gl_force_redraw")

	def update(self):
		self.plot_widget.reload()
		self.plot_widget.do_plot()



