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

## @package optics_sources_tab.py
#  A mesh editor for the time domain mesh.
#


import os

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QLabel,QHBoxLayout,QToolBar,QSizePolicy,QAction, QMenu

from g_tab2_bin import g_tab2_bin
from global_objects import global_object_run

from plot_widget import plot_widget
from cal_path import sim_paths

from icon_lib import icon_get
from tab import tab_class
import i18n
_ = i18n.language.gettext
from sim_name import sim_name
from json_c import json_tree_c

class optics_light_src(QWidget):
 
	def __init__(self,search_path,uid,name):
		QWidget.__init__(self)
		self.bin=json_tree_c()

		self.serach_path=search_path
		self.uid=uid

		self.main_vbox_y0 = QVBoxLayout()
		label_left=QLabel(name)
		self.main_vbox_y0.addWidget(label_left)
		toolbar2=QToolBar()
		toolbar2.setIconSize(QSize(32, 32))

		self.main_vbox_y0.addWidget(toolbar2)
	
		self.tab_y0 = g_tab2_bin(toolbar=toolbar2)
		self.tab_y0.set_tokens(["light_spectrum","light_multiplyer"])
		self.tab_y0.set_labels([_("Spectrum"),_("Multiplyer")])
		self.tab_y0.setColumnWidth(0, 250)
		self.tab_y0.setColumnWidth(2, 250)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar2.addWidget(spacer)

		label = QLabel(_("External\ninterface:"))
		toolbar2.addWidget(label)

		#external interface
		self.optical_external_interface = QAction(icon_get("reflection"), _("External\nReflection"), self)
		self.optical_external_interface.setCheckable(True)
		self.optical_external_interface.triggered.connect(self.callback_filter_clicked)

		self.menu_optical_external_interface = QMenu(self)
		self.optical_external_interface.setMenu(self.menu_optical_external_interface)

		self.external_interface_edit=QAction(_("Edit"), self)
		self.external_interface_edit.triggered.connect(self.callback_external_interface_window)
		self.menu_optical_external_interface.addAction(self.external_interface_edit)
		toolbar2.addAction(self.optical_external_interface)


		self.tab_y0.json_root_path=self.serach_path
		self.tab_y0.uid=uid
		self.tab_y0.json_postfix="virtual_spectra.light_spectra"
		self.tab_y0.populate()

		self.tab_y0.new_row_clicked.connect(self.callback_new_row_clicked)
		self.tab_y0.changed.connect(self.on_cell_edited)


		self.main_vbox_y0.addWidget(self.tab_y0)

		self.plot_widget=plot_widget(enable_toolbar=False,widget_mode="graph")
		self.plot_widget.set_labels([_("Light intensity")])
		plot_file=os.path.join(sim_paths.get_sim_path(),"optical_output","light_src_"+self.uid+".csv")

		self.plot_widget.load_data([plot_file])
		self.plot_widget.canvas.x0_mul=0.2
		self.plot_widget.canvas.y_label=""
		self.plot_widget.canvas.x_label="Wavelength"
		self.plot_widget.canvas.enable_wavelength_to_rgb=True
		self.plot_widget.setMinimumHeight(250)
		self.update()

		self.main_vbox_y0.addWidget(self.plot_widget)
		self.setLayout(self.main_vbox_y0)

	def refind_json_path(self):
		ret=self.bin.find_path_by_uid(self.serach_path,self.uid)
		return ret

	def callback_new_row_clicked(self,row):
		self.plot_widget.do_plot()

	def on_cell_edited(self):
		self.plot_widget.do_plot()
		global_object_run("gl_force_redraw")

	def update(self):
		self.plot_widget.reload()
		self.plot_widget.do_plot()
		json_path=self.refind_json_path()
		enabled=self.bin.get_token_value(json_path+".virtual_spectra.external_interface","enabled")
		self.blockSignals(True)
		self.optical_external_interface.setChecked(enabled)

		self.blockSignals(False)

	def callback_filter_clicked(self):
		path=self.refind_json_path()
		json_path=self.refind_json_path()
		value=self.optical_external_interface.isChecked()
		self.bin.set_token_value(json_path+".virtual_spectra.external_interface","enabled",value)
		self.bin.save()


	def callback_external_interface_window(self):

		json_path=self.refind_json_path()
		self.widget=tab_class(json_path+".virtual_spectra.external_interface")
		self.widget.setWindowIcon(icon_get("reflection"))

		self.widget.setWindowTitle(_("Reflective interface editor")+sim_name.web_window_title)    

		self.widget.show()



