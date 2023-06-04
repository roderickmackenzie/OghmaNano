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

## @package tab_main
#  The main tab in the simulation window which displays the picture of the device.
#

from tab_base import tab_base
from help import help_window
from display import display_widget
from PySide2.QtWidgets import QWidget,QHBoxLayout,QSplitter
from gQtCore import Qt

from ribbon_device import ribbon_device

import i18n
_ = i18n.language.gettext

class tab_main(QWidget,tab_base):

	
	def __init__(self):
		QWidget.__init__(self)
		self.sun=1
		hbox=QHBoxLayout(self)
		mainLayout = QSplitter(Qt.Horizontal)
		#splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
		self.three_d=display_widget()
		#self.three_d.show()

		self.ribbon=ribbon_device()
		self.ribbon.addWidget(self.three_d.display.toolbar0)
		self.ribbon.addWidget(self.three_d.display.toolbar1)

		mainLayout.addWidget(self.ribbon)
		self.ribbon.setMinimumSize(100, 0)
		mainLayout.addWidget(self.three_d)
		mainLayout.setStretchFactor ( 1, 1 )

		hbox.addWidget(mainLayout)
		
		self.setLayout(hbox)
		
	def help(self):
		help_window().help_set_help(["device.png",_("<big><b>The device structure tab</b></big>\n Use this tab to change the structure of the device, the layer thicknesses and to perform optical simulations.  You can also browse the materials data base and  edit the electrical mesh.")])

