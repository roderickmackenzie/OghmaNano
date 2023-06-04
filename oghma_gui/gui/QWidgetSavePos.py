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

from PySide2.QtWidgets import QWidget

from json_local_root import json_local_root
from json_local_root import json_save_window
from PySide2.QtWidgets import QWidget, QDesktopWidget
from sim_name import sim_name

def resize_window_to_be_sane(window,x,y):
	shape=QDesktopWidget().screenGeometry()
	w=int(shape.width()*x)
	h=int(shape.height()*y)
	window.resize(w,h)

class QWidgetSavePos(QWidget):

	def closeEvent(self, event):
		event.accept()
		
	def moveEvent(self,event):
		if self.window_name=="center":
			return

		data=json_local_root()
		x=self.x()
		y=self.y()
		for seg in data.windows.segments:
			if seg.name==self.window_name:
				seg.x=x
				seg.y=y
				data.save()
				break

		event.accept()

	def setWindowTitle2(self,text):
		self.setWindowTitle(text+sim_name.web_window_title)

	def __init__(self,window_name):
		QWidget.__init__(self)
		self.window_name=window_name

		data=json_local_root()
		found=False

		shape=QDesktopWidget()#.screenGeometry()

		desktop_w=shape.width()
		desktop_h=shape.height()

		w=self.width()
		h=self.height()
		sain_x=desktop_w/2-w/2
		sain_y=desktop_h/2-h/2

		if window_name!="center":
			for seg in data.windows.segments:
				#print(seg.name,window_name)
				if seg.name==window_name:

					x=int(seg.x)
					y=int(seg.y)
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
			a=json_save_window()
			a.name=window_name
			a.x=sain_x
			a.y=sain_y
			self.move(a.x,a.y)
			data.windows.segments.append(a)
			data.save()
