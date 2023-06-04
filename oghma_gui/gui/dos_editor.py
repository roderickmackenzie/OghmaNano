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

## @package tab_homo
#  A tab to draw the analytical HOMO/LUMO.
#

import os

from open_save_dlg import save_as_image

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView, QMenuBar,QGroupBox,QHBoxLayout, QTableWidgetItem, QStatusBar, QDialog
from PySide2.QtGui import QPainter,QIcon

from gQtCore import gSignal

from icon_lib import icon_get

from ribbon_complex_dos import ribbon_complex_dos 
from g_tab2 import g_tab2
from cal_path import sim_paths
from dat_file import dat_file

from plot_widget import plot_widget

from QComboBoxLang import QComboBoxLang

from error_dlg import error_dlg
from str2bool import str2bool
from json_root import json_root
from json_dos import shape_homo_lumo_item
from sim_name import sim_name
from bytes2str import str2bytes
from math import exp

class equation_editor(QGroupBox):

	changed = gSignal()

	def __init__(self,name,uid):
		QGroupBox.__init__(self)
		self.setTitle(name)
		self.setStyleSheet("QGroupBox {  border: 1px solid gray;}")
		vbox=QVBoxLayout()
		self.setLayout(vbox)

		self.toolbar=QToolBar()
		vbox.addWidget(self.toolbar)

		self.tab2 = g_tab2(toolbar=self.toolbar)
		self.tab2.set_tokens(["function","function_enable","function_a","function_b","function_c"])
		self.tab2.set_labels([_("Function"),_("Enabled"), _("a"), _("b"), _("c")])
		self.tab2.json_search_path="json_root().epitaxy"
		self.tab2.uid=uid
		self.tab2.base_obj=shape_homo_lumo_item()
		self.tab2.postfix="segments"
		self.tab2.populate()
		self.tab2.setColumnWidth(0, 150)
		self.tab2.setColumnWidth(1, 150)
		self.tab2.setColumnWidth(2, 100)
		self.tab2.setColumnWidth(3, 100)
		self.tab2.setColumnWidth(4, 100)

		#self.tab2.resizeColumnsToContents()
		self.tab2.verticalHeader().setVisible(False)

		self.tab2.changed.connect(self.callback_changed)
		
		vbox.addWidget(self.tab2)
		
	def callback_changed(self):
		json_root().save()
		self.changed.emit()		


class dos_editor(QWidget):

	def update_graph(self):
		self.gen_mesh()
		self.plot.do_plot()

	def callback_save(self):
		file_name=save_as_image(self)
		if file_name!=False:
			self.canvas_lumo.figure.savefig(file_name)


	def gen_mesh(self):
		self.mesh=[]
		dos_data=self.get_json()

		Xi=dos_data.Xi
		Eg=dos_data.Eg
		try:
			srh_stop=float(dos_data.srh_start)
		except:
			error_dlg(self,str(dos_data.srh_start)+" "+_("is not a number.."))

		try:
			bands=int(dos_data.srh_bands)
		except:
			error_dlg(self,str(bands)+" "+_("is not a number.."))
		
		start=Xi
		stop=Xi-Eg
		pos=start
		dx=(stop-start)/100
		while(pos>stop):
			pos=pos+dx
			self.mesh.append(pos)

		self.data_lumo=dat_file()
		self.data_lumo.data_min=1e10
		self.data_lumo.data_max=1e27
		self.data_lumo.title=b"LUMO Density of states"

		self.data_lumo.y_label=b"Energy"
		self.data_lumo.data_label=b"States"

		self.data_lumo.y_units=b"Ev"
		self.data_lumo.data_units=b"m^{-3} eV"
		
		self.data_lumo.y_mul=1.0
		self.data_lumo.data_mul=1.0

		self.data_lumo.logdata=True

		self.data_lumo.x_len=1
		self.data_lumo.y_len=len(self.mesh)
		self.data_lumo.z_len=1

		self.data_lumo.init_mem()

		self.data_numerical_lumo=dat_file()
		self.data_numerical_lumo.title=b"LUMO Numerical DoS"

		self.data_numerical_lumo.data_min=1e10
		self.data_numerical_lumo.data_max=1e27

		self.data_numerical_lumo.y_label=b"Energy"
		self.data_numerical_lumo.data_label=b"States"

		self.data_numerical_lumo.y_units=b"Ev"
		self.data_numerical_lumo.data_units=b"m^{-3} eV"
		
		self.data_numerical_lumo.y_mul=1.0
		self.data_numerical_lumo.data_mul=1.0

		self.data_numerical_lumo.logdata=True

		self.data_numerical_lumo.x_len=1
		self.data_numerical_lumo.y_len=len(self.mesh)
		self.data_numerical_lumo.z_len=1

		self.data_numerical_lumo.init_mem()

		self.data_homo=dat_file()

		self.data_homo.title=b"HOMO Density of states"

		self.data_homo.data_min=1e10
		self.data_homo.data_max=1e27

		self.data_homo.y_label=b"Energy"
		self.data_homo.data_label=b"States"

		self.data_homo.y_units=b"Ev"
		self.data_homo.data_units=b"m^{-3} eV"
		
		self.data_homo.y_mul=1.0
		self.data_homo.data_mul=1.0

		self.data_homo.logdata=True

		self.data_homo.x_len=1
		self.data_homo.y_len=len(self.mesh)
		self.data_homo.z_len=1

		self.data_homo.init_mem()

		self.data_numerical_homo=dat_file()
		self.data_numerical_homo.title=b"HOMO Numerical DoS"

		self.data_numerical_homo.data_min=1e10
		self.data_numerical_homo.data_min=1e27

		self.data_numerical_homo.y_label=b"Energy"
		self.data_numerical_homo.data_label=b"States"

		self.data_numerical_homo.y_units=b"Ev"
		self.data_numerical_homo.data_units=b"m^{-3} eV"
		
		self.data_numerical_homo.y_mul=1.0
		self.data_numerical_homo.data_mul=1.0

		self.data_numerical_homo.logdata=True

		self.data_numerical_homo.x_len=1
		self.data_numerical_homo.y_len=len(self.mesh)
		self.data_numerical_homo.z_len=1

		self.data_numerical_homo.init_mem()

		tot_lumo=0.0
		tot_homo=0.0

		for iy in range(0,len(self.mesh)):
			x=self.mesh[iy]
			y=0
			homo_y=0

			for s in dos_data.complex_lumo.segments:
				if s.function_enable==True:
					a=s.function_a
					b=s.function_b
					c=s.function_c

					if s.function=="exp":
						if b!=0:
							y = y+ a*exp((x-Xi)/b)

					elif s.function=="gaus":
						if b!=0:
							y = y+ a*exp(-pow(((c+(x-Xi))/(sqrt(2.0)*b*1.0)),2.0))
					elif s.function=="lorentzian":
							gamma=b
							norm=((3.14*gamma)/2.0)*a
							dx=(x-Xi)
							y = y+ norm*(1.0/3.1415926)*(0.5*gamma/((dx+c)*(dx+c)+(0.5*gamma)*(0.5*gamma)))

			for s in dos_data.complex_homo.segments:
				if s.function_enable==True:
					a=s.function_a
					b=s.function_b
					c=s.function_c

					if s.function=="exp":
						if b!=0:
							homo_y = homo_y+ a*exp((Xi-Eg-x)/b)

					elif s.function=="gaus":
						if b!=0:
							homo_y = homo_y+ a*exp(-pow(((Xi-Eg-x+c)/(sqrt(2.0)*b*1.0)),2.0))
					elif s.function=="lorentzian":
							gamma=b
							norm=((3.14*gamma)/2.0)*a
							dx=(Xi-Eg-x)
							homo_y = homo_y+ norm*(1.0/3.1415926)*(0.5*gamma/((dx+c)*(dx+c)+(0.5*gamma)*(0.5*gamma)))

			tot_lumo=tot_lumo+y*abs(dx)
			tot_homo=tot_homo+homo_y*abs(dx)

			self.data_numerical_lumo.y_scale[iy]=x
			self.data_numerical_homo.y_scale[iy]=x

			self.data_lumo.y_scale[iy]=x
			self.data_lumo.data[0][0][iy]=y

			self.data_homo.y_scale[iy]=x
			#print(x,homo_y)
			self.data_homo.data[0][0][iy]=homo_y

		if bands!=0:
			dE_band=srh_stop/bands

			srh_lumo_pos=Xi
			srh_homo_pos=Xi-Eg

			srh_lumo_stop_points=[]
			srh_lumo_avg=[]
			srh_lumo_count=[]

			srh_homo_stop_points=[]
			srh_homo_avg=[]
			srh_homo_count=[]

			for i in range(0,bands+1):

				srh_lumo_stop_points.append(srh_lumo_pos)
				srh_homo_stop_points.append(srh_homo_pos)

				srh_lumo_avg.append(0.0)
				srh_homo_avg.append(0.0)

				srh_lumo_count.append(0.0)
				srh_homo_count.append(0.0)

				srh_lumo_pos=srh_lumo_pos+dE_band
				srh_homo_pos=srh_homo_pos-dE_band

			#build numeical LUMO
			for iy in range(0,len(self.mesh)):
				x=self.mesh[iy]
				for i in range(0,len(srh_lumo_stop_points)-1):
					if srh_lumo_stop_points[i+1]<x:
						srh_lumo_avg[i]=srh_lumo_avg[i]+self.data_lumo.data[0][0][iy]
						srh_lumo_count[i]=srh_lumo_count[i]+1
						break

			for iy in range(0,len(self.mesh)):
				x=self.mesh[iy]
				for i in range(0,len(srh_lumo_stop_points)-1):
					if srh_lumo_stop_points[i+1]<x:
						self.data_numerical_lumo.data[0][0][iy]=srh_lumo_avg[i]/srh_lumo_count[i]
						break

			#build numeical HOMO
			for iy in range(0,len(self.mesh)):
				x=self.mesh[iy]
				for i in range(0,len(srh_homo_stop_points)-1):
					if srh_homo_stop_points[i+1]>x:
						srh_homo_avg[i]=srh_homo_avg[i]+self.data_homo.data[0][0][iy]
						srh_homo_count[i]=srh_homo_count[i]+1
						break

			for iy in range(0,len(self.mesh)):
				x=self.mesh[iy]
				for i in range(0,len(srh_homo_stop_points)-1):
					if srh_homo_stop_points[i+1]>x:
						if srh_homo_count[i]!=0:
							self.data_numerical_homo.data[0][0][iy]=srh_homo_avg[i]/srh_homo_count[i]
						break

		self.data_numerical_lumo.file_name=str2bytes(os.path.join(os.getcwd(),"lumo_numberical.dat"))
		self.data_numerical_homo.file_name=str2bytes(os.path.join(os.getcwd(),"homo_numberical.dat"))

		self.data_lumo.file_name=str2bytes(os.path.join(os.getcwd(),"lumo.dat"))
		self.data_homo.file_name=str2bytes(os.path.join(os.getcwd(),"homo.dat"))

		self.plot.data=[self.data_numerical_lumo,self.data_numerical_homo,self.data_lumo,self.data_homo]

		tot_lumo_str="{:.2e}".format(tot_lumo)
		tot_homo_str="{:.2e}".format(tot_homo)

		self.status_bar.showMessage("Trap density: LUMO="+tot_lumo_str+" m-3,  HOMO="+tot_homo_str+" m-3")

	def get_json(self):
		json_path=eval(self.search_path)
		data=json_path.find_object_by_id(self.uid)
		return data

	def __init__(self,search_path,uid):
		QWidget.__init__(self)
		self.uid=uid
		self.search_path=search_path
		dos_data=self.get_json()


		self.setWindowTitle(_("Complex Density of states editor")+sim_name.web_window_title)
		self.setWindowIcon(icon_get("electrical"))
		self.setMinimumSize(1400,500)

		edit_boxes=QWidget()
		vbox=QVBoxLayout()

		self.lumo=equation_editor("LUMO",dos_data.complex_lumo.id)
		vbox.addWidget(self.lumo)
		
		self.homo=equation_editor("HOMO",dos_data.complex_homo.id)
		vbox.addWidget(self.homo)
		
		self.plot=plot_widget(enable_toolbar=False)
		self.plot.set_labels([_("LUMO"),_("HOMO"),_("LUMO numerical"),_("HOMO numerical")])

		self.status_bar=QStatusBar()

		self.gen_mesh()

		edit_boxes.setLayout(vbox)

		hbox=QHBoxLayout()

		self.plot.do_plot()

		hbox.addWidget(self.plot)

		hbox.addWidget(edit_boxes)
		
		self.ribbon=ribbon_complex_dos()

		self.main_layout_widget=QWidget()
		self.main_layout_widget.setLayout(hbox)

		self.big_vbox=QVBoxLayout()

		self.big_vbox.addWidget(self.ribbon)
		self.big_vbox.addWidget(self.main_layout_widget)

		self.setLayout(self.big_vbox)

		self.lumo.changed.connect(self.update_graph)
		self.homo.changed.connect(self.update_graph)
		

		self.big_vbox.addWidget(self.status_bar)
		json_root().add_call_back(self.update)

	def update(self):
		self.lumo.tab2.update()
		self.homo.tab2.update()
		#self.update_graph()
