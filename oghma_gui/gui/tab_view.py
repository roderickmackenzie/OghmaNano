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

## @package tab_view
#  A tab used to show the results of the simulation.
#

from layer_widget import layer_widget
from help import help_window

from PySide2.QtWidgets import QWidget,QHBoxLayout,QSplitter
from gQtCore import Qt

import i18n
_ = i18n.language.gettext

from dir_viewer import dir_viewer
from cal_path import sim_paths
from server import server_get

class tab_view(QWidget):

		
	def __init__(self):
		QWidget.__init__(self)

		hbox=QHBoxLayout(self)
		QSplitter(Qt.Horizontal)
		self.viewer=dir_viewer(sim_paths.get_sim_path())
		self.viewer.data.allow_navigation=True
		self.viewer.set_directory_view(True)
		self.viewer.data.show_back_arrow=True
		self.viewer.set_multi_select()
		
		hbox.addWidget(self.viewer)
		
		self.setLayout(hbox)
		server_get().sim_finished.connect(self.refresh)
		
	def refresh(self):
		self.viewer.fill_store()

	def help(self):
		help_window().help_set_help("device.png",_("<big><b>The device structure tab</b></big>\n Use this tab to change the structure of the device, the layer thicknesses and to perform optical simulations.  You can also browse the materials data base and  edit the electrical mesh."))

	def got_help(self,data):
		if data!="":
			help_window().help_append("star.png",_("<big><b>Update available!</b></big><br>"+data))
