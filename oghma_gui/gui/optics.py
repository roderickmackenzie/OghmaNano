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
from plot_gen import plot_gen
from icon_lib import icon_get
from tab import tab_class
from progress_class import progress_class
from help import my_help_class

#path
from cal_path import get_exe_command

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QSystemTrayIcon,QMenu, QComboBox, QMenuBar, QLabel, QStatusBar
from PySide2.QtGui import QIcon

#windows
from band_graph2 import band_graph2

from plot_widget import plot_widget

from server import server_get

from global_objects import global_object_delete
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos

from optics_ribbon import optics_ribbon

from css import css_apply
from gui_util import yes_no_dlg
from json_root import json_root
from config_window import class_config_window
from help import help_window

class class_optical(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"optics")

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

		self.ribbon.optics.optical_thickness.triggered.connect(self.callback_optical_thickness)

		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

		self.main_vbox.addWidget(self.ribbon)


		self.progress_window=progress_class()

		self.notebook = QTabWidget()
		css_apply(self.notebook,"tab_default.css")
		self.notebook.setMovable(True)


		self.plot_widgets=[]
		self.progress_window.start()
		for i in range(0,len(self.input_files)):
			self.plot_widgets.append(plot_widget(enable_toolbar=False,widget_mode="pyqtgraph_imageview"))	#matplotlib
			self.plot_widgets[i].hide_title=True
			self.plot_widgets[i].set_labels([self.plot_labels[0]])
			self.plot_widgets[i].load_data([self.input_files[i]])
			#self.plot_widgets[i].watermark_alpha=0.5
			self.plot_widgets[i].do_plot()
			#self.plot_widgets[i].show()
			self.notebook.addTab(self.plot_widgets[i],self.plot_labels[i])

		self.input_files.append(os.path.join(sim_paths.get_sim_path(),"optical_output","G_y.csv"))
		self.fig_gen_rate = band_graph2()
		self.fig_gen_rate.set_data_file(self.input_files[-1])
		self.notebook.addTab(self.fig_gen_rate,_("Generation rate"))


		self.fig_gen_rate.draw_graph()
		self.progress_window.stop()

		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.main_vbox.addWidget(self.notebook)


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

	def callback_configwindow(self):
		data=json_root()
		self.config_window=class_config_window([data.optical.light],[_("Output files")])
		self.config_window.show()

	def callback_optical_thickness(self):
		from optical_thickness_editor import optical_thickness_editor
		self.window_optical_thickness=optical_thickness_editor()
		self.window_optical_thickness.show()
		help_window().help_set_help(["optical_thickness",_("<big><b>Optical thickness</b></big><br>Usually the optical thickness of a layer will be taken from the layer structure set out in the layer editor. However, sometimes one wants to simulate very thick layers. This window will enable you to force the optical thickness to a value while maintaining it's physical thickness.")])

	def callback_save(self):
		tab = self.notebook.currentWidget()
		tab.save_image()

	def onclick(self, event):
		for i in range(0,len(self.layer_end)):
			if (self.layer_end[i]>event.xdata):
				break
		pwd=sim_paths.get_sim_path()
		plot_gen([os.path.join(pwd,"materials",self.layer_name[i],"alpha.csv")],[],None,"")


	def closeEvent(self, event):
		global_object_delete("optics_force_redraw")
		self.hide()
		event.accept()

	def optics_sim_finished(self):
		data=json_root()
		data.optical.light.dump_verbosity=self.dump_verbosity
		data.save()
		self.force_redraw()

	def force_redraw(self):
		self.fig_gen_rate.build_bands()
		self.fig_gen_rate.draw_graph()

		#print("redraw optics3")
		for i in range(0,len(self.plot_widgets)):
			self.plot_widgets[i].update()
		#print("redraw optics4")			
		self.ribbon.update()
		
	def callback_run(self):
		data=json_root()
		self.my_server=server_get()
		self.dump_verbosity=data.optical.light.dump_verbosity

		data.optical.light.dump_verbosity=1
		data.save()

		self.my_server.clear_cache()
		self.my_server.clear_jobs()
		self.my_server.add_job(sim_paths.get_sim_path(),"--simmode opticalmodel@optics")
		self.my_server.sim_finished.connect(self.optics_sim_finished)
		self.my_server.start()

	def changed_click(self):
		i = self.notebook.currentIndex()
		self.status_bar.showMessage(self.input_files[i])
