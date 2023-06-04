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

## @package plot_window
#  A plot window which uses the plot widget.
#


import os
#import shutil
#from token_lib import tokens
from plot_widget import plot_widget
from PySide2.QtWidgets import QWidget, QVBoxLayout, QSlider, QStatusBar, QSizePolicy
from gQtCore import Qt
from dat_file import dat_file
from icon_lib import icon_get

from gl import glWidget
from vec import vec
from process_events import process_events
from sim_name import sim_name
from bytes2str import bytes2str

class dissection(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.frac_max=1.0
		self.frac_min=0.0

		self.setWindowTitle("Dissection Window")
		main_layout = QVBoxLayout()

		self.slider_y_min = QSlider(Qt.Horizontal)
		self.slider_y_min.setRange(0, 100)

		self.slider_y_max = QSlider(Qt.Horizontal)
		self.slider_y_max.setRange(0, 100)


		main_layout.addWidget(self.slider_y_min)
		main_layout.addWidget(self.slider_y_max)

		self.setLayout(main_layout)


class plot_window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.main_vbox=QVBoxLayout()
		self.setMinimumSize(200,200)
		self.shown=False
		self.data=dat_file()
		self.status_bar=QStatusBar()

	def update_status_bar(self,text):
		self.status_bar.showMessage(text)

	def destroy(self):
		self.shown=False
		self.window.destroy()

	def callback_destroy(self,widget):
		self.destroy()

	def update_dissection_y_min(self, position):
		self.plot.frac_min=position/100.0
		self.plot.do_draw()

	def update_dissection_y_max(self, position):
		self.frac_max=position/100.0
		self.plot.plot.do_draw()


	def init(self,input_files,plot_labels,force_mode="2d"):
		three_d=False
		data_type="xy"

		print("loading:",input_files[0])

		if len(input_files)==1:
			self.data.load(input_files[0])
			data_type=bytes2str(self.data.type)

		three_d=False
		if data_type=="gobj":
			three_d=True

		if data_type=="zxy-d" or data_type=="circuit" or data_type=="poly":
			three_d=True
		elif force_mode=="3d":
			three_d=True
		elif self.data.cols==b"zxyzxyzxyzxy":
			three_d=True
		elif self.data.type==b"3d-mesh":
			three_d=True

		if three_d==True:
			self.setWindowTitle(_("3D object viewer")+sim_name.web_window_title)
			self.setWindowIcon(icon_get("shape"))
			self.dissection=dissection()

			self.plot=glWidget(self)

			self.plot.enable_views(["plot"])
			self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.main_vbox.addWidget(self.plot)
			self.main_vbox.addWidget(self.status_bar)
			self.plot.text_output.connect(self.update_status_bar)

			self.setLayout(self.main_vbox)

			self.plot.draw_electrical_mesh=False
			self.plot.active_view.draw_device=False
			self.plot.active_view.draw_rays=False
			self.plot.active_view.render_photons=False
			self.plot.active_view.optical_mode=False

			if data_type=="zxy-d":
				self.plot.active_view.plot_graph=True
				self.plot.data_files=[self.data]
				if self.data.title!="":
					self.setWindowTitle(bytes2str(self.data.title))

				self.dissection.slider_y_min.sliderMoved.connect(self.update_dissection_y_min)
				self.dissection.slider_y_max.sliderMoved.connect(self.update_dissection_y_max)

				self.dissection.show()
			elif data_type=="circuit":

				self.plot.draw_electrical_mesh=False
				self.plot.active_view.draw_device=False
				self.plot.active_view.draw_rays=False
				self.plot.active_view.plot_graph=False
				self.plot.plot_circuit=True
				self.plot.active_view.render_photons=False
				self.plot.data_files=[self.data]

			elif data_type=="poly" or self.data.type==b"3d-mesh":
				#self.data=dat_file()
				self.plot.draw_electrical_mesh=False
				self.plot.active_view.draw_device=False
				self.plot.active_view.draw_rays=False
				self.plot.active_view.render_photons=False
				self.plot.active_view.show_world_box=False
				self.plot.active_view.show_detectors=False
				#self.data.load(input_files[0])
				self.plot.data_files=[self.data]
				self.main_vbox.addWidget(self.status_bar)
				self.plot.text_output.connect(self.update_status_bar)

			self.show()
			#print(self.plot.enabled_veiws)
			process_events()
			self.plot.force_redraw()
		else:
			self.shown=True

			self.plot=plot_widget()

			if len(plot_labels)==0:
				for i in range(0,len(input_files)):
					plot_labels.append(os.path.basename(input_files[i]).replace("_","\_"))

			#print plot_labels
			for i in range(0,len(plot_labels)):
				if len(plot_labels[i])>0:
					if plot_labels[i][0]=="\\":
						plot_labels[i]=plot_labels[i][1:]
				plot_labels[i].replace("\\","/")

			self.plot.load_data(input_files)
			self.plot.set_labels(plot_labels)

			self.plot.do_plot()
			self.plot.show()	
		



