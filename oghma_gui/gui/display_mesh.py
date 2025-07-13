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

## @package display
#  The display widget, this either displays the 3D OpenGL image of the device or the fallback non OpenGL widget.
#

import os

from gl import glWidget
#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QMessageBox, QLineEdit,QLabel
from gQtCore import QTimer
from gQtCore import gSignal

from icon_lib import icon_get
from help import help_window
from str2bool import str2bool
from cal_path import sim_paths
from global_objects import global_object_register
from global_objects import global_object_run

from dat_file import dat_file
from server import server_get
from json_c import json_tree_c
from json_c import json_files_gui_config
import ctypes
from bytes2str import str2bytes

class display_mesh(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.complex_display=False

		self.hbox=QHBoxLayout()
		self.data=dat_file()
		self.my_server=server_get()
		self.my_server.sim_finished.connect(self.refresh_display)
		self.display=glWidget(self)
		self.display.lib.gl_load_views( ctypes.byref(self.display.gl_main), ctypes.byref(json_files_gui_config), ctypes.c_char_p(str2bytes("circuit_plot_3d")))
		self.display.enable_views(["circuit_plot_3d"],by_hash=True)

		if self.bin.get_token_value("electrical_solver","solver_type")=="circuit":
			

			toolbar=QToolBar()
			toolbar.setOrientation(Qt.Vertical)
			toolbar.setIconSize(QSize(42, 42))

			spacer = QWidget()
			spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			toolbar.addWidget(spacer)

			self.tb_refresh = QAction(icon_get("view-refresh"), _("Refresh"), self)
			self.tb_refresh.triggered.connect(self.rebuild_mesh)
			toolbar.addAction(self.tb_refresh)


			toolbar.addWidget(self.display.toolbar0)
			toolbar.addWidget(self.display.toolbar1)

			self.hbox.addWidget(toolbar)
			
			#self.display.find_active_view()
			self.display.draw_electrical_mesh=False
			self.display.gl_main.active_view.contents.draw_device=False
			self.display.gl_main.active_view.contents.draw_rays=False
			self.display.gl_main.active_view.contents.render_photons=False
			self.display.gl_main.active_view.contents.plot_graph=True

		self.hbox.addWidget(self.display)
			
		self.setLayout(self.hbox)
		self.refresh_display()

	def refresh_display(self):
		self.display.gl_graph_load_files([os.path.join(sim_paths.get_sim_path(),"electrical_nodes.csv"), os.path.join(sim_paths.get_sim_path(),"electrical_links.csv") ])
		self.display.force_redraw()
		self.display.update()

	def rebuild_mesh(self):
		#try:
		#	self.my_server.sim_finished.disconnect(self.refresh_display)
		#except:
		#	pass

		self.my_server.add_job(sim_paths.get_sim_path(),"--simmode circuit_mesh@mesh_gen_electrical")
		self.my_server.print_jobs()
		self.my_server.start()

	def update(self):
		pass
		#self.display.reset()


