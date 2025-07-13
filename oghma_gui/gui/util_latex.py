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

## @package util_latex
#  Latex helper routines
#

import os
import ctypes
from cal_path import sim_paths
from bytes2str import str2bytes,bytes2str
from json_c import json_string

class latex:
	def __init__(self):
		self.lines=[]
		self.lib=sim_paths.get_dll_py()

	def tab_start(self,labels):
		labels=",".join(labels)
		a=json_string()
		ret=self.lib.latex_tab_start(ctypes.byref(a), ctypes.c_char_p(str2bytes(labels)))
		ret=a.get_data()
		a.free()
		self.lines.append(ret.split("\n"))

	def tab_add_row(self,values):
		a=""
		for v in values:
			a=a+v+" &"
		a=a[:-1]
		a=a+"\\\\  \n"
		self.lines.append(a)

	def document_start(self):
		a=json_string()
		ret=self.lib.latex_document_start(ctypes.byref(a))
		ret=a.get_data()
		a.free()
		self.lines.append(ret.split("\n"))

	def latex_document_end(self):
		a=json_string()
		ret=self.lib.latex_document_end(ctypes.byref(a))
		ret=a.get_data()
		a.free()
		self.lines.append(ret.split("\n"))

	def tab_end(self,caption=""):
		a=json_string()
		ret=self.lib.latex_tab_end(ctypes.byref(a), ctypes.c_char_p(str2bytes(caption)))
		ret=a.get_data()
		a.free()
		self.lines.append(ret.split("\n"))

	def save(self,file_name):
		self.file_name=file_name
		dir_name=os.path.dirname(file_name)
		if os.path.isdir(dir_name)==False:
			os.mkdir(dir_name)

		out_file=open(file_name,"w")
		out_file.write("\n".join(self.lines))
		out_file.close()

	def make_jpg(self,ext=".jpg",makefile=False):
		#ext= os.path.splitext(self.file_name)[1]
		input_no_ext=os.path.splitext(self.file_name)[0]
		output_dir=os.path.dirname(self.file_name)
		if (ext==".pdf"):
			os.system("latex -interaction=batchmode --output-directory "+output_dir+" "+input_no_ext)
			os.system("dvipdf "+input_no_ext+".dvi")
			#os.system("mv "+input_no_ext+".pdf "+output)

		if (ext==".jpg"): 
			command0="latex -interaction=batchmode --output-directory "+output_dir+" "+input_no_ext
			command1="convert -trim -bordercolor White -border 20x10 +repage -density 300 "+input_no_ext+".dvi "+input_no_ext+".jpg"
			os.system(command0)
			os.system(command1)

		if makefile==True:
			out_file=open(os.path.join(output_dir,"makefile"),"w")
			out_file.write("main:\n")
			out_file.write("\tlatex -interaction=batchmode "+os.path.basename(input_no_ext)+"||true\n")
			out_file.write("\tconvert -trim -bordercolor White -border 20x10 +repage -density 300 "+os.path.basename(input_no_ext)+".dvi "+os.path.basename(input_no_ext)+".jpg\n")
			out_file.close()

	def number_to_latex(self,data):
		if type(data)==str:
			data=float(data)

		if data>0.01 and data<1000.0:
			return "{:.3f}".format(data)

		ret="%1.1e" % data
		if (ret.count('e')!=0):
			a,b=ret.split('e')
			b=b.replace("+","")
			ret=a+"\\e{"+b+"}"

		return ret

	def numbers_to_latex(self,data):
		a=json_string()
		ret=self.lib.latex_insert_number(ctypes.byref(a),str2bytes(data))
		if ret==-1:
			return None
		ret=a.get_data()
		a.free()
		return ret

	def str_to_latex(self,in_val):
		in_buf=ctypes.create_string_buffer(str2bytes(in_val),len(in_val)+100)
		self.lib.str_escape_latex(in_buf)
		return bytes2str(in_buf.value)



