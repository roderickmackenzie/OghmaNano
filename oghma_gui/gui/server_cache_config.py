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
from json_root import json_root
from gui_util import yes_no_dlg
from msg_dlg import msg_dlg

class server_cache_config(QWidgetSavePos):

	def __init__(self):
		QWidgetSavePos.__init__(self,"server_cache_config")
		self.setWindowIcon(icon_get("cache"))
		self.setMinimumSize(800,300)
		config=json_root().electrical_solver.cache

		self.setWindowTitle2("Cache editor")
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle = self.frameGeometry()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

		vbox=QVBoxLayout()

		self.title_text=QLabel("OghmaNano cache editor:  OghmaNano uses a disk based cached to accelerate simulation, use this window to either increase the size of the cache or to clear the cache.  If you want to save disk space clear the cache, if you want fast simulations increase the size of the cache.")
		self.title_text.setFont(QFont('SansSerif', 15))
		#self.title_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.title_text.setWordWrap(True)
		vbox.addWidget(self.title_text)

		self.progress=g_progress()
		self.progress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.progress.setMinimumSize(-1,50)
		vbox.addWidget(self.progress)

		self.data_text=QLabel()
		self.data_text.setFont(QFont('SansSerif', 15))

		self.data_text.setWordWrap(True)
		vbox.addWidget(self.data_text)

		#spin
		spin_widget=QWidget()
		spin_widget_layout=QHBoxLayout()
		spin_widget.setLayout(spin_widget_layout)

		spin_label=QLabel(_("Maximum size in Mb:"))
		spin_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		spin_widget_layout.addWidget(spin_label)

		self.spin=QSpinBox()
		self.spin.setMaximum(1e6)
		self.spin.setValue(config.cache_max_size)

		spin_widget_layout.addWidget(self.spin)

		self.spin.valueChanged.connect(self.callback_spin_edited)
		vbox.addWidget(spin_widget)

		#Cache path
		cache_path_widget=QWidget()
		cache_path_layout=QHBoxLayout()
		cache_path_widget.setLayout(cache_path_layout)

		cache_path_label=QLabel(_("Cache path:"))
		cache_path_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		cache_path_layout.addWidget(cache_path_label)

		self.cache_path_text = QLineEdit()
		self.cache_path_text.setText(self.get_cache_path())
		self.cache_path_text.textChanged.connect(self.callback_cache_path)
		cache_path_layout.addWidget(self.cache_path_text)
		vbox.addWidget(cache_path_widget)

		#turn off cache
		widget=QWidget()
		widget.setMinimumSize(-1,50)
		widget_layout=QHBoxLayout()
		widget.setLayout(widget_layout)

		label=QLabel(("Cache enabled:"))
		label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		widget_layout.addWidget(label)

		self.enable_switch=gtkswitch()
		self.enable_switch.set_value(config.cache_enabled)
		self.enable_switch.changed.connect(self.callback_enabled)
		widget_layout.addWidget(self.enable_switch)

		vbox.addWidget(widget)

		##
		button_box=QHBoxLayout()

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		button_box.addWidget(spacer)

		self.clear=QPushButton("Clear cache", self)
		self.clear.clicked.connect(self.callback_clear_cache)
		button_box.addWidget(self.clear)


		button_box_widget=QWidget()
		button_box_widget.setLayout(button_box)
		vbox.addWidget(button_box_widget)

		self.setLayout(vbox)
		self.update_progress()
		self.show()

	def callback_cache_path(self):
		config=json_root().electrical_solver.cache
		json_root().electrical_solver.cache.cache_path=self.cache_path_text.text()
		json_root().save()

	def get_cache_path(self):
		config=json_root().electrical_solver.cache
		if config.cache_path=="none_none_none_default":
			return os.path.join(sim_paths.get_user_settings_dir(),"cache")
		else:
			return json_root().electrical_solver.cache.cache_path


	def callback_enabled(self):
		config=json_root().electrical_solver.cache
		config.cache_enabled= not config.cache_enabled
		json_root().save()

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
		config=json_root().electrical_solver.cache
		self.progress.setValue(self.cur_size/config.cache_max_size)
		self.data_text.setText(str(self.cur_size)+"Mb used of "+str(config.cache_max_size)+"Mb used.")

	def callback_spin_edited(self):
		config=json_root().electrical_solver.cache
		config.cache_max_size=self.spin.value()
		json_root().save()
		self.update_progress()

	def get_size(self):
		tot = 0
		for dirpath, dirnames, filenames in os.walk(self.get_cache_path()):
			for f in filenames:
			    fp = os.path.join(dirpath, f)
			    if not os.path.islink(fp):
			        tot += os.path.getsize(fp)

		return tot/1024/1024

