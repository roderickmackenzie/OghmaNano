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

## @package triangle
#  A base triangle class
#

from math import cos, sin
from json_base import json_base
import ctypes

class vec(json_base,ctypes.Structure):
	_fields_ = [('x', ctypes.c_double),
				('y', ctypes.c_double),
				('z', ctypes.c_double)]

	def __init__(self,name="vec"):
		json_base.__init__(self,name)
		self.var_list=[]
		self.var_list.append(["x",0.0])
		self.var_list.append(["y",0.0])
		self.var_list.append(["z",0.0])
		self.var_list_build()

	def __str__(self):
		return "(x="+str(self.x)+",y="+str(self.y)+",z="+str(self.z)+")"

	def __sub__(self,data):
		a=vec()
		a.x=self.x-data.x
		a.y=self.y-data.y
		a.z=self.z-data.z
		return a

	def __add__(self,data):
		if type(data)==vec:
			a=vec()
			a.x=self.x+data.x
			a.y=self.y+data.y
			a.z=self.z+data.z
		if type(data)==float or type(data)==int:
			a=vec()
			a.x=self.x+float(data)
			a.y=self.y+float(data)
			a.z=self.z+float(data)
		return a

	def __truediv__(self,data):
		if type(data)==vec:
			a=vec()
			if data.x!=0:
				a.x=self.x/data.x

			if data.y!=0:
				a.y=self.y/data.y

			if data.z!=0:
				a.z=self.z/data.z

		if type(data)==float:
			a=vec()
			a.x=self.x/data
			a.y=self.y/data
			a.z=self.z/data

		return a

	def __mul__(self,data):
		a=vec()
		if type(data)==vec:
			a.x=self.x*data.x
			a.y=self.y*data.y
			a.z=self.z*data.z
		if type(data)==float:
			a.x=self.x*data
			a.y=self.y*data
			a.z=self.z*data

		return a
	
	def rotate(self,theta):
		theta_rad=(theta/360.0)*2*3.14159
		#print()
		a=vec()
		a.x=self.x*cos(theta_rad)-self.y*sin(theta_rad)
		a.y=self.x*sin(theta_rad)+self.y*cos(theta_rad)
		a.z=0.0
		return a

	def rotate_y(self,theta):		#rotate around the y axis
		theta_rad=(theta/360.0)*2*3.14159
		a=vec()
		a.x = self.x*cos(theta_rad) + self.z*sin(theta_rad)
		a.y = self.y
		a.z = self.z*cos(theta_rad) - self.x*sin(theta_rad)
		return a

	def cpy(self,data):
		self.x=data.x
		self.y=data.y
		self.z=data.z

	def set(self,x,y,z):
		self.x=x
		self.y=y
		self.z=z

