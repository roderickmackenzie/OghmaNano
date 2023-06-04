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
import shutil
import re
import glob
from util_zip import zip_get_data_file
from util_zip import zip_get_raw_data
from math import pow
from bytes2str import bytes2str
from cal_path import sim_paths
import ctypes

def peek_data(file_name):
	try:
		text=zip_get_raw_data(file_name,bytes=100)
		if text==False:
			return b"none"
		return text
	except:
		pass
	return b"none"

def wrap_text(text,width):
	count=0
	r=False
	out=""
	for i in range(0,len(text)):
		if count>width:
			r=True
		else:
			r=False
		
		add=text[i]
		if r==True:
			if text[i]==" ":
				add="\n"
				count=0
		
		out=out+add
				
		count=count+1
	return out

def gui_print_path(text,path,length):
	remove=len(text)+len(path)-length
	if remove>0:
		ret=text+path[remove:]
	else:
		ret=text+path

	return ret

def is_number(data_in):
	try:
		float(data_in)
		return True
	except ValueError:
		return False

	return False

def isfiletype(file_name,ext_in):
	ext=ext_in
	if ext.startswith(".")==False:
		ext="."+ext
	if file_name.endswith(ext):
		return True
	return False


def pygtk_to_latex_subscript(in_string):
	out_string=in_string.replace("<sub>","_{")
	out_string=out_string.replace("</sub>","}")
	out_string=out_string.replace("<sup>","^{")
	out_string=out_string.replace("</sup>","}")
	return out_string

def latex_to_html(in_string):
	in_string=bytes2str(in_string)
	out=re.compile(r"_\{([^\]]*?)\}").sub("<sub>\\1</sub>", in_string)
	out=re.compile(r"\^\{([^\]]*?)\}").sub("<sup>\\1</sup>", out)
	return out

def time_with_units(time):
	buf = (ctypes.c_char * 64)()
	mul_ = (ctypes.POINTER(ctypes.c_double) * 1)()

	sim_paths.get_dll_py().get_time_dim(buf,ctypes.byref(mul_),ctypes.c_double(time))

	mul=ctypes.cast(mul_, ctypes.POINTER(ctypes.c_double)).contents.value
	units=bytes2str(ctypes.cast(buf, ctypes.c_char_p).value)
	return mul,units

def fx_with_units(fx):
	buf = (ctypes.c_char * 64)()
	mul_ = (ctypes.POINTER(ctypes.c_double) * 1)()

	sim_paths.get_dll_py().fx_with_units(buf,ctypes.byref(mul_),ctypes.c_double(distance))

	mul=ctypes.cast(mul_, ctypes.POINTER(ctypes.c_double)).contents.value
	units=bytes2str(ctypes.cast(buf, ctypes.c_char_p).value)
	return mul,units

def distance_with_units(distance):
	buf = (ctypes.c_char * 64)()
	mul_ = (ctypes.POINTER(ctypes.c_double) * 1)()

	sim_paths.get_dll_py().get_meter_dim(buf,ctypes.byref(mul_),ctypes.c_double(distance))

	mul=ctypes.cast(mul_, ctypes.POINTER(ctypes.c_double)).contents.value
	units=bytes2str(ctypes.cast(buf, ctypes.c_char_p).value)
	return mul,units

def wavelength_to_rgb(wavelength):
	r_int = (ctypes.POINTER(ctypes.c_int) * 1)()
	g_int = (ctypes.POINTER(ctypes.c_int) * 1)()
	b_int = (ctypes.POINTER(ctypes.c_int) * 1)()

	sim_paths.get_dll_py().wavelength_to_rgb(ctypes.byref(r_int),ctypes.byref(g_int),ctypes.byref(b_int),ctypes.c_double(wavelength*1e-9))

	r=ctypes.cast(r_int, ctypes.POINTER(ctypes.c_int)).contents.value/255.0
	g=ctypes.cast(g_int, ctypes.POINTER(ctypes.c_int)).contents.value/255.0
	b=ctypes.cast(b_int, ctypes.POINTER(ctypes.c_int)).contents.value/255.0

	return r,g,b

