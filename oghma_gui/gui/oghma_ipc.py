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

if get_platform()=="linux" or get_platform()=="wine":
	import dbus
	from dbus.mainloop.glib import DBusGMainLoop
	DBusGMainLoop(set_as_default=True)

class ipc_data(ctypes.Structure):
	_fields_ = [('connection', ctypes.c_void_p ),
				('buf', ctypes.c_char * 4096 )]

class oghma_ipc(QWidget):
	new_data = gSignal(str)

	def __init__(self):
		QWidget.__init__(self)
		self.lib=sim_paths.get_dll_py()
		self.lib.ipc_read.restype = ctypes.c_int

	def windows_pipe_read(self,data):
		while(1):
			ret = self.lib.ipc_read(ctypes.byref(data))
			if ret >=0:
				decoded_data=bytes2str(ctypes.cast(data.buf, ctypes.c_char_p).value) 
				self.new_data.emit(decoded_data)
			else:
				print("no more data")
				break
			#except:
			#	print("pipe closed")
			#	break
#		win32pipe.DisconnectNamedPipe(p)

	def callback_dbus(self,bus, message):
		data=message.get_member()
		if data!=None:
			self.new_data.emit(data)

	def windows_main_loop(self):
		while(1):
			data=ipc_data()
			self.lib.ipc_open_listen(ctypes.byref(data))
			th = Thread(target=self.windows_pipe_read, args=(data,))
			th.daemon = True
			th.start()

	def start(self):
		if get_platform()=="linux":
			self.bus = dbus.SessionBus()
			self.bus.add_match_string_non_blocking("type='signal',interface='org.my.oghmanano'")
			self.bus.add_message_filter(self.callback_dbus)
		elif get_platform()=="wine":
			self.bus = dbus.SessionBus()
			self.bus.add_match_string_non_blocking("type='signal',interface='org.my.oghmanano'")
			self.bus.add_message_filter(self.callback_dbus)
		else:
			p = Thread(target=self.windows_main_loop)
			p.daemon = True
			p.start()


