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

## @package dat_file_math
#  Do math on the dat file class.
#

from bytes2str import bytes2str
import ctypes

class dat_file_save():

	def gen_output_data(self):
		self.lib.dat_file_reset(ctypes.byref(self))
		self.lib.buffer_add_json(ctypes.byref(self))
		lines=bytes2str(self.buf).splitlines()

		for i in range(0,self.y_len):
			y_text=str('{:.6e}'.format(float(self.y_scale[i])))
			data_text=str('{:.6e}'.format(float(self.data[0][0][i])))
			lines.append(y_text+"\t"+data_text)

		return lines

	def save_as_txt(self,file_name):
		if file_name.endswith(".txt")==False:
			file_name=file_name+".txt"

		lines=[]

		for i in range(0,self.y_len):
			y_text=str('{:.8e}'.format(float(self.y_scale[i])))
			data_text=str('{:.8e}'.format(float(self.data[0][0][i])))
			lines.append(y_text+" "+data_text)

		dump=""
		for item in lines:
			dump=dump+item+"\n"
			
		f=open(file_name, mode='w')
		lines = f.write(dump)
		f.close()

	def save(self,file_name):
		a = open(file_name, "w", encoding="utf-8")
		a.write("\n".join(self.gen_output_data()))
		a.close()

	def __str__(self):
		return "\n".join(self.gen_output_data())

	def dump_info(self):
		self.lib.dat_file_dump_info(ctypes.byref(self))
