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

## @package dir_viewer_new
#  Make new files/directories
#


import os

#qt
from PySide2.QtGui import QIcon, QPixmap
from gQtCore import QSize, Qt, QTimer, gSignal
from PySide2.QtWidgets import QMenu,QAbstractItemView,QListWidgetItem,QPushButton,QListView,QWidget,QListWidget,QAction,QDialog
from dlg_get_text2 import dlg_get_text2
from cal_path import sim_paths
from clone_materials import clone_material
from json_c import json_c
from error_dlg import error_dlg

class dir_viewer_new():
	def new_shape(self):
		from shape_editor_io import shape_editor_io
		a=shape_editor_io(None)
		a.new_shape(self.path)
		self.fill_store()

	def new_morphology(self):
		from morphology_editor_io import morphology_editor_io
		a=morphology_editor_io(None)
		a.new_morphology(self.path)
		self.fill_store()

	def new_emission(self):
		new_sim_name=dlg_get_text2( _("New emission spectra name:"), _("New emission spectra name"),"add_emission")
		new_sim_name=new_sim_name.ret
		if new_sim_name!=None:
			new_emission=os.path.join(self.path,new_sim_name)
			ret=clone_material(new_emission,os.path.join(sim_paths.get_base_emission_path(),"Irppy3"))
			if ret==False:
				error_dlg(self,_("I cant write to:")+new_emission+" "+_("This means either the disk is full or your system administrator has not given you write permissions to that location."))

			from json_emission_db_item import json_emission_db_item
			a=json_emission_db_item()
			a.save_as(os.path.join(new_emission,"data.json"))

			self.fill_store()

	def new_spectra(self):
		new_sim_name=dlg_get_text2( _("New spectra name:"), _("New spectra name"),"add_spectra")
		new_sim_name=new_sim_name.ret
		if new_sim_name!=None:
			new_spectra=os.path.join(self.path,new_sim_name)
			ret=clone_material(new_spectra,os.path.join(sim_paths.get_base_spectra_path(),"AM1.5G"))
			if ret==False:
				error_dlg(self,_("I cant write to:")+new_spectra+" "+_("This means either the disk is full or your system administrator has not given you write permissions to that location."))

			a=json_c("spectra_db")
			a.build_template()
			a.save_as(os.path.join(new_spectra,"data.json"))

			self.fill_store()

	def new_material(self):
		new_sim_name=dlg_get_text2( _("New material name:"), _("New material name"),"organic_material")
		new_sim_name=new_sim_name.ret
		if new_sim_name!=None:
			new_material=os.path.join(self.path,new_sim_name)
			print(new_material)
			try:
				os.makedirs(new_material)
			except:
				error_dlg(self,_("I cant write to: ")+new_material+" "+_("This means either the disk is full or your system administrator has not given you write permissions to that location."))
			
			a=json_c("material_db")
			a.build_template()
			a.save_as(os.path.join(new_material,"data.json"))
			self.fill_store()

	def new_filter(self):
		new_sim_name=dlg_get_text2( _("New filter name:"), _("New filter name"),"filter_wheel")
		new_sim_name=new_sim_name.ret
		if new_sim_name!=None:
			new_filter=os.path.join(self.path,new_sim_name)
			os.makedirs(new_filter)

			a=json_c("filter_db")
			a.build_template()
			a.save_as(os.path.join(new_filter,"data.json"))

			self.fill_store()

	def new_dir(self):
		new_sim_name=dlg_get_text2( _("New directory name:"), _("New directory"),"document-new")
		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:
			name=os.path.join(self.path,new_sim_name)
			os.mkdir(name)
		self.fill_store()
