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

## @package util
#  General helper functions.
#



import os
from cal_path import sim_paths
import ctypes
from bytes2str import bytes2str

class list_struct(ctypes.Structure):
	_fields_ = [('names', ctypes.POINTER(ctypes.c_char_p)),
				('len', ctypes.c_int ),
				('len_max', ctypes.c_int )]

class cpu_struct(ctypes.Structure):
	_fields_ = [('work_jiffies0', ctypes.c_double),
				('total_jiffies0', ctypes.c_double),
				('work_jiffies1', ctypes.c_double),
				('total_jiffies1', ctypes.c_double),
				('percent', ctypes.c_int)]

class g_io():

	def __init__(self):
		self.cpu=cpu_struct()
		self.lib=sim_paths.get_dll_py()
		self.lib.g_disk_writes.restype = ctypes.c_long
		self.lib.cpu_usage_init(ctypes.byref(self.cpu))


	def g_get_mounts(self):
		ret=[]
		a=list_struct()
		self.lib.g_get_mounts(ctypes.byref(a))
		for i in range(0,a.len):
			ret.append(bytes2str(a.names[i]))
		self.lib.list_free(ctypes.byref(a))
		return ret

	def cpu_usage_get(self):
		self.lib.cpu_usage_get(ctypes.byref(self.cpu))
		return self.cpu.percent
