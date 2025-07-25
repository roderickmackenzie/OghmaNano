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

## @package ribbon_cluster
#  A ribbon containing clustering commands.
#


from icon_lib import icon_get

#qt
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt,QFile,QIODevice
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton,QToolBar, QLineEdit, QToolButton, QTabWidget

#windows
from help import help_window
from server import server_get

from global_objects import global_object_run

from util import wrap_text
from ribbon_page import ribbon_page

class ribbon_cluster(ribbon_page):
	def __init__(self):
		ribbon_page.__init__(self)
		self.myserver=server_get()

		self.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		self.setIconSize(QSize(42, 42))

		self.cluster_get_data = QAction(icon_get("server_get_data"), wrap_text(_("Cluster get data"),8), self)
		self.cluster_get_data.triggered.connect(self.callback_cluster_get_data)
		self.addAction(self.cluster_get_data)
		self.cluster_get_data.setEnabled(False)

		self.cluster_copy_src = QAction(icon_get("server_copy_src"), wrap_text(_("Copy src to cluster"),8), self)
		self.cluster_copy_src.triggered.connect(self.callback_cluster_copy_src)
		self.addAction(self.cluster_copy_src)
		self.cluster_copy_src.setEnabled(False)

		self.cluster_make = QAction(icon_get("server_make"), wrap_text(_("Make on cluster"),6), self)
		self.cluster_make.triggered.connect(self.callback_cluster_make)
		self.addAction(self.cluster_make)
		self.cluster_make.setEnabled(False)

		self.cluster_clean = QAction(icon_get("server_clean"), wrap_text(_("Clean cluster"),8), self)
		self.cluster_clean.triggered.connect(self.callback_cluster_clean)
		self.addAction(self.cluster_clean)
		self.cluster_clean.setEnabled(False)

		self.cluster_off = QAction(icon_get("off"), wrap_text(_("Kill all cluster code"),8), self)
		self.cluster_off.triggered.connect(self.callback_cluster_off)
		self.addAction(self.cluster_off)
		self.cluster_off.setEnabled(False)


		self.cluster_sync = QAction(icon_get("sync"),  _("Sync"), self)
		self.cluster_sync.triggered.connect(self.callback_cluster_sync)
		self.addAction(self.cluster_sync)
		self.cluster_sync.setEnabled(False)

		self.config_cluster = QAction(icon_get("server"), _("Cluster"), self)
		self.config_cluster.setStatusTip(_("Cluster"))
		self.config_cluster.triggered.connect(self.callback_configure_cluster)
		self.config_cluster.setEnabled(False)
		self.addAction(self.config_cluster)


		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.addWidget(spacer)
		
		self.help = QAction(icon_get("internet-web-browser"), _("Help"), self)
		self.addAction(self.help)
		
	def callback_cluster_make(self):
		self.myserver.cluster_make()

	def callback_cluster_clean(self):
		self.myserver.cluster_clean()

	def callback_cluster_off(self):
		self.myserver.cluster_quit()
		self.update()

	def callback_cluster_sync(self):
		self.myserver.copy_src_to_cluster_fast()

	def callback_cluster_sleep(self):
		self.myserver.sleep()

	def callback_cluster_poweroff(self):
		self.myserver.poweroff()

	def callback_cluster_print_jobs(self):
		self.myserver.print_jobs()

	def callback_wol(self, widget, data):
		self.myserver.wake_nodes()

			
	def update(self):
		return
		if self.myserver.cluster==True:
			self.cluster_clean.setEnabled(True)
			self.cluster_make.setEnabled(True)
			self.cluster_copy_src.setEnabled(True)
			self.cluster_get_data.setEnabled(True)
			self.cluster_off.setEnabled(True)
			self.cluster_sync.setEnabled(True)
			self.config_cluster.setEnabled(True)

		else:
			self.cluster_clean.setEnabled(False)
			self.cluster_make.setEnabled(False)
			self.cluster_copy_src.setEnabled(False)
			self.cluster_get_data.setEnabled(False)
			self.cluster_off.setEnabled(False)
			self.cluster_sync.setEnabled(False)
			self.config_cluster.setEnabled(False)

	def setEnabled(self,val):
		print("")
		#self.undo.setEnabled(val)

	def callback_cluster_get_data(self):
		self.myserver.cluster_get_data()

	def callback_cluster_copy_src(self):
		self.myserver.copy_src_to_cluster()

	def callback_configure_cluster(self):
		from cluster_config_window import cluster_config_window
		self.win=cluster_config_window(self)
		self.win.show()

