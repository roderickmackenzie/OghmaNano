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

## @package gl_input
#  The mouse and keyboard input to the OpenGL display.
#

import sys
open_gl_ok=False

from math import fabs
from PySide2.QtWidgets import QApplication,QWidget,QVBoxLayout,QToolBar,QAction
from PySide2.QtGui import QCursor
from gQtCore import QSize, QTimer, Qt
import time
from icon_lib import icon_get
from gl_video_maker import gl_video_maker

class gl_toolbar():

	def __init__(self):
		#toolbar0
		self.toolbar0=QWidget()
		self.box0=QVBoxLayout()
		self.box0.setSpacing(0)
		self.box0.setContentsMargins(0, 0, 0, 0)
		self.toolbar0.setLayout(self.box0)
		self.box_tb0=QToolBar()
		self.box_tb0.setIconSize(QSize(32, 32))
		self.box0.addWidget(self.box_tb0)
		self.box_tb1=QToolBar()
		self.box_tb1.setIconSize(QSize(32, 32))
		self.box0.addWidget(self.box_tb1)

		self.xy = QAction(icon_get("xy"), _("xy"), self)
		self.box_tb0.addAction(self.xy)
		self.xy.triggered.connect(self.view_move_to_xy)

		self.yz = QAction(icon_get("yz"), _("yz"), self)
		self.box_tb0.addAction(self.yz)
		self.yz.triggered.connect(self.view_move_to_yz)

		self.xz = QAction(icon_get("xz"), _("xz"), self)
		self.box_tb1.addAction(self.xz)
		self.xz.triggered.connect(self.view_move_to_xz)

		self.tb_orthographic = QAction(icon_get("orthographic"), _("Orthographic"), self)
		self.box_tb1.addAction(self.tb_orthographic)
		self.tb_orthographic.triggered.connect(self.view_move_to_orthographic)


		#toolbar1
		self.toolbar1=QWidget()
		self.box1=QVBoxLayout()
		self.box1.setSpacing(0)
		self.box1.setContentsMargins(0, 0, 0, 0)
		self.toolbar1.setLayout(self.box1)
		self.box_tb2=QToolBar()
		self.box_tb2.setIconSize(QSize(32, 32))
		self.box1.addWidget(self.box_tb2)
		self.box_tb3=QToolBar()
		self.box_tb3.setIconSize(QSize(32, 32))
		self.box1.addWidget(self.box_tb3)


		self.tb_video = QAction(icon_get("fly"), _("Fly"), self)
		self.box_tb2.addAction(self.tb_video)
		self.tb_video.triggered.connect(self.callback_videomaker)

		self.tb_rotate = QAction(icon_get("rotate.png"), _("Rotate"), self)
		self.box_tb2.addAction(self.tb_rotate)
		self.tb_rotate.setEnabled(True)
		self.tb_rotate.triggered.connect(self.start_rotate)


	def callback_videomaker(self):
		self.video_maker_window=gl_video_maker(self)
		self.video_maker_window.show()

