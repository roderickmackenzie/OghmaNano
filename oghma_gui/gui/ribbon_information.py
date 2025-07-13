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

## @package ribbon_information
#  The information ribbon.
#


import os
from icon_lib import icon_get

#qt
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

import webbrowser
from help import help_window

from inp import inp

from cal_path import sim_paths
from util import wrap_text

from ribbon_page import ribbon_page
from sim_name import sim_name
from json_c import json_c

class ribbon_information(ribbon_page):
	def __init__(self):
		ribbon_page.__init__(self)
		self.simulation_notes_window=None

		self.simulation_notes = QAction(icon_get("text-x-generic"), _("Simulation\nNotes"), self)
		self.simulation_notes.triggered.connect(self.callback_simulation_notes)
		self.addAction(self.simulation_notes)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.addWidget(spacer)

		self.hints = QAction(icon_get("hints.png"), _("Hints\nWindow"), self)
		self.hints.triggered.connect(self.callback_help)
		self.addAction(self.hints)

		self.lang = QAction(icon_get("preferences-desktop-locale"), _("Interface\nLanguage"), self)
		self.lang.triggered.connect(self.callback_language)
		self.addAction(self.lang)

		self.forum = QAction(icon_get("forum"), _("User\nForum"), self)
		self.forum.triggered.connect(self.callback_forum)
		self.addAction(self.forum)


		self.paper = QAction(icon_get("pdf"), wrap_text(_("Assosiated paper"),8), self)
		self.paper.triggered.connect(self.callback_paper)
		self.addAction(self.paper)



		self.man = QAction(icon_get("internet-web-browser"), _("Documentation")+"\n", self)
		self.man.triggered.connect(self.callback_on_line_help)
		self.addAction(self.man)

	def update(self):
		if inp().isfile(os.path.join(sim_paths.get_sim_path(),"sim.bib"))==True:
			self.paper.setVisible(True)
		else:
			self.paper.setVisible(False)

	def setEnabled(self,val):
		self.license.setEnabled(val)
		self.ref.setEnabled(val)
		self.hints.setEnabled(val)
		self.youtube.setEnabled(val)
		self.man.setEnabled(val)

	def callback_license(self):
		webbrowser.open(sim_name.web+"/license.html")


	def callback_paper(self):
		a=json_c("file_defined")
		if a.load(os.path.join(sim_paths.get_sim_path(),"sim.bib"))==False:
			return

		text=a.bib_cite("simulation")
		a.free()
		if text!=None:
			if r.url!="":
				webbrowser.open(r.url)


	def callback_on_line_help(self):
		webbrowser.open(sim_name.web+"/docs.html")

	def callback_forum(self):
		webbrowser.open("https://www.oghma-nano.com/forum/")

	def callback_help(self):
		help_window().toggle_visible()
			

	def callback_language(self):
		from config_window import class_config_window
		from tab_lang import language_tab_class
		self.config_window=class_config_window([],[])
		lang_tab=language_tab_class()
		self.config_window.notebook.addTab(lang_tab,_("Language"))
		self.config_window.show()

	def callback_simulation_notes(self):
		help_window().help_set_help("si.png",_("<big><b>Record notes about the simulation here</b></big><br>Use this window to make notes about the simulation."))


		if self.simulation_notes_window==None:
			from window_simulation_notes import window_simulation_notes
			self.simulation_notes_window=window_simulation_notes()

		if self.simulation_notes_window.isVisible()==True:
			self.simulation_notes_window.hide()
		else:
			self.simulation_notes_window.show()
