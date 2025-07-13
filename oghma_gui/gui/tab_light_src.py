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

## @package tab_light_src
#  A tab to hold diffent types of JV experiments.
#

import i18n
_ = i18n.language.gettext

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTabWidget
from PySide2.QtGui import QPainter,QIcon
from tab import tab_class
from css import css_apply
from global_objects import global_object_run
from optics_sources_tab import optics_light_src
from optics_filters_tab import optics_filters_tab

class tab_light_src(QTabWidget):

	def __init__(self,json_path,uid, json_postfix=None):
		QTabWidget.__init__(self)
		css_apply(self ,"tab_default.css")

		self.setMovable(True)
		self.light_src=optics_light_src("optical.light_sources.lights",uid,_("Light source (y0)"))
		self.addTab(self.light_src,_("Light source"))

		self.light_filters=optics_filters_tab("optical.light_sources.lights",uid,_("Filters (y0)"))
		self.addTab(self.light_filters,_("Filters"))

		self.configure=tab_class(json_path,uid=uid, json_postfix=json_postfix)
		self.addTab(self.configure,_("Configure"))
		self.configure.tab.changed.connect(self.callback_configure_changed)

	def update(self):
		self.light_src.update()
		self.light_filters.update()

	def callback_configure_changed(self,item):
		if item=="light_illuminate_from":
			global_object_run("gl_force_redraw")

