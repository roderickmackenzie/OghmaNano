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

## @package QWidgetSavePos
#  A winndow base class which saves the window position.
#

from PySide2.QtWidgets import QWidget, QDesktopWidget
from PySide2.QtGui import QGuiApplication, QCursor
from json_c import json_local_root
from sim_name import sim_name
from json_c import json_tree_c
from PySide2.QtCore import QTimer

def resize_window_to_be_sane(window,x,y):
	shape=QDesktopWidget().screenGeometry()
	w=int(shape.width()*x)
	h=int(shape.height()*y)
	window.resize(w,h)

class QWidgetSavePos(QWidget):

	def __init__(self,window_name):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.bin_local=json_local_root()
		style_sheet=""

		r=self.bin.get_token_value("gui_config.interface","bk_r")
		g=self.bin.get_token_value("gui_config.interface","bk_g")
		b=self.bin.get_token_value("gui_config.interface","bk_b")
		if r!=-1.0:
			rgb=(r*255,g*255,b*244)
			style_sheet=style_sheet+"background-color: rgb(%d,%d,%d);" % rgb

		r=self.bin.get_token_value("gui_config.interface","col_text_r")
		g=self.bin.get_token_value("gui_config.interface","col_text_g")
		b=self.bin.get_token_value("gui_config.interface","col_text_b")
		if r!=-1.0:
			rgb=(r*255,g*255,b*244)
			style_sheet=style_sheet+"color: rgb(%d,%d,%d);" % rgb

		if style_sheet!="":
			#print(style_sheet)
			self.setStyleSheet(style_sheet)

		self.window_name=window_name
		if window_name=="center":
			screen = QGuiApplication.screenAt(QCursor().pos())
			fg = self.frameGeometry()
			fg.moveCenter(screen.geometry().center())
			self.move(fg.topLeft())
			return

		found=False

		shape=QDesktopWidget()

		desktop_w=shape.width()
		desktop_h=shape.height()

		w=self.width()
		h=self.height()
		sain_x=desktop_w/2-w/2
		sain_y=desktop_h/2-h/2

		segments=self.bin_local.get_token_value("windows","segments")
		for seg in range(0,segments):
			path="windows.segment"+str(seg)
			if self.bin_local.get_token_value(path,"name")==window_name:

				x=self.bin_local.get_token_value(path,"x")
				y=self.bin_local.get_token_value(path,"y")
				if (x+w>desktop_w) or x<0:
					x=sain_x
					#print("Reset with",x,desktop_w)
				if (y+h>desktop_h) or y<0:
					y=sain_y
					#print("Reset height",y)
				self.move(x,y)
				#print("moving to",x,y)
				found=True
				break

		if found==False:
			path=self.bin_local.make_new_segment("windows","",-1)
			self.bin_local.set_token_value(path,"name",window_name)
			self.bin_local.set_token_value(path,"x",sain_x)
			self.bin_local.set_token_value(path,"y",sain_y)
			self.move(sain_x,sain_y)
			self.bin_local.save()

		self.move_timer = QTimer()
		self.move_timer.setSingleShot(True)
		self.move_timer.timeout.connect(self.on_move_end)
		self.last_position = self.pos()

	def closeEvent(self, event):
		event.accept()
		
	def moveEvent(self,event):
		if self.window_name=="center":
			return

		self.move_timer.start(100)
		self.last_position = self.pos()
		event.accept()

	def on_move_end(self):
		if self.window_name=="center":
			return

		new_position = self.pos()
		#print(new_position,self.last_position)
		if new_position == self.last_position:
			x=self.x()
			y=self.y()
			segments=self.bin_local.get_token_value("windows","segments")
			for seg in range(0,segments):
				path="windows.segment"+str(seg)
				if self.bin_local.get_token_value(path,"name")==self.window_name:
					self.bin_local.set_token_value(path,"x",x)
					self.bin_local.set_token_value(path,"y",y)
					self.bin_local.save()
					break


	def setWindowTitle2(self,text):
		self.setWindowTitle(text+sim_name.web_window_title)


