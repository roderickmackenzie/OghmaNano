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

from process_events import process_events
from sim_name import sim_name
from bytes2str import bytes2str
from gQtCore import gSignal

class plot_window(QWidget):
	closed = gSignal(object)

	def __init__(self):
		QWidget.__init__(self)
		self.main_vbox=QVBoxLayout()
		self.setMinimumSize(200,200)
		self.data=dat_file()
		
		self.setLayout(self.main_vbox)

	def update_status_bar(self,text):
		self.status_bar.showMessage(text)

	def init(self,input_files,plot_labels=[]):
		three_d=False
		data_type="xy"

		print("loading:",input_files[0])

		if len(input_files)==1:
			self.data.load_only_info(input_files[0])
			data_type=bytes2str(self.data.type)
		#This needs moving into the plot widget but not today
		three_d=False
		if data_type=="gobj":
			three_d=True

		if self.data.type==b"zxy-d":
			if self.data.cols==b"zxd":
				three_d=True
			if self.data.cols==b"xyd":
				three_d=True
			if self.data.cols==b"zxyd":
				three_d=True

		if data_type=="circuit" or data_type=="poly":
			three_d=True
		elif self.data.cols==b"zxyzxyzxyzxy":
			three_d=True
		elif self.data.cols==b"zxyzxyrgb":
			three_d=True
		elif self.data.cols==b"zxyrgb":
			three_d=True
		elif self.data.type==b"3d-mesh":
			three_d=True

		self.plot=plot_widget(widget_mode="graph",force_2d3d=three_d)

		self.plot.load_data(input_files)
		self.plot.set_labels(plot_labels)
		self.main_vbox.addWidget(self.plot)

		self.plot.do_plot()
		self.setWindowTitle("OghmaNano (https://www.oghma-nano.com)")

		self.status_bar=QStatusBar()
		self.main_vbox.addWidget(self.status_bar)
		self.plot.text_output.connect(self.update_status_bar)

		self.show()

	def closeEvent(self, event):
		self.closed.emit(self)
		event.accept() 

	def keyPressEvent(self, event):
		keyname=chr(event.key()).lower()
		print(keyname)
		if keyname == "q":
			self.close()

		self.plot.keyPressEvent(event)

