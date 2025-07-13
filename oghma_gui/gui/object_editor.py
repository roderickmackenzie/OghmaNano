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

from util import wrap_text

from cal_path import sim_paths

from dlg_get_text2 import dlg_get_text2
from gui_util import yes_no_dlg
from tick_cross import tick_cross
from json_viewer_bin import json_viewer_bin
from help import QAction_help
from bytes2str import bytes2str
from json_c import json_tree_c
import ctypes
from object_editor_base import object_editor_base

class object_editor(QWidgetSavePos,object_editor_base):

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

	def load(self,ids):
		i=0
		if type(ids)==str:
			ids=[ids]

		self.root_id=ids[0]

		for uid in ids:
			json_path=self.bin.find_path_by_uid("",uid)
			name=self.bin.get_token_value(json_path,"name")
			my_tab=json_viewer_bin(self.bin)
			my_tab.populate(json_path,uid=uid)
			my_tab.changed.connect(self.callback_edit)
			self.notebook.addTab(my_tab,name)	

			i=i+1
		return

		#This needs to be added back in when we add groups
		all_g_ids=[]
		for id in ids:
			groups=json_root().world.groups.get_groups(id)
	
			for g_id in groups:
				if all_g_ids.count(g_id)==0:
					g=json_root().find_object_by_id(g_id)
					my_tab=json_viewer()
					my_tab.populate(g)

					my_tab.changed.connect(self.callback_edit)

					name=g.name
					self.notebook.addTab(my_tab,name)
					all_g_ids.append(g_id)
					i=i+1

	def callback_edit(self,item):
		self.notebook.currentWidget()
		self.bin.save()
		if item=="shape_type" or item=="obj_type":
			self.force_redraw(level="reload_rebuild")
		else:
			self.force_redraw()

	def callback_enable_disable(self):
		tab = self.notebook.currentWidget()
		if tab!=None:
			tab.setEnabled(self.enable.enabled)
			json_path=self.bin.find_path_by_uid("",tab.uid)
			self.bin.set_token_value(json_path,"enabled",self.enable.enabled)
			self.bin.save()
			self.force_redraw()

	def changed_click(self):
		tab = self.notebook.currentWidget()
		if tab!=None:
			json_path=self.bin.find_path_by_uid("",tab.uid)
			enabled=self.bin.get_token_value(json_path,"enabled")
			name=self.bin.get_token_value(json_path,"name")
			tab.setEnabled(enabled)
			self.enable.setState(enabled)
			self.status_bar.showMessage(name+" "+bytes2str(tab.uid))

			#if self.notebook.currentIndex()==0:
			#self.tb_delete.setEnabled(False)
			#self.tb_clone.setEnabled(False)
			#else:
			#self.tb_delete.setEnabled(True)
			#self.tb_clone.setEnabled(True)

	def callback_add_shape(self):
		json_path=self.add_new_shape_to_object(self.root_id)
		if json_path!=None:
			name=self.bin.get_token_value(json_path,"name")
			uid=self.bin.get_token_value(json_path,"id")
			my_tab=json_viewer_bin(self.bin)
			my_tab.populate(json_path,uid=uid)
			self.notebook.addTab(my_tab,name)
			my_tab.changed.connect(self.callback_edit)

	def callback_rename_shape(self):
		tab = self.notebook.currentWidget()
		new_name=self.rename_object(tab.uid)
		if new_name!=None:
			index=self.notebook.currentIndex() 
			self.notebook.setTabText(index, new_name)


	def callback_clone_shape(self):
		tab = self.notebook.currentWidget()
		json_path=self.clone_object(tab.uid)
		name=self.bin.get_token_value(json_path,"name")
		uid=self.bin.get_token_value(json_path,"id")

		my_tab=json_viewer_bin(self.bin)
		my_tab.populate(json_path,uid=uid)
		my_tab.changed.connect(self.callback_edit)
		self.notebook.addTab(my_tab,name)

	def callback_delete_shape(self):
		tab = self.notebook.currentWidget()
		self.delete_object([tab.uid])
		index=self.notebook.currentIndex() 
		self.notebook.removeTab(index)

