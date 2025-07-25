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

## @package progress
#  Progress bar window, when not in GUI mode it will do a text based one.
#


import sys
import time
from math import exp, isnan, isinf
from gui_enable import gui_get
	
class progress_base():
	def __init__(self):
		self.start_time=time.time()
		self.fraction=0.0
		self.finish_time=""
		self.elapsed_time=""
		self.avg=[]
		self.text=""

	def left_time(self):
		if self.fraction!=0:
			delta=(time.time()-self.start_time)*(1.0-self.fraction)/self.fraction
			t=time.time()+delta
			self.avg.append(t)
			if len(self.avg)>100:
				del self.avg[0]
			t=0.0
			
			l=len(self.avg)
			w_sum=0.0
			for i in range(0,l):
				weight=exp(-(l-i)*1e-1)
				t=t+self.avg[i]*weight
				w_sum=w_sum+weight
			if w_sum<=0.0:
				return
			t=t/w_sum

			self.finish_time=time.strftime('%A %H:%M:%S', time.localtime(t))

			s=time.time()-self.start_time
			hours, remainder = divmod(s, 3600)
			minutes, seconds = divmod(remainder, 60)

			self.elapsed_time='{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

	def draw(self):
		length=40
		full=int(self.fraction*length)
		empty=int((1.0-self.fraction)*length)
		sys.stdout.write('[')
		for i in range(0,full):
			sys.stdout.write('#')

		for i in range(0,empty):
			sys.stdout.write(' ')

		sys.stdout.write("] "+str(self.fraction*100.0)+"% \n")
		sys.stdout.write(self.text+"\n") 
		if self.finish_time!="":
			sys.stdout.write(_("Finish time:")+" "+self.finish_time+" "+self.elapsed_time+" \n")
			sys.stdout.write("\033[F\033[F\033[F")
		else:
			sys.stdout.write("\033[F\033[F")
		sys.stdout.flush()
	
	def enable_pulse(self,value):
		print("pulse")
		
	def set_fraction(self,fraction):
		if isnan(fraction)==True or isinf(fraction)==True:
			return False
		self.fraction=fraction
		self.left_time()
		if gui_get()==False:
			self.draw()
		return True

	def pulse(self):
		print("pulse")
		
	def start(self):
		self.draw()

	def show(self):
		self.draw()

	def stop(self):
		return
		print("stop")

	def set_text(self,text):
		self.text=text
		self.draw()
	
if gui_get()==True:

	from gQtCore import QSize, Qt
	from PySide2.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout,QLabel,QDesktopWidget
	from g_progress import g_progress
	from spinner import spinner
	from icon_lib import icon_get

	#from help import my_help_class

	class progress_class(QWidget,progress_base):

		def __init__(self):
			QWidget.__init__(self)
			progress_base.__init__(self)
			#self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
			self.setWindowTitle("Working...")
			image=icon_get("icon")
			if image!=False:
				self.setWindowIcon(image)
			self.setMinimumSize(400, 100)
			main_vbox = QVBoxLayout()
			hbox= QHBoxLayout()
			hbox.setContentsMargins(0, 0, 0, 0)
			self.progress = g_progress()
			self.spinner=spinner()

			hbox.addWidget(self.progress, 0)
			hbox.addWidget(self.spinner, 0)
			w=QWidget()
			w.setLayout(hbox)
			main_vbox.addWidget(w,0)

			self.label=QLabel()
			self.label.setText(_("Running")+"...")
			main_vbox.addWidget(self.label)

			self.label_time=QLabel()
			self.label_time.setText("")
			main_vbox.addWidget(self.label_time)


			self.setLayout(main_vbox)

		def hide_time(self):
			self.label_time.hide()
			self.setFixedSize(400, 70)

		def enable_pulse(self,value):
			self.progress.enablePulse(value)

		def set_fraction(self,fraction):
			if super().set_fraction(fraction)==False:
				return

			self.progress.setValue(fraction)
			if self.finish_time!="":
				self.label_time.setText(_("Finish time:")+" "+self.finish_time+" "+self.elapsed_time)

		def pulse(self):
			self.progress.pulse()
			
		def start(self,offset=True):
			if offset==True:
				shape=QDesktopWidget().screenGeometry()

				w=shape.width()
				shape.height()
				win_w=self.frameGeometry().width()
				self.frameGeometry().height()

				x=w-win_w
				y=0
				self.move(x,y)
			self.show()
			self.spinner.start()
			self.enable_pulse(False)

		def stop(self):
			self.hide()
			self.spinner.stop()

			#self.spin.stop()
			#my_help_class.help_show()

		def set_text(self,text):
			text=text
			l=len(text)
			if l>50:
				l=l-50
				text=text[l:]

			self.label.setText(text)

else:
	class progress_class(progress_base):

		def __init__(self):
			progress_base.__init__(self)


