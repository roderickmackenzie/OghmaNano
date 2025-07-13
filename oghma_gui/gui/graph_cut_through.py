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

## @package gl_graph
#  The gl_graph class for the OpenGL display.
#

import os
import sys

from PySide2.QtWidgets import QWidget,QSlider,QHBoxLayout,QVBoxLayout, QLabel
from gQtCore import QSize, Qt

class graph_cut_through(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.frac_max=1.0
		self.frac_min=0.0

		self.setWindowTitle("Cut through window")

		main_layout = QVBoxLayout()

		# Create Z slider and label
		self.z_layout = QHBoxLayout()
		self.z_label = QLabel("z:")
		self.z_pos = QLabel("")
		self.z_slider = QSlider(Qt.Horizontal)
		self.z_slider.setRange(0, 100)
		self.z_slider.setValue(100)
		self.z_layout.addWidget(self.z_label)
		self.z_layout.addWidget(self.z_slider)
		self.z_layout.addWidget(self.z_pos)

		# Create X slider and label
		self.x_layout = QHBoxLayout()
		self.x_label = QLabel("x:")
		self.x_pos = QLabel("")
		self.x_slider = QSlider(Qt.Horizontal)
		self.x_slider.setRange(0, 100)
		self.x_slider.setValue(100)
		self.x_layout.addWidget(self.x_label)
		self.x_layout.addWidget(self.x_slider)
		self.x_layout.addWidget(self.x_pos)

		# Create Y slider and label
		self.y_layout = QHBoxLayout()
		self.y_label = QLabel("y:")
		self.y_pos = QLabel("")
		self.y_slider = QSlider(Qt.Horizontal)
		self.y_slider.setRange(0, 100)
		self.y_slider.setValue(100)
		self.y_layout.addWidget(self.y_label)
		self.y_layout.addWidget(self.y_slider)
		self.y_layout.addWidget(self.y_pos)

		# Add both slider layouts to the main layout
		main_layout.addLayout(self.z_layout)
		main_layout.addLayout(self.x_layout)
		main_layout.addLayout(self.y_layout)

		# Set main layout to window
		self.setLayout(main_layout)

		main_layout = QVBoxLayout()

		self.slider_y_min = QSlider(Qt.Horizontal)
		self.slider_y_min.setRange(0, 100)

		self.slider_y_max = QSlider(Qt.Horizontal)
		self.slider_y_max.setRange(0, 100)


		main_layout.addWidget(self.slider_y_min)
		main_layout.addWidget(self.slider_y_max)

		self.setLayout(main_layout)

	def show_hide(self,z,x,y):
		self.z_label.setVisible(z)
		self.z_pos.setVisible(z)
		self.z_slider.setVisible(z)

		self.x_label.setVisible(x)
		self.x_pos.setVisible(x)
		self.x_slider.setVisible(x)

		self.y_label.setVisible(y)
		self.y_pos.setVisible(y)
		self.y_slider.setVisible(y)

