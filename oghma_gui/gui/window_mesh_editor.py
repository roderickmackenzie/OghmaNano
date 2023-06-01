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

## @package emesh
#  The main window to edit the electrical mesh, can select between a 1D, 2D and 3D mesh.
#

from icon_lib import icon_get

#qt
from PySide2.QtWidgets import QAction
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QToolBar,QMessageBox,QVBoxLayout


from global_objects import global_object_run
from QWidgetSavePos import QWidgetSavePos

from global_objects import global_object_register
from tab_mesh_editor import tab_mesh_editor
from config_window import class_config_window
from tab_view import tab_view

from json_root import json_root
from help import QAction_help
from json_mesh import json_mesh_segment
from gui_util import yes_no_dlg

class window_mesh_editor(QWidgetSavePos):

	def __init__(self,json_path_to_mesh="json_root().electrical_solver.mesh",window_title=_("Electrical Mesh Editor")):
		self.json_path_to_mesh=json_path_to_mesh
		data=eval(json_path_to_mesh)
		QWidgetSavePos.__init__(self,"emesh")

		self.setMinimumSize(1200, 600)
		self.setWindowIcon(icon_get("mesh"))

		self.setWindowTitle2(window_title)
		

		self.main_vbox = QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)

		if data.mesh_y!=None:
			self.tb_y = QAction(icon_get("y"), _("Y\nDimension"), self)
			self.tb_y.triggered.connect(self.callback_dim_y)
			self.tb_y.setCheckable(True)
			toolbar.addAction(self.tb_y)

		if data.mesh_x!=None:
			self.tb_x = QAction(icon_get("x"), _("X\nDimension"), self)
			self.tb_x.triggered.connect(self.callback_dim_x)
			self.tb_x.setCheckable(True)
			toolbar.addAction(self.tb_x)

		if data.mesh_z!=None:
			self.tb_z = QAction(icon_get("z"), _("Z\nDimension"), self)
			self.tb_z.triggered.connect(self.callback_dim_z)
			self.tb_z.setCheckable(True)
			toolbar.addAction(self.tb_z)

		if data.mesh_l!=None:
			self.tb_l = QAction(icon_get("lambda"), _("Wavelength"), self)
			self.tb_l.triggered.connect(self.callback_dim_l)
			self.tb_l.setCheckable(True)
			toolbar.addAction(self.tb_l)
			self.tb_l.setChecked(True)

		if data.mesh_t!=None:
			self.tb_t = QAction(icon_get("t"), _("Temperature"), self)
			self.tb_t.triggered.connect(self.callback_dim_t)
			self.tb_t.setCheckable(True)
			toolbar.addAction(self.tb_t)
			self.tb_t.setChecked(True)

		configure = QAction(icon_get("preferences-system"),  _("Configure\nmesh"), self)
		configure.triggered.connect(self.on_configure_click)
		toolbar.addAction(configure)

		mesh_import = QAction(icon_get("mesh_import"),  _("Import from\nlayer editor"), self)
		mesh_import.triggered.connect(self.callback_mesh_import)
		toolbar.addAction(mesh_import)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)
		

		widget=QWidget()
		mesh_hbox=QHBoxLayout()
		widget.setLayout(mesh_hbox)
		no_user_edit=False
		if json_root().electrical_solver.solver_type=="circuit":
			no_user_edit=True

		if data.mesh_x!=None:
			self.emesh_editor_x=tab_mesh_editor(self.json_path_to_mesh+".mesh_x")
			self.emesh_editor_x.changed.connect(self.emit_now)
			mesh_hbox.addWidget(self.emesh_editor_x)

		if data.mesh_y!=None:
			self.emesh_editor_y=tab_mesh_editor(self.json_path_to_mesh+".mesh_y",no_user_edit=no_user_edit)
			self.emesh_editor_y.changed.connect(self.emit_now)
			mesh_hbox.addWidget(self.emesh_editor_y)

		if data.mesh_z!=None:
			self.emesh_editor_z=tab_mesh_editor(self.json_path_to_mesh+".mesh_z")
			self.emesh_editor_z.changed.connect(self.emit_now)
			mesh_hbox.addWidget(self.emesh_editor_z)

		if data.mesh_l!=None:
			self.emesh_editor_l=tab_mesh_editor(self.json_path_to_mesh+".mesh_l")
			self.emesh_editor_l.changed.connect(self.emit_now)
			mesh_hbox.addWidget(self.emesh_editor_l)
		
		if data.mesh_t!=None:
			self.emesh_editor_t=tab_mesh_editor(self.json_path_to_mesh+".mesh_t",show_auto=True)
			self.emesh_editor_t.changed.connect(self.emit_now)
			mesh_hbox.addWidget(self.emesh_editor_t)			

		self.main_vbox.addWidget(widget)

		self.update_dim()

		self.setLayout(self.main_vbox)
		self.mesh_config=None
		global_object_register("mesh_update",self.update)
	
	def on_configure_click(self):
		if self.mesh_config==None:
			data=eval(self.json_path_to_mesh)
			self.mesh_config=class_config_window([data.config],[_("Remesh")],title=_("Configure mesh"),icon="mesh")
			self.mesh_config.show()
		self.mesh_config.show()

	def save_image(self,file_name):
		self.fig.savefig(file_name)

	def update(self):
		self.emesh_editor_x.update()
		self.emesh_editor_y.update()
		self.emesh_editor_z.update()
		self.update_dim()

	def callback_dim_y(self):
		data=eval(self.json_path_to_mesh)
		data.mesh_y.enabled=not data.mesh_y.enabled
		json_root().save()
		self.update_dim()
		
	def callback_dim_x(self):
		data=eval(self.json_path_to_mesh)
		data.mesh_x.enabled=not data.mesh_x.enabled
		json_root().save()
		self.update_dim()

	def callback_dim_z(self):
		data=eval(self.json_path_to_mesh)
		data.mesh_z.enabled=not data.mesh_z.enabled
		json_root().save()
		self.update_dim()

	def callback_dim_l(self):
		self.tb_l.setChecked(True)

	def callback_dim_t(self):
		self.tb_t.setChecked(True)

	def update_dim(self):
		data=eval(self.json_path_to_mesh)

		if data.mesh_x!=None:
			if data.mesh_x.enabled==True:
				self.emesh_editor_x.show()
			else:
				self.emesh_editor_x.hide()
			self.tb_x.setChecked(data.mesh_x.enabled)

		if data.mesh_y!=None:
			if data.mesh_y.enabled==True:
				self.emesh_editor_y.show()
			else:
				self.emesh_editor_y.hide()
			self.tb_y.setChecked(data.mesh_y.enabled)

		if data.mesh_z!=None:
			if data.mesh_z.enabled==True:
				self.emesh_editor_z.show()
			else:
				self.emesh_editor_z.hide()
			self.tb_z.setChecked(data.mesh_z.enabled)

		self.emit_now()

	def emit_now(self):
		global_object_run("gl_force_redraw")
		
	def callback_mesh_import(self):
		if yes_no_dlg(self,_("Are you sure you want to overwrite the electrical mesh with a guessed mesh based on the layer structure?"))==True:
			self.emesh_editor_y.tab.remove_all_rows()
			data=eval(self.json_path_to_mesh)
			data.mesh_y.segments=[]
			for l in json_root().epi.layers:
				a=json_mesh_segment()
				a.len=l.dy
				a.points=10.0
				data.mesh_y.segments.append(a)
				
			json_root().save()
			
			self.emesh_editor_y.tab.populate()
			self.emesh_editor_y.redraw()
