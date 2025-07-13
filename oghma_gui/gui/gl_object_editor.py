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
from PySide2.QtWidgets import QMenu,QApplication, QShortcut
from PySide2.QtGui import QKeySequence
from object_editor import object_editor
from gui_util import  yes_no_dlg
from icon_lib import icon_get
from dlg_get_text2 import dlg_get_text2
from cal_path import sim_paths
from bytes2str import str2bytes
from cal_path import subtract_paths
from bytes2str import bytes2str
import ctypes
from json_c import json_tree_c
from object_editor import object_editor

class gl_object_editor():

	def __init__(self):
		shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
		shortcut.activated.connect(self.callback_group)

		shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
		shortcut.activated.connect(self.callback_ungroup)

		shortcut = QShortcut(QKeySequence("Del"), self)
		shortcut.activated.connect(self.callback_delete)

		shortcut = QShortcut(QKeySequence("Backspace"), self)
		shortcut.activated.connect(self.callback_delete)
		self.bin=json_tree_c()

	def menu_obj(self,event,uid):
		json_path=self.bin.find_path_by_uid("",uid)
		if json_path==None:
			return

		view_menu = QMenu(self)

		menu = QMenu(self)
		is_epi_layer=False
		if json_path.startswith("epitaxy"):
			if json_path.startswith("epitaxy.contacts")==False:
				is_epi_layer=True

		self.is_light_source=False
		self.is_detector=False
		self.is_gl_light=False
		if json_path.startswith("optical.light_sources.lights"):
			self.is_light_source=True

		if json_path.startswith("optical.detectors"):
			self.is_detector=True

		if json_path.startswith("gl.gl_lights"):
			self.is_gl_light=True

		if is_epi_layer==True:
			action=menu.addAction(icon_get("go-up"),_("Move up"))
			action.triggered.connect(self.layer_move_up)

			action=menu.addAction(icon_get("go-down"),_("Move down"))
			action.triggered.connect(self.layer_move_down)

			action=menu.addAction(icon_get("list-add"),_("Add layer"))
			action.triggered.connect(self.layer_add)

			action=menu.addAction(icon_get("list-add"),_("Add object inside"))
			action.triggered.connect(self.callback_add_shape_to_object)

			menu.addSeparator()

		action=menu.addAction(icon_get("list-remove"),_("Delete"))
		action.triggered.connect(self.callback_delete)

		action=menu.addAction(icon_get("rename"),_("Rename"))
		action.triggered.connect(self.callback_rename)

		menu.addSeparator()

		action=menu.addAction(icon_get("edit-copy"),_("Copy json"))
		action.triggered.connect(self.object_copy_json)

		action=menu.addAction(icon_get("edit-paste"),_("Paste"))
		action.triggered.connect(self.object_paste)

		menu.addSeparator()

		action=menu.addAction(_("Edit"))
		action.triggered.connect(self.layer_object_editor)
		n_objs=self.gl_main.get_number_objects_selected(True)

		if n_objs>1:
			group=self.is_selected_group()
			menu.addSeparator()
			action=menu.addAction(icon_get("align_left"),_("Align and distribute"))
			action.triggered.connect(self.callback_align)

			action=menu.addAction(icon_get("mesh_tri"),_("Join mesh"))
			action.triggered.connect(self.callback_join_mesh)

			action=menu.addAction(icon_get("object-group"),_("Group (Ctrl+G)"))
			action.triggered.connect(self.callback_group)

			if group!=False:
				action.setEnabled(False)

			action=menu.addAction(icon_get("object-ungroup"),_("Ungroup (Ctrl+U)"))
			action.triggered.connect(self.callback_ungroup)
			if group==False:
				action.setEnabled(False)


			menu.addSeparator()

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

			show_solid=self.bin.get_token_value(json_path+".display_options","show_solid")
			show_mesh=self.bin.get_token_value(json_path+".display_options","show_mesh")
			show_cut_through_x=self.bin.get_token_value(json_path+".display_options","show_cut_through_x")
			show_cut_through_y=self.bin.get_token_value(json_path+".display_options","show_cut_through_y")
			hidden=self.bin.get_token_value(json_path+".display_options","hidden")

			self.menu_show_solid.setChecked(show_solid)
			self.menu_show_mesh.setChecked(show_mesh)
			self.menu_show_cut_through_x.setChecked(show_cut_through_x)
			self.menu_show_cut_through_y.setChecked(show_cut_through_y)
			self.menu_hidden.setChecked(hidden)

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
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			json_path=self.bin.find_path_by_uid("",obj.id)
			if json_path!=None:
				self.bin.set_token_value(json_path+".display_options","show_solid",self.menu_show_solid.isChecked())
				self.bin.set_token_value(json_path+".display_options","show_mesh",self.menu_show_mesh.isChecked())
				self.bin.set_token_value(json_path+".display_options","show_cut_through_x",self.menu_show_cut_through_x.isChecked())
				self.bin.set_token_value(json_path+".display_options","show_cut_through_y",self.menu_show_cut_through_y.isChecked())
				self.bin.set_token_value(json_path+".display_options","hidden",self.menu_hidden.isChecked())
				self.bin.save()
		self.force_redraw()


	def object_copy_json(self):
		obj=self.gl_objects_get_first_selected()
		
		if obj!=None:
			json_path=self.bin.find_path_by_uid("",obj.id)
			if json_path!=None:
				lines=self.bin.gen_json(json_path)
				lines[0]="\"data\": "+lines[0].split(":")[1]
				all_data=[]
				all_data.append("{")
				all_data.append("\"data_type\": \"\",")

				all_data.extend(lines)
				all_data.append("}")

				cb = QApplication.clipboard()
				cb.clear(mode=cb.Clipboard )
				cb.setText("\n".join(all_data), mode=cb.Clipboard)

	def object_copy_path(self):
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			json_path=self.bin.find_path_by_uid("",obj.id)
			cb = QApplication.clipboard()
			cb.clear(mode=cb.Clipboard )
			cb.setText(json_path, mode=cb.Clipboard)


	def object_paste(self):
		print("not yet implemented")
		return
		cb = QApplication.clipboard()
		text=cb.text()
		json_data=json.loads(text)
		for n in range(0,json_data['segments']):
			print(json_data["segment"+str(n)])

	def layer_add(self):
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			json_path=self.bin.find_path_by_uid("",obj.id)
			if json_path.startswith("epitaxy") and json_path.count("contacts")==0:
				dy=self.bin.get_token_value(json_path,"dy")
				number=int(json_path[len("epitaxy.segment"):])
				path_of_new_segment=self.bin.make_new_segment("epitaxy","",number)
				self.bin.set_token_value(path_of_new_segment,"dy",dy)
				self.bin.save()
				self.force_redraw_hard()

	def layer_move_down(self):
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			json_path=self.bin.find_path_by_uid("",obj.id)
			if json_path.startswith("epitaxy") and json_path.count("contacts")==0:
				number=int(json_path[len("epitaxy.segment"):])
				a,b=self.bin.segments_move_up_down("epitaxy","down",number)
				self.bin.save()
				self.force_redraw()

	def layer_move_up(self):
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			json_path=self.bin.find_path_by_uid("",obj.id)
			if json_path.startswith("epitaxy") and json_path.count("contacts")==0:
				number=int(json_path[len("epitaxy.segment"):])
				a,b=self.bin.segments_move_up_down("epitaxy","up",number)
				self.bin.save()
				self.force_redraw()

	def callback_delete(self):
		objs=self.gl_objects_get_selected()
		ids=[]
		for o in objs:
			ids.append(o.id)

		self.delete_object(ids)

	def callback_rename(self):
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			self.rename_object(obj.id)


	def layer_object_editor(self):
		objs=self.gl_objects_get_selected()

		ids=[]
		for obj in objs:
			if obj.id!=b"selection_box":
				json_path=self.bin.find_path_by_uid("",obj.id)
				if json_path!=None:
					ids.append(bytes2str(obj.id))
					segments=self.bin.get_token_value(json_path,"segments")
					if segments!=None:
						for s in range(0,segments):
							json_sub_path=json_path+".segment"+str(s)
							sub_uid=self.bin.get_token_value(json_sub_path,"id")
							ids.append(sub_uid)

				ids=list(set(ids))

		if ids!=[]:
			self.shape_edit=object_editor(self.force_redraw)
			self.shape_edit.load(ids)
			self.shape_edit.show()

	def is_selected_group(self):
		uid = ctypes.create_string_buffer(100)
		ret=self.bin.lib.gl_objects_selected_is_exact_group(uid,ctypes.byref(json_tree_c()),ctypes.byref(self.gl_main))
		uid = uid.value.decode('utf-8') 
		if ret==-1:
			return False		

		return uid

	def callback_group(self):
		self.bin.lib.gl_group_make_new_group_from_selected(ctypes.byref(json_tree_c()),ctypes.byref(self.gl_main))
		self.bin.save()

	def callback_ungroup(self):
		self.bin.lib.gl_group_ungroup_selected(ctypes.byref(json_tree_c()),ctypes.byref(self.gl_main))
		self.bin.save()

