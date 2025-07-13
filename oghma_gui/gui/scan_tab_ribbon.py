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

## @package scan_tab_ribbon
#  The ribbon for the scan window.
#

import os

from cal_path import sim_paths

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QMenu
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar, QLineEdit, QToolButton
from PySide2.QtWidgets import QTabWidget

from icon_lib import icon_get

from about import about_dlg

from util import wrap_text

from ribbon_base import ribbon_base
from play import play

class scan_tab_ribbon(ribbon_base):
		

	def simulations(self):
		toolbar = QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(42, 42))

		self.tb_simulate = play(self,"scan_play",play_icon="forward",run_text=wrap_text(_("Run scan"),2))#QAction(icon_get("build_play2"), wrap_text(_("Run scan"),2), self)
		toolbar.addAction(self.tb_simulate)

		toolbar.addSeparator()

		self.tb_plot = QAction(icon_get("plot"), wrap_text(_("Plot"),4), self)
		toolbar.addAction(self.tb_plot)
	
		#self.tb_plot_time = QAction(icon_get("plot_time"), wrap_text(_("Time domain plot"),6), self)
		#toolbar.addAction(self.tb_plot_time)

		self.tb_clean = QAction(icon_get("clean"), wrap_text(_("Clean simulation"),4), self)
		toolbar.addAction(self.tb_clean)

		self.tb_optimizer = QAction(icon_get("optimizer"), wrap_text(_("Fast Optimizer"),3), self)
		self.tb_optimizer.setCheckable(True)

		self.menu_tb_optimizer = QMenu(self)
		self.menu_tb_optimizer_configure_item=QAction(_("Configure"), self)
		self.menu_tb_optimizer.addAction(self.menu_tb_optimizer_configure_item)
		self.tb_optimizer.setMenu(self.menu_tb_optimizer)
		toolbar.addAction(self.tb_optimizer)


		self.box_widget=QWidget()
		self.box=QVBoxLayout()
		self.box_widget.setLayout(self.box)
		self.box_tb0=QToolBar()
		self.box_tb0.setIconSize(QSize(32, 32))
		self.box.addWidget(self.box_tb0)
		self.box_tb1=QToolBar()
		self.box_tb1.setIconSize(QSize(32, 32))
		self.box.addWidget(self.box_tb1)
		
		self.tb_build = QAction(icon_get("cog"), wrap_text(_("Build scan"),2), self)
		self.box_tb0.addAction(self.tb_build)

		self.tb_rerun = QAction(icon_get("play-green"), wrap_text(_("Rerun"),2), self)
		#self.box_tb0.addAction(self.tb_rerun)

		self.tb_zip = QAction(icon_get("package-x-generic"), wrap_text(_("Archive simulations"),2), self)
		self.box_tb0.addAction(self.tb_zip)


		self.tb_notes = QAction(icon_get("text-x-generic"), wrap_text(_("Notes"),3), self)
		toolbar.addAction(self.tb_notes)

		toolbar.addWidget(self.box_widget)

		return toolbar

	def update(self):
		print("update")
		#self.device.update()
		#self.simulations.update()
		#self.configure.update()
		#self.home.update()

	def callback_about_dialog(self):
		dlg=about_dlg()
		dlg.exec_()

	def __init__(self):
		ribbon_base.__init__(self)
		self.setMaximumHeight(130)
		#self.setStyleSheet("QWidget {	background-color:cyan; }")

		self.about = QToolButton(self)
		self.about.setText(_("About"))
		self.about.pressed.connect(self.callback_about_dialog)

		self.setCornerWidget(self.about)

		
		w=self.simulations()
		self.addTab(w,_("Simulations"))

		#w=self.advanced()
		#self.addTab(w,_("Advanced"))

		#w=self.ml()
		#self.addTab(w,_("ML"))

		sheet=self.readStyleSheet(os.path.join(sim_paths.get_css_path(),"style.css"))
		if sheet!=None:
			sheet=str(sheet,'utf-8')
			self.setStyleSheet(sheet)

