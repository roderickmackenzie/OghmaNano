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

## @package dim_editor
#  A window to edit the dimentions of the device.
#

from str2bool import str2bool
from icon_lib import icon_get
from g_open import g_open
from cal_path import get_materials_path
from global_objects import global_object_get
from help import help_window

#windows
from error_dlg import error_dlg


#qt
from gQtCore import QSize, Qt
from PySide2.QtGui import QIcon,QPalette
from PySide2.QtWidgets import QWidget, QVBoxLayout,QProgressBar,QLineEdit,QLabel,QToolBar,QHBoxLayout,QAction, QSizePolicy, QTableWidget, QTableWidgetItem,QComboBox,QDialog, QTabWidget

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget

from global_objects import global_object_run

from global_objects import global_isobject
from global_objects import global_object_get

from QComboBoxLang import QComboBoxLang

import i18n
_ = i18n.language.gettext

from g_select import g_select

from cal_path import sim_paths
from cal_path import get_default_material_path
from QWidgetSavePos import QWidgetSavePos

from json_root import json_root
from tab import tab_class
from help import QAction_help
import copy
from yes_no_cancel_dlg import yes_no_cancel_dlg
from error_dlg import error_dlg

class dim_editor(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"dim_editor")

		self.setWindowTitle2(_("Dimension editor"))
		self.setWindowIcon(icon_get("dimensions"))
		self.setMinimumSize(600, 200)


		self.main_vbox=QVBoxLayout()

		self.toolbar=QToolBar()
		self.toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		self.toolbar.setIconSize(QSize(42, 42))

		spacer = QWidget()


		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

		self.help = QAction_help()
		self.toolbar.addAction(self.help)

		#self.main_vbox.addWidget(self.toolbar)

		#notebook
		self.notebook = QTabWidget()

		#device page
		self.xz_widget=QWidget()
		self.xz_vbox=QVBoxLayout()
		self.widget0 = QWidget()
		self.widget0_hbox=QHBoxLayout()
		self.widget0.setLayout(self.widget0_hbox)

		self.widget0_label=QLabel("x size")
		self.widget0_hbox.addWidget(self.widget0_label)

		self.widget0_edit=QLineEdit()
		self.widget0_edit.setText(str(json_root().electrical_solver.mesh.mesh_x.get_len()))
		self.widget0_edit.textChanged.connect(self.apply)
		self.widget0_hbox.addWidget(self.widget0_edit)
		self.widget0_label=QLabel("m")
		self.widget0_hbox.addWidget(self.widget0_label)

		self.xz_vbox.addWidget(self.widget0)

		self.widget1 = QWidget()
		self.widget1_hbox=QHBoxLayout()
		self.widget1.setLayout(self.widget1_hbox)
		self.widget1_label=QLabel("z size")
		self.widget1_hbox.addWidget(self.widget1_label)
		self.widget1_edit=QLineEdit()
		self.widget1_edit.setText(str(json_root().electrical_solver.mesh.mesh_z.get_len()))
		self.widget1_edit.textChanged.connect(self.apply)
		self.widget1_hbox.addWidget(self.widget1_edit)
		self.widget1_label=QLabel("m")
		self.widget1_hbox.addWidget(self.widget1_label)
		self.xz_vbox.addWidget(self.widget1)

		self.xz_widget.setLayout(self.xz_vbox)
		if len(json_root().epitaxy.layers)!=0:
			self.notebook.addTab(self.xz_widget,_("Substrate xz size"))

		#World size
		self.local_data=copy.deepcopy(json_root().world.config)
		self.world_widget=tab_class(self.local_data,enable_apply_button=True)
		self.notebook.addTab(self.world_widget,_("World size"))
		self.world_widget.changed.connect(self.apply_button)
		self.main_vbox.addWidget(self.notebook)
		self.setLayout(self.main_vbox)



		#self.tab.itemSelectionChanged.connect(self.layer_selection_changed)


	def apply(self):
		data=json_root()
		try:
			val=float(self.widget0_edit.text())
			if val<=0:
				return
		except:
			return
		data.electrical_solver.mesh.mesh_x.set_len(val)

		try:
			val=float(self.widget1_edit.text())
			if val<=0:
				return

		except:
			return

		data.electrical_solver.mesh.mesh_z.set_len(val)

		data.save()
		global_object_run("mesh_update")
		self.callback_refresh_model()

	def apply_button(self):
		response=yes_no_cancel_dlg(self,"Rescale all objects in the world?")

		if response=="yes":
			dx1=self.local_data.world_x1-self.local_data.world_x0
			dx0=json_root().world.config.world_x1-json_root().world.config.world_x0

			dy1=self.local_data.world_y1-self.local_data.world_y0
			dy0=json_root().world.config.world_y1-json_root().world.config.world_y0

			dz1=self.local_data.world_z1-self.local_data.world_z0
			dz0=json_root().world.config.world_z1-json_root().world.config.world_z0
			if dx0==0.0 or dy0==0.0 or dz0==0.0:
				error_dlg(self,"Your world has zero size.")
				return
			rx=dx1/dx0
			ry=dy1/dy0
			rz=dz1/dz0
			data=json_root()
			
			data.rescale_world(rx,ry,rz)

		elif response=="cancel":
			return

		
		json_root().world.config.world_x0=self.local_data.world_x0
		json_root().world.config.world_x1=self.local_data.world_x1

		json_root().world.config.world_y0=self.local_data.world_y0
		json_root().world.config.world_y1=self.local_data.world_y1

		json_root().world.config.world_z0=self.local_data.world_z0
		json_root().world.config.world_z1=self.local_data.world_z1

		json_root().world.config.world_margin_x0=self.local_data.world_margin_x0
		json_root().world.config.world_margin_x1=self.local_data.world_margin_x1

		json_root().world.config.world_margin_y0=self.local_data.world_margin_y0
		json_root().world.config.world_margin_y1=self.local_data.world_margin_y1

		json_root().world.config.world_margin_z0=self.local_data.world_margin_z0
		json_root().world.config.world_margin_x1=self.local_data.world_margin_x1

		json_root().world.config.world_automatic_size=self.local_data.world_automatic_size
		json_root().world.config.world_fills_mesh=self.local_data.world_fills_mesh

		json_root().save()

		self.callback_refresh_model()

	def callback_refresh_model(self):
		global_object_run("gl_force_redraw_hard")

