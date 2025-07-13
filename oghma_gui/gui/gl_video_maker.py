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

## @package gl_video_maker
#  The main tab class, used to display material properties.
#

import os

from token_lib import tokens
from undo import undo_list_class
from help import help_window

from gQtCore import gSignal

from PySide2.QtWidgets import QTextEdit,QWidget, QScrollArea,QVBoxLayout,QLabel,QHBoxLayout,QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,QComboBox,QGridLayout,QLineEdit, QToolBar,QAction
from gQtCore import QSize, Qt
from PySide2.QtGui import QPixmap, QIcon

from icon_lib import icon_get

from gQtCore import QTimer

import i18n
_ = i18n.language.gettext

from error_dlg import error_dlg

from experiment_bin import experiment_bin
from tab_jv import tab_jv
from error_dlg import error_dlg
from json_c import json_tree_c

class gl_video_maker(experiment_bin):

	changed = gSignal()

	def __init__(self,gl_widget):
		experiment_bin.__init__(self,"tab_jv",window_save_name="tab_gl_video_maker", window_title=_("Flyby video maker"),json_search_path="gl.flybys",icon="fly")
		self.bin=json_tree_c()

		self.tb_start = QAction(icon_get("fly"), _("Set\nposition"), self)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_start)
		self.tb_start.triggered.connect(self.callback_set_pos)

		self.tb_goto = QAction(icon_get("fly"), _("Goto"), self)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_goto)
		self.tb_goto.triggered.connect(self.callback_goto)

		self.tb_run = QAction(icon_get("forward"), _("Run"), self)
		self.ribbon.file.insertAction(self.ribbon.tb_rename,self.tb_run)
		self.tb_run.triggered.connect(self.callback_run)

		self.gl_widget=gl_widget

	def callback_goto(self):
		tab = self.notebook.currentWidget()
		if tab==None:
			return
		path=self.bin.find_path_by_uid("gl.flybys",tab.uid)

		self.gl_widget.gl_main.view_target.xRot=self.bin.get_token_value(path,"xRot")
		self.gl_widget.gl_main.view_target.yRot=self.bin.get_token_value(path,"yRot")
		self.gl_widget.gl_main.view_target.zRot=self.bin.get_token_value(path,"zRot")
		self.gl_widget.gl_main.view_target.x_pos=self.bin.get_token_value(path,"x_pos")
		self.gl_widget.gl_main.view_target.y_pos=self.bin.get_token_value(path,"y_pos")
		self.gl_widget.gl_main.view_target.zoom=self.bin.get_token_value(path,"zoom")

		self.gl_widget.timer=QTimer()
		self.gl_widget.timer.timeout.connect(self.gl_widget.ftimer_target)
		self.gl_widget.timer.start(25)

	def set_edit(self,editable):
		self.tab.editable=editable

	def callback_set_pos(self):
		tab = self.notebook.currentWidget()
		if tab==None:
			return
		path=self.bin.find_path_by_uid("gl.flybys",tab.uid)

		self.bin.set_token_value(path,"xRot",self.gl_widget.gl_main.active_view.contents.xRot)
		self.bin.set_token_value(path,"yRot",self.gl_widget.gl_main.active_view.contents.yRot)
		self.bin.set_token_value(path,"zRot",self.gl_widget.gl_main.active_view.contents.zRot)
		self.bin.set_token_value(path,"x_pos",self.gl_widget.gl_main.active_view.contents.x_pos)
		self.bin.set_token_value(path,"y_pos",self.gl_widget.gl_main.active_view.contents.y_pos)
		self.bin.set_token_value(path,"zoom",self.gl_widget.gl_main.active_view.contents.zoom)

		self.bin.save()
		tab.tab.tab.update_values()


	def callback_run(self):
		if (self.gl_widget.width() % 2) != 0:
			error_dlg(self,_("window width not divisible by two"))
			return
		if (self.gl_widget.height() % 2) != 0:
			error_dlg(self,_("window height not divisible by two"))
			return

		path="gl.flybys.segment0"

		self.gl_widget.gl_main.view_target.xRot=self.bin.get_token_value(path,"xRot")
		self.gl_widget.gl_main.view_target.yRot=self.bin.get_token_value(path,"yRot")
		self.gl_widget.gl_main.view_target.zRot=self.bin.get_token_value(path,"zRot")
		self.gl_widget.gl_main.view_target.x_pos=self.bin.get_token_value(path,"x_pos")
		self.gl_widget.gl_main.view_target.y_pos=self.bin.get_token_value(path,"y_pos")
		self.gl_widget.gl_main.view_target.zoom=self.bin.get_token_value(path,"zoom")
		self.gl_widget.gl_main.active_view.contents.max_angle_shift=1.0

		self.next=1
		self.set_next_target()

	def set_next_target(self):
		segments=self.bin.get_token_value("gl.flybys","segments")

		if self.next<segments:
			path="gl.flybys.segment"+str(self.next)
			self.gl_widget.gl_main.view_target.xRot=self.bin.get_token_value(path,"xRot")
			self.gl_widget.gl_main.view_target.yRot=self.bin.get_token_value(path,"yRot")
			self.gl_widget.gl_main.view_target.zRot=self.bin.get_token_value(path,"zRot")
			self.gl_widget.gl_main.view_target.x_pos=self.bin.get_token_value(path,"x_pos")
			self.gl_widget.gl_main.view_target.y_pos=self.bin.get_token_value(path,"y_pos")
			self.gl_widget.gl_main.view_target.zoom=self.bin.get_token_value(path,"zoom")
			self.gl_widget.gl_main.active_view.max_angle_shift=1.0
			self.next=self.next+1

			self.gl_widget.timer_save_files=True
			self.gl_widget.timer_end_callback=self.callback_timer_end
			self.gl_widget.timer=QTimer()
			self.gl_widget.timer.timeout.connect(self.gl_widget.ftimer_target)
			self.gl_widget.timer.start(250)
			return True
		return False

	def callback_timer_end(self):
		print(self.gl_widget.timer_save_files_number)
		if self.gl_widget.timer_save_files_number==0:
			return

		if self.set_next_target()==True:
			print("oh")
			return

		out_file_name=os.path.join(os.getcwd(),"flyby","movie.mp4")
		files_list_path=os.path.join(os.getcwd(),"flyby","files.txt")
		f=open(files_list_path,"w")
		for i in range(0,self.gl_widget.timer_save_files_number):
			
			f.write(os.path.join(os.getcwd(),"flyby",str(i)+".jpg"+"\n"))
		f.close()
		
		fps=int(float(self.gl_widget.timer_save_files_number)/5.0)
		encode_line="mencoder mf://@"+files_list_path+" -mf type=jpg:fps="+str(fps)+" -o "+out_file_name+" -ovc x264"
		encode_line2="\nffmpeg -i movie.mp4 -r 15 -vf scale=-1:-1 -ss 00:00:1 movie.gif"

		f=open(os.path.join(os.getcwd(),"flyby","encode.sh"),"w")
		f.write(encode_line+encode_line2)
		f.close()

		os.system(encode_line)

		self.gl_widget.timer_save_files=False
		self.gl_widget.timer_save_files_number=0
