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

## @package play
#  A play button
#


#qt
from gQtCore import gSignal
from PySide2.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PySide2.QtGui import QIcon
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QSizePolicy,QHBoxLayout,QPushButton,QDialog,QFileDialog,QToolBar,QMessageBox, QAction, QMenu

from icon_lib import icon_get

from color_map import color_map


class QColorMap(QAction,color_map):

	changed = gSignal()

	def setState(self,state):
		pass


	def __init__(self,parent):
		QAction.__init__(self)
		self.setIcon(icon_get("color-wheel"))
		self.setText(_("Colors"))
		color_map.__init__(self)
		self.color_menu = QMenu(parent)
		self.setMenu(self.color_menu)
		self.triggered.connect(self.callback_random)

		for name in self.get_color_names():
			menu_item=QAction(name, parent)
			self.color_menu.addAction(menu_item)
			menu_item.triggered.connect(self.callback_colors)
		
	def callback_random(self):
		self.find_random_map()
		self.changed.emit()

	def callback_colors(self):
		action = self.sender()
		self.find_map(action.text())
		self.changed.emit()

