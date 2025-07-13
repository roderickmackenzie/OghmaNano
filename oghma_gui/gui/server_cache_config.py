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

import os

from gQtCore import QDir, Qt, QUrl
from PySide2.QtWidgets import QHBoxLayout,QSpinBox, QLineEdit, QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget,QDesktopWidget
from PySide2.QtWidgets import QWidget, QPushButton, QAction
from PySide2.QtGui import QIcon

from cal_path import sim_paths

from progress_class import progress_class
from PySide2.QtGui import QFont
from g_progress import g_progress

from icon_lib import icon_get
from safe_delete import safe_delete
from gtkswitch import gtkswitch
from QWidgetSavePos import QWidgetSavePos
from gui_util import yes_no_dlg
from msg_dlg import msg_dlg
from json_viewer_bin import json_viewer_bin
from json_c import json_tree_c

class server_cache_config(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"server_cache_config")
		vbox=QVBoxLayout()
		self.bin=json_tree_c()
		self.tab=json_viewer_bin(self.bin)
		self.tab.populate("electrical_solver.cache")
		self.tab.changed.connect(self.callback_edit)

		vbox.addWidget(self.tab)

		#turn off cache
		widget=QWidget()
		widget.setMinimumSize(150,50)
		widget_layout=QHBoxLayout()
		widget.setLayout(widget_layout)

		#Cache path
		cache_path_widget=QWidget()
		cache_path_layout=QHBoxLayout()
		cache_path_widget.setLayout(cache_path_layout)

		cache_path_label=QLabel(_("Cache path:"))
		cache_path_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		cache_path_layout.addWidget(cache_path_label)

		#progress bar
		self.title_text=QLabel(_("Newton cache used"))
		self.title_text.setFont(QFont('SansSerif', 15))
		#self.title_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.title_text.setWordWrap(True)
		vbox.addWidget(self.title_text)

		self.progress=g_progress()
		self.progress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.progress.setMinimumSize(50,25)
		vbox.addWidget(self.progress)

		self.data_text=QLabel()
		self.data_text.setFont(QFont('SansSerif', 15))

		self.data_text.setWordWrap(True)
		vbox.addWidget(self.data_text)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		vbox.addWidget(spacer)

		self.setLayout(vbox)
		self.update_progress()
		self.show()

	def get_cache_path(self):
		cache_path=self.bin.get_token_value("electrical_solver.cache","cache_path")
		if cache_path=="none_none_none_default":
			return sim_paths.get_newton_cache_path()
		else:
			return cache_path

	def callback_clear_cache(self):
		path=self.get_cache_path()
		files=[]
		if os.path.isdir(path)==False:
			msgBox = msg_dlg()
			msgBox.setText(_("The cache directory does not exist"))
			msgBox.exec_()
			return

		if path.endswith("cache"):
			for f in os.listdir(path):
				if f.startswith("oghma_cache_") and f.endswith(".dat"):
					files.append(os.path.join(path,f))
		else:
			msgBox = msg_dlg()
			msgBox.setText(_("The cache path needs to end in cache."))
			msgBox.exec_()
			return

		if len(files)==0:
			msgBox = msg_dlg()
			msgBox.setText(_("The cache is empty"))
			msgBox.exec_()
			return

		short=",".join(files)
		if len(short)>1000:
			short=short[:1000]

		response=yes_no_dlg(self,"Do you want to delete the following files: "+short)
		if response == True:
			for f in files:
				os.remove(os.path.join(path,f))

			self.update_progress()
			msgBox = msg_dlg()
			msgBox.setText(_("I have emptied the cache"))
			msgBox.exec_()
		else:
			return

	def update_progress(self):
		self.cur_size=round(self.get_size())
		cache_max_size=self.bin.get_token_value("electrical_solver.cache","cache_max_size")
		self.progress.setValue(self.cur_size/cache_max_size)
		self.data_text.setText(str(self.cur_size)+"Mb used of "+str(cache_max_size)+"Mb used.")

	def get_size(self):
		tot = 0
		for dirpath, dirnames, filenames in os.walk(self.get_cache_path()):
			for f in filenames:
			    fp = os.path.join(dirpath, f)
			    if not os.path.islink(fp):
			        tot += os.path.getsize(fp)

		return tot/1024/1024

	def callback_edit(self,token):
		self.update_progress()
		self.bin.save()

