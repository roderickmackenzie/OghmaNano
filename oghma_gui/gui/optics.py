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

## @package optics
#  The main optics window
#


import os
from icon_lib import icon_get
from tab import tab_class
from progress_class import progress_class
from help import my_help_class

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QSystemTrayIcon,QMenu, QComboBox, QMenuBar, QLabel, QStatusBar
from PySide2.QtGui import QIcon

#windows
from plot_widget import plot_widget

from server import server_get

from global_objects import global_object_delete
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos

from optics_ribbon import optics_ribbon

from css import css_apply
from gui_util import yes_no_dlg
from config_window import class_config_window
from help import help_window
from json_c import json_tree_c
from graph import graph_widget
from global_objects import global_object_run

class class_optical(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"optics")
		self.bin=json_tree_c()

		self.setWindowIcon(icon_get("optics"))

		self.setMinimumSize(1000, 600)
		self.setWindowTitle2(_("Optical simulation editor"))    

		self.ribbon=optics_ribbon()

		self.edit_list=[]
		self.line_number=[]
		self.articles=[]
		self.input_files=[]
		self.input_files.append(os.path.join(sim_paths.get_sim_path(),"optical_output","photons_yl.csv"))
		self.input_files.append(os.path.join(sim_paths.get_sim_path(),"optical_output","photons_abs_yl.csv"))

		self.plot_labels=[]
		self.plot_labels.append(_("Photon distribution"))
		self.plot_labels.append(_("Photon distribution absorbed"))


		self.setWindowIcon(icon_get("optics"))

		self.main_vbox=QVBoxLayout()

		self.ribbon.optics.run.start_sim.connect(self.callback_run)

		self.ribbon.optics.configwindow.triggered.connect(self.callback_configwindow)

		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

		self.main_vbox.addWidget(self.ribbon)


		self.progress_window=progress_class()

		self.notebook = QTabWidget()
		css_apply(self.notebook,"tab_default.css")
		self.notebook.setMovable(True)


		self.plot_widgets=[]
		self.progress_window.start()
		for i in range(0,len(self.input_files)):
			self.plot_widgets.append(plot_widget(enable_toolbar=False,widget_mode="graph",color_widget_in=self.ribbon.optics.color_map))
			self.plot_widgets[i].canvas.graph.show_title=False
			self.plot_widgets[i].set_labels([self.plot_labels[0]])
			self.plot_widgets[i].load_data([self.input_files[i]])
			#self.plot_widgets[i].watermark_alpha=0.5
			self.plot_widgets[i].do_plot()
			#self.plot_widgets[i].show()
			self.notebook.addTab(self.plot_widgets[i],self.plot_labels[i])

		self.input_files.append(os.path.join(sim_paths.get_sim_path(),"optical_output","G_y.csv"))
		self.fig_gen_rate = graph_widget()
		self.fig_gen_rate.load([os.path.join(sim_paths.get_sim_path(),"optical_output","G_y.csv")])
		self.fig_gen_rate.graph.load_bands(self.bin)
		self.fig_gen_rate.graph.show_title=False
		self.notebook.addTab(self.fig_gen_rate,_("Generation rate"))

		self.check_sim_button_is_there()
		file_name=os.path.join(sim_paths.get_sim_path(),"optical_output","reflect.csv")
		self.input_files.append(file_name)
		self.plot_widgets.append(plot_widget(enable_toolbar=False,widget_mode="graph"))
		self.plot_widgets[-1].canvas.graph.show_title=False
		self.plot_widgets[-1].set_labels(["Reflected light"])
		self.plot_widgets[-1].load_data([file_name])
		self.plot_widgets[-1].do_plot()
		self.notebook.addTab(self.plot_widgets[-1],"Reflected light")

		self.progress_window.stop()

		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.main_vbox.addWidget(self.notebook)

		self.ribbon.optics.color_map.changed.connect(self.callback_color_map)
		self.setLayout(self.main_vbox)

		if os.path.isfile(os.path.join(sim_paths.get_sim_path(),"optical_output","photons_yl.csv"))==False:
			response=yes_no_dlg(self,"You have not yet run a full optical simulation, to use this feature you need to.  Would you run one now?")
			if response == True:
				self.callback_run()
			else:
				self.close()

		self.status_bar = QStatusBar()
		self.main_vbox.addWidget(self.status_bar)
		self.notebook.currentChanged.connect(self.changed_click)
		self.changed_click()

	def check_sim_button_is_there(self):
		segments=self.bin.get_token_value("sims.transfer_matrix","segments")
		if segments==0:
			self.bin.make_new_segment("sims.transfer_matrix","Transfer matrix",-1)
			global_object_run("ribbon_sim_mode_update")

	def callback_configwindow(self):
		self.config_window=class_config_window(["optical.light"],[_("Configure transfer matrix solver")])
		self.config_window.show()

	def callback_save(self):
		tab = self.notebook.currentWidget()
		tab.save_image()


	def closeEvent(self, event):
		global_object_delete("optics_force_redraw")
		self.hide()
		event.accept()

	def optics_sim_finished(self):
		self.bin.set_token_value("optical.light","dump_verbosity",self.dump_verbosity)
		self.bin.save()
		self.force_redraw()

	def force_redraw(self):
		self.fig_gen_rate.load([os.path.join(sim_paths.get_sim_path(),"optical_output","G_y.csv")])
		self.fig_gen_rate.graph.load_bands(self.bin)

		for i in range(0,len(self.plot_widgets)):
			self.plot_widgets[i].update()

		self.ribbon.update()
		
	def callback_run(self):
		self.my_server=server_get()
		self.dump_verbosity=self.bin.get_token_value("optical.light","dump_verbosity")
		self.bin.set_token_value("optical.light","dump_verbosity",1)
		self.bin.save()

		self.my_server.clear_cache()
		self.my_server.clear_jobs()
		self.my_server.add_job(sim_paths.get_sim_path(),"--simmode opticalmodel@optics")
		self.my_server.sim_finished.connect(self.optics_sim_finished)
		self.my_server.start()

	def changed_click(self):
		i = self.notebook.currentIndex()
		self.status_bar.showMessage(self.input_files[i])

	def callback_color_map(self):
		#tab = self.notebook.currentWidget()
		#self.force_redraw()
		for i in range(0,len(self.plot_widgets)):
			self.plot_widgets[i].callback_color_map()

