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

## @package cost
#  A window to calculate the cost of the solar cell.
#

import os
from tab import tab_class
from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QAbstractItemView
from PySide2.QtGui import QPainter,QIcon
from g_tab import g_tab
from help import help_window
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos
from help import QAction_help
from json_c import json_tree_c
from json_c import json_c

class cost(QWidgetSavePos):


	def __init__(self):
		QWidgetSavePos.__init__(self,"cost")
		self.bin=json_tree_c()
		self.setFixedSize(900, 600)
		self.setWindowIcon(icon_get("jv"))

		self.setWindowTitle(_("Cost and energy payback calculator")) 
		
		self.main_vbox = QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))

		self.play = QAction(icon_get("media-playback-start"), _("Re-calcualte"), self)
		self.play.triggered.connect(self.update)
		toolbar.addAction(self.play)
		
		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		self.help = QAction_help()
		toolbar.addAction(self.help)

		self.main_vbox.addWidget(toolbar)

		self.tab= g_tab()

		self.main_vbox.addWidget(self.tab)
		self.setLayout(self.main_vbox)

		self.update()

	def update(self):
		self.tab.clear()
		self.tab.setColumnCount(5)
		self.tab.setRowCount(0)
		self.tab.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tab.setHorizontalHeaderLabels([_("material"), _("Volume")+" (m^-3)", _("Mass")+" (kg)", _("Cost")+" ($)", _("Energy")+" (J)"])
		self.tab.setColumnWidth(1, 200)
		self.tab.setColumnWidth(2, 200)
		self.tab.setColumnWidth(3, 200)
		self.tab.setColumnWidth(4, 200)

		energy_tot=0.0
		cost_tot=0.0
		segments=self.bin.get_token_value("epitaxy","segments")
		for s in range(0,segments):
			path="epitaxy.segment"+str(s)
			dy=self.bin.get_token_value(path,"dy")
			optical_material=self.bin.get_token_value(path,"optical_material")
			volume=dy*1.0*1.0

			mat_file=os.path.join(sim_paths.get_materials_path(),optical_material,"data.json")
			data=json_c("material_db")
			data.load(mat_file)
			density=data.get_token_value("lca","lca_density")
			cost_per_kg=data.get_token_value("lca","lca_cost")
			energy_per_kg=data.get_token_value("lca","lca_energy")
			data.free()

			mass=density*volume
			cost=mass*cost_per_kg
			energy=energy_per_kg*mass

			self.tab.add([optical_material,str(volume),str(mass),str(cost),str(energy)])

			energy_tot=energy_tot+energy
			cost_tot=cost_tot+cost

		sim_info=json_c("file_defined")
		sim_info.load(os.path.join(sim_paths.get_sim_path(),"sim_info.dat"))

		pce=data.get_token_value("","pce")
		sim_info.free()

		payback_time=-1.0
		if pce!=None:
			pce=float(pce)
			gen_energy=1366.0*pce/100.0
			payback_time=energy_tot/gen_energy/60.0/60.0/24/365
		
		self.tab.add(["sum","","",str(cost_tot),str(energy_tot)])
		self.tab.add(["","","pay back time=",str(payback_time),"years"])




