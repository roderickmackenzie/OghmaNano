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
from help import QAction_help
from QAction_lock import QAction_lock
from cal_path import sim_paths
from QWidgetSavePos import QWidgetSavePos

class server_config(QWidgetSavePos):

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

		self.tb_benchmark = QAction_lock("cpu", _("RNG\ntest"), self,"hardware_benchmark")
		toolbar.addAction(self.tb_benchmark)
		self.tb_benchmark.clicked.connect(self.callback_rand_test)

		self.tb_color_test = QAction_lock("cpu", _("Color map\ntest"), self,"hardware_benchmark")
		toolbar.addAction(self.tb_color_test)
		self.tb_color_test.clicked.connect(self.callback_color_test)

		self.tb_clear_newton_cache = QAction_lock("clean", _("Clear\nNewton cache"), self,"clean_newton_cache")
		toolbar.addAction(self.tb_clear_newton_cache)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		toolbar.addWidget(spacer)


		self.help = QAction_help()
		toolbar.addAction(self.help)
		self.main_vbox.addWidget(toolbar)

		

		self.notebook = QTabWidget()

		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)

		tab=tab_class("server")
		self.notebook.addTab(tab,_("CPU/GPU configuration"))

		self.cache_config=server_cache_config()
		self.notebook.addTab(self.cache_config,_("Newton cache"))
		self.tb_clear_newton_cache.clicked.connect(self.cache_config.callback_clear_cache)

		tab=tab_class("math.random")
		self.notebook.addTab(tab,_("Random numbers"))

		tab=tab_class("math.matrix")
		self.notebook.addTab(tab,_("Matrix solvers"))

		self.my_server=server_get()
		self.setLayout(self.main_vbox)
		self.notebook.currentChanged.connect(self.callback_tab_changed)


		self.callback_tab_changed()

	def callback_benchmark(self):
		self.my_server.clear_jobs()
		self.my_server.add_job(sim_paths.get_sim_path(),"--benchmark")
		#self.my_server.sim_finished.connect(self.optics_sim_finished)
		self.my_server.start()

	def callback_rand_test(self):
		self.my_server.clear_jobs()
		self.my_server.add_job(sim_paths.get_sim_path(),"--rand-test")
		self.my_server.start()

	def callback_color_test(self):
		self.my_server.clear_jobs()
		self.my_server.add_job(sim_paths.get_sim_path(),"--color-test")
		self.my_server.start()

	def callback_tab_changed(self):
		index = self.notebook.currentIndex()
		tab_ml=self.notebook.currentWidget()
		if self.notebook.tabText(index)==_("Newton cache"):
			self.tb_clear_newton_cache.setEnabled(True)
		else:
			self.tb_clear_newton_cache.setEnabled(False)

