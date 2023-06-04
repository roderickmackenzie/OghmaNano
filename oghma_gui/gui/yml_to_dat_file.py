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

import os
from math import pow
from math import sqrt
import yaml
from dat_file import dat_file

def yml_to_dat_file(settingsMap):
	n=dat_file()
	n.y_mul=1e9
	n.title=b"Refractive index"
	n.type=b"xy"
	n.cols=b"yd"
	n.y_label=b"Wavelength"
	n.y_units=b"nm"
	n.data_label=b"Refractive index"
	n.data_units=b"m^{-1}"
	n.x_len=1
	n.z_len=1
	n.data=[[[]]]

	alpha=dat_file()
	alpha.y_mul=1e9
	alpha.title=b"Absorption"
	alpha.type=b"xy"
	alpha.cols=b"yd"
	alpha.y_label=b"Wavelength"
	alpha.y_units=b"nm"
	alpha.data_label=b"Absorption"
	alpha.data_units=b"m^{-1}"
	alpha.x_len=1
	alpha.z_len=1
	alpha.data=[[[]]]

	understood_n=False
	understood_alpha=False

	for main in settingsMap:
		if main=="DATA":
			lines_n=[]
			n_x=[]
			n_y=[]

			for data_number in range(0,len(settingsMap['DATA'])):

				if settingsMap['DATA'][data_number]['type']=="tabulated nk":
					lines=settingsMap['DATA'][data_number]['data'].split("\n")

					for i in range(0,len(lines)):
						l=lines[i].split()
						if len(l)==3:
							try:
								lam=float(l[0])*1e-6
								n_val=float(l[1])
								alpha_val=4*3.14159*float(l[2])/lam
								n.y_scale.append(lam)
								n.data[0][0].append(n_val)
							
								alpha.y_scale.append(lam)
								alpha.data[0][0].append(alpha_val)
							except:
								pass
					understood_n=True
					understood_alpha=True

				elif settingsMap['DATA'][data_number]['type']=="tabulated n":
					lines=settingsMap['DATA'][data_number]['data'].split("\n")

					for i in range(0,len(lines)):
						l=lines[i].split()
						if len(l)==2:
							try:
								lam=float(l[0])*1e-6
								n_val=float(l[1])
								n.y_scale.append(lam)
								n.data[0][0].append(n_val)
							except:
								pass

					understood_n=True

				elif settingsMap['DATA'][data_number]['type']=="tabulated k":
					lines=settingsMap['DATA'][data_number]['data'].split("\n")
					for i in range(0,len(lines)):
						l=lines[i].split()
						#print(len(l))
						if len(l)==2:
							lam=float(l[0])*1e-6
							alpha_val=4*3.14159*float(l[1])/lam
							alpha.y_scale.append(lam)
							alpha.data[0][0].append(alpha_val)

					#print(lines_alpha)
					understood_alpha=True

				elif settingsMap['DATA'][data_number]['type'].startswith("formula")==True:
					#print(settingsMap['DATA'][0])
					r=settingsMap['DATA'][data_number]['wavelength_range'].split()
					r0=float(r[0])*1e-6
					r1=float(r[1])*1e-6
					#print("range",r0*1e9,r1*1e9)
					delta=(r1-r0)/2000.0
					(r1-r0)/2000.0

					c=settingsMap['DATA'][data_number]['coefficients'].split()
					cf=[]
					for v in c:
						cf.append(float(v))
					c=cf
					c0=c[0]
					c.pop(0)


					if (settingsMap['DATA'][data_number]['type']=="formula 1"):
						lam=r0
						while(lam<r1):
							n2=c0+1
							for i in range(0,int(len(c)/2)):
								n2=n2+(c[(i*2)]*pow((lam/1e-6),2.0))/(pow((lam/1e-6),2.0)-pow(c[(i*2)+1],2.0))

							#print(n2)
							if n2<0.0:
								break
							n_val=sqrt(n2)
							n.y_scale.append(lam)
							n.data[0][0].append(n_val)

							lam=lam+delta
						#print(lines_n)
						understood_n=True

					elif (settingsMap['DATA'][data_number]['type']=="formula 2"):
						lam=r0
						while(lam<r1):
							n2=c0+1
							for i in range(0,int(len(c)/2)):
								n2=n2+(c[(i*2)]*pow((lam/1e-6),2.0))/(pow((lam/1e-6),2.0)-c[(i*2)+1])

							#print(n2)
							n_val=sqrt(n2)
							n.y_scale.append(lam)
							n.data[0][0].append(n_val)

							lam=lam+delta
						#print(lines_n)
						understood_n=True


					elif (settingsMap['DATA'][data_number]['type']=="formula 3"):
						lam=r0
						while(lam<r1):
							n2=c0
							for i in range(0,int(len(c)/2)):
								#print(n2,c[(i*2)],lam,c[(i*2)+1])
								n2=n2+c[(i*2)]*pow((lam/1e-6),c[(i*2)+1])

							#print(n2)
							n_val=sqrt(n2)

							n.y_scale.append(lam)
							n.data[0][0].append(n_val)
						
							lam=lam+delta
						#print(lines_n)
						understood_n=True

					elif (settingsMap['DATA'][data_number]['type']=="formula 5"):
						lam=r0
						while(lam<r1):
							n_val=c0
							for i in range(0,int(len(c)/2)):
								#print(n2,c[(i*2)],lam,c[(i*2)+1])
								n_val=n_val+c[(i*2)]*pow((lam/1e-6),c[(i*2)+1])

							#print(n2)
							#n=sqrt(n2)
							n.y_scale.append(lam)
							n.data[0][0].append(n_val)

							lam=lam+delta
						#print(lines_n)
						understood_n=True

	if len(alpha.y_scale)==0:
		alpha=False

	if len(n.y_scale)==0:
		n=False
		
	if understood_alpha==False:
		alpha=False

	if understood_n==False:
		n=False

	return alpha,n
