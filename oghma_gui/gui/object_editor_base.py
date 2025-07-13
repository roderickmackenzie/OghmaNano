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
from gui_util import  yes_no_dlg
from icon_lib import icon_get
from dlg_get_text2 import dlg_get_text2
from cal_path import sim_paths
from bytes2str import str2bytes
from bytes2str import bytes2str
import ctypes
from json_c import json_tree_c

class object_editor_base():

	def add_new_shape_to_object(self,uid):
		json_path=self.bin.find_path_by_uid("",uid)
		#print(json_path)
		if json_path!=None:
			dz=self.bin.get_token_value(json_path,"dz")
			dx=self.bin.get_token_value(json_path,"dx")
			dy=self.bin.get_token_value(json_path,"dy")
			path_of_new_segment=self.bin.make_new_segment(json_path,"",-1)
			self.bin.set_token_value(path_of_new_segment,"dz",dz/2.0)
			self.bin.set_token_value(path_of_new_segment,"dx",dx/2.0)
			self.bin.set_token_value(path_of_new_segment,"dy",dy/2.0)
			self.bin.set_token_value(path_of_new_segment,"moveable",True)
			self.bin.save()
			self.force_redraw(level="reload_rebuild")
			return path_of_new_segment

	def rename_object(self,uid):
		json_path=self.bin.find_path_by_uid("",uid)
		if json_path!=None:
			old_name=self.bin.get_token_value(json_path,"name")
			name=dlg_get_text2( _("Rename the object:"), old_name,"rename.png")
			name=name.ret

			if name!=None:
				self.bin.set_token_value(json_path,"name",name)
				self.bin.save()
				self.force_redraw() 
				return name
		return None

	def delete_object(self,in_ids):
		if len(in_ids)>0:
			question="Do you really want to delete the objects: \n"
			ids=[]
			for my_id in in_ids:
				json_path=self.bin.find_path_by_uid("",my_id)
				if json_path!=None:
					name=self.bin.get_token_value(json_path,"name")
					if my_id not in ids:
						ids.append(my_id)
						question=question+name+"\n"
			response=yes_no_dlg(self,question)
			if response == True:
				for my_id in ids:
					json_path=self.bin.find_path_by_uid("",my_id)
					path, seg = json_path.rsplit('.', 1)
					self.bin.delete_segment(path,seg)
				self.bin.save()
				self.force_redraw(level="reload_rebuild")

	def clone_object(self,uid):
		segment_path=self.bin.find_path_by_uid("",uid)
		root_path,segment=segment_path.rsplit(".",1)
		name=self.bin.get_token_value(segment_path,"name")

		new_sim_name=dlg_get_text2( "Clone the object:", name,"clone.png")
		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:
			new_path=self.bin.clone_segment(root_path,segment,new_sim_name)

			x0=self.bin.get_token_value(new_path, "x0")
			dx=self.bin.get_token_value(new_path, "dx")
			self.bin.set_token_value(new_path,"x0",x0+dx)

			self.bin.save()
			self.force_redraw(level="reload_rebuild")
			return new_path

		return False

	def callback_add_shape_to_object(self):
		obj=self.gl_objects_get_first_selected()
		if obj!=None:
			self.add_new_shape_to_object(obj.id)

	def gl_add_object_to_world(self,path=None):
		self.bin.lib.gl_make_new_shape_in_world(ctypes.byref(json_tree_c()), ctypes.byref(self.gl_main),ctypes.byref(sim_paths))
		self.force_redraw()
		self.bin.save()

	def callback_add_light_source(self):
		self.bin.lib.gl_make_new_light_soruce_in_world(ctypes.byref(json_tree_c()), ctypes.byref(self.gl_main),ctypes.byref(sim_paths))
		self.force_redraw()
		self.bin.save()

	def gl_add_detector_to_world(self):
		self.bin.lib.gl_make_new_detector_in_world(ctypes.byref(json_tree_c()), ctypes.byref(self.gl_main),ctypes.byref(sim_paths))
		self.force_redraw()
		self.bin.save()


