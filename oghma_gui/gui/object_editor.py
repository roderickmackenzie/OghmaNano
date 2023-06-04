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

## @package object_editor
#  An editor for shape files
#

from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget, QStatusBar
from PySide2.QtGui import QPainter,QIcon

from help import help_window
from QWidgetSavePos import QWidgetSavePos
from css import css_apply

from epitaxy import get_epi
from util import wrap_text

from shape import shape
from cal_path import sim_paths

from dlg_get_text2 import dlg_get_text2
from gui_util import yes_no_dlg
from tick_cross import tick_cross
from json_viewer import json_viewer
from json_root import json_root
import copy
from help import QAction_help
from bytes2str import bytes2str

class object_editor(QWidgetSavePos):


	def __init__(self,gl_forece_redraw):
		QWidgetSavePos.__init__(self,"object_editor")
		self.setMinimumSize(600, 500)
		self.setWindowIcon(icon_get("shape"))

		self.setWindowTitle2(_("Object editor")) 
		
		self.force_redraw=gl_forece_redraw
		self.main_vbox = QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(48, 48))

		self.tb_new = QAction(icon_get("document-new"), wrap_text("New object",2), self)
		self.tb_new.triggered.connect(self.callback_add_shape)

		toolbar.addAction(self.tb_new)

		self.tb_delete = QAction(icon_get("edit-delete"), wrap_text("Delete object",3), self)
		self.tb_delete.triggered.connect(self.callback_delete_shape)

		toolbar.addAction(self.tb_delete)

		self.tb_rename = QAction(icon_get("rename"), wrap_text("Rename object",3), self)
		self.tb_rename.triggered.connect(self.callback_rename_shape)
		toolbar.addAction(self.tb_rename)

		self.tb_clone = QAction(icon_get("clone"), wrap_text("Clone object",3), self)
		self.tb_clone.triggered.connect(self.callback_clone_shape)
		toolbar.addAction(self.tb_clone)

		self.enable=tick_cross(enable_text=_("Object\nenabled"),disable_text=_("Object\ndisabled"))
		self.enable.changed.connect(self.callback_enable_disable)
		toolbar.addAction(self.enable)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)


		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)


		self.notebook = QTabWidget()
		css_apply(self.notebook,"tab_default.css")
		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)

		self.notebook.currentChanged.connect(self.changed_click)

		self.status_bar=QStatusBar()
		self.main_vbox.addWidget(self.status_bar)

		self.setLayout(self.main_vbox)
		self.epi=get_epi()

	def load(self,ids):
		i=0
		if type(ids)==str:
			ids=[ids]

		self.root_id=ids[0]

		for id in ids:
			s=json_root().find_object_by_id(id)
			my_tab=json_viewer()
			my_tab.populate(s)

			my_tab.changed.connect(self.callback_edit)

			name=s.name

			self.notebook.addTab(my_tab,name)	
			i=i+1

	def callback_edit(self,item):
		data=json_root()
		self.notebook.currentWidget()
		data.save()
		if item=="shape_type":
			self.force_redraw(level="reload_rebuild")
		else:
			self.force_redraw()

	def callback_enable_disable(self):
		data=json_root()
		tab = self.notebook.currentWidget()
		if tab!=None:
			tab.setEnabled(self.enable.enabled)
			s=tab.template_widget
			s.enabled=self.enable.enabled
			data.save()
			self.force_redraw()
			

	def changed_click(self):
		tab = self.notebook.currentWidget()
		if tab!=None:
			s=tab.template_widget
			tab.setEnabled(s.enabled)
			self.enable.setState(s.enabled)
			self.status_bar.showMessage(s.name+" "+bytes2str(s.id))

			if self.notebook.currentIndex()==0:
				self.tb_delete.setEnabled(False)
				self.tb_clone.setEnabled(False)
			else:
				self.tb_delete.setEnabled(True)
				self.tb_clone.setEnabled(True)

	def callback_add_shape(self):
		data=json_root()
		obj=json_root().find_object_by_id(self.root_id)
		s=shape()
		s.dx=obj.dx/2.0
		s.dy=obj.dy/2.0
		s.dz=obj.dz/2.0
		s.moveable=True
		obj.segments.append(s)
		my_tab=json_viewer()
		my_tab.populate(s)
		my_tab.changed.connect(self.callback_edit)
		self.notebook.addTab(my_tab,s.name)
		my_tab.changed.connect(self.callback_edit)
		self.force_redraw(level="reload_rebuild")
		data.save()

	def callback_rename_shape(self):
		data=json_root()
		tab = self.notebook.currentWidget()

		new_sim_name=dlg_get_text2( "Rename the object:", tab.template_widget.name,"rename.png")

		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:
			tab.template_widget.name=new_sim_name
			index=self.notebook.currentIndex() 
			self.notebook.setTabText(index, new_sim_name)
			data.save()


	def callback_clone_shape(self):
		tab = self.notebook.currentWidget()
		name=tab.template_widget.name+"_new"

		new_sim_name=dlg_get_text2( "Clone the object:", name,"clone.png")
		new_sim_name=new_sim_name.ret

		if new_sim_name!=None:
			obj=json_root().find_object_by_id(self.root_id)
			for s in obj.segments:
				if s.name==tab.template_widget.name:
					my_shape=copy.deepcopy(s)
					my_shape.name=new_sim_name
					my_shape.update_random_ids()
					obj.segments.append(my_shape)
					
					my_tab=json_viewer()
					my_tab.populate(my_shape)
					self.notebook.addTab(my_tab,my_shape.name)
					my_tab.changed.connect(self.callback_edit)
					self.force_redraw()

	def callback_delete_shape(self):
		data=json_root()
		tab = self.notebook.currentWidget()
		name=tab.template_widget.name
		
		response=yes_no_dlg(self,"Do you really want to the object: "+name)

		if response == True:

			index=self.notebook.currentIndex() 
			self.notebook.removeTab(index)
			obj=json_root().find_object_by_id(self.root_id)
			for i in range(0,len(obj.segments)):
				if obj.segments[i].name==tab.template_widget.name:
					obj.segments.pop(i)
					data.save()
					break

		self.force_redraw()

