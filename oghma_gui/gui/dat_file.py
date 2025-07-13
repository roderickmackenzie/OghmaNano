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

import os
from util_zip import zip_get_data_file
from inp import inp
from quiver import quiver
from util import is_number
from dat_file_math import dat_file_math
import codecs
from dat_file_save import dat_file_save
from cal_path import sim_paths
import ctypes
from bytes2str import bytes2str
from bytes2str import str2bytes
from vec import vec
from g_io import list_struct
from dat_file_decode import dat_file_decode
from color_map import rgb_char

class dat_file_display_options(ctypes.Structure):
	_fields_ = [('normal_graph', ctypes.c_int),
				('threeD_world', ctypes.c_int)]

class dat_file_trap_map(ctypes.Structure):

	_fields_ = [('Ec_f', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) )) ),
				('nf', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) )) ),
				('Ec', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) ))) ),
				('nt', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) ))) ),
				('Ev_f', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) )) ),
				('pf', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) )) ),
				('Ev', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) ))) ),
				('pt', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) ))) ),
				('Ec_max', ctypes.c_double),
				('Ev_min', ctypes.c_double)]

class dat_file(dat_file_math,dat_file_save,dat_file_decode,ctypes.Structure):

	_fields_ = [('title', ctypes.c_char * 100),
					('type', ctypes.c_char * 100),
					('x_mul', ctypes.c_double),
					('y_mul', ctypes.c_double),
					('z_mul', ctypes.c_double),  
					('x_offset', ctypes.c_double),
					('y_offset', ctypes.c_double),
					('z_offset', ctypes.c_double),
					('data_mul', ctypes.c_double),
					('x_label', ctypes.c_char * 100),
					('y_label', ctypes.c_char * 100),
					('z_label', ctypes.c_char * 100),
					('data_label', ctypes.c_char * 100),
					('x_units', ctypes.c_char * 100),
					('y_units', ctypes.c_char * 100),
					('z_units', ctypes.c_char * 100),
					('rgb', rgb_char),
					('icon', ctypes.c_char * 100),
					('data_units', ctypes.c_char * 100),
					('logscale_x', ctypes.c_int ),
					('logscale_y', ctypes.c_int ),
					('logscale_z', ctypes.c_int ),
					('logscale_data', ctypes.c_int ),
					('write_to_zip', ctypes.c_int ),
					('norm_x_axis', ctypes.c_int ),
					('norm_y_axis', ctypes.c_int ),
					('data_min', ctypes.c_double ),
					('data_max', ctypes.c_double ),
					('data_min1', ctypes.c_double ),
					('data_max1', ctypes.c_double ),
					('x_len', ctypes.c_int ),
					('y_len', ctypes.c_int ),
					('z_len', ctypes.c_int ),
					('srh_bands', ctypes.c_int ),
					('time', ctypes.c_double ),
					('Vexternal', ctypes.c_double ),
					('buf', ctypes.c_char_p ),
					('dataC', ctypes.c_void_p ),
					('len', ctypes.c_int ),
					('max_len', ctypes.c_int ),
					('zip_file_name', ctypes.c_char * 400 ),
					('file_name', ctypes.c_char * 4096 ),
					('cols', ctypes.c_char * 20 ),
					('bin', ctypes.c_int ),
					('valid_data', ctypes.c_int ),
					('modify_time', ctypes.c_long ),
					('new_read', ctypes.c_int ),
					('x_scaleC', ctypes.POINTER(ctypes.c_double) ),
					('y_scaleC', ctypes.POINTER(ctypes.c_double) ),
					('z_scaleC', ctypes.POINTER(ctypes.c_double) ),
					('py_data', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double) ))),
					('encrypted', ctypes.c_int ),
					('list', list_struct ),
					('col_count', ctypes.c_int ),
					('append', ctypes.c_int ),
					('part', ctypes.c_int ),
					('search_started', ctypes.c_int ),
					('include_json_header', ctypes.c_int ),
					('xlsx_format', ctypes.c_int ),
					('plotted', ctypes.c_int ),
					('transpose', ctypes.c_int ),
					('flip_z', ctypes.c_int ),
					('flip_x', ctypes.c_int ),
					('flip_y', ctypes.c_int ),
					('trap_map', dat_file_trap_map)]

	def __init__(self):
		self.grid=False
		self.show_pointer=False
		self.label_data=False
		self.invert_y=False
		self.normalize=False
		self.norm_to_peak_of_all_data=False
		self.subtract_first_point=False
		self.add_min=False
		self.legend_pos="lower right"
		self.ymax=-1
		self.ymin=-1
		self.xmax=-1
		self.xmin=-1
		self.zmax=-1
		self.zmin=-1
		self.plot_type=""		#wireframe/heat etc...

		self.key_units=""
		self.key_text=""
		self.file0=""
		self.tag0=""
		self.file1=""
		self.tag1=""
		self.file2=""
		self.tag2=""
		self.other_file=""

		self.x_start=0
		self.x_stop=1
		self.x_points=25
		self.y_start=0
		self.y_stop=1
		self.y_points=25
		
		self.x_scale=[]
		self.y_scale=[]
		self.z_scale=[]
		self.data=[]
		self.labels=[]
		self.file_age=0
		self.id="id"+codecs.encode(os.urandom(int(16 / 2)), 'hex').decode()
		self.error=""
		self.lib=sim_paths.get_dll_py()
		self.lib.dat_file_init(ctypes.byref(self))
		self.convert_to_yd=False		#This is used for converting xd files to yd files

	def __del__(self):
		self.free()

	def free(self):
		lib=sim_paths.get_dll_py()
		if lib!=None:
			lib.dat_file_free(ctypes.byref(self))

	def how_can_i_display(self):
		a=dat_file_display_options()
		ret=self.lib.dat_file_how_can_i_display_the_data(ctypes.byref(a), ctypes.byref(self))
		return a

	def load_yd_from_csv(self,file_name,x_col=0,y_col=1,skip_lines=0,known_col_sep=None):
		self.lib.dat_file_load_yd_from_csv(ctypes.byref(self), bytes(file_name, encoding='utf8'), x_col, y_col, skip_lines )
		self.convert_from_C_to_python()
		#dat_file_load_yd_from_csv(struct dat_file *in,char *file_name, int col);

	def import_data(self,file_name,x_col=0,y_col=1,skip_lines=0,known_col_sep=None):
		#This needs to be removed and merged into load_yd_from_csv
		if self.have_i_loaded_this(file_name)==True:
			return True

		f=inp()
		if f.load(os.path.join(file_name))==False:
			self.error="Problem loading file"
			return False

		if f.lines==False:
			self.error="Problem loading file"
			return False

		if len(f.lines)<skip_lines:
			self.error="Not enough lines"
			return False

		x_col=self.col_name_to_pos(f.lines,x_col,known_col_sep)
		y_col=self.col_name_to_pos(f.lines,y_col,known_col_sep)

		lines=f.lines[skip_lines:]

		self.x_scale=[]
		self.y_scale=[]
		self.z_scale=[]
		self.data=[]
		data_started=False
		self.data=[[[0.0 for k in range(0)] for j in range(1)] for i in range(1)]

		for i in range(0, len(lines)):
			s,label=self.decode_line(lines[i],known_col_sep=known_col_sep)
			l=len(s)
			if l>0:

				if data_started==False:
					if is_number(s[0])==True:
						data_started=True

				if s[0]=="#end":
					break

				if data_started==True:
					number_ok=False
					try:
						float(s[x_col])
						float(s[y_col])
						number_ok=True
					except:
						pass

					if number_ok==True:
						if max(x_col,y_col)<l:
							duplicate=False
							if float(s[x_col]) in self.y_scale:
								duplicate=True

							if duplicate==False:
								self.y_scale.append(float(s[x_col]))
								self.data[0][0].append(float(s[y_col]))

		self.x_len=1
		self.y_len=len(self.data[0][0])
		self.z_len=1
		self.cols=b"yd"
		return True

	def import_xy_data(self,x,y):
		self.y_len=len(x)
		self.x_len=1
		self.z_len=1
		self.init_mem()

		for i in range(0,len(x)):
			self.y_scale[i]=x[i]
			self.data[0][0][i]=y[i]

	def rgb_to_hex(self):
		if self.r==-1.0:
			return None

		return format(int(self.r*255), '02x')+format(int(self.g*255), '02x')+format(int(self.b*255), '02x')

	def copy(self, in_data):
		self.x_len=in_data.x_len
		self.y_len=in_data.y_len
		self.z_len=in_data.z_len

		self.init_mem()

		for i in range(0,len(self.x_scale)):
			self.x_scale[i]=in_data.x_scale[i]

		for i in range(0,len(self.y_scale)):
			self.y_scale[i]=in_data.y_scale[i]

		for i in range(0,len(self.z_scale)):
			self.z_scale[i]=in_data.z_scale[i]

		self.y_mul=in_data.y_mul
		self.y_units=in_data.y_units
		self.data_mul=in_data.data_mul
		self.data_units=in_data.data_units

		for z in range(0,len(self.z_scale)):
			for x in range(0,len(self.x_scale)):
				for y in range(0,len(self.y_scale)):
					self.data[z][x][y]=in_data.data[z][x][y]


	def init_mem(self,dim="zxy"):
		if dim=="zxy":
			self.data=[[[0.0 for k in range(self.y_len)] for j in range(self.x_len)] for i in range(self.z_len)]
		elif dim=="zx":
			self.data=[[0.0 for j in range(self.x_len)] for i in range(self.z_len)]				
		self.x_scale= [0.0]*self.x_len
		self.y_scale= [0.0]*self.y_len
		self.z_scale= [0.0]*self.z_len
		self.valid_data=True

	def decode_circuit_lines(self,lines):
		self.data=[]
		for line in lines:
			s,label=self.decode_line(line)
			l=len(s)
			if l>0:
				if s[0].startswith("#")==False:
					c=component()
					c.z0=float(s[0])
					c.x0=float(s[1])
					c.y0=float(s[2])
					c.z1=float(s[3])
					c.x1=float(s[4])
					c.y1=float(s[5])
					c.name=s[6]

					self.data.append(c)

		return True


	def have_i_loaded_this(self,file_name):
		if os.path.isfile(file_name)==True:
			age=os.path.getmtime(file_name)

			if age==self.file_age:
				self.new_read=False
				return True
			else:
				self.new_read=True
				self.file_age=age

		return False

	def load_only_info(self,file_name):
		ret=self.lib.dat_file_load_info_peek(ctypes.byref(self), None, None, bytes(file_name, encoding='utf8'))
		if ret==0:
			return True

		return False

	def convert_from_C_to_python(self):
		done=False
		self.labels=[]

		if self.convert_to_yd==True:
			if self.y_len==1 and self.z_len==1 and self.x_len>=1:
				self.data=[[[float(self.py_data[z][x][y]) for x in range(self.x_len)] for y in range(self.y_len)] for z in range(self.z_len)]
				self.x_scale= [self.y_scaleC[y] for y in range(self.y_len)]
				self.y_scale= [self.x_scaleC[x] for x in range(self.x_len)]
				self.z_scale= [self.z_scaleC[z] for z in range(self.z_len)]
				tmp=self.x_len
				self.x_len=self.y_len
				self.y_len=tmp
				done=True

		if done==False:
			self.data=[[[float(self.py_data[z][x][y]) for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]
			self.x_scale= [self.x_scaleC[x] for x in range(self.x_len)]
			self.y_scale= [self.y_scaleC[y] for y in range(self.y_len)]
			self.z_scale= [self.z_scaleC[z] for z in range(self.z_len)]

		for l in range(0,self.list.len):
			self.labels.append(bytes2str(self.list.names[l]))


		self.valid_data=True

	def load(self,file_name,guess=True,raw_data=False):
		self.file_name=str2bytes(file_name)

		if file_name==None:
			self.valid_data=False
			return False


		ret=self.lib.dat_file_load(ctypes.byref(self), bytes(file_name, encoding='utf8'))
		#print(self.cols,file_name,self.type)
		if ret==0:
			if self.cols==b"yrgb" or self.type==b"yrgb":
				self.valid_data=True
				return True
			if self.cols==b"zxrgb":
				self.valid_data=True
				return True
			elif self.cols==b"poly" or self.type==b"poly":
				self.valid_data=True
				return True
			elif self.cols==b"zxy":
				self.valid_data=True
				return True
			elif self.cols==b"zxyEd":
				self.valid_data=True
				return True
			if self.cols==b"zxyrgb":
				self.valid_data=True
				return True
			if self.cols==b"zxyzxyrgb":
				self.valid_data=True
				return True
			elif self.cols==b"rays":
				self.valid_data=True
				return True
			elif self.cols==b"zxyzxyzxyzxy":
				self.valid_data=True
				return True
			else:
				self.convert_from_C_to_python()
				return True
		else:
			#print("Dll fail for the file",self.file_name)
			pass
		
		if self.have_i_loaded_this(file_name)==True:
			return True

		found,lines=zip_get_data_file(file_name)
		if found==False:
			return False

		self.x_scale=[]
		self.y_scale=[]
		self.z_scale=[]
		self.data=[]

		if self.type==b"circuit":
			return self.decode_circuit_lines(lines)


		return False

