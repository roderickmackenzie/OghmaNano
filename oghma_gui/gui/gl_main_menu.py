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

## @package gl_main_menu
#  The gl_main_menu class for the OpenGL display.
#

import io
import os
import sys

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	pass


from gQtCore import QTimer, Qt
from cal_path import sim_paths
from PySide2.QtWidgets import QDialog, QFontDialog, QColorDialog, QApplication, QMenu
from open_save_dlg import save_as_filter
from PySide2.QtGui import QImage
from icon_lib import icon_get
from json_c import json_tree_c
import json
from json_c import json_files_gui_config
from json_c import json_string
from bytes2str import str2bytes

class gl_main_menu():

	def __init__(self):
		self.bin=json_tree_c()

	def build_main_menu(self):
		view_menu = QMenu(self)
		

		self.main_menu = QMenu(self)

		export=self.main_menu.addMenu(_("Save as"))

		action=export.addAction(icon_get("image-x-generic"),_("Save as image"))
		action.triggered.connect(self.callback_save_as_image)

		action=export.addAction(icon_get("vector"),_("Save as gobj"))
		action.triggered.connect(self.callback_save_as_gobj)

		view=self.main_menu.addMenu(_("View"))

		optical=view.addMenu(_("Optical"))

		#optical
		self.menu_view_render_photons=optical.addAction(_("Show photons"))
		self.menu_view_render_photons.triggered.connect(self.menu_toggle_view)
		self.menu_view_render_photons.setCheckable(True)

		self.menu_view_fdtd_grid=optical.addAction(_("FDTD grid"))
		self.menu_view_fdtd_grid.triggered.connect(self.menu_toggle_view)
		self.menu_view_fdtd_grid.setCheckable(True)

		self.menu_view_optical_mode=optical.addAction(_("Optical mode"))
		self.menu_view_optical_mode.triggered.connect(self.menu_toggle_view)
		self.menu_view_optical_mode.setCheckable(True)

		self.menu_view_light_source=optical.addAction(_("Light source"))
		self.menu_view_light_source.triggered.connect(self.menu_toggle_view)
		self.menu_view_light_source.setCheckable(True)

		self.menu_view_draw_rays=optical.addAction(_("Rays"))
		self.menu_view_draw_rays.triggered.connect(self.menu_toggle_view)
		self.menu_view_draw_rays.setCheckable(True)

		self.menu_view_ray_solid_lines=optical.addAction(_("Solid rays"))
		self.menu_view_ray_solid_lines.triggered.connect(self.menu_toggle_view)
		self.menu_view_ray_solid_lines.setCheckable(True)


		self.menu_show_detectors=optical.addAction(_("Show detectors"))
		self.menu_show_detectors.triggered.connect(self.menu_toggle_view)
		self.menu_show_detectors.setCheckable(True)
		#end

		self.menu_view_draw_device=view.addAction(_("Show device"))
		self.menu_view_draw_device.triggered.connect(self.menu_toggle_view)
		self.menu_view_draw_device.setCheckable(True)

		self.menu_view_grid=view.addAction(_("Grid"))
		self.menu_view_grid.triggered.connect(self.menu_toggle_view)
		self.menu_view_grid.setCheckable(True)


		self.menu_view_cords=view.addAction(_("Coordinates"))
		self.menu_view_cords.triggered.connect(self.menu_toggle_view)
		self.menu_view_cords.setCheckable(True)


		self.menu_view_text=view.addAction(_("Show text"))
		self.menu_view_text.triggered.connect(self.menu_toggle_view)
		self.menu_view_text.setCheckable(True)

		self.menu_view_dimensions=view.addAction(_("Show Dimensions"))
		self.menu_view_dimensions.triggered.connect(self.menu_toggle_view)
		self.menu_view_dimensions.setCheckable(True)

		self.menu_view_plot=view.addAction(_("Show plot"))
		self.menu_view_plot.triggered.connect(self.menu_toggle_view)
		self.menu_view_plot.setCheckable(True)

		self.menu_view_transparent_objects=view.addAction(_("Transparent objects"))
		self.menu_view_transparent_objects.triggered.connect(self.menu_toggle_view)
		self.menu_view_transparent_objects.setCheckable(True)

		action=view.addAction(_("Ray tracing mesh"))
		action.triggered.connect(self.menu_toggle_view)

		self.menu_show_world_box=view.addAction(_("Show world box"))
		self.menu_show_world_box.triggered.connect(self.menu_toggle_view)
		self.menu_show_world_box.setCheckable(True)

		self.menu_show_electrical_box=view.addAction(_("Show electrical box"))
		self.menu_show_electrical_box.triggered.connect(self.menu_toggle_view)
		self.menu_show_electrical_box.setCheckable(True)

		self.menu_show_thermal_box=view.addAction(_("Show thermal box"))
		self.menu_show_thermal_box.triggered.connect(self.menu_toggle_view)
		self.menu_show_thermal_box.setCheckable(True)

		self.menu_lock_view=view.addAction(_("Lock view"))
		self.menu_lock_view.triggered.connect(self.menu_toggle_view)
		self.menu_lock_view.setCheckable(True)

		self.menu_show_gl_lights=view.addAction(_("Show gl lights"))
		self.menu_show_gl_lights.triggered.connect(self.menu_toggle_view)
		self.menu_show_gl_lights.setCheckable(True)

		self.menu_show_buttons=view.addAction(_("Show buttons"))
		self.menu_show_buttons.triggered.connect(self.menu_toggle_view)
		self.menu_show_buttons.setCheckable(True)

		self.menu_stars=view.addAction(_("Stars"))
		self.menu_stars.triggered.connect(self.menu_toggle_view)
		self.menu_stars.setCheckable(True)


		edit=self.main_menu.addMenu(_("Edit"))

		action=edit.addAction(_("Font"))
		action.triggered.connect(self.menu_toggle_view)

		action=edit.addAction(icon_get("preferences-color"),_("Background color"))
		action.triggered.connect(self.menu_background_color)

		action=edit.addAction(icon_get("preferences-color"),_("Interface background color"))
		action.triggered.connect(self.menu_interface_color)

		action=edit.addAction(icon_get("preferences-color"),_("Interface text color"))
		action.triggered.connect(self.menu_text_color)

		objects=self.main_menu.addMenu(_("Objects"))
		action=objects.addAction(icon_get("list-add"),_("New free object"))
		action.triggered.connect(self.gl_add_object_to_world)

		action=objects.addAction(icon_get("lighthouse"),_("New light source"))
		action.triggered.connect(self.callback_add_light_source)

		action=objects.addAction(icon_get("ccd"),_("New detector"))
		action.triggered.connect(self.gl_add_detector_to_world)

		action=objects.addAction(icon_get("edit-paste"),_("Paste"))
		action.triggered.connect(self.callback_paste_object)

		action=objects.addAction(icon_get("view-refresh"),_("Rescale"))
		action.triggered.connect(self.callback_rescale)

		action=objects.addAction(icon_get("tree"),_("Object tree"))
		action.triggered.connect(self.callback_object_tree)

		#action=objects.addAction(icon_get("view-refresh"),_("Debug"))
		#action.triggered.connect(self.callback_debug)

		copy=self.main_menu.addMenu(_("Copy"))

		action=copy.addAction(icon_get("edit-copy"),_("Copy image"))
		action.triggered.connect(self.callback_copy)

		action=copy.addAction(icon_get("edit-copy"),_("Copy json"))
		action.triggered.connect(self.callback_copy)

		action=copy.addAction(icon_get("edit-paste"),_("Paste json"))
		action.triggered.connect(self.callback_paste_object)


	def callback_object_tree(self):
		from window_json_tree_view import window_json_tree_view
		self.w=window_json_tree_view(title=_("Object tree viewer"))
		self.w.double_click.connect(self.callback_tree_view_object_clicked)
		self.w.object_mode="shapes"
		self.w.english=True
		self.w.show_data_items=True
		self.w.language_mode="python"
		self.w.update()
		self.w.show()

	def callback_tree_view_object_clicked(self):
		print("fixme")
		from object_editor import object_editor
		data=json_root()
		path=get_python_path_from_human_path(data,self.w.path_python[5:])
		try:
			ids=[eval(path+".id")]
		except:
			return
		if ids!=[]:
			self.shape_edit=object_editor(self.force_redraw)
			self.shape_edit.load(ids)
			self.shape_edit.show()

	def callback_rescale(self):
		self.scale.set_m2screen()
		self.build_scene()

	def callback_paste_object(self):
		cb = QApplication.clipboard()
		cb_text=cb.text()

		sender = self.sender()
		text=sender.text()
		
		if text==_("Paste json"):
			text_send=ctypes.c_char_p(str2bytes(cb_text))
			text_len=ctypes.c_int(len(cb_text))
			self.lib.gl_views_from_clip(ctypes.byref(json_files_gui_config), ctypes.byref(self.gl_main) ,text_send,text_len)
			self.force_redraw()
		else:
			json_data=json.loads(cb_text)
			for n in range(0,json_data['segments']):
				a=shape()
				a.decode_from_json(json_data["segment"+str(n)])
				a.load_triangles()
				a.x0=a.x0+a.dx

				a.id=a.random_id()
				
				json_root().world.world_data.segments.append(a)

				self.bin.save()
			self.force_redraw()

	def menu(self,event):
		self.main_menu.exec_(event.globalPos())

	def callback_copy(self):
		sender = self.sender()
		text=sender.text()
		
		if text==_("Copy image"):
			self.render_to_screen()
			QApplication.clipboard().setImage(self.grabFrameBuffer())
		elif text==_("Copy json"):
			a=json_string()
			ret=self.lib.gl_views_to_clip(ctypes.byref(a), ctypes.byref(self.gl_main),ctypes.byref(json_files_gui_config))

			if ret==-1:
				return None
			ret=a.get_data()
			a.free()
			cb = QApplication.clipboard()
			cb.clear(mode=cb.Clipboard )
			cb.setText(ret, mode=cb.Clipboard)

	def callback_save_as_image(self):
		ret=save_as_filter(self,"png (*.png)")
		if ret!=None:
			if ret.endswith("png"):
				self.grabFrameBuffer().save(ret)

	def callback_save_as_gobj(self):
		#ret=save_as_filter(self,"3D object file (*.gobj)")
		#if ret!=None:
		#	if ret.endswith("gojb"):
		pass

	def menu_background_color(self,event):
		col = QColorDialog.getColor(Qt.white, self)
		if col.isValid():
			self.gl_main.active_view.contents.background_color.r=col.red()/255
			self.gl_main.active_view.contents.background_color.g=col.green()/255
			self.gl_main.active_view.contents.background_color.b=col.blue()/255
			self.force_redraw()

			self.lib.gl_save_views(ctypes.byref(json_files_gui_config), ctypes.byref(self.gl_main))

	def menu_interface_color(self,event):
		col = QColorDialog.getColor(Qt.white, self)
		if col.isValid():
			self.bin.set_token_value("gui_config.interface","bk_r",col.red()/255)
			self.bin.set_token_value("gui_config.interface","bk_g",col.green()/255)
			self.bin.set_token_value("gui_config.interface","bk_b",col.blue()/255)
			self.lib.gl_save_views(ctypes.byref(json_files_gui_config), ctypes.byref(self.gl_main))

	def menu_text_color(self,event):
		col = QColorDialog.getColor(Qt.white, self)
		if col.isValid():
			self.bin.set_token_value("gui_config.interface","col_text_r",col.red()/255)
			self.bin.set_token_value("gui_config.interface","col_text_g",col.green()/255)
			self.bin.set_token_value("gui_config.interface","col_text_b",col.blue()/255)
			self.lib.gl_save_views(ctypes.byref(json_files_gui_config), ctypes.byref(self.gl_main))

	def menu_toggle_view(self):
		action = self.sender()
		text=action.text()
		self.gl_main.active_view.contents.render_photons=self.menu_view_render_photons.isChecked()
		self.gl_main.active_view.contents.render_grid=self.menu_view_grid.isChecked()
		self.gl_main.active_view.contents.render_fdtd_grid=self.menu_view_fdtd_grid.isChecked()
		self.gl_main.active_view.contents.render_cords=self.menu_view_cords.isChecked()
		self.gl_main.active_view.contents.draw_device=self.menu_view_draw_device.isChecked()
		self.gl_main.active_view.contents.optical_mode=self.menu_view_optical_mode.isChecked()
		self.gl_main.active_view.contents.text=self.menu_view_text.isChecked()
		self.gl_main.active_view.contents.dimensions=self.menu_view_dimensions.isChecked()
		self.gl_main.active_view.contents.render_plot=self.menu_view_plot.isChecked()
		self.gl_main.active_view.contents.transparent_objects=self.menu_view_transparent_objects.isChecked()
		self.gl_main.active_view.contents.render_light_sources=self.menu_view_light_source.isChecked()
		self.gl_main.active_view.contents.draw_rays=self.menu_view_draw_rays.isChecked()
		self.gl_main.active_view.contents.ray_solid_lines=self.menu_view_ray_solid_lines.isChecked()
		self.gl_main.active_view.contents.show_world_box=self.menu_show_world_box.isChecked()
		self.gl_main.active_view.contents.show_electrical_box=self.menu_show_electrical_box.isChecked()
		self.gl_main.active_view.contents.show_thermal_box=self.menu_show_thermal_box.isChecked()
		self.gl_main.active_view.contents.show_detectors=self.menu_show_detectors.isChecked()
		self.gl_main.active_view.contents.enable_view_move=not self.menu_lock_view.isChecked()
		self.gl_main.active_view.contents.show_gl_lights=self.menu_show_gl_lights.isChecked()
		self.gl_main.active_view.contents.show_buttons=self.menu_show_buttons.isChecked()
		self.gl_main.active_view.contents.stars=self.menu_stars.isChecked()

		if text==_("Ray tracing mesh"):
			self.gl_main.active_view.contents.draw_rays= not self.gl_main.active_view.contents.draw_rays
		if text==_("Device view"):
			self.enable_draw_device = not self.enable_draw_device
		if text==_("Font"):
			diag=QFontDialog()
			font, ok = QFontDialog.getFont(self.font)
			if ok:
				self.font = font

		self.force_redraw()

		self.lib.gl_save_views(ctypes.byref(json_files_gui_config), ctypes.byref(self.gl_main))

	def menu_update(self):
		self.menu_view_render_photons.setChecked(self.gl_main.active_view.contents.render_photons)
		self.menu_view_grid.setChecked(self.gl_main.active_view.contents.render_grid)
		self.menu_view_fdtd_grid.setChecked(self.gl_main.active_view.contents.render_fdtd_grid)
		self.menu_view_cords.setChecked(self.gl_main.active_view.contents.render_cords)
		self.menu_view_draw_device.setChecked(self.gl_main.active_view.contents.draw_device)
		self.menu_view_optical_mode.setChecked(self.gl_main.active_view.contents.optical_mode)
		self.menu_view_text.setChecked(self.gl_main.active_view.contents.text)
		self.menu_view_dimensions.setChecked(self.gl_main.active_view.contents.dimensions)		
		self.menu_view_plot.setChecked(self.gl_main.active_view.contents.render_plot)
		self.menu_view_transparent_objects.setChecked(self.gl_main.active_view.contents.transparent_objects)
		self.menu_view_light_source.setChecked(self.gl_main.active_view.contents.render_light_sources)
		self.menu_view_draw_rays.setChecked(self.gl_main.active_view.contents.draw_rays)
		self.menu_view_ray_solid_lines.setChecked(self.gl_main.active_view.contents.ray_solid_lines)
		self.menu_show_world_box.setChecked(self.gl_main.active_view.contents.show_world_box)
		self.menu_show_electrical_box.setChecked(self.gl_main.active_view.contents.show_electrical_box)
		self.menu_show_thermal_box.setChecked(self.gl_main.active_view.contents.show_thermal_box)
		self.menu_show_detectors.setChecked(self.gl_main.active_view.contents.show_detectors)
		self.menu_lock_view.setChecked(not self.gl_main.active_view.contents.enable_view_move)
		self.menu_show_gl_lights.setChecked(self.gl_main.active_view.contents.show_gl_lights)
		self.menu_show_buttons.setChecked(self.gl_main.active_view.contents.show_buttons)
		self.menu_stars.setChecked(self.gl_main.active_view.contents.stars)



