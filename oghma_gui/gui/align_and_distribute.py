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

## @package align_and_distribute
#  Align and distribute widget
#

#qt
from PySide2.QtWidgets import QAction
from gQtCore import QSize
from PySide2.QtWidgets import QVBoxLayout,QToolBar,QToolBar, QAction, QLabel
from QWidgetSavePos import QWidgetSavePos
from icon_lib import icon_get
from json_c import json_tree_c
from bytes2str import str2bytes
import ctypes

class align_and_distribute(QWidgetSavePos):
	def __init__(self,gl_interface):
		QWidgetSavePos.__init__(self,"align_and_distribute")
		self.bin=json_tree_c()
		self.main_vbox = QVBoxLayout()

		self.setWindowIcon(icon_get("thermal_kappa"))

		self.setWindowTitle2(_("Align and distribute")) 
		self.gl_interface=gl_interface
		toolbar_x=QToolBar()
		toolbar_x.setIconSize(QSize(48, 48))

		#spacer = QWidget()
		#spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.label_x=QLabel(_("x"))
		self.main_vbox.addWidget(self.label_x)

		self.align_left_x = QAction(icon_get("align_left"), _("Left"), self)
		toolbar_x.addAction(self.align_left_x)
		self.align_left_x.triggered.connect(self.callback_align_left_x)

		self.align_right_x = QAction(icon_get("align_right"), _("Right"), self)
		toolbar_x.addAction(self.align_right_x)
		self.align_right_x.triggered.connect(self.callback_align_right_x)

		self.main_vbox.addWidget(toolbar_x)

		############
		toolbar_y=QToolBar()
		toolbar_y.setIconSize(QSize(48, 48))

		self.label_y=QLabel(_("y"))
		self.main_vbox.addWidget(self.label_y)

		self.distribute_y = QAction(icon_get("align_left"), _("Distribute"), self)
		toolbar_y.addAction(self.distribute_y)
		self.distribute_y.triggered.connect(self.callback_align_y_min)

		self.main_vbox.addWidget(toolbar_y)

		self.setLayout(self.main_vbox)

		############
		toolbar_z=QToolBar()
		toolbar_z.setIconSize(QSize(48, 48))

		self.label_z=QLabel(_("z"))
		self.main_vbox.addWidget(self.label_z)

		self.distribute_z = QAction(icon_get("distribute_x"), _("Distribute"), self)
		toolbar_z.addAction(self.distribute_z)
		self.distribute_z.triggered.connect(self.callback_distribute_z)

		self.main_vbox.addWidget(toolbar_z)

		self.setLayout(self.main_vbox)

	def callback_align_left_x(self):
		self.bin.lib.gl_objects_align(ctypes.byref(json_tree_c()), ctypes.byref(self.gl_interface.gl_main), ctypes.c_char_p(str2bytes("x0")), ctypes.c_int(True))
		self.bin.save()
		self.gl_interface.force_redraw() 

	def callback_align_y_min(self):
		self.bin.lib.gl_objects_align(ctypes.byref(json_tree_c()), ctypes.byref(self.gl_interface.gl_main), ctypes.c_char_p(str2bytes("y0")), ctypes.c_int(True))
		self.bin.save()
		self.gl_interface.force_redraw() 


	def callback_align_right_x(self):
		self.bin.lib.gl_objects_align(ctypes.byref(json_tree_c()), ctypes.byref(self.gl_interface.gl_main), ctypes.c_char_p(str2bytes("x0")), ctypes.c_int(False))
		self.bin.save()
		self.gl_interface.force_redraw() 


	def callback_distribute_z(self):
		self.bin.lib.gl_objects_distribute(ctypes.byref(json_tree_c()), ctypes.byref(self.gl_interface.gl_main), ctypes.c_char_p(str2bytes("z0")), ctypes.c_char_p(str2bytes("dz")))
		self.bin.save()
		self.gl_interface.force_redraw() 


