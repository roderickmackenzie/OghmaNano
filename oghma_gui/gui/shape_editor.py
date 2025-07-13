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
from json_dialog import json_dialog

from shape_image_flat_view import shape_image_flat_view

from config_window import class_config_window
from server import server_get
from cal_path import sim_paths

from gl import glWidget
from shape_editor_io import shape_editor_io

from vec import vec
import shutil
from shape_bildverarbeitung import shape_bildverarbeitung
from ref import ref_window
from json_c import json_c

class shape_editor(QWidgetSavePos):

	def reload(self):
		self.shape_image_flat_view.force_update()
		self.load_data()
		self.three_d_shape.force_redraw()

	def load_data(self):
		path=os.path.join(self.path,"shape.inp")
		self.three_d_shape.scale.set_m2screen()
		self.three_d_shape.gl_graph_load_files([path],scale=True)


	def update(self):
		self.alpha.update()

	def callback_norm_y(self):
		self.io.bin.set_token_value("import_config","shape_import_y_norm",self.ribbon.tb_norm_y.isChecked())
		self.io.save()
		im=self.io.load_image()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)
		self.shape_image_flat_view.force_update()

	def callback_tb_gaus(self):
		im=self.io.draw_gauss()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_tb_honeycomb(self):
		im=self.io.draw_honeycomb()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_tb_xtal(self):
		im=self.io.draw_xtal()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_tb_lens(self):
		im=self.io.draw_lens()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)	
		self.shape_image_flat_view.force_update()

	def callback_tb_saw_wave(self):
		im=self.io.draw_saw_wave()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)
		self.shape_image_flat_view.force_update()

	def callback_rotate(self):
		rotate=self.io.bin.get_token_value("import_config","shape_import_rotate")
		rotate=rotate+90
		if rotate>360:
			rotate=0
		self.io.bin.set_token_value("import_config","shape_import_rotate",rotate)
		self.io.save()
		im=self.io.load_image()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)
		self.shape_image_flat_view.force_update()


	def callback_filters_update(self):
		self.io.bin.set_token_value("blur","shape_import_blur_enabled",self.ribbon.tb_blur.isChecked())
		self.io.bin.set_token_value("threshold","threshold_enabled",self.ribbon.tb_threshold.isChecked())
		self.io.bin.set_token_value("import_config","shape_import_z_norm",self.ribbon.tb_norm_z.isChecked())
		self.io.bin.set_token_value("boundary","boundary_enabled",self.ribbon.tb_boundary.isChecked())
		self.io.save()
		im=self.io.load_image()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)
		self.shape_image_flat_view.force_update()

	def callback_menu_blur(self):
		self.config_window=class_config_window(["blur"],[_("Blur menu")],data=self.io.bin)
		self.config_window.show()

	def callback_mesh_editor(self):
		self.config_window=class_config_window(["mesh"],[_("Configure mesh")],data=self.io.bin)
		self.config_window.show()

	def callback_mesh_build(self):
		self.my_server=server_get()
		self.io.add_job_to_server(sim_paths.get_sim_path(),self.my_server)
		#self.my_server.add_job(sim_paths.get_sim_path(),"--simmode data@mesh_gen --path "+self.path)
		self.my_server.sim_finished.connect(self.reload)
		self.my_server.start()

	def callback_edit_norm_y(self):
		shape_import_y_norm_percent=self.io.bin.get_token_value("import_config","shape_import_y_norm_percent")


		data=json_c("file_defined")
		data.json_py_add_obj_double("", "shape_import_y_norm_percent", shape_import_y_norm_percent)
		data.dump()

		self.a=json_dialog(data,title=_("Normalization editor"),icon="shape")
		ret=self.a.run()

		if ret==QDialog.Accepted:
			shape_import_y_norm_percent=data.get_token_value("","shape_import_y_norm_percent")
			self.io.bin.set_token_value("import_config","shape_import_y_norm_percent",shape_import_y_norm_percent)
			self.io.save()
			im=self.io.load_image()
			f=shape_bildverarbeitung(self.path,self.io.bin)
			f.apply(im)
			self.shape_image_flat_view.force_update()

		data.dump()
		data.free()

	def callback_open_image(self):
		file_name=open_as_filter(self,"png (*.png);;jpg (*.jpg)",path=self.path)
		if file_name!=None:
			im = Image.open(file_name)
			im.save(os.path.join(self.path,"image.png"))				#This is the edited one
			im.save(os.path.join(self.path,"image_original.png"))		#This is the original image
			self.shape_image_flat_view.load_image()
			self.shape_image_flat_view.build_mesh()
			self.callback_filters_update()

	def __init__(self,path):
		QWidgetSavePos.__init__(self,"shape_import")
		self.path=path

		#backward compatibility
		self.orig_image_file=os.path.join(path,"image_original.png")
		self.image_file=os.path.join(path,"image.png")
		if os.path.isfile(self.orig_image_file)==False:
			if os.path.isfile(self.image_file)==True:
				shutil.copyfile(self.image_file, self.orig_image_file)



		self.io=shape_editor_io(self.path)
		self.io.load()
		self.io.loaded=True
		self.io.save()
		#print(">>>",self.path)
		self.shape_image_flat_view=shape_image_flat_view(self.path,self.io)


		self.setMinimumSize(900, 900)
		self.setWindowIcon(icon_get("shape"))

		self.setWindowTitle2(os.path.basename(self.path)+" "+_("Shape editor")) 

		self.main_vbox = QVBoxLayout()

		self.ribbon=ribbon_shape_import()
		shape_import_y_norm=self.io.bin.get_token_value("import_config","shape_import_y_norm")
		self.ribbon.tb_norm_y.setChecked(shape_import_y_norm)



		self.ribbon.menu_threshold.triggered.connect(self.callback_threshold_menu_edit)

		self.ribbon.mesh_edit.triggered.connect(self.callback_mesh_editor)
		self.ribbon.mesh_build.clicked.connect(self.callback_mesh_build)
		self.ribbon.tb_ref.triggered.connect(self.callback_ref)
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
		shape_import_z_norm=self.io.bin.get_token_value("import_config","shape_import_z_norm")
		self.ribbon.tb_norm_z.setChecked(shape_import_z_norm)

		self.ribbon.tb_blur.triggered.connect(self.callback_filters_update)
		shape_import_blur_enabled=self.io.bin.get_token_value("blur","shape_import_blur_enabled")
		self.ribbon.tb_blur.setChecked(shape_import_blur_enabled)

		self.ribbon.tb_threshold.triggered.connect(self.callback_filters_update)
		threshold_enabled=self.io.bin.get_token_value("threshold","threshold_enabled")
		self.ribbon.tb_threshold.setChecked(threshold_enabled)

		self.ribbon.tb_boundary.triggered.connect(self.callback_filters_update)
		boundary_enabled=self.io.bin.get_token_value("boundary","boundary_enabled")
		self.ribbon.tb_boundary.setChecked(boundary_enabled)

		self.ribbon.tb_norm_y.triggered.connect(self.callback_norm_y)
		self.ribbon.tb_rotate.triggered.connect(self.callback_rotate)
		self.ribbon.tb_apply.triggered.connect(self.callback_filters_update)

		self.ribbon.import_image.clicked.connect(self.callback_open_image)
		self.ribbon.save_data.clicked.connect(self.callback_import)
		self.ribbon.show_mesh.clicked.connect(self.callback_show_mesh)

		mesh_show=self.io.bin.get_token_value("mesh","mesh_show")
		self.ribbon.show_mesh.setChecked(mesh_show)

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

		display=QWidget()
		layout = QHBoxLayout()
		display.setLayout(layout)
		layout.addWidget(self.three_d_shape)
		layout.addWidget(self.shape_image_flat_view)

		self.notebook.addTab(display,_("Shape"))

		#self.notebook.addTab(self.shape_image_flat_view,_("Image"))

		self.setLayout(self.main_vbox)
		
		self.load_data()
		#self.three_d_shape.force_redraw()

		self.timer=QTimer()
		self.timer.timeout.connect(self.callback_timed_redraw)
		self.timer.start(20)

	def callback_honeycomb_menu_edit(self):
		self.config_window=class_config_window(["honeycomb"],[_("Configure honeycomb")],data=self.io.bin)
		self.config_window.show()

	def callback_xtal_menu_edit(self):
		self.config_window=class_config_window(["xtal"],[_("Configure photonic xtal")],data=self.io.bin)
		self.config_window.show()

	def callback_lens_menu_edit(self):
		self.config_window=class_config_window(["lens"],[_("Configure photonic lens")],data=self.io.bin)
		self.config_window.show()

	def callback_saw_wave_menu_edit(self):
		self.config_window=class_config_window(["saw_wave"],[_("Configure saw wave")],data=self.io.bin)
		self.config_window.show()

	def callback_gaus_menu_edit(self):
		self.config_window=class_config_window(["gauss"],[_("Configure gaussian")],data=self.io.bin)
		self.config_window.show()

	def callback_boundary_menu_edit(self):
		self.config_window=class_config_window(["boundary"],[_("Configure boundary")],data=self.io.bin)
		self.config_window.show()

	def callback_threshold_menu_edit(self):
		self.config_window=class_config_window(["threshold"],[_("Configure threshold")],data=self.io.bin)
		self.config_window.show()

	def callback_configure(self):
		self.config_window=class_config_window([""],[_("Configure")],data=self.io.bin)
		self.config_window.show()

	def callback_show_mesh(self):
		self.io.bin.set_token_value("mesh","mesh_show",self.ribbon.show_mesh.isChecked())
		self.shape_image_flat_view.repaint()
		self.io.save()

	def callback_import(self):
		shutil.copyfile( self.orig_image_file,self.image_file)
		im=self.io.load_image()
		f=shape_bildverarbeitung(self.path,self.io.bin)
		f.apply(im)
		self.shape_image_flat_view.force_update()

	def callback_timed_redraw(self):
		self.timer.stop()
		self.three_d_shape.force_redraw()
		
	def callback_ref(self):
		self.ref_window=ref_window(os.path.join(self.path,"shape.bib"),"image")
		self.ref_window.show()

