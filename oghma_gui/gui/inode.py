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
import ctypes
from bytes2str import bytes2str
from cal_path import sim_paths



class inode(ctypes.Structure):
	_fields_ = [('icon', ctypes.c_char * 128),
				('file_name', ctypes.c_char * 256),
				('display_name', ctypes.c_char * 256),
				('hidden', ctypes.c_int),
				('type', ctypes.c_char * 128),
				('isdir', ctypes.c_int),
				('allow_navigation', ctypes.c_int),
				('sub_icon', ctypes.c_char * 128),
				('hide_this_json_file', ctypes.c_int),
				('view_type', ctypes.c_char * 256),
				('can_delete', ctypes.c_int)]

	def __init__(self):
		self.lib=sim_paths.get_dll_py()	
		self.lib.inode_init(ctypes.byref(self))

	def __str__(self):
		return bytes2str(self.file_name)+","+bytes2str(self.display_name)+","+bytes2str(self.icon)+","+bytes2str(self.type)+", hidden="+str(int(self.hidden))



