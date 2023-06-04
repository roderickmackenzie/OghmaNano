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

## @package multiplot_from_tokens
#  This will generate plot files from tokens
#

import os
import i18n
_ = i18n.language.gettext

from cal_path import subtract_paths
from inp import inp
from cal_path import sim_paths
from search import search_simulations
from dat_file import dat_file
from token_lib import tokens

class multiplot_from_tokens:

	def __init__(self):
		self.sims=[]

	def gen_plot(self,base_path,file0,token0,file1,token1,output_file=""):
		x=[]
		y=[]
		plot_labels=[]
		my_token_lib=tokens()

		print(base_path,output_file)
		if output_file=="":
			out_file_name=os.path.join(base_path,os.path.splitext(file0)[0]+token0+"#"+os.path.splitext(file1)[0]+token1+".dat")
		else:
			out_file_name=output_file

		sims=search_simulations(base_path)
		out=dat_file()

		t0=my_token_lib.find(token0)
		t1=my_token_lib.find(token1)

		out.title=t0.info+" v.s. "+t1.info
		out.y_label=t0.info
		out.data_label=t1.info
		out.y_units=t0.units
		out.data_units=t1.units

		for s in sims:
			f=inp()
			f.load(os.path.join(s,file0))
			x.append(float(f.get_token(token0)))

			f=inp()
			f.load(os.path.join(s,file1))
			y.append(float(f.get_token(token1)))

		x, y = zip(*sorted(zip(x, y)))


		out.x_len=1
		out.y_len=len(y)
		out.z_len=1

		out.init_mem()

		for i in range(0,len(x)):
			out.y_scale[i]=x[i]
			out.data[0][0][i]=y[i]

		out.save(out_file_name)

		return [out_file_name], plot_labels, ""
