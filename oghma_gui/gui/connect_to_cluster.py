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

## @package connect_to_cluster
#  Dialog box to connect to the cluster.
#

import os

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QPushButton,QCheckBox,QHBoxLayout,QLabel,QWidget,QDialog,QVBoxLayout,QSizePolicy,QAction,QTabWidget,QMenu
from PySide2.QtGui import QIcon

#calpath
from icon_lib import icon_get
from error_dlg import error_dlg

from help import help_window

from tab import tab_class

from server import server_get
from json_local_root import json_local_root
from json_cluster import json_cluster_node
from sim_name import sim_name

class connect_to_cluster(QDialog):

	def callback_close(self):
		self.reject()

	def callback_connect(self):
		self.accept()

	def __init__(self):
		QDialog.__init__(self)
		data=json_local_root()
		self.main_vbox=QVBoxLayout()
		self.setFixedSize(600,450) 
		self.setWindowTitle(_("Connect to cluster")+sim_name.web_window_title)
		self.setWindowIcon(icon_get("si"))

		if data.cluster.segments==[]:
			data.cluster.segments.append(json_cluster_node())

		active_cluster_config=data.cluster.find_enabled_segment()

		self.viewer=tab_class(active_cluster_config.config)

		self.main_vbox.addWidget(self.viewer)

		self.hwidget=QWidget()


		self.myserver=server_get()
		if self.myserver.cluster==False:
			self.nextButton = QPushButton(_("Connect"))
			self.nextButton.setEnabled(False)
		else:
			self.nextButton = QPushButton(_("Disconnect"))

		self.cancelButton = QPushButton(_("Cancel"))

		self.files=[]

		hbox = QHBoxLayout()


		hbox.addStretch(1)
		hbox.addWidget(self.cancelButton)
		hbox.addWidget(self.nextButton)
		self.hwidget.setLayout(hbox)

		self.main_vbox.addWidget(self.hwidget)

		self.setLayout(self.main_vbox)

		self.nextButton.clicked.connect(self.callback_connect)
		self.cancelButton.clicked.connect(self.callback_close)




