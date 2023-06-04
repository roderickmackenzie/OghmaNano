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

## @package ribbon_file
#  A ribbon for the file menu
#

from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt, gSignal
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu, QToolBar


from QAction_lock import QAction_lock
from used_files import used_files_load

from util import wrap_text

from scripts import scripts
from cite_me import cite_me
from ribbon_page import ribbon_page
from play import play
from server import server_get
from help import help_window
from global_objects import global_object_register
import webbrowser
from ribbon_page import ribbon_page

class ribbon_file(ribbon_page):
	used_files_click= gSignal(str)
	def __init__(self):
		ribbon_page.__init__(self)
		self.myserver=server_get()
		self.build_tutorial_list()

		self.home_new = QAction_lock("document-new", _("New simulation").replace(" ","\n"), self,"main_new")
		#self.home_new.setText(_("New\nsimulation"))
		self.addAction(self.home_new)

		self.old = QAction(icon_get("document-new"), _("New simulation").replace(" ","\n"), self)


		self.home_open = QAction_lock("document-open", _("Open\nsimulation"), self,"main_open")


		self.used_files_menu = QMenu(self)
		self.populate_used_file_menu()
		self.home_open.setMenu(self.used_files_menu)
		self.addAction(self.home_open)
		w=self.widgetForAction(self.home_open)
		w.setMinimumWidth(100)

		self.home_export = QAction_lock("zip", _("Export\nZip"), self,"main_zip")
		self.addAction(self.home_export)

		self.addSeparator()

		self.run = play(self,"main_play_button",run_text=wrap_text(_("Run\nsimulation"),2))
		server_get().sim_finished.connect(self.run.stop)
		server_get().sim_started.connect(self.run.start)
		self.run.setToolTip(_("Run simulation")+" (F9)")
		self.addAction(self.run)

		self.addSeparator()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.addWidget(spacer)

		self.tb_tutorials = QAction(icon_get("book"), _("Tutorials"), self)
		self.tb_tutorials.triggered.connect(self.callback_tutorials)
		self.tutorials_menu = QMenu(self)
		self.populate_tutorials_menu()
		self.tb_tutorials.setMenu(self.tutorials_menu)
		self.addAction(self.tb_tutorials)
		w=self.widgetForAction(self.tb_tutorials)
		w.setMinimumWidth(100)

		self.tb_manual = QAction(icon_get("book"), _("Manual"), self)
		self.tb_manual.triggered.connect(self.callback_manual)
		self.addAction(self.tb_manual)
		w=self.widgetForAction(self.tb_manual)
		w.setMinimumWidth(100)

		self.twitter = QAction(icon_get("twitter"), _("Follow on\nTwitter"), self)
		self.twitter.triggered.connect(self.callback_twitter)
		self.addAction(self.twitter)

		self.youtube = QAction(icon_get("youtube.png"), _("Subscribe\non Youtube"), self)
		self.youtube.triggered.connect(self.callback_youtube)
		self.addAction(self.youtube)

		self.addSeparator()

		self.cite_me=cite_me()
		if self.iconSize().width()>24:
			self.addWidget(self.cite_me)

		#self.home_help = QAction(icon_get("internet-web-browser"), _("Help"), self)
		#self.addAction(self.home_help)
		#self.tb_script_editor = QAction_lock("script", _("Script\nEditor"), self,"script_editor")
		#self.tb_script_editor.clicked.connect(self.callback_script)
		#self.addAction(self.tb_script_editor)


	def build_tutorial_list(self):
		self.tutorials=[]
		self.tutorials.append([_("Getting started"),"getting_started"])
		self.tutorials.append([_("1D Simulations"),"1d"])
		self.tutorials.append([_("Carrier trapping"),"trapping"])
		self.tutorials.append([_("2D electrical structures (OFETs)"),"2d"])
		self.tutorials.append([_("Large area devices/circuit models"),"large_area"])
		self.tutorials.append([_("OLEDs"),"oleds"])
		self.tutorials.append([_("Material databases"),"materials"])
		self.tutorials.append([_("Scripting"),"scripting"])
		self.tutorials.append([_("Frequency domain simulations"),"fxdomain"])
		self.tutorials.append([_("Transient simulations"),"transient"])
		self.tutorials.append([_("Optical simulations"),"optical"])
		self.tutorials.append([_("Excitonic simulations"),"excition"])
		self.tutorials.append([_("Fitting"),"fitting"])
		self.tutorials.append([_("Misc"),"misc"])
		self.tutorials.append([_("Basics"),"getting_started"])

	def populate_used_file_menu(self):
		self.used_files_menu.clear()
		files=used_files_load()
		for f in files:
			f=QAction(f, self)
			f.triggered.connect(self.callback_menu)
			self.used_files_menu.addAction(f)

	def populate_tutorials_menu(self):
		self.tutorials_menu.clear()

		for f in self.tutorials:
			new_menu_item=QAction(f[0], self)
			new_menu_item.triggered.connect(self.callback_tutorials_menu)
			self.tutorials_menu.addAction(new_menu_item)
		self.tutorials_menu.addSeparator()

		new_menu_item=QAction(_("Manual"), self)
		new_menu_item.triggered.connect(self.callback_manual)
		self.tutorials_menu.addAction(new_menu_item)

	def callback_tutorials_menu(self):
		action = self.sender()
		for t in self.tutorials:
			if t[0]==action.text():
				webbrowser.open("https://www.oghma-nano.com/docs.html?page=Videos#"+t[1])
				break

	def callback_menu(self):
		action = self.sender()
		self.used_files_click.emit(action.text())

	def update(self):

		self.populate_used_file_menu()


	def setEnabled(self,val,do_all=False):
		self.home_new.setEnabled(val)
		self.home_open.setEnabled(val)
		self.home_export.setEnabled(val)
		#self.plot.setEnabled(val)

	def setEnabled_other(self,val):
		self.home_export.setEnabled(val)
		#self.tb_script_editor.setEnabled(val)
		self.run.setEnabled(val)
		self.cite_me.setEnabled(val)


	def callback_tutorials(self):
		#w = self.widgetForAction(self.action_NewDataType);
		#m_ui->action_NewDataType->menu()->popup(w->mapToGlobal(QPoint(0, w->height())))
		webbrowser.open("https://www.oghma-nano.com/docs.html?page=Videos")

	def callback_manual(self):
		webbrowser.open("https://www.oghma-nano.com/docs.html?page=Manual")

	def callback_twitter(self):
		webbrowser.open("https://twitter.com/OghmaNano")

	def callback_youtube(self):
		webbrowser.open("https://www.youtube.com/channel/UCbm_0AKX1SpbMMT7jilxFfA")

