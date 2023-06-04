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

## @package circuit
#  Widget to draw circuit diagram
#

from cal_path import get_image_file_path
from tb_pulse_load_type import tb_pulse_load_type

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QMenuBar,QStatusBar
from PySide2.QtGui import QPainter,QIcon,QPixmap
from ersatzschaltbild import ersatzschaltbild

class my_draw(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.mQImage = QPixmap("document-new.png")

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(100,10, self.mQImage)
        painter.end()


class circuit(QWidget):

	def update(self,object):
		self.darea.queue_draw()

	def __init__(self,data):
		QWidget.__init__(self)
		self.data=data
		vbox=QVBoxLayout()


		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))


		self.load_type=tb_pulse_load_type(data.config)

		toolbar.addWidget(self.load_type)
		vbox.addWidget(toolbar)

		self.darea = QWidget()


		self.diagram=ersatzschaltbild()
		self.diagram.dx=200
		self.diagram.dy=200
		self.diagram.editable=False

		vbox.addWidget(self.diagram)

		
		self.setLayout(vbox)
		self.load_type.changed.connect(self.update)
		self.update()

	def update(self):
		self.diagram.clear()
		if self.load_type.sim_mode.currentText()=="load":
			self.diagram.add_object0(1,1,1,2,"diode")

			self.diagram.add_object0(1,1,2,1,"wire")
			self.diagram.add_object0(1,2,2,2,"wire")

			self.diagram.add_object0(2,1,2,2,"capacitor")
			self.diagram.add_object0(2,1,3,1,"wire")
			self.diagram.add_object0(2,2,3,2,"wire")

			self.diagram.add_object0(3,1,3,2,"resistor")
			self.diagram.add_object0(3,1,4,1,"resistor")
			self.diagram.add_object0(3,2,4,2,"wire")

			self.diagram.add_object0(4,1,5,1,"resistor")
			self.diagram.add_object0(5,1,5,2,"vsource")

			self.diagram.add_object0(4,2,5,2,"wire")

		elif self.load_type.sim_mode.currentText()=="ideal_diode_ideal_load":

			self.diagram.add_object0(1,1,1,2,"diode")

			self.diagram.add_object0(1,1,2,1,"wire")
			self.diagram.add_object0(1,2,2,2,"wire")

			self.diagram.add_object0(2,1,3,1,"wire")
			self.diagram.add_object0(2,2,3,2,"wire")

			self.diagram.add_object0(3,1,3,2,"vsource")

		else:
			self.diagram.add_object0(1,1,1,2,"diode")

			self.diagram.add_object0(1,1,2,1,"wire")
			self.diagram.add_object0(1,2,2,2,"wire")

			self.diagram.add_object0(2,1,2,2,"capacitor")
			self.diagram.add_object0(2,1,3,1,"wire")
			self.diagram.add_object0(2,2,3,2,"wire")

			self.diagram.add_object0(3,1,3,2,"resistor")
			self.diagram.add_object0(3,1,4,1,"resistor")
			self.diagram.add_object0(3,2,4,2,"wire")

		self.diagram.repaint()

