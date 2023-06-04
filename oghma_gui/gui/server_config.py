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

from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget
from PySide2.QtGui import QPainter,QIcon

#python modules

#windows
from tab import tab_class
from server import server_get
from gQtCore import gSignal
from QWidgetSavePos import QWidgetSavePos
from json_root import json_root
from help import QAction_help
from QAction_lock import QAction_lock
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos

class server_config(QWidgetSavePos):

	def callback_tab_changed(self):
		self.changed.emit()

	def __init__(self):
		from server_cache_config import server_cache_config

		QWidgetSavePos.__init__(self,"server_config")
		
		self.setMinimumSize(900, 600)
		self.setWindowIcon(icon_get("cpu"))

		self.setWindowTitle2(_("Configure hardware")) 
		

		self.main_vbox = QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)

		self.tb_benchmark = QAction_lock("cpu", _("Hardware\nbenchmark"), self,"hardware_benchmark")
		toolbar.addAction(self.tb_benchmark)
		self.tb_benchmark.clicked.connect(self.callback_benchmark)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		toolbar.addWidget(spacer)


		self.help = QAction_help()
		toolbar.addAction(self.help)
		self.main_vbox.addWidget(toolbar)

		

		self.notebook = QTabWidget()

		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)

		data=json_root()

		tab=tab_class(data.server)
		self.notebook.addTab(tab,_("Server configuration"))

		self.cache_config=server_cache_config()
		self.notebook.addTab(self.cache_config,_("Cache"))
		self.my_server=server_get()
		self.setLayout(self.main_vbox)

	def callback_benchmark(self):
		self.my_server.clear_jobs()
		self.my_server.add_job(sim_paths.get_sim_path(),"--benchmark")
		#self.my_server.sim_finished.connect(self.optics_sim_finished)
		self.my_server.start()


