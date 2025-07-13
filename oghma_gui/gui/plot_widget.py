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

## @package plot_widget
#  The main plot widget.
#

import io

#qt
from gQtCore import  gSignal,QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView, QMenuBar,QApplication
from PySide2.QtGui import QPainter,QIcon,QImage

#calpath
from icon_lib import icon_get
from dlg_get_text2 import dlg_get_text2

from plot_ribbon import plot_ribbon
from lock import get_lock

from QAction_lock import QAction_lock
import os
from color_map import color_map
from PySide2.QtWidgets import QWidget
from graph import graph_widget
from QWidgetSavePos import QWidgetSavePos
from dat_file import dat_file
from graph_cut_through import graph_cut_through
import ctypes
from bytes2str import str2bytes
from cal_path import subtract_paths
from cal_path import sim_paths
from json_c import json_files_gui_config

class plot_widget(QWidgetSavePos):
	text_output = gSignal(str)

	def __init__(self,enable_toolbar=True,widget_mode="graph",force_2d3d=False,color_widget_in=None):
		QWidgetSavePos.__init__(self,window_name="center")
		self.setFocusPolicy(Qt.StrongFocus)
		self.input_files=[]
		self.force_data_max=False
		self.force_data_min=False
		self.fix_scales=False
		self.setWindowIcon(icon_get("plot"))
		self.force_2d3d=force_2d3d
		self.plot_ribbon=plot_ribbon()
		self.main_vbox = QVBoxLayout()
		self.canvas=None
		self.widget_mode=widget_mode

		if color_widget_in==None:
			self.color_widget=self.plot_ribbon.color_map
			self.color_widget.find_map("Plot line colors")
		else:
			self.color_widget=color_widget_in


		if self.widget_mode=="graph":
			rb=self.plot_ribbon
			if enable_toolbar==False:
				rb=None
			self.canvas = graph_widget(plot_ribbon_in=rb)
			self.canvas.setMinimumSize(800, 350)
		if self.widget_mode=="circuit":
			from circuit_editor import circuit_editor
			self.canvas=circuit_editor(show_toolbar=False)
			self.canvas.ersatzschaltbild.show_resistance_values=False

		self.open_gl_enabled=False
		self.gl_plot=None
		self.log_data_lock=False
		self.zero_frame_enable=False
		self.zero_frame_list=[]

		self.cb=None

		if enable_toolbar==True:
			if self.widget_mode!="circuit":
				self.main_vbox.addWidget(self.plot_ribbon)

		if self.force_2d3d==True:
			self.open_gl_enabled=True

		self.build_toolbar()
		#print(">>>",self.open_gl_enabled,self.force_2d3d)
		if self.force_2d3d==True:
			self.callback_3d_mode()

		if self.canvas!=None:
			self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.main_vbox.addWidget(self.canvas)

		self.cut=graph_cut_through()
		self.cut.setVisible(False)  
		self.main_vbox.addWidget(self.cut)
		self.cut.z_slider.sliderMoved.connect(self.callback_z)
		self.cut.x_slider.sliderMoved.connect(self.callback_x)
		self.cut.y_slider.sliderMoved.connect(self.callback_y)


		self.setLayout(self.main_vbox)

	def contextMenuEvent(self,event):
		if self.open_gl_enabled==True:
			try:
				event.reject()
				return
			except:
				pass
			return
		elif self.widget_mode=="graph":
			self.canvas.show_menu(event)
			return

		#event.ignore()

	def do_plot(self):
		self.update_toolbar()
		if self.open_gl_enabled==True:
			self.gl_plot.gl_graph_load_files(self.input_files)
			self.gl_plot.force_redraw()
		else:
			if self.widget_mode=="graph":
				self.canvas.update()
			elif self.widget_mode=="circuit":
				self.canvas.ersatzschaltbild.load()
			

	def set_labels(self,labels):
		self.canvas.set_key_text(labels)

	def set_plot_types(self,plot_types):
		if len(self.input_files)!=len(plot_types):
			return
		#need to finish

	def reload(self):
		if self.widget_mode=="circuit":
			self.canvas.ersatzschaltbild.file_current_voltage=self.input_files[0]
			return
		elif self.widget_mode=="graph":
			self.canvas.load(self.input_files)
			return

	def load_data(self,input_files):
		self.lx=None
		self.ly=None
		self.input_files=input_files

		if len(input_files)==0:
			print(_("No files were given to load"))
			return

		if self.open_gl_enabled==True:
			if input_files[0].startswith(sim_paths.get_sim_path()):
				sub_paths=subtract_paths(sim_paths.get_sim_path(),input_files[0])
			else:
				sub_paths=input_files[0]

			sub_paths=subtract_paths(sim_paths.get_sim_path(),input_files[0])
			self.gl_plot.lib.gl_load_views(ctypes.byref(self.gl_plot.gl_main), ctypes.byref(json_files_gui_config), ctypes.c_char_p(str2bytes(sub_paths)))
			self.gl_plot.enable_views([sub_paths],by_hash=True)

		self.reload()

	def callback_color_map(self):
		if self.widget_mode=="graph":
			self.canvas.set_color_map(self.color_widget.map)
			self.do_plot()
		if self.open_gl_enabled==True: 
			self.gl_plot.gl_main.active_view.contents.color_map_graph=self.color_widget.map
			self.gl_plot.lib.gl_save_views(ctypes.byref(json_files_gui_config), ctypes.byref(self.gl_plot.gl_main))
			self.gl_plot.gl_graph_load_files(self.input_files)
			self.gl_plot.force_redraw()

	def callback_key(self):
		if len(self.data)>0:
			self.data[0].legend_pos=widget.get_label()
			self.do_plot()

	def callback_autoscale_y(self):
		self.fix_scales=self.plot_ribbon.tb_scale_autoscale.isChecked()
		if self.widget_mode=="matplotlib":
			if self.fix_scales==True:
				my_max,my_min=self.data[0].max_min()
				for i in range(0,len(self.data)):
					my_max,my_min=self.data[i].max_min(cur_min=my_min,cur_max=my_max)
				self.force_data_max=my_max
				self.force_data_min=my_min
				self.do_plot()
			else:
				self.force_data_max=False
				self.force_data_min=False

	def update(self):
		self.load_data(self.input_files)
		self.do_plot()

	def build_toolbar(self):
		self.plot_ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

		self.tb_3d_mode = QAction(icon_get("vector"), _("3D\nMode"), self)
		self.tb_3d_mode.setCheckable(True)
		self.tb_3d_mode.triggered.connect(self.callback_3d_mode)

		self.color_widget.changed.connect(self.callback_color_map)

		self.plot_ribbon.tb_scale_autoscale.triggered.connect(self.callback_autoscale_y)

		self.tb_3d_mode.triggered.connect(self.callback_3d_mode)
		self.plot_ribbon.plot_toolbar.addAction(self.tb_3d_mode)

	def update_toolbar(self):
		if len(self.input_files)>0:
			a=dat_file()
			if type(self.input_files[0])==str:
				a.load_only_info(self.input_files[0])
			else:
				a=self.input_files[0]
			b=a.how_can_i_display()
			self.tb_3d_mode.setVisible(False)
			if b.threeD_world==True and b.normal_graph==True:
				self.tb_3d_mode.setVisible(True)

			if self.cut!=None:
				if a.type==b'zxy-d' and a.x_len>1 and a.y_len>1 and a.z_len>1:
					self.cut.setVisible(True)
					self.cut.show_hide(True,False,True)

				if a.type==b'trap_map':
					if a.z_len==1 and a.x_len==1:
						self.cut.setVisible(False)
					else:
						self.cut.setVisible(True)
						self.cut.show_hide(a.z_len>1,a.x_len>1,False)

			if self.gl_plot!=None:
				self.gl_plot.gl_main.draw_electrical_mesh=False
				self.gl_plot.gl_main.active_view.contents.text=False
				self.gl_plot.gl_main.active_view.contents.draw_device=False
				self.gl_plot.gl_main.active_view.contents.draw_rays=False
				self.gl_plot.gl_main.active_view.contents.render_photons=False
				self.gl_plot.gl_main.active_view.contents.optical_mode=False

				if a.type=="zxy-d":
					self.gl_plot.gl_main.active_view.contents.plot_graph=True

				elif a.type=="circuit":

					self.gl_plot.draw_electrical_mesh=False
					self.gl_plot.gl_main.active_view.contents.draw_device=False
					self.gl_plot.gl_main.active_view.contents.draw_rays=False
					self.gl_plot.gl_main.active_view.contents.plot_graph=False
					self.gl_plot.plot_circuit=True
					self.gl_plot.gl_main.active_view.contents.render_photons=False

				elif a.type=="poly" or a.type==b"3d-mesh":
					self.gl_plot.draw_electrical_mesh=False
					self.gl_plot.gl_main.active_view.contents.draw_device=False
					self.gl_plot.gl_main.active_view.contents.draw_rays=False
					self.gl_plot.gl_main.active_view.contents.render_photons=False
					self.gl_plot.gl_main.active_view.contents.show_world_box=False
					self.gl_plot.gl_main.active_view.contents.show_detectors=False

		if self.open_gl_enabled==True:
			self.plot_ribbon.tb_pointer.setVisible(True)
			self.plot_ribbon.tb_home.setVisible(False)
		else:
			self.plot_ribbon.tb_pointer.setVisible(False)
			self.plot_ribbon.tb_home.setVisible(True)

	def callback_3d_mode(self):
		self.open_gl_enabled=False

		if self.tb_3d_mode.isChecked()==True:
			self.open_gl_enabled=True

		if self.force_2d3d==True:
			self.open_gl_enabled=True

		if self.open_gl_enabled==True:
			if self.canvas!=None:
				self.canvas.setVisible(False)

			if self.gl_plot==None:
				from gl import glWidget
				self.gl_plot=glWidget(self,plot_ribbon_in=self.plot_ribbon)
				self.gl_plot.draw_electrical_mesh=False
				self.gl_plot.gl_main.active_view.contents.draw_device=True
				self.gl_plot.gl_main.active_view.contents.draw_rays=False
				self.gl_plot.gl_main.active_view.contents.render_fdtd_grid=False
				self.gl_plot.scene_built=True
				self.gl_plot.plot_graph=True
				self.gl_plot.render_plot=True
				self.main_vbox.addWidget(self.gl_plot)
				self.plot_ribbon.plot_toolbar.addWidget(self.gl_plot.toolbar0)
				self.plot_ribbon.plot_toolbar.addWidget(self.gl_plot.toolbar1)
				self.gl_plot.tb_orthographic.setEnabled(False)

			self.gl_plot.setVisible(True)
			self.gl_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.setMinimumSize(650, 650)
			self.do_plot()

		else:
			self.gl_plot.setVisible(False)
			if self.canvas!=None:
				self.canvas.setVisible(True)
			#self.matplotlib_nav_bar.setVisible(True)

	def grab(self):
		if self.open_gl_enabled==True:
			return self.gl_plot.grabFrameBuffer()
		else:
			return self.canvas.grab()

	def save_image(self,file_name):
		image=self.grab()
		ext = os.path.splitext(file_name)[1][1:].lower()
		if ext not in ["png", "jpg", "jpeg"]:
			ext = "png" 
		image.save(file_name, ext)

	def callback_z(self, position):
		if self.open_gl_enabled==True:
			self.gl_plot.gl_main.active_view.contents.cut_through_frac_z=position/100.0
			self.gl_plot.force_redraw()
		else:
			self.canvas.graph.cut_through_frac_z=position/100.0
			self.do_plot()

	def callback_x(self, position):
		if self.open_gl_enabled==True:
			self.gl_plot.gl_main.active_view.contents.cut_through_frac_x=position/100.0
			self.gl_plot.force_redraw()
		else:
			self.canvas.graph.cut_through_frac_x=position/100.0
			self.do_plot()

	def callback_y(self, position):
		if self.open_gl_enabled==True:
			self.gl_plot.gl_main.active_view.contents.cut_through_frac_y=position/100.0
			self.gl_plot.force_redraw()
		else:
			self.canvas.graph.cut_through_frac_y=position/100.0
			self.do_plot()


			
