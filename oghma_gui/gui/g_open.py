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

## @package g_open
#  A file viewer which uses the dir_viewer widget.
#

import os

#qt
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QMenu,QAbstractItemView,QAction,QToolBar,QDialog,QVBoxLayout,QDialog,QWidget,QLineEdit

#cal_path
from icon_lib import icon_get
from dir_viewer import dir_viewer
from util import wrap_text
from QWidgetSavePos import QWidgetSavePos
from sim_name import sim_name
from bytes2str import str2bytes
from bytes2str import bytes2str

import i18n
_ = i18n.language.gettext

class g_open_base(QVBoxLayout):
	def __init__(self,path,act_as_browser=True,big_toolbar=False,title=_("Open file"),fake_dir_structure=None):
		QVBoxLayout.__init__(self)
		self.act_as_browser=act_as_browser
		self.show_directories=True

		self.toolbar=QToolBar()
		if big_toolbar==True:
			self.toolbar.setIconSize(QSize(42, 42))
			self.toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)

		self.up = QAction(icon_get("go-up"), wrap_text(_("Back"),8), self)
		self.up.triggered.connect(self.on_up_clicked)
		self.toolbar.addAction(self.up)

		self.home = QAction(icon_get("user-home"), wrap_text(_("Home"),8), self)
		self.home.triggered.connect(self.on_home_clicked)
		self.toolbar.addAction(self.home)
	
		self.path_widget=QLineEdit()
		self.toolbar.addWidget(self.path_widget)

		self.addWidget(self.toolbar)

		if self.act_as_browser==False:
			self.viewer=dir_viewer(path,open_own_files=False,fake_dir_structure=fake_dir_structure)
		else:
			self.viewer=dir_viewer(path,fake_dir_structure=fake_dir_structure)

		self.viewer.set_directory_view(True)
		self.addWidget(self.viewer)

		self.root_dir= path

		self.path_widget.setText(path)

		self.viewer.path_changed.connect(self.change_path)

		self.change_path()


	def on_home_clicked(self, widget):
		self.viewer.data.path = str2bytes(self.root_dir)
		self.change_path()
		

	def change_path(self):
		self.path_widget.setText(bytes2str(self.viewer.data.path))

		self.viewer.fill_store()
		sensitive = True
		if bytes2str(self.viewer.data.path) == self.root_dir:
			sensitive = False

		self.up.setEnabled(sensitive)

	def on_up_clicked(self, widget):
		self.viewer.set_path(os.path.dirname(self.viewer.data.path))
		self.change_path()
		self.viewer.fill_store()

class g_open(QDialog):

	def __init__(self,path,act_as_browser=True,big_toolbar=False,title=_("Open file"),fake_dir_structure=None):
		QDialog.__init__(self)
		self.vbox=g_open_base(path,act_as_browser=act_as_browser,big_toolbar=big_toolbar,fake_dir_structure=fake_dir_structure)
		self.setLayout(self.vbox)
		self.resize(800,500)
		self.setWindowTitle(title+sim_name.web_window_title)
		self.setWindowIcon(icon_get("folder"))

		if act_as_browser==False:
			self.vbox.viewer.accept.connect(self.callback_accept)

		#self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
		#self.setModal(False)
		#self.setWindowModality(Qt.NonModal)

		self.show()

	def callback_accept(self):
		self.accept()

	def get_filename(self):
		return self.vbox.viewer.file_path

class g_open_window(QWidgetSavePos):

	def __init__(self,path,act_as_browser=True,big_toolbar=False,title=_("Open file")):
		QWidgetSavePos.__init__(self,"g_open_window")
		self.vbox=g_open_base(path,act_as_browser=act_as_browser,big_toolbar=big_toolbar)
		self.setLayout(self.vbox)
		self.resize(800,500)
		self.setWindowTitle2(title)
		self.setWindowIcon(icon_get("folder"))


