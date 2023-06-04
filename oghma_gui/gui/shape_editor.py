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

from ribbon_shape_import import ribbon_shape_import

from open_save_dlg import open_as_filter

from dat_file import dat_file

from gQtCore import gSignal
from PIL import Image, ImageFilter,ImageOps, ImageDraw
from PIL.ImageQt import ImageQt
from json_dialog import json_dialog

from shape_image_flat_view import shape_image_flat_view
from scripts import scripts

from config_window import class_config_window
from cal_path import get_exe_command
from server import server_get
from cal_path import sim_paths

from gl import glWidget
from bibtex import bibtex
from json_shape_db_item import shape_db_item
from shape_editor_io import shape_editor_io

from vec import vec
from json_base import json_base
import shutil
from shape_bildverarbeitung import shape_bildverarbeitung

class shape_editor(QWidgetSavePos):

	def changed_click(self):

		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Shape"):
			b=bibtex()
			if b.load(os.path.join(self.path,"shape.bib"))!=False:
				text=b.get_text()
				help_window().help_set_help(["shape.png",_("<big><b>Shape file</b></big><br>"+text)])


	def reload(self):
		self.shape_image_flat_view.force_update()
		self.load_data()
		self.three_d_shape.force_redraw()

	def load_data(self):
		self.data=dat_file()
		self.data.load(os.path.join(self.path,"shape.inp"),raw_data=True)
		if self.data.data!=None:
			a=vec()
			min_vec=self.data.gl_triangles_get_min()
			self.data.gl_triangles_sub_vec(min_vec)
			max_vec=self.data.gl_triangles_get_max()
			self.data.gl_triangles_div_vec(max_vec)
			
			self.three_d_shape.scale.set_m2screen()
			self.three_d_shape.graph_data=[self.data]

	def update(self):
		self.alpha.update()

	def callback_norm_y(self):
		self.io.import_config.shape_import_y_norm=self.ribbon.tb_norm_y.isChecked()
		self.io.save()
		im=self.io.load_image()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)
		self.shape_image_flat_view.force_update()

	def callback_tb_gaus(self):
		im=self.io.draw_gauss()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_tb_honeycomb(self):
		im=self.io.draw_honeycomb()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_tb_xtal(self):
		im=self.io.draw_xtal()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_tb_lens(self):
		im=self.io.draw_lens()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_tb_saw_wave(self):
		im=self.io.draw_saw_wave()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_rotate(self):
		rotate=self.io.import_config.shape_import_rotate
		rotate=rotate+90
		if rotate>360:
			rotate=0
		self.io.import_config.shape_import_rotate=rotate
		self.io.save()
		im=self.io.load_image()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)
		self.shape_image_flat_view.force_update()


	def callback_filters_update(self):
		self.io.blur.shape_import_blur_enabled=self.ribbon.tb_blur.isChecked()
		self.io.threshold.threshold_enabled=self.ribbon.tb_threshold.isChecked()
		self.io.import_config.shape_import_z_norm=self.ribbon.tb_norm_z.isChecked()
		self.io.boundary.boundary_enabled=self.ribbon.tb_boundary.isChecked()
		self.io.save()
		im=self.io.load_image()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)
		self.shape_image_flat_view.force_update()

	def callback_menu_blur(self):
		self.config_window=class_config_window([self.io.blur],[_("Blur menu")],data=self.io)
		self.config_window.show()

	def callback_mesh_editor(self):
		self.config_window=class_config_window([self.io.mesh],[_("Configure mesh")],data=self.io)
		self.config_window.show()

	def callback_mesh_build(self):
		self.my_server=server_get()
		self.io.add_job_to_server(sim_paths.get_sim_path(),self.my_server)
		#self.my_server.add_job(sim_paths.get_sim_path(),"--simmode data@mesh_gen --path "+self.path)
		self.my_server.sim_finished.connect(self.reload)
		self.my_server.start()

	def callback_edit_norm_y(self):
		self.a=json_dialog(title=_("Normalization editor"),icon="shape")
		data=json_base("dlg")
		data.var_list.append(["shape_import_y_norm_percent",self.io.import_config.shape_import_y_norm_percent])
		data.var_list_build()
		ret=self.a.run(data)

		if ret==QDialog.Accepted:
			self.io.import_config.shape_import_y_norm_percent=data.shape_import_y_norm_percent
			self.io.save()
			im=self.io.load_image()
			f=shape_bildverarbeitung(self.path,self.io)
			f.apply(im)
			self.shape_image_flat_view.force_update()


	def callback_open_image(self):
		file_name=open_as_filter(self,"png (*.png);;jpg (*.jpg)",path=self.path)
		if file_name!=None:
			im = Image.open(file_name)
			im.save(os.path.join(self.path,"image.png"))				#This is the edited one
			im.save(os.path.join(self.path,"image_original.png"))		#This is the original image
			self.shape_image_flat_view.load_image()
			self.shape_image_flat_view.build_mesh()
			self.callback_filters_update()

	def callback_script(self):
		self.scripts.show()

	def __init__(self,path):
		QWidgetSavePos.__init__(self,"shape_import")
		self.path=path

		#backward compatibility
		self.orig_image_file=os.path.join(path,"image_original.png")
		self.image_file=os.path.join(path,"image.png")
		if os.path.isfile(self.orig_image_file)==False:
			if os.path.isfile(self.image_file)==True:
				shutil.copyfile(self.image_file, self.orig_image_file)



		self.io=shape_editor_io()
		self.io.load(os.path.join(self.path,"data.json"))
		self.io.loaded=True
		self.io.save()
		print(">>>",self.path)
		self.shape_image_flat_view=shape_image_flat_view(self.path,self.io)


		self.setMinimumSize(900, 900)
		self.setWindowIcon(icon_get("shape"))

		self.setWindowTitle2(os.path.basename(self.path)+" "+_("Shape editor")) 

		self.scripts=scripts(path=self.path,api_callback=self.shape_image_flat_view.force_update)

		self.scripts.ribbon.help.setVisible(False)
		self.scripts.ribbon.plot.setVisible(False)
		self.scripts.ribbon.hashtag.setVisible(False)

		self.main_vbox = QVBoxLayout()

		self.ribbon=ribbon_shape_import()

		self.ribbon.tb_norm_y.setChecked(self.io.import_config.shape_import_y_norm)



		self.ribbon.menu_threshold.triggered.connect(self.callback_threshold_menu_edit)

		self.ribbon.mesh_edit.triggered.connect(self.callback_mesh_editor)
		self.ribbon.mesh_build.clicked.connect(self.callback_mesh_build)
		server_get().sim_finished.connect(self.ribbon.mesh_build.stop)
		server_get().sim_started.connect(self.ribbon.mesh_build.start)

		self.ribbon.edit_norm_y.triggered.connect(self.callback_edit_norm_y)
		self.ribbon.menu_blur.triggered.connect(self.callback_menu_blur)


		self.ribbon.tb_gaus.triggered.connect(self.callback_tb_gaus)
		self.ribbon.tb_gaus_menu_edit.triggered.connect(self.callback_gaus_menu_edit)

		self.ribbon.tb_honeycomb.triggered.connect(self.callback_tb_honeycomb)
		self.ribbon.tb_honeycomb_menu_edit.triggered.connect(self.callback_honeycomb_menu_edit)

		self.ribbon.tb_xtal.triggered.connect(self.callback_tb_xtal)
		self.ribbon.tb_xtal_menu_edit.triggered.connect(self.callback_xtal_menu_edit)

		self.ribbon.tb_lens.triggered.connect(self.callback_tb_lens)
		self.ribbon.tb_lens_menu_edit.triggered.connect(self.callback_lens_menu_edit)

		self.ribbon.tb_saw_wave.triggered.connect(self.callback_tb_saw_wave)
		self.ribbon.tb_saw_wave_menu_edit.triggered.connect(self.callback_saw_wave_menu_edit)

		self.ribbon.menu_boundary.triggered.connect(self.callback_boundary_menu_edit)

		self.ribbon.tb_configure.triggered.connect(self.callback_configure)

		#On button depress filters
		self.ribbon.tb_norm_z.triggered.connect(self.callback_filters_update)
		self.ribbon.tb_norm_z.setChecked(self.io.import_config.shape_import_z_norm)

		self.ribbon.tb_blur.triggered.connect(self.callback_filters_update)
		self.ribbon.tb_blur.setChecked(self.io.blur.shape_import_blur_enabled)

		self.ribbon.tb_threshold.triggered.connect(self.callback_filters_update)
		self.ribbon.tb_threshold.setChecked(self.io.threshold.threshold_enabled)

		self.ribbon.tb_boundary.triggered.connect(self.callback_filters_update)
		self.ribbon.tb_boundary.setChecked(self.io.boundary.boundary_enabled)

		self.ribbon.tb_norm_y.triggered.connect(self.callback_norm_y)
		self.ribbon.tb_rotate.triggered.connect(self.callback_rotate)
		self.ribbon.tb_apply.triggered.connect(self.callback_filters_update)

		self.ribbon.import_image.clicked.connect(self.callback_open_image)
		self.ribbon.save_data.clicked.connect(self.callback_import)
		self.ribbon.show_mesh.clicked.connect(self.callback_show_mesh)
		self.ribbon.show_mesh.setChecked(self.io.mesh.mesh_show)

		self.ribbon.tb_script.clicked.connect(self.callback_script)

		self.main_vbox.addWidget(self.ribbon)

		self.notebook = QTabWidget()

		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)

		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


		#3d widget
		self.three_d_shape=glWidget(self)
		self.three_d_shape.enable_views(["plot"])
		self.three_d_shape.draw_electrical_mesh=False
		self.three_d_shape.active_view.draw_device=False
		self.three_d_shape.active_view.draw_rays=False
		self.three_d_shape.active_view.render_fdtd_grid=False
		self.three_d_shape.scene_built=True
		self.three_d_shape.active_view.plot_graph=True
		self.three_d_shape.render_plot=True
		self.three_d_shape.active_view.render_grid=True
		self.three_d_shape.active_view.ray_solid_lines=True
		self.three_d_shape.active_view.render_photons=False
		self.three_d_shape.active_view.optical_mode=False

		display=QWidget()
		layout = QHBoxLayout()
		display.setLayout(layout)
		layout.addWidget(self.three_d_shape)
		layout.addWidget(self.shape_image_flat_view)

		self.notebook.addTab(display,_("Shape"))

		#self.notebook.addTab(self.shape_image_flat_view,_("Image"))

		self.setLayout(self.main_vbox)
		
		self.load_data()
		self.notebook.currentChanged.connect(self.changed_click)
		#self.three_d_shape.force_redraw()

		self.timer=QTimer()
		self.timer.timeout.connect(self.callback_timed_redraw)
		self.timer.start(1000)

	def callback_honeycomb_menu_edit(self):
		self.config_window=class_config_window([self.io.honeycomb],[_("Configure honeycomb")],data=self.io)
		self.config_window.show()

	def callback_xtal_menu_edit(self):
		self.config_window=class_config_window([self.io.xtal],[_("Configure photonic xtal")],data=self.io)
		self.config_window.show()

	def callback_lens_menu_edit(self):
		self.config_window=class_config_window([self.io.lens],[_("Configure photonic lens")],data=self.io)
		self.config_window.show()

	def callback_saw_wave_menu_edit(self):
		self.config_window=class_config_window([self.io.saw_wave],[_("Configure saw wave")],data=self.io)
		self.config_window.show()

	def callback_gaus_menu_edit(self):
		self.config_window=class_config_window([self.io.gauss],[_("Configure gaussian")],data=self.io)
		self.config_window.show()

	def callback_boundary_menu_edit(self):
		self.config_window=class_config_window([self.io.boundary],[_("Configure boundary")],data=self.io)
		self.config_window.show()

	def callback_threshold_menu_edit(self):
		self.config_window=class_config_window([self.io.threshold],[_("Configure threshold")],data=self.io)
		self.config_window.show()

	def callback_configure(self):
		self.config_window=class_config_window([self.io],[_("Configure")],data=self.io)
		self.config_window.show()

	def callback_show_mesh(self):
		self.io.mesh.mesh_show=self.ribbon.show_mesh.isChecked()
		self.shape_image_flat_view.repaint()
		self.io.save()

	def callback_import(self):
		shutil.copyfile( self.orig_image_file,self.image_file)
		im=self.io.load_image()
		f=shape_bildverarbeitung(self.path,self.io)
		f.apply(im)
		self.shape_image_flat_view.force_update()

	def callback_timed_redraw(self):
		self.timer.stop()
		self.three_d_shape.force_redraw()
		
