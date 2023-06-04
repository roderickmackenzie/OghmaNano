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

## @package dat_file
#  Load and dump a dat file into a dat class
#

from util_zip import zip_get_data_file
from inp import inp_save_lines_to_file
		#self.lib.dat_file_save(bytes(file_name, encoding='utf8'),ctypes.byref(self))
def dat_files_to_csv(file_name,data):
	if file_name.endswith(".csv")==False:
		file_name=file_name+".csv"

	max=data[0].y_len
	for d in data:
		if d.y_len>max:
			max=d.y_len
	out=[]
	line=""
	for i in range(0,len(data)):
		line=line+str(data[i].key_text)+" "+str(data[i].y_label)+","+str(data[i].key_text)+" "+str(data[i].data_label)+","

	line=line[:-1]
	out.append(line)

	for i in range(0,max):
		line=""
		for ii in range(0,len(data)):
			y_text=""
			data_text=""
			if i<data[ii].y_len:
				y_text=str('{:.8e}'.format(float(data[ii].y_scale[i])))
				data_text=str('{:.8e}'.format(float(data[ii].data[0][0][i])))
			line=line+y_text+","+data_text+","
		line=line[:-1]
		out.append(line)

	inp_save_lines_to_file(file_name,out)


