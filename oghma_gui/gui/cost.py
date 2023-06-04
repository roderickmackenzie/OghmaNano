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


from cal_path import get_materials_path
from QWidgetSavePos import QWidgetSavePos
from help import QAction_help
from json_root import json_root
from json_material_db_item import json_material_db_item
from json_base import json_base

class cost(QWidgetSavePos):


	def __init__(self):
		QWidgetSavePos.__init__(self,"cost")
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
		epi=json_root().epi
		for l in epi.layers:
			
			volume=l.dy*1.0*1.0
			name=l.optical_material
			mat_file=os.path.join(get_materials_path(),l.optical_material,"data.json")
			data=json_material_db_item()
			data.load(mat_file)

			density = data.lca.lca_density
			mass=density*volume

			cost_per_kg = data.lca.lca_cost
			cost=mass*cost_per_kg

			energy_per_kg = data.lca.lca_energy
			energy=energy_per_kg*mass

			self.tab.add([name,str(volume),str(mass),str(cost),str(energy)])

			energy_tot=energy_tot+energy
			cost_tot=cost_tot+cost

		sim_info=json_base("decode")
		sim_info.import_from_file("sim_info.dat")

		pce=sim_info.pce
		payback_time=-1.0
		if pce!=None:
			pce=float(pce)
			gen_energy=1366.0*pce/100.0
			payback_time=energy_tot/gen_energy/60.0/60.0/24/365
		
		self.tab.add(["sum","","",str(cost_tot),str(energy_tot)])
		self.tab.add(["","","pay back time=",str(payback_time),"years"])




