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

import copy
from math import isnan
import time
import ctypes

class dat_file_math():

	def pow(self,val):
		a=self.__class__()
		a.copy(self)

		for z in range(0,len(self.z_scale)):
			for x in range(0,len(self.x_scale)):
				for y in range(0,len(self.y_scale)):
					a.data[z][x][y]=pow(self.data[z][x][y],val)
		return a		

	def __sub__(self,val):
		a=self.__class__()
		a.copy(self)
		a.name="hello"
		if type(val)==float:
			for z in range(0,len(self.z_scale)):
				for x in range(0,len(self.x_scale)):
					for y in range(0,len(self.y_scale)):
						a.data[z][x][y]=self.data[z][x][y]-val
		elif type(val)==type(self):
			for z in range(0,len(self.z_scale)):
				for x in range(0,len(self.x_scale)):
					for y in range(0,len(self.y_scale)):
						a.data[z][x][y]=self.data[z][x][y]-val.data[z][x][y]
						#print("a",self.data[z][x][y],val.data[z][x][y],a.data[z][x][y])
		return a

	def __add__(self,val):
		a=self.__class__()
		a.copy(self)
		if type(val)==float:
			for z in range(0,len(self.z_scale)):
				for x in range(0,len(self.x_scale)):
					for y in range(0,len(self.y_scale)):
						a.data[z][x][y]=self.data[z][x][y]+val
		else:
			for z in range(0,len(self.z_scale)):
				for x in range(0,len(self.x_scale)):
					for y in range(0,len(self.y_scale)):
						a.data[z][x][y]=self.data[z][x][y]+val.data[z][x][y]

		return a

	def __truediv__(self,in_data):
		a=self.__class__()
		a.copy(self)

		for z in range(0,len(self.z_scale)):
			for x in range(0,len(self.x_scale)):
				for y in range(0,len(self.y_scale)):
					a.data[z][x][y]=self.data[z][x][y]/in_data.data[z][x][y]
		return a

	def __rsub__(self,val):
		a=self.__class__()
		a.copy(self)

		if type(val)==float:
			for z in range(0,len(self.z_scale)):
				for x in range(0,len(self.x_scale)):
					for y in range(0,len(self.y_scale)):
						a.data[z][x][y]=val-self.data[z][x][y]
		elif type(val)==type(self):
			for z in range(0,len(self.z_scale)):
				for x in range(0,len(self.x_scale)):
					for y in range(0,len(self.y_scale)):
						a.data[z][x][y]=val.data[z][x][y]-self.data[z][x][y]
		
		return a


	def chop_y(self,y0,y1):
		if y0==0 and y1==0:
			return

		self.y_scale=self.y_scale[y0:y1]
		self.y_len=len(self.y_scale)

		for z in range(0,len(self.z_scale)):
			for x in range(0,len(self.x_scale)):
				self.data[z][x]=self.data[z][x][y0:y1]
				#for y in range(0,len(self.y_scale)):
				#	self.data[z][x][y]=val

	def __mul__(self,in_data):
		a=self.__class__()
		a.copy(self)

		if type(in_data)==float:
			for z in range(0,len(self.z_scale)):
				for x in range(0,len(self.x_scale)):
					for y in range(0,len(self.y_scale)):
						a.data[z][x][y]=in_data*self.data[z][x][y]
		else:
			for z in range(0,len(self.z_scale)):
				for x in range(0,len(self.x_scale)):
					for y in range(0,len(self.y_scale)):
						a.data[z][x][y]=in_data.data[z][x][y]*self.data[z][x][y]

		return a

	def __rmul__(self, in_data):
		return self.__mul__(in_data)


	def max_min(self,cur_min=None,cur_max=None,only_use_data=False):
		my_max = (ctypes.POINTER(ctypes.c_double) * 1)()
		my_min = (ctypes.POINTER(ctypes.c_double) * 1)()
		self.lib.dat_file_min_max(ctypes.byref(my_min),ctypes.byref(my_max),ctypes.byref(self))

		my_max=ctypes.cast(my_max, ctypes.POINTER(ctypes.c_double)).contents.value
		my_min=ctypes.cast(my_min, ctypes.POINTER(ctypes.c_double)).contents.value

		if cur_min!=None:
			if cur_min<my_min:
				my_min=cur_min

		if cur_max!=None:
			if cur_max>my_max:
				my_max=cur_max
		return [my_max,my_min]

	def dat_file_sub(self,one):
		if (self.x_len==one.x_len) and (self.y_len==one.y_len) and (self.z_len==one.z_len):
			for z in range(0,self.z_len):
				for x in range(0,self.x_len):
					for y in range(0,self.y_len):
						self.data[z][x][y]=self.data[z][x][y]-one.data[z][x][y]

	def dat_file_sub_float(self,val):
			for z in range(0,self.z_len):
				for x in range(0,self.x_len):
					for y in range(0,self.y_len):
						self.data[z][x][y]=self.data[z][x][y]-val
						
	def dat_file_mul(self,val):
			for z in range(0,self.z_len):
				for x in range(0,self.x_len):
					for y in range(0,self.y_len):
						self.data[z][x][y]*=val

	def abs(self):
			for z in range(0,self.z_len):
				for x in range(0,self.x_len):
					for y in range(0,self.y_len):
						self.data[z][x][y]=abs(self.data[z][x][y])


