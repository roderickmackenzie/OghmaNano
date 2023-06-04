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


class dat_file_trap_map():

	def load_trap_map(self):
		pos=0
		self.data=None
		self.Ec=[[[[0.0 for band in range(self.srh_bands)] for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]
		self.Ev=[[[[0.0 for band in range(self.srh_bands)] for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]
		self.nt=[[[[0.0 for band in range(self.srh_bands)] for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]
		self.pt=[[[[0.0 for band in range(self.srh_bands)] for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]

		self.Ec_f=[[[0.0 for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]
		self.Ev_f=[[[0.0 for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]
		self.nf=[[[0.0 for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]
		self.pf=[[[0.0 for y in range(self.y_len)] for x in range(self.x_len)] for z in range(self.z_len)]

		self.z_scale=[]
		for z in range(0,self.z_len):
			self.z_scale.append(self.py_data[0][0][pos])
			pos=pos+1

		self.x_scale=[]
		for x in range(0,self.x_len):
			self.x_scale.append(self.py_data[0][0][pos])
			pos=pos+1

		self.y_scale=[]
		for y in range(0,self.y_len):
			self.y_scale.append(self.py_data[0][0][pos])
			pos=pos+1

		self.data_min=1e6
		self.data_max=-1e6
		self.Ev_min=1e6
		self.Ec_max=-1e6

		for z in range(0,self.z_len):
			for x in range(0,self.x_len):
				for y in range(0,self.y_len):
					self.Ec_f[z][x][y]=self.py_data[0][0][pos]
					if self.Ec_max<self.py_data[0][0][pos]:
						self.Ec_max=self.py_data[0][0][pos]
					pos=pos+1

					self.nf[z][x][y]=self.py_data[0][0][pos]
					if self.data_min>self.py_data[0][0][pos]:
						self.data_min=self.py_data[0][0][pos]
					elif self.data_max<self.py_data[0][0][pos]:
						self.data_max=self.py_data[0][0][pos]
					pos=pos+1

					for band in range(0,self.srh_bands):
						self.Ec[z][x][y][band]=self.py_data[0][0][pos]
						if self.Ec_max<self.py_data[0][0][pos]:
							self.Ec_max=self.py_data[0][0][pos]
						pos=pos+1

						self.nt[z][x][y][band]=self.py_data[0][0][pos]
						if self.data_min>self.py_data[0][0][pos]:
							self.data_min=self.py_data[0][0][pos]
						elif self.data_max<self.py_data[0][0][pos]:
							self.data_max=self.py_data[0][0][pos]
						pos=pos+1

					self.Ev_f[z][x][y]=self.py_data[0][0][pos]
					if self.Ev_min>self.py_data[0][0][pos]:
						self.Ev_min=self.py_data[0][0][pos]
					pos=pos+1

					self.pf[z][x][y]=self.py_data[0][0][pos]
					if self.data_min>self.py_data[0][0][pos]:
						self.data_min=self.py_data[0][0][pos]
					elif self.data_max<self.py_data[0][0][pos]:
						self.data_max=self.py_data[0][0][pos]

					pos=pos+1

					for band in range(0,self.srh_bands):
						self.Ev[z][x][y][band]=self.py_data[0][0][pos]
						if self.Ev_min>self.py_data[0][0][pos]:
							self.Ev_min=self.py_data[0][0][pos]
						pos=pos+1

						self.pt[z][x][y][band]=self.py_data[0][0][pos]
						if self.data_min>self.py_data[0][0][pos]:
							self.data_min=self.py_data[0][0][pos]
						elif self.data_max<self.py_data[0][0][pos]:
							self.data_max=self.py_data[0][0][pos]

						pos=pos+1


