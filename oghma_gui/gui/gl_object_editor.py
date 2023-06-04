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

## @package gl_object_editor
#  An OpenGL object editor.
#

import os
import json
from PySide2.QtWidgets import QMenu,QApplication
from object_editor import object_editor
from epitaxy import get_epi
from epitaxy_class import epi_layer
from gui_util import  yes_no_dlg
from icon_lib import icon_get
from shape import shape
from dlg_get_text2 import dlg_get_text2
from json_contacts import contact
from json_root import json_root
from json_base import json_base
from json_light_sources import json_light_source
from json_detectors import json_detector
from json_gl_lights import json_gl_light
from cal_path import sim_paths
from bytes2str import str2bytes
from cal_path import subtract_paths
from bytes2str import bytes2str

import ctypes

class gl_object_editor():

	def menu_obj(self,event,obj):
		view_menu = QMenu(self)

		menu = QMenu(self)
		
		is_epi_layer=False
		if obj in json_root().epi.layers:
			is_epi_layer=True

		self.is_light_source=False
		self.is_detector=False
		self.is_gl_light=False
		if obj in json_root().optical.light_sources.lights.segments:
			self.is_light_source=True

		if obj in json_root().optical.detectors.segments:
			self.is_detector=True

		if obj in json_root().gl.gl_lights.segments:
			self.is_gl_light=True

		if is_epi_layer==True:
			action=menu.addAction(icon_get("go-up"),_("Move up"))
			action.triggered.connect(self.layer_move_up)

			action=menu.addAction(icon_get("go-down"),_("Move down"))
			action.triggered.connect(self.layer_move_down)

			action=menu.addAction(icon_get("list-add"),_("Add layer"))
			action.triggered.connect(self.layer_add)

			action=menu.addAction(icon_get("list-add"),_("Add object inside"))
			action.triggered.connect(self.add_shape_to_object)

			menu.addSeparator()

		action=menu.addAction(icon_get("list-remove"),_("Delete"))
		action.triggered.connect(self.layer_delete)

		action=menu.addAction(icon_get("rename"),_("Rename"))
		action.triggered.connect(self.layer_rename)

		menu.addSeparator()

		action=menu.addAction(icon_get("edit-copy"),_("Copy json"))
		action.triggered.connect(self.object_copy_json)

		action=menu.addAction(icon_get("edit-paste"),_("Paste"))
		action.triggered.connect(self.object_paste)

		menu.addSeparator()

		action=menu.addAction(_("Edit"))
		action.triggered.connect(self.layer_object_editor)

		objs=self.gl_objects_get_selected()
		if len(objs)>1:
			action=menu.addAction(icon_get("align_left"),_("Align and distribute"))
			action.triggered.connect(self.callback_align)

		if len(objs)>1:
			action=menu.addAction(icon_get("mesh_tri"),_("Join mesh"))
			action.triggered.connect(self.callback_join_mesh)

		script=menu.addMenu(_("Script"))
		action=script.addAction(icon_get("edit-copy"),_("Copy path (Python)"))
		action.triggered.connect(self.object_copy_path)

		if self.is_light_source==False and self.is_detector==False and self.is_gl_light==False:
			view=menu.addMenu(_("View"))

			self.menu_show_solid=view.addAction(_("Show solid"))
			self.menu_show_solid.triggered.connect(self.menu_toggle_object_view)
			self.menu_show_solid.setCheckable(True)

			self.menu_show_mesh=view.addAction(_("Show mesh"))
			self.menu_show_mesh.triggered.connect(self.menu_toggle_object_view)
			self.menu_show_mesh.setCheckable(True)

			self.menu_show_cut_through_x=view.addAction(_("Show cut through x"))
			self.menu_show_cut_through_x.triggered.connect(self.menu_toggle_object_view)
			self.menu_show_cut_through_x.setCheckable(True)

			self.menu_show_cut_through_y=view.addAction(_("Show cut through y"))
			self.menu_show_cut_through_y.triggered.connect(self.menu_toggle_object_view)
			self.menu_show_cut_through_y.setCheckable(True)

			self.menu_hidden=view.addAction(_("Hidden"))
			self.menu_hidden.triggered.connect(self.menu_toggle_object_view)
			self.menu_hidden.setCheckable(True)

			self.menu_show_solid.setChecked(obj.display_options.show_solid)
			self.menu_show_mesh.setChecked(obj.display_options.show_mesh)
			self.menu_show_cut_through_x.setChecked(obj.display_options.show_cut_through_x)
			self.menu_show_cut_through_y.setChecked(obj.display_options.show_cut_through_y)
			self.menu_hidden.setChecked(obj.display_options.hidden)

		menu.exec_(event.globalPos())

	def callback_align(self):
		from align_and_distribute import align_and_distribute
		self.a=align_and_distribute(self)
		self.a.show()

	def callback_join_mesh(self):
		data=json_root()
		objs=self.gl_objects_get_selected()
		i=0
			
		shape_type0=""
		shape_type1=""

		for obj in objs:
			if obj.id!=b"selection_box":
				s=data.find_thing_by_id(obj.id)
				if s!=None:
					if i==0:
						shape_type0=s.shape_type
						in_file0=str2bytes(os.path.join(sim_paths.get_shape_path(),s.shape_type,"shape.inp"))
					elif i==1:
						shape_type1=s.shape_type
						in_file1=str2bytes(os.path.join(sim_paths.get_shape_path(),s.shape_type,"shape.inp"))
					i=i+1

		from shape_editor_io import shape_editor_io
		a=shape_editor_io()
		ret_data=a.merge_shapes(sim_paths.get_shape_path(),info=[[_("New shape name"),_("New shape name")],[shape_type0+" fraction",str(1.0)],[shape_type1+" fraction",str(1.0)]])

		if ret_data!=None:
			new_shape_path=ret_data[0]
			out_file=str2bytes(os.path.join(new_shape_path,"shape.inp"))
			#print(out_file,in_file0,in_file1)
			self.lib.triangles_join(None,ctypes.c_char_p(out_file),ctypes.c_char_p(in_file0),ctypes.c_char_p(in_file1),ctypes.c_double(float(ret_data[1])),ctypes.c_double(float(ret_data[2])))
			delta_path=subtract_paths(sim_paths.get_shape_path(),new_shape_path)
			#print("DELTA:",delta_path)
			self.gl_add_object_to_world(path=delta_path)

	def menu_toggle_object_view(self):
		data=json_root()

		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			s=data.find_thing_by_id(obj.id)
			if s!=None:
				s.display_options.show_solid=self.menu_show_solid.isChecked()
				s.display_options.show_mesh=self.menu_show_mesh.isChecked()
				s.display_options.show_cut_through_x=self.menu_show_cut_through_x.isChecked()
				s.display_options.show_cut_through_y=self.menu_show_cut_through_y.isChecked()
				s.display_options.hidden=self.menu_hidden.isChecked()
				data.save()
		self.force_redraw()



	def object_copy_json(self):
		data=json_root()
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			epi=get_epi()
			s=data.find_thing_by_id(obj.id)

			b=json_base("",segment_class=True)

			b.segments.append(s)
			#print(s.gen_json())
			cb = QApplication.clipboard()
			cb.clear(mode=cb.Clipboard )
			cb.setText("\n".join(b.gen_json())[3:], mode=cb.Clipboard)

	def object_copy_path(self):
		data=json_root()
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			obj,path=data.find_object_path_by_id(obj.id)
			cb = QApplication.clipboard()
			cb.clear(mode=cb.Clipboard )
			cb.setText(path, mode=cb.Clipboard)


	def object_paste(self):
		cb = QApplication.clipboard()
		text=cb.text()
		json_data=json.loads(text)
		for n in range(0,json_data['segments']):
			print(json_data["segment"+str(n)])

	def layer_add(self):
		data=json_root()
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			s=json_root().find_thing_by_id(obj.id)
			if type(s)==epi_layer or type(s)==shape:
				epi=get_epi()
				layer_index=epi.find_layer_by_id(bytes2str(obj.id))
				a=epi.add_new_layer(pos=layer_index)
				data.save()
				self.force_redraw_hard()

	def add_shape_to_object(self):
		data=json_root()
		gl_obj=self.gl_objects_get_first_selected()
		if gl_obj!=None:
			obj=json_root().find_thing_by_id(gl_obj.id)
			if obj!=None:
				s=shape()
				s.dx=obj.dx/2.0
				s.dy=obj.dy/2.0
				s.dz=obj.dz/2.0
				s.moveable=True
				obj.segments.append(s)
				data.save()
				self.force_redraw(level="reload_rebuild")

	def layer_move_down(self):
		data=json_root()
		gl_obj=self.gl_objects_get_first_selected()
		if gl_obj!=None:
			obj=json_root().find_thing_by_id(gl_obj.id)
			if obj in json_root().epi.layers:
				pos=json_root().epi.layers.index(obj)
				epi=get_epi()
				epi.move_down(pos)
				data.save()
				self.force_redraw() 

	def layer_move_up(self):
		data=json_root()
		gl_obj=self.gl_objects_get_first_selected()
		if gl_obj!=None:
			obj=json_root().find_thing_by_id(gl_obj.id)
			if obj in json_root().epi.layers:
				pos=json_root().epi.layers.index(obj)
				epi=get_epi()
				epi.move_up(pos)
				data.save()
				self.force_redraw() 

	def layer_delete(self):
		data=json_root()

		objs=self.gl_objects_get_selected()
		if len(objs)>0:
			question="Do you really want to delete the objects: \n"
			ids=[]
			for obj in objs:
				s=data.find_thing_by_id(obj.id)
				if s!=None:
					ids.append(s.id)
					question=question+s.name+"\n"
			response=yes_no_dlg(self,question)
			if response == True:
				for my_id in ids:
					data.pop_object_by_id(my_id)
				data.save()
				self.force_redraw_hard()

	def layer_rename(self):
		data=json_root()
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			s=data.find_thing_by_id(obj.id)
			if s!=None:
				old_name=s.name
				name=dlg_get_text2( _("Rename the layer:"), old_name,"rename.png")
				name=name.ret

				if name!=None:
					s.name=name
					data.save()

			self.force_redraw() 

	def layer_object_editor(self):
		epi=get_epi()
		data=json_root()
		objs=self.gl_objects_get_selected()
		ids=[]
		for obj in objs:
			s=data.find_thing_by_id(obj.id)
			if type(s)==json_light_source:
				ids.append(obj.id)
			if type(s)==json_detector:
				ids.append(obj.id)
			if type(s)==json_gl_light:
				for light in json_root().gl.gl_lights.segments:
					ids.append(light.id)
			if type(s)==shape or type(s)==contact or type(s)==epi_layer:
				ids.append(obj.id)
				sub_shapes=epi.get_all_sub_shapes(obj.id)

				for sub in sub_shapes:
					if sub.id not in ids:
						ids.append(sub.id)
		#print(ids)
		if ids!=[]:
			self.shape_edit=object_editor(self.force_redraw)
			self.shape_edit.load(ids)
			self.shape_edit.show()

	def gl_add_object_to_world(self,path=None):
		a=shape()
				
		max_dist_x=10
		max_dist_z=10
		max_dist_y=10

		a.dy=self.scale.world_delta.y*0.2
		a.dx=self.scale.world_delta.x*0.2
		a.dz=self.scale.world_delta.z*0.2

		a.name="object"
		a.segments=[]
		a.color_r=1.0
		a.color_g=0
		a.color_b=0
		a.color_alpha=0.5
		a.moveable=True
		if path!=None:
			a.shape_type=path
		a.load_triangles()
		json_root().world.world_data.segments.append(a)
		self.force_redraw()


