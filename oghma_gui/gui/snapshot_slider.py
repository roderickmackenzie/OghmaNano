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

## @package snapshot_slider
#  A slider to scroll through simulation snapshots.
#
import os

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QSlider,QHBoxLayout,QLabel,QComboBox,QAbstractItemView
from PySide2.QtGui import QPainter,QIcon
from gQtCore import gSignal

from gQtCore import QTimer
from icon_lib import icon_get
from g_tab2_bin import g_tab2_bin
from json_c import json_c

class snapshot_slider(QWidget):

	changed = gSignal()

	def __init__(self,path):
		QWidget.__init__(self)
		self.bin=json_c("snapshots")
		self.bin.build_template()
		self.bin.load(os.path.join(path,"data.json"))
		self.path=path
		self.timer=None
		self.files=[]
		self.tb_play = QAction(icon_get("media-playback-start"), _("Play"), self)
		self.tb_play.triggered.connect(self.timer_toggle)

		self.setWindowTitle(_("Snapshot slider")) 
		
		self.main_vbox = QVBoxLayout()

		self.slider_hbox0= QHBoxLayout()
		
		self.slider0 = QSlider(Qt.Horizontal)

		self.slider0.setTickPosition(QSlider.TicksBelow)
		self.slider0.setTickInterval(5)
		self.slider0.valueChanged.connect(self.slider0_change)

		self.slider_hbox0.addWidget(self.slider0)

		self.label0 = QLabel()
		self.label0.setText("")

		pos=self.bin.get_token_value("","pos")
		if pos==None:
			pos=1
		self.slider0.setValue(pos)

		self.slider_hbox0.addWidget(self.label0)

		self.widget0=QWidget()
		self.widget0.setLayout(self.slider_hbox0)

		self.main_vbox.addWidget(self.widget0)

		self.toolbar=QToolBar()
		self.main_vbox.addWidget(self.toolbar)

		self.tab=g_tab2_bin(toolbar=self.toolbar,json_bin=self.bin)
		self.tab.verticalHeader().setVisible(True)
		self.tab.set_tokens(["snapshot_file","snapshot_plot_type"])
		self.tab.set_labels([ _("File to plot"),_("Plot type")])
		self.tab.dir_path=self.find_template_dir()
		self.tab.setMinimumSize(self.width(), 120)
		self.tab.setColumnWidth(0, 400)
		self.tab.json_root_path="list"

		self.tab.populate()
		
		self.tab.changed.connect(self.on_cell_edited)

		self.main_vbox.addWidget(self.tab)

		self.setLayout(self.main_vbox)
		self.update_slider_max()

	def find_template_dir(self):
		for i in range(0,100):
			dir_name=os.path.join(self.path,str(i))
			if os.path.isdir(dir_name)==True:
				return dir_name

		return os.path.join(self.path,"0")

	def update_slider_max(self):
		self.files=[]
		all_files=os.listdir(self.path)
		all_files = [f for f in all_files if f.isdigit()]
		all_files=sorted(all_files, key=int)
		if os.path.isdir(self.path)==True:
			for f in all_files: 
				file_name=os.path.join(self.path,f)
				if os.path.isdir(file_name):
					self.files.append(file_name)
		
		self.slider0.setMaximum(len(self.files))

	def __del__(self):
		self.bin.free()

	def on_cell_edited(self):
		self.bin.save()
		self.changed.emit()

	def slider0_change(self):
		value = self.slider0.value()
		self.label0.setText(str(value))
		self.bin.set_token_value("","pos",value)
		self.bin.save()
		self.changed.emit()

	def get_file_names(self):
		files=[]
		plot_types=[]

		val=self.slider0.value()
		if val>=len(self.files):
			return [],[]

		for y in range(0,self.tab.rowCount()):
			file_path=os.path.join(self.files[val],self.tab.get_value(y,0))
			if os.path.isfile(file_path)==True:
				files.append(file_path)
				plot_types.append(self.tab.get_value(y,1))

		return files,plot_types

	def update_files_combo(self):
		for y in range(0,self.tab.rowCount()):
			self.cellWidget(y, 0).update()

	#animation
	def timer_toggle(self):
		if self.timer==None:
			self.timer=QTimer()
			self.timer.timeout.connect(self.slider_auto_incroment)
			self.timer.start(100)
			self.tb_play.setIcon(icon_get("media-playback-pause"))
		else:
			self.anim_stop()

	def anim_stop(self):
		if self.timer!=None:
			self.timer.stop()
			self.timer=None
			self.tb_play.setIcon(icon_get("media-playback-start"))

	def slider_auto_incroment(self):
		val=self.slider0.value()
		val=val+1
		if val>self.slider0.maximum():
			val=0
		self.slider0.setValue(val)
