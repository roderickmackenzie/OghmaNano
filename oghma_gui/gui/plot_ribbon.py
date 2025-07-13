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

## @package plot_ribbon
#  A ribbon for the plot window
#


import os

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
from QAction_lock import QAction_lock
from cal_path import sim_paths
from QColorMap import QColorMap

class plot_ribbon(ribbon_base):

	def plot(self):
		self.plot_toolbar = QToolBar()
		self.plot_toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		self.plot_toolbar.setIconSize(QSize(42, 42))

		self.tb_home = QAction(icon_get("mpl_home"), _("Home"), self)
		self.tb_home.setCheckable(True)
		self.plot_toolbar.addAction(self.tb_home)

		self.tb_pointer = QAction(icon_get("pointer"), _("Pointer"), self)
		self.tb_pointer.setCheckable(True)
		self.plot_toolbar.addAction(self.tb_pointer)
		self.tb_pointer.setVisible(False)

		self.tb_zoom = QAction(icon_get("mpl_zoom_to_rect"), _("Zoom"), self)
		self.tb_zoom.setCheckable(True)
		self.plot_toolbar.addAction(self.tb_zoom)

		self.tb_move = QAction(icon_get("mpl_move"), _("Move"), self)
		self.tb_move.setCheckable(True)
		self.plot_toolbar.addAction(self.tb_move)

		self.tb_rotate = QAction(icon_get("rotate"), _("Rotate"), self)
		self.tb_rotate.setCheckable(True)
		self.plot_toolbar.addAction(self.tb_rotate)

		self.color_map=QColorMap(self)
		self.plot_toolbar.addAction(self.color_map)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.plot_toolbar.addWidget(spacer)

		return self.plot_toolbar


	def scale(self):
		toolbar = QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(42, 42))


		self.tb_scale_autoscale = QAction(icon_get("plot_log_x"), _("Autoscale"), self)
		self.tb_scale_autoscale.setCheckable(True)
		self.tb_scale_autoscale.setChecked(True)
		toolbar.addAction(self.tb_scale_autoscale)

		toolbar.addSeparator()

		self.tb_scale_log_x = QAction(icon_get("plot_log_x"), _("Log x"), self)
		self.tb_scale_log_x.setCheckable(True)
		toolbar.addAction(self.tb_scale_log_x)

		self.tb_scale_log_y = QAction(icon_get("plot_log_y"), _("Log y"), self)
		self.tb_scale_log_y.setCheckable(True)
		toolbar.addAction(self.tb_scale_log_y)

		self.tb_scale_log_z = QAction(icon_get("plot_log_y"), _("Log z"), self)
		self.tb_scale_log_z.setCheckable(True)
		toolbar.addAction(self.tb_scale_log_z)

		toolbar.addSeparator()

		self.tb_transpose = QAction(icon_get("rotate_right"), _("Transpose"), self)
		self.tb_transpose.setCheckable(True)
		toolbar.addAction(self.tb_transpose)

		toolbar.addSeparator()

		self.tb_flip_x = QAction(icon_get("plot_log_x"), _("Flip x"), self)
		self.tb_flip_x.setCheckable(True)
		toolbar.addAction(self.tb_flip_x)

		self.tb_flip_y = QAction(icon_get("plot_log_y"), _("Flip y"), self)
		self.tb_flip_y.setCheckable(True)
		toolbar.addAction(self.tb_flip_y)

		self.tb_flip_z = QAction(icon_get("plot_log_y"), _("Flip z"), self)
		self.tb_flip_z.setCheckable(True)
		toolbar.addAction(self.tb_flip_z)

		return toolbar


	def __init__(self):
		ribbon_base.__init__(self)
		#self.setMaximumHeight(130)
		#self.setStyleSheet("QWidget {	background-color:cyan; }")

		self.tab_plot=self.plot()
		self.addTab(self.tab_plot,_("Plot"))

		self.scale_toolbar=self.scale()
		self.addTab(self.scale_toolbar,_("Scale"))


		sheet=self.readStyleSheet(os.path.join(sim_paths.get_css_path(),"style.css"))
		if sheet!=None:
			sheet=str(sheet,'utf-8')
			self.setStyleSheet(sheet)

