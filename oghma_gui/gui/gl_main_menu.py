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
from json_root import json_root
from icon_lib import icon_get

import json

class gl_main_menu():
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

		self.menu_view_draw_electrical_mesh=view.addAction(_("Electrical mesh"))
		self.menu_view_draw_electrical_mesh.triggered.connect(self.menu_toggle_view)
		self.menu_view_draw_electrical_mesh.setCheckable(True)

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

		action=edit.addAction(_("Background color"))
		action.triggered.connect(self.menu_background_color)

		objects=self.main_menu.addMenu(_("Objects"))
		action=objects.addAction(icon_get("list-add"),_("New free object"))
		action.triggered.connect(self.callback_add_object)

		action=objects.addAction(icon_get("lighthouse"),_("New light source"))
		action.triggered.connect(self.callback_add_light_source)

		action=objects.addAction(icon_get("ccd"),_("New detector"))
		action.triggered.connect(self.callback_add_object)

		action=objects.addAction(icon_get("edit-paste"),_("Paste"))
		action.triggered.connect(self.callback_paste_object)

		action=objects.addAction(icon_get("view-refresh"),_("Rescale"))
		action.triggered.connect(self.callback_rescale)

		action=objects.addAction(icon_get("view-refresh"),_("Debug"))
		action.triggered.connect(self.callback_debug)

		self.main_menu.addSeparator()

		action=self.main_menu.addAction(icon_get("edit-copy"),_("Copy image"))
		action.triggered.connect(self.callback_copy)

	def callback_debug(self):
		self.load_from_json(os.path.join(sim_paths.get_sim_path(),"electrical_mesh.dat"),dz=-0.012)
		self.force_redraw()
		self.do_draw()

	def callback_rescale(self):
		self.scale.set_m2screen()
		self.build_scene()

	def callback_add_object(self):
		self.gl_add_object_to_world()

	def callback_add_light_source(self):
		from json_light_sources import json_light_source
		a=json_light_source()
		
		max_dist_x=10
		max_dist_z=10
		max_dist_y=10

		a.dy=self.scale.world_delta.y*0.2
		a.dx=self.scale.world_delta.x*0.2
		a.dz=self.scale.world_delta.z*0.2

		a.name="Light"
		a.segments=[]
		a.color_r=1.0
		a.color_g=0
		a.color_b=0
		a.color_alpha=0.5
		a.moveable=True
		a.light_illuminate_from="xyz"
		json_root().optical.light_sources.lights.segments.append(a)
		json_root().save()
		self.force_redraw()

	def callback_paste_object(self):
		from shape import shape
		cb = QApplication.clipboard()
		text=cb.text()
		json_data=json.loads(text)
		for n in range(0,json_data['segments']):
			a=shape()
			a.decode_from_json(json_data["segment"+str(n)])
			a.load_triangles()
			a.x0=a.x0+a.dx
			#a.y0=a.y0+a.dy
			#a.z0=a.z0+a.dz

			a.id=a.random_id()
			
			json_root().world.world_data.segments.append(a)

		json_root().save()
		self.force_redraw()

	def menu(self,event):
		self.main_menu.exec_(event.globalPos())

	def callback_copy(self):
		self.render()
		QApplication.clipboard().setImage(self.grabFrameBuffer())

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
			self.active_view.color_r=col.red()/255
			self.active_view.color_g=col.green()/255
			self.active_view.color_b=col.blue()/255
			self.force_redraw()

			json_root().save()

	def menu_toggle_view(self):
		action = self.sender()
		text=action.text()
		self.draw_electrical_mesh=self.menu_view_draw_electrical_mesh.isChecked()
		self.active_view.render_photons=self.menu_view_render_photons.isChecked()
		self.active_view.render_grid=self.menu_view_grid.isChecked()
		self.active_view.render_fdtd_grid=self.menu_view_fdtd_grid.isChecked()
		self.active_view.render_cords=self.menu_view_cords.isChecked()
		self.active_view.draw_device=self.menu_view_draw_device.isChecked()
		self.active_view.optical_mode=self.menu_view_optical_mode.isChecked()
		self.active_view.text=self.menu_view_text.isChecked()
		self.active_view.dimensions=self.menu_view_dimensions.isChecked()
		self.active_view.render_plot=self.menu_view_plot.isChecked()
		self.active_view.transparent_objects=self.menu_view_transparent_objects.isChecked()
		self.active_view.render_light_sources=self.menu_view_light_source.isChecked()
		self.active_view.draw_rays=self.menu_view_draw_rays.isChecked()
		self.active_view.ray_solid_lines=self.menu_view_ray_solid_lines.isChecked()
		self.active_view.show_world_box=self.menu_show_world_box.isChecked()
		self.active_view.show_detectors=self.menu_show_detectors.isChecked()
		self.active_view.enable_view_move=not self.menu_lock_view.isChecked()
		self.active_view.show_gl_lights=self.menu_show_gl_lights.isChecked()
		self.active_view.show_buttons=self.menu_show_buttons.isChecked()
		self.active_view.stars=self.menu_stars.isChecked()

		if text==_("Ray tracing mesh"):
			self.active_view.draw_rays= not self.active_view.draw_rays
		if text==_("Device view"):
			self.enable_draw_device = not self.enable_draw_device
		if text==_("Font"):
			diag=QFontDialog()
			font, ok = QFontDialog.getFont(self.font)
			if ok:
				self.font = font

		self.force_redraw()
		json_root().save()

	def menu_update(self):
		self.menu_view_draw_electrical_mesh.setChecked(self.draw_electrical_mesh)
		self.menu_view_render_photons.setChecked(self.active_view.render_photons)
		self.menu_view_grid.setChecked(self.active_view.render_grid)
		self.menu_view_fdtd_grid.setChecked(self.active_view.render_fdtd_grid)
		self.menu_view_cords.setChecked(self.active_view.render_cords)
		self.menu_view_draw_device.setChecked(self.active_view.draw_device)
		self.menu_view_optical_mode.setChecked(self.active_view.optical_mode)
		self.menu_view_text.setChecked(self.active_view.text)
		self.menu_view_dimensions.setChecked(self.active_view.dimensions)		
		self.menu_view_plot.setChecked(self.active_view.render_plot)
		self.menu_view_transparent_objects.setChecked(self.active_view.transparent_objects)
		self.menu_view_light_source.setChecked(self.active_view.render_light_sources)
		self.menu_view_draw_rays.setChecked(self.active_view.draw_rays)
		self.menu_view_ray_solid_lines.setChecked(self.active_view.ray_solid_lines)
		self.menu_show_world_box.setChecked(self.active_view.show_world_box)
		self.menu_show_detectors.setChecked(self.active_view.show_detectors)
		self.menu_lock_view.setChecked(not self.active_view.enable_view_move)
		self.menu_show_gl_lights.setChecked(self.active_view.show_gl_lights)
		self.menu_show_buttons.setChecked(self.active_view.show_buttons)
		self.menu_stars.setChecked(self.active_view.stars)


