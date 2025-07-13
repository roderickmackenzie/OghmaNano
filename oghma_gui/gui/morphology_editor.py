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

## @package shape_editor
#  The shape editor
#


import os
from tab import tab_class
from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt, QTimer
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget, QDialog, QHBoxLayout
from PySide2.QtGui import QPainter,QIcon,QPixmap,QPen,QColor

#python modules

from help import help_window

from plot_widget import plot_widget
from win_lin import desktop_open

from QWidgetSavePos import QWidgetSavePos

from ribbon_morphology import ribbon_morphology

from open_save_dlg import open_as_filter

from dat_file import dat_file

from gQtCore import gSignal
from json_dialog import json_dialog

from config_window import class_config_window
from server import server_get
from cal_path import sim_paths

from gl import glWidget
from morphology_editor_io import morphology_editor_io

import shutil
import ctypes
from ref import ref_window
from json_c import json_c
from graph_cut_through import graph_cut_through
from bytes2str import str2bytes
from json_c import json_files_gui_config

class morphology_editor(QWidgetSavePos):

	def reload(self):
		self.load_data()
		self.three_d_shape.force_redraw()

	def load_data(self):
		path=os.path.join(self.path,"morphology.csv")
		self.three_d_shape.scale.set_m2screen()
		self.three_d_shape.gl_graph_load_files([path],scale=False)

	def __init__(self,path):
		QWidgetSavePos.__init__(self,"shape_import")
		self.path=path
		self.data=dat_file()
		#backward compatibility
		self.orig_image_file=os.path.join(path,"image_original.png")
		self.image_file=os.path.join(path,"image.png")
		if os.path.isfile(self.orig_image_file)==False:
			if os.path.isfile(self.image_file)==True:
				shutil.copyfile(self.image_file, self.orig_image_file)

		self.io=morphology_editor_io(self.path)
		self.io.load()
		self.io.loaded=True
		self.io.save()

		self.setMinimumSize(900, 900)
		self.setWindowIcon(icon_get("shape"))

		self.setWindowTitle2(os.path.basename(self.path)+" "+_("Morphology editor")) 

		self.main_vbox = QVBoxLayout()

		self.ribbon=ribbon_morphology()

		#self.ribbon.mesh_edit.triggered.connect(self.callback_mesh_editor)
		self.ribbon.tb_rebuild.clicked.connect(self.callback_rebuild)
		self.ribbon.tb_ref.triggered.connect(self.callback_ref)
		server_get().sim_finished.connect(self.ribbon.tb_rebuild.stop)
		server_get().sim_started.connect(self.ribbon.tb_rebuild.start)

		self.ribbon.color_map.changed.connect(self.callback_color_map)

		self.ribbon.tb_configure.triggered.connect(self.callback_configure)

		#On button depress filters
	
		self.main_vbox.addWidget(self.ribbon)

		self.notebook = QTabWidget()

		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)

		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

		#3d widget
		self.three_d_shape=glWidget(self)
		self.three_d_shape.lib.gl_load_views(ctypes.byref(self.three_d_shape.gl_main), ctypes.byref(json_files_gui_config), ctypes.c_char_p(str2bytes(self.path)))
		self.three_d_shape.enable_views([self.path],by_hash=True)
		self.three_d_shape.draw_electrical_mesh=False
		self.three_d_shape.gl_main.active_view.contents.draw_device=False
		self.three_d_shape.gl_main.active_view.contents.draw_rays=False
		self.three_d_shape.gl_main.active_view.contents.render_fdtd_grid=False
		self.three_d_shape.scene_built=True
		self.three_d_shape.gl_main.active_view.contents.plot_graph=True
		self.three_d_shape.render_plot=True
		self.three_d_shape.gl_main.active_view.contents.render_grid=True
		self.three_d_shape.gl_main.active_view.contents.ray_solid_lines=True
		self.three_d_shape.gl_main.active_view.contents.render_photons=False
		self.three_d_shape.gl_main.active_view.contents.optical_mode=False
		self.three_d_shape.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		display=QWidget()
		layout = QVBoxLayout()
		display.setLayout(layout)
		layout.addWidget(self.three_d_shape)

		self.cut=graph_cut_through()
		self.cut.show_hide(True,False,True)
		layout.addWidget(self.cut)
		self.cut.y_slider.sliderMoved.connect(self.callback_y)
		self.cut.z_slider.sliderMoved.connect(self.callback_z)

		self.notebook.addTab(display,_("Shape"))
		self.setLayout(self.main_vbox)
		self.load_data()
		self.timer=QTimer()
		self.timer.timeout.connect(self.callback_timed_redraw)
		self.timer.start(20)

	def callback_configure(self):
		self.config_window=class_config_window(["config",""],[_("Configure"),_("General")],data=self.io.bin)
		self.config_window.show()

	def callback_timed_redraw(self):
		self.timer.stop()
		self.three_d_shape.force_redraw()

	def callback_ref(self):
		self.ref_window=ref_window(os.path.join(self.path,"morphology.bib"),"morphology")
		self.ref_window.show()

	def callback_rebuild(self):
		self.my_server=server_get()
		self.io.add_job_to_server(sim_paths.get_sim_path(),self.my_server)
		self.my_server.sim_finished.connect(self.reload)
		self.my_server.start()

	def callback_y(self, position):
		self.three_d_shape.gl_main.active_view.contents.cut_through_frac_y=position/100.0
		self.three_d_shape.force_redraw()

	def callback_z(self, position):
		self.three_d_shape.gl_main.active_view.contents.cut_through_frac_z=position/100.0
		self.three_d_shape.force_redraw()

	def callback_color_map(self):
		self.three_d_shape.gl_main.active_view.contents.color_map_graph=self.ribbon.color_map.map
		#self.three_d_shape.gl_graph_load_files(self.input_files)
		self.three_d_shape.force_redraw()

