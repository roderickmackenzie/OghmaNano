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

## @package oghma_ipc
#  A windows pipe class for communication with the backend
#

from threading import Thread

#qt
from gQtCore import  gSignal
from PySide2.QtWidgets import QWidget, QWidget
import ctypes
from cal_path import sim_paths
from win_lin import get_platform
from bytes2str import bytes2str

import time


class oghma_ipc_win_pipes():
	def windows_pipe_read(self,data):
		while(1):
			ret = self.lib.ipc_read(ctypes.byref(data))
			if ret >=0:
				decoded_data=bytes2str(ctypes.cast(data.buf, ctypes.c_char_p).value) 
				self.new_data.emit(decoded_data)
			else:
				print("no more data")
				break

	def windows_main_loop(self):
		while(1):
			self.lib.ipc_win_pipe_listen_open(ctypes.byref(self.data))
			th = Thread(target=self.windows_pipe_read, args=(self.data,))
			th.daemon = True
			th.start()

class oghma_ipc(QWidget,oghma_ipc_win_pipes):
	new_data = gSignal(str)

	def __init__(self,ipc_data):
		QWidget.__init__(self)
		self.data=ipc_data
		self.lib=sim_paths.get_dll_py()
		self.lib.ipc_read.restype = ctypes.c_int

	def callback_dbus(self,bus, message):
		data=message.get_member()
		if data!=None:
			self.new_data.emit(data)

	def dbus_main_loop(self):
		while(1):
			ret=self.lib.ipc_read(ctypes.byref(self.data))
			if ret == -2:
				time.sleep(1)

			if ret>0:
				decoded_data=bytes2str(ctypes.cast(self.data.buf, ctypes.c_char_p).value)
				for d in decoded_data.split("\n"):
					if len(d)>0:
						self.new_data.emit(d)

		#print("exit")

	def start(self):
		if get_platform()=="linux":
			self.lib.ipc_open_listen(ctypes.byref(self.data))
			p = Thread(target=self.dbus_main_loop)
			p.daemon = True
			p.start()
		elif get_platform()=="wine":
			self.lib.ipc_open_listen(ctypes.byref(self.data))
			p = Thread(target=self.dbus_main_loop)
			p.daemon = True
			p.start()
		else:
			#p = Thread(target=self.windows_main_loop)
			#p.daemon = True
			#p.start()
			self.lib.ipc_open_listen(ctypes.byref(self.data))
			p = Thread(target=self.dbus_main_loop)
			p.daemon = True
			p.start()


