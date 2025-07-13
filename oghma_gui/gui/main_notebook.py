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

## @package main_notebook
#  The main notebook for the main window.
#


import os
import random

#tabs
from tab_main import tab_main
from tab import tab_class

#qt
from PySide2.QtWidgets import QTabWidget,QWidget

#window
from tab_terminal import tab_terminal


from help import help_window

import i18n
_ = i18n.language.gettext

from global_objects import global_object_register
from cal_path import sim_paths

from tab_view import tab_view

from circuit_editor import circuit_editor
from display_mesh import display_mesh
from inp import inp
from mesh_math import mesh_math
from json_c import json_tree_c

from information_noweb import information
from oghma_QTabWidget import oghma_QTabWidget

class main_notebook(oghma_QTabWidget):
	item_factory=None


	def __init__(self):
		oghma_QTabWidget.__init__(self)
		self.bin=json_tree_c()
		self.terminal=None
		self.update_display_function=None
		self.currentChanged.connect(self.changed_click)
		global_object_register("notebook_goto_page",self.goto_page)
		self.state_loaded=False
		self.display_mesh=None

	def update(self):
		for i in range(0,self.count()):
			w=self.widget(i)
			w.update()

	def changed_click(self):

		if self.tabText(self.currentIndex()).strip()==_("Device structure"):
			help_window().help_set_help("device.png",_("<big><b>The device structure tab</b></big><br> Use this tab to change the structure of the device, the layer thicknesses and to perform optical simulations.  You can also browse the materials data base and  edit the electrical mesh."))

		if self.tabText(self.currentIndex()).strip()==_("Terminal"):
			help_window().help_set_help("utilities-terminal.png",_("<big><b>The terminal window</b></big><br>The output of the model will be displayed in this window, watch this screen for debugging and convergence information."))

		if self.tabText(self.currentIndex()).strip()==_("Tutorials/Documentation"):
			help_window().help_set_help("help.png",_("<big><b>Tutorials/Documentation</b></big><br>Here you can find tutorials, videos, worksheets, and talks about this software and simulating opto-electronic devices in general.  Although this software is easy to use with it's friendly interface, under the hood it is a highly complex model and powerful model, it is worth taking time to read the documentation to understand it.  This will enable you to get the most out of this software and your experimental data."))
			help_window().help_append("youtube",_("<big><b><a href=\"https://youtu.be/XBbaogu61Ps\">Watch the video</a></b></big><br> Performing my first solar cell simulation"))

		if self.tabText(self.currentIndex()).strip()==_("Output"):
			help_window().help_set_help("dat_file.png",_("<big><b>Output</b></big><br>This shows the root simulation directory, this is where the results are stored.  Double click on a file to see what is in it.."))

	def get_current_page(self):
		i=self.currentIndex()
		return self.tabText(i)

	def add_info_page(self):
		files=os.listdir(sim_paths.get_html_path())
		info_files=[]
		for i in range(0,len(files)):
			if files[i].startswith("info") and files[i].endswith("html"):
				info_files.append(files[i])
		file_name=random.choice(info_files)


		browser=information(file_name)

		self.addTab(browser,_("Information"))

	def add_docs_page(self):
		browser=information("docs.html")

		self.addTab(browser,_("Tutorials/Documentation"))

	def load(self):
		self.clear()
		self.last_page=0

		#self.setTabsClosable(True)
		self.setMovable(True)
		if inp().isfile(os.path.join(sim_paths.get_sim_path(),"sim.json"))==True:

			self.tab_main=tab_main()
			self.addTab(self.tab_main,_("Device structure"))

			self.update_circuit_window()

			self.update_display_function=self.tab_main.update
			#self.tab_main.three_d.display.force_redraw()

			self.terminal=tab_terminal()
			self.terminal.init()
			self.addTab(self.terminal,_("Terminal"))
			self.terminal.run(os.getcwd(),sim_paths.get_exe_command()+" --version2 --gui --html")
			global_object_register("terminal",self.terminal)

			widget=tab_view()
			widget.viewer.fill_store()
			self.addTab(widget,_("Output"))
			self.add_docs_page()
			self.state_loaded=True

		else:
			self.add_info_page()
			self.goto_page(_("Information"))
			self.state_loaded=False

	def update_circuit_window(self):
		mesh_x=mesh_math("electrical_solver.mesh.mesh_x")
		mesh_z=mesh_math("electrical_solver.mesh.mesh_z")

		next_tab=None
		if self.bin.get_token_value("electrical_solver","solver_type")=="circuit":
			if  mesh_x.get_points()==1 and mesh_z.get_points()==1:
				next_tab=circuit_editor()
			else:
				next_tab=display_mesh()

		if self.display_mesh!=next_tab:
			if self.display_mesh!=None:
				index=self.indexOf(self.display_mesh)
				self.removeTab(index)
			self.display_mesh=next_tab
			if self.display_mesh!=None:
				self.insertTab(1,self.display_mesh,_("Circuit diagram"))

	def is_loaded(self):
		return self.state_loaded

	def setEnabled(self,val):
		for i in range(0,self.count()):
			w=self.widget(i)
			w.setEnabled(val)


