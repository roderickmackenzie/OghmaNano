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

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar
from PySide2.QtGui import QPainter,QIcon,QPixmap
from ersatzschaltbild import ersatzschaltbild, display_component
from icon_lib import icon_get
import functools
from gui_util import yes_no_dlg
from cal_path import sim_paths
from circuit_editor_toolbar import circuit_editor_toolbar
from json_c import json_tree_c

class tool_item(QAction):
	def __init__(self,icon_name,comp,s):
		self.icon=icon_name
		self.comp=comp
		QAction.__init__(self,icon_get(icon_name), comp,s)
		self.setCheckable(True)

class circuit_editor(QWidget):

	def __init__(self,show_toolbar=True):
		QWidget.__init__(self)
		self.bin=json_tree_c()

		vbox=QHBoxLayout()

		if show_toolbar==True:
			self.toolbox = circuit_editor_toolbar()
			self.toolbox.setMaximumWidth(250)
			self.toolbox.clicked.connect(self.callback_click)
			vbox.addWidget(self.toolbox)

		self.ersatzschaltbild = ersatzschaltbild()

		vbox.addWidget(self.ersatzschaltbild)

		self.setLayout(vbox)
		#self.setMinimumSize(800, 800)
		self.build_from_epi()

		self.bin.add_call_back(self.ersatzschaltbild.load)
		self.destroyed.connect(self.doSomeDestruction)

		
		#self.window.show()

	def doSomeDestruction(self):
		self.bin.remove_call_back(self.ersatzschaltbild.load)

	def build_from_epi(self):
			if self.bin.get_token_value("circuit","enabled")==False:
				pos=3

				a=display_component()
				a.x0=pos
				a.y0=3
				a.x1=pos+1
				a.y1=3
				a.comp="bat"
				self.ersatzschaltbild.add_object(a)

				pos=pos+1
				layers=self.bin.get_token_value("epitaxy","segments")
				for l in range(0,layers):
					path="epitaxy.segment"+str(l)
					obj_type=self.bin.get_token_value(path,"obj_type")
					component=self.bin.get_token_value(path+".shape_electrical","electrical_component")
					if obj_type=="active":# or l.obj_type=="contact":
						if component=="resistance":
							a=display_component()
							a.x0=pos
							a.y0=3
							a.x1=pos+1
							a.y1=3
							a.comp="resistor"
							self.ersatzschaltbild.add_object(a)
						if component=="diode":
							a=display_component()
							a.x0=pos
							a.y0=3
							a.x1=pos+1
							a.y1=3
							a.comp="diode"
							self.ersatzschaltbild.add_object(a)
						pos=pos+1

				a=display_component()
				a.x0=pos
				a.y0=3
				a.x1=pos+1
				a.y1=3
				a.comp="ground"
				self.ersatzschaltbild.add_object(a)

				self.ersatzschaltbild.objects_push()
			else:
				self.ersatzschaltbild.load()

	def callback_click(self,text):
		self.ersatzschaltbild.selected=text

