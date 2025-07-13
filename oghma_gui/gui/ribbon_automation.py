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
from PySide2.QtWidgets import QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout,QPushButton, QLineEdit, QToolButton, QTextEdit, QAction, QTabWidget, QMenu

from lock import get_lock
from QAction_lock import QAction_lock
from used_files import used_files_load

from util import wrap_text

from cite_me import cite_me
from ribbon_page import ribbon_page
from help import help_window
from global_objects import global_object_register
import webbrowser
from lock import get_lock
from server import server_get

class ribbon_automation(ribbon_page):
	used_files_click= gSignal(str)
	def __init__(self):
		ribbon_page.__init__(self)

		self.window_ml=None
		self.window_probes=None
		self.scan_window=None
		self.fit_window=None
		self.tb_ml_build_vectors = QAction(icon_get("ml"), wrap_text(_("Machine\nLearning"),4), self)

		self.addAction(self.tb_ml_build_vectors)
		self.tb_ml_build_vectors.triggered.connect(self.callback_ml)

		self.tb_map_pin = QAction(icon_get("map_pin"), _("Edit\nProbes"), self)
		self.addAction(self.tb_map_pin)
		self.tb_map_pin.triggered.connect(self.callback_probes)

		self.scan = QAction_lock("scan", _("Parameter\nscan"), self,"ribbon_home_scan")
		self.scan.clicked.connect(self.callback_scan)
		self.addAction(self.scan)

		self.fit = QAction_lock("fit", _("Fit to\nexperiment"), self,"ribbon_home_fit")
		self.fit.clicked.connect(self.callback_run_fit)
		self.addAction(self.fit)

		self.json_tree_viewer = QAction(icon_get("json_file"), _("Json\nexplorer"), self)
		self.json_tree_viewer_menu = QMenu(self)
		self.json_tree_viewer.setMenu(self.json_tree_viewer_menu)
		self.addAction(self.json_tree_viewer)
		self.json_tree_viewer.triggered.connect(self.callback_json_tree_viewer)

		new_menu_item=QAction(icon_get("json_matlab"),_("Matlab paths"), self)
		new_menu_item.triggered.connect(self.callback_json_tree_viewer_matlab)
		self.json_tree_viewer_menu.addAction(new_menu_item)

		new_menu_item=QAction(icon_get("json_python"),_("Python paths"), self)
		new_menu_item.triggered.connect(self.callback_json_tree_viewer_python)
		self.json_tree_viewer_menu.addAction(new_menu_item)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.addWidget(spacer)

	def update(self):
		self.close_window(self.window_ml)
		self.close_window(self.scan_window)
		self.close_window(self.fit_window)

		self.fit.setVisible(True)

	def setEnabled(self,val,do_all=False):
		self.tb_ml_build_vectors.setEnabled(val)
		self.tb_map_pin.setEnabled(val)
		self.scan.setEnabled(val)
		self.json_tree_viewer.setEnabled(val)
		self.fit.setEnabled(val)

	def callback_probes(self):
		help_window().help_set_help("map_pin.png",_("<big><b>Probes window</b></big><br>Use this window to setup simulation probes, which can be used to extract values from the simulations at any given mesh point."))

		self.close_window(self.window_probes)
		from experiment_windows import window_probes
		self.window_probes=window_probes()
		self.show_window(self.window_probes)

	def callback_ml(self):
		help_window().help_set_help("ml.png",_("<big><b>Machine learning window</b></big><br>Use this window to generate machine learning vectors"))

		self.close_window(self.window_ml)
		from window_ml import window_ml
		self.window_ml=window_ml()
		self.show_window(self.window_ml)

	def callback_scan(self, widget):
		help_window().help_set_help("scan.png",_("<big><b>The scan window</b></big><br> Very often it is useful to be able to systematically very a device parameter such as mobility or density of trap states.  This window allows you to do just that."))
		help_window().help_append("list-add.png",_("Use the plus icon to add a new scan line to the list."))
		help_window().help_append("youtube",_("<big><b><a href=\"https://www.youtube.com/watch?v=cpkPht-CKeE\">Tutorial video</b></big><br>Using the parameter scan window."))

		self.close_window(self.scan_window)
		from window_scan import window_scan
		self.scan_window=window_scan()
		self.show_window(self.scan_window)

	def callback_json_tree_viewer(self):
		from window_json_tree_view import window_json_tree_view
		self.w=window_json_tree_view()
		self.w.show()

	def callback_json_tree_viewer_matlab(self):
		from window_json_tree_view import window_json_tree_view
		self.w=window_json_tree_view(language_mode="matlab")
		self.w.show()

	def callback_json_tree_viewer_python(self):
		from window_json_tree_view import window_json_tree_view
		self.w=window_json_tree_view(language_mode="python_json")
		self.w.show()

	def callback_run_fit(self, widget):
		self.close_window(self.fit_window)
		from fit_window import fit_window
		self.fit_window=fit_window()

		help_window().help_set_help("fit.png",_("<big><b>Fit window</b></big><br> Use this window to fit the simulation to experimental data.  The model uses advanced and optimized fitting algorithms to fit the model to your experimental data, so that material parameters such as mobilities and recombination rates can be extracted."))
		help_window().help_append("youtube",_("<big><b><a href=\"https://www.youtube.com/watch?v=61umU4hrsqk\">Watch the tutorial video 1</b></big><br>Fitting the model to experimental data to extract mobility and recombination rate parameters."))
		help_window().help_append("youtube",_("<big><b><a href=\"https://www.youtube.com/watch?v=_cm3Cb3kzUg\">Watch the tutorial video 2</b></big><br>Fitting the model to large area solar cells"))
		self.show_window(self.fit_window)
