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

## @package solar_main
#  Part of solar module - delete
#
import sys
from PySide2.QtWidgets import QMenuBar, QWidget, QCalendarWidget,QTimeEdit, QAction,QDesktopWidget,QTabWidget,QVBoxLayout,QHBoxLayout, QLineEdit, QLabel
from PySide2.QtGui import QIcon
from gQtCore import QTime

import os

from ribbon_solar import ribbon_solar

from icon_lib import icon_get
from gQtCore import gSignal
from plot_widget import plot_widget
from spctral2 import spctral2
from dat_file import dat_file

from open_save_dlg import save_as_simfile
from cal_path import sim_paths
from json_c import json_tree_c
from json_c import json_c

class spctral2_gui(QWidget):

	def __init__(self):
		super().__init__()
		self.bin=json_tree_c()
		top_hbox=QHBoxLayout()
		top_widget=QWidget()

		self.spctral2=spctral2()

		self.plot=plot_widget(enable_toolbar=False)		
		self.plot.do_plot()

		date_widget=QWidget()
		date_vbox=QVBoxLayout()
		self.cal = QCalendarWidget(self)
		self.cal.setGridVisible(True)
		self.cal.move(10, 20)
		self.time=QTimeEdit()
		time=QTime(12, 30);
		self.time.setTime(time);
		date_vbox.addWidget(self.cal)
		date_vbox.addWidget(self.time)

		self.lat_widget=QWidget()
		self.lat_layout=QHBoxLayout()
		self.lat_label=QLabel("Latitude")
		self.lat_edit=QLineEdit()
		self.lat_layout.addWidget(self.lat_label)
		self.lat_layout.addWidget(self.lat_edit)
		self.lat_widget.setLayout(self.lat_layout)
		date_vbox.addWidget(self.lat_widget)


		self.preasure_widget=QWidget()
		self.preasure_layout=QHBoxLayout()
		self.preasure_label=QLabel("Preasure (bar)")
		self.preasure_edit=QLineEdit()
		self.preasure_layout.addWidget(self.preasure_label)
		self.preasure_layout.addWidget(self.preasure_edit)
		self.preasure_widget.setLayout(self.preasure_layout)
		date_vbox.addWidget(self.preasure_widget)

		self.aod_widget=QWidget()
		self.aod_layout=QHBoxLayout()
		self.aod_label=QLabel("AOD (cm-1)")
		self.aod_edit=QLineEdit()
		self.aod_layout.addWidget(self.aod_label)
		self.aod_layout.addWidget(self.aod_edit)
		self.aod_widget.setLayout(self.aod_layout)
		date_vbox.addWidget(self.aod_widget)

		self.water_widget=QWidget()
		self.water_layout=QHBoxLayout()
		self.water_label=QLabel("Water (cm-1)")
		self.water_edit=QLineEdit()
		self.water_layout.addWidget(self.water_label)
		self.water_layout.addWidget(self.water_edit)
		self.water_widget.setLayout(self.water_layout)
		date_vbox.addWidget(self.water_widget)

		self.no2_widget=QWidget()
		self.no2_layout=QHBoxLayout()
		self.no2_label=QLabel("NO2 (cm-1)")
		self.no2_edit=QLineEdit()
		self.no2_layout.addWidget(self.no2_label)
		self.no2_layout.addWidget(self.no2_edit)
		self.no2_widget.setLayout(self.no2_layout)
		date_vbox.addWidget(self.no2_widget)

		date_widget.setLayout(date_vbox)

		top_hbox.addWidget(self.plot)
		top_hbox.addWidget(date_widget)

		self.setLayout(top_hbox)

		self.water_edit.setText(str(self.bin.get_token_value("optical.spctral2","spctral2_water")))
		self.aod_edit.setText(str(self.bin.get_token_value("optical.spctral2","spctral2_aod")))
		self.preasure_edit.setText(str(self.bin.get_token_value("optical.spctral2","spctral2_preasure")))
		self.lat_edit.setText(str(self.bin.get_token_value("optical.spctral2","spctral2_lat")))
		self.no2_edit.setText(str(self.bin.get_token_value("optical.spctral2","spctral2_no2")))

		self.calculate()

	def calculate(self):
		self.plot.data=[]
		self.water_edit.text()

		day=self.cal.selectedDate().dayOfYear()
		hour=self.time.time().hour()
		minute=self.time.time().minute()

		self.bin.set_token_value("optical.spctral2","spctral2_day",int(day))
		self.bin.set_token_value("optical.spctral2","spctral2_hour",int(hour))
		self.bin.set_token_value("optical.spctral2","spctral2_minute",int(minute))
		
		self.bin.set_token_value("optical.spctral2","spctral2_lat",float(self.lat_edit.text()))
		self.bin.set_token_value("optical.spctral2","spctral2_aod",float(self.aod_edit.text()))

		self.bin.set_token_value("optical.spctral2","spctral2_preasure",float(self.preasure_edit.text()))
		self.bin.set_token_value("optical.spctral2","spctral2_water",float(self.water_edit.text()))
		self.bin.set_token_value("optical.spctral2","spctral2_no2",float(self.no2_edit.text()))

		self.bin.save()

		self.spctral2.calc()

		am=dat_file()
		am.load(os.path.join(sim_paths.get_spectra_path(),"AM1.5G","spectra.csv"))
		am.key_text="AM1.5G"
		self.plot.data.append(am)

		self.plot.data.append(self.spctral2.Iglobal)

		self.plot.data.append(self.spctral2.Id)

		self.plot.data.append(self.spctral2.Is)

		#self.plot.norm_data()
		self.plot.do_plot()

	def export(self):
		path=save_as_simfile(self,directory = sim_paths.get_spectra_path())
		if path!=None:
			os.makedirs(path)
			self.spctral2.Iglobal.save(os.path.join(path,"spectra.csv"))

			a=json_c("spectra_db")
			a.build_template()
			a.save_as(os.path.join(path,"data.json"))

