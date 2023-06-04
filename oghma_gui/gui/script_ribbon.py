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

## @package optics_ribbon
#  The ribbon for the optics window
#


import os

from cal_path import get_css_path

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QMessageBox, QLineEdit, QToolButton
from PySide2.QtWidgets import QTabWidget

from icon_lib import icon_get

from about import about_dlg

from util import wrap_text
from ribbon_base import ribbon_base
from play import play
from QAction_lock import QAction_lock
from cal_path import sim_paths
import webbrowser
from g_open import g_open
from inp import inp
from cal_path import sim_paths
from help import QAction_help

class mode_button(QAction_lock):
	def __init__(self,image,text,s,name):
		QAction_lock.__init__(self,image,text,s,name)
		self.setCheckable(True)
		self.mode="full"



class script_ribbon(ribbon_base):

	def file(self):
		toolbar = QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(48, 48))

		self.tb_new = QAction_lock("document-new", _("New"), self,"ribbion_script_new")
		toolbar.addAction(self.tb_new)

		self.tb_rename = QAction_lock("rename", _("Rename"), self,"ribbion_script_rename")
		toolbar.addAction(self.tb_rename)

		self.run = play(self,"scripts_ribbon_run",run_text=wrap_text(_("Run"),3))
		toolbar.addAction(self.run)

		self.tb_save = QAction_lock("document-save", _("Save"), self,"ribbion_script_save")
		toolbar.addAction(self.tb_save)

		self.plot = QAction_lock("plot", _("Plot\nFile"), self,"ribbon_script_plot")
		self.plot.clicked.connect(self.callback_plot_select)
		toolbar.addAction(self.plot)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		self.hashtag = QAction(icon_get("json_file"), _("View raw\njson"), self)
		toolbar.addAction(self.hashtag)
		self.hashtag.triggered.connect(self.callback_view_json)

		self.help = QAction_help()
		toolbar.addAction(self.help)
		return toolbar

	def callback_plot_select(self):
		dialog=g_open(sim_paths.get_sim_path())
		dialog.show_directories=False
		dialog.exec_()		

	def update(self):
		return

	def callback_about_dialog(self):
		dlg=about_dlg()
		dlg.exec_()

	def __init__(self):
		QTabWidget.__init__(self)
		#self.setStyleSheet("QWidget {	background-color:cyan; }")

		self.about = QToolButton(self)
		self.about.setText(_("About"))
		self.about.pressed.connect(self.callback_about_dialog)

		self.setCornerWidget(self.about)

		w=self.file()
		self.addTab(w,_("File"))

		sheet=self.readStyleSheet(os.path.join(get_css_path(),"style.css"))
		if sheet!=None:
			sheet=str(sheet,'utf-8')
			self.setStyleSheet(sheet)

	def callback_view_json(self):
		f=inp()
		f.load(os.path.join(sim_paths.get_sim_path(),"sim.json"))
		f.save_as(os.path.join(sim_paths.get_tmp_path(),"sim.json"),dest="file")
		webbrowser.open(os.path.join(sim_paths.get_tmp_path(),"sim.json"))

