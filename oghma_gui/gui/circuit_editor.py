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
from PySide2.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QStatusBar
from PySide2.QtGui import QPainter,QIcon,QPixmap
from ersatzschaltbild import ersatzschaltbild
from icon_lib import icon_get
import functools
from gui_util import yes_no_dlg
from epitaxy import get_epi
from cal_path import sim_paths
from json_circuit import json_component
from json_root import json_root

class tool_item(QAction):
	def __init__(self,icon_name,comp,s):
		self.icon=icon_name
		self.comp=comp
		QAction.__init__(self,icon_get(icon_name), comp,s)
		self.setCheckable(True)

class circuit_editor(QWidget):

	def __init__(self,show_toolbar=True):
		QWidget.__init__(self)

		vbox=QHBoxLayout()

		self.toolbar=QToolBar()
		self.toolbar.setOrientation(Qt.Vertical)
		self.toolbar.setIconSize(QSize(48, 48))

		self.buttons=[]
		self.buttons.append(tool_item("resistor", _("Resistor"),self))
		self.buttons.append(tool_item("capacitor", _("Capacitor"),self))
		self.buttons.append(tool_item("diode", _("Diode"),self))
		self.buttons.append(tool_item("power", _("Power law"),self))
		self.buttons.append(tool_item("wire", _("Wire"),self))
		self.buttons.append(tool_item("ground", _("Ground"),self))
		self.buttons.append(tool_item("bat", _("Voltage source"),self))
		self.buttons.append("sep")
		self.buttons.append(tool_item("pointer", _("Pointer"),self))
		self.buttons.append(tool_item("clean", _("Clean"),self))

		self.buttons[1].setChecked(True)

		for item in self.buttons:
			if item=="sep":
				self.toolbar.addSeparator()
			else:
				self.toolbar.addAction(item)
				item.triggered.connect(functools.partial(self.callback_click,item))

		if show_toolbar==True:
			vbox.addWidget(self.toolbar)

		self.ersatzschaltbild = ersatzschaltbild()
		self.ersatzschaltbild.dx=80
		self.ersatzschaltbild.dy=80
		self.ersatzschaltbild.init()

		vbox.addWidget(self.ersatzschaltbild)

		self.setLayout(vbox)
		#self.setMinimumSize(800, 800)
		self.build_from_epi()

		json_root().add_call_back(self.ersatzschaltbild.load)
		self.destroyed.connect(self.doSomeDestruction)

	def doSomeDestruction(self):
		json_root().remove_call_back(self.ersatzschaltbild.load)

	def build_from_epi(self):
			data=json_root()
			if data.circuit.enabled==False:
				epi=get_epi()
				pos=3

				a=json_component()
				a.x0=pos
				a.y0=3
				a.x1=pos+1
				a.y1=3
				a.comp="bat"
				self.ersatzschaltbild.add_object(a)

				pos=pos+1
				
				for l in epi.layers:
					if l.layer_type=="active":# or l.layer_type=="contact":
						component=l.shape_electrical.electrical_component
						if component=="resistance":
							a=json_component()
							a.x0=pos
							a.y0=3
							a.x1=pos+1
							a.y1=3
							a.comp="resistor"
							self.ersatzschaltbild.add_object(a)
						if component=="diode":
							a=json_component()
							a.x0=pos
							a.y0=3
							a.x1=pos+1
							a.y1=3
							a.comp="diode"
							self.ersatzschaltbild.add_object(a)
						pos=pos+1

				a=json_component()
				a.x0=pos
				a.y0=3
				a.x1=pos+1
				a.y1=3
				a.comp="ground"
				self.ersatzschaltbild.add_object(a)

				self.ersatzschaltbild.objects_push()
			else:
				self.ersatzschaltbild.load()

	def callback_click(self,widget):
		for item in self.buttons:
			if item!="sep":
				item.setChecked(False)

		widget.setChecked(True)

		self.ersatzschaltbild.selected=widget.icon

