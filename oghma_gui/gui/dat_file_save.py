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

from json_base import json_base
from bytes2str import bytes2str
class dat_file_save():

	def gen_header_new(self):
		a=json_base("none")
		a.include_name=False
		a.var_list=[]
		a.var_list.append(["title",bytes2str(self.title)])
		a.var_list.append(["type",bytes2str(self.type)])

		if self.x_label!=b"":
			a.var_list.append(["x_label",bytes2str(self.x_label)])

		if self.y_label!=b"":
			a.var_list.append(["y_label",bytes2str(self.y_label)])

		if self.z_label!=b"":
			a.var_list.append(["z_label",bytes2str(self.z_label)])

		if self.data_label!=b"":
			a.var_list.append(["data_label",bytes2str(self.data_label)])

		if self.x_units!=b"":
			a.var_list.append(["x_units",bytes2str(self.x_units)])
		if self.y_units!=b"":
			a.var_list.append(["y_units",bytes2str(self.y_units)])
		if self.z_units!=b"":
			a.var_list.append(["z_units",bytes2str(self.z_units)])

		if self.x_mul!=1.0:
			a.var_list.append(["x_mul",self.x_mul])

		if self.y_mul!=1.0:
			a.var_list.append(["y_mul",self.y_mul])

		if self.z_mul!=1.0:
			a.var_list.append(["z_mul",self.z_mul])

		if self.data_mul!=1.0:
			a.var_list.append(["data_mul",self.data_mul])


		if self.rgb_to_hex()!=None:
			a.var_list.append(["rgb ",self.rgb_to_hex()])

		if self.data_units!=b"":
			a.var_list.append(["data_units",bytes2str(self.data_units)])

		if self.logy!=False:
			a.var_list.append(["logscale_y",self.logy])

		if self.logx!=False:
			a.var_list.append(["logscale_x",self.logx])

		if self.logz!=False:
			a.var_list.append(["logscale_z",self.logz])

		if self.logdata!=False:
			a.var_list.append(["logscale_data",self.logdata])

		if self.icon!=None:
			a.var_list.append(["icon",self.icon])

		a.var_list.append(["time ",self.time])
		a.var_list.append(["Vexternal",self.Vexternal])
		a.var_list.append(["x_len",self.x_len])
		a.var_list.append(["y_len",self.y_len])
		a.var_list.append(["z_len",self.z_len])
		a.var_list.append(["cols","yd"])
		a.var_list_build()
		ret="#oghma_csv"+"".join(a.gen_json()).replace("\t","")+"*"
		return [ret]

	def gen_output_data(self):
		lines=self.gen_header_new()

		for i in range(0,self.y_len):
			y_text=str('{:.6e}'.format(float(self.y_scale[i])))
			data_text=str('{:.6e}'.format(float(self.data[0][0][i])))
			lines.append(y_text+"\t"+data_text)

		return lines

	def save_as_csv(self,file_name):
		if file_name.endswith(".csv")==False:
			file_name=file_name+".csv"

		lines=[]

		lines.append(self.y_label+","+self.data_label)

		for i in range(0,self.y_len):
			y_text=str('{:.8e}'.format(float(self.y_scale[i])))
			data_text=str('{:.8e}'.format(float(self.data[0][0][i])))
			lines.append(y_text+","+data_text)

		dump=""
		for item in lines:
			dump=dump+item+"\n"
			
		f=open(file_name, mode='w')
		lines = f.write(dump)
		f.close()

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

