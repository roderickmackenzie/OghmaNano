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

## @package register
#  Registration window
#



#qt
from gQtCore import Qt 
from PySide2.QtWidgets import QWidget,QDialog

from error_dlg import error_dlg
from lock import lock
from gQtCore import QTimer
from gQtCore import gSignal
from lock_register import register

from lock import get_lock
from lock_trial import lock_trial
from msg_dlg import msg_dlg

from cal_path import get_image_file_path
from help import help_window
from sim_name import sim_name
from bytes2str import bytes2str

class lock_gui(QWidget):
	#disable_all=gSignal()
	#enable_all=gSignal()


	def timer_callback(self):
		self.timer.stop()

		if get_lock().get_next_gui_action()=="register":
			self.register=register()
			ret=self.register.run()
			if ret==QDialog.Accepted:
				get_lock().check_license_thread()
				from video import video
				self.v=video()
				self.v.show()
				get_lock().registered=True
				#text="Thank you for registering."

				#msgBox = msg_dlg()

				#msgBox.setText(text)


				#msgBox.exec_()
				#self.enable_all.emit()
				return
			else:
				return

		if get_lock().status=="expired":
			self.trial=lock_trial(override_text="<br><br>Thank you for using "+sim_name.name+".  "+sim_name.name.capitalize()+" can only continue to exist if users support it by buying licenses.  Your license has expired, please purchase a new one.  Thank you for using "+sim_name.name+".<br>",title_font_size=14)
			ret=self.trial.run()
			if ret==QDialog.Accepted:
				msgBox = msg_dlg()
				msgBox.setText("Thank you for buying "+sim_name.name)
				msgBox.exec_()
		#if get_lock().is_disabled()==True:
		#	self.disable_all.emit()

		get_lock().check_license_thread()

		
		if get_lock().get_next_gui_action()=="no_internet":
			msgBox = msg_dlg()
			msgBox.setText("I can not connect to the update server.  "+sim_name.name.capitalize()+" may not be able to run.  Please connect to the internet.")
			msgBox.exec_()
			return

		if get_lock().update_available==True:
			help_window().help_append(["star.png",_("<big><b>Update available!</b></big><br>Download it now from <a href=\""+sim_name.web+"\">"+sim_name.web+"</a>")])

		if bytes2str(get_lock().message)!="":
			msgBox = msg_dlg()
			msgBox.setText(bytes2str(get_lock().message))
			msgBox.exec_()

	def __init__(self):
		QWidget.__init__(self)
		self.timer=QTimer()
		self.timer.timeout.connect(self.timer_callback)
		self.update_available=False

	def run(self):
		self.timer.start(1000)


