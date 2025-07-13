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
from str2bool import str2bool
from inp import inp_save_lines_to_file

#This exists in dat_file_save_as_gnuplot.c
def dat_file_to_gnuplot_header(dat_file):
	ret=[]
	ret.append("set title '"+str(dat_file.title)+"'")
	ret.append("set ylabel '"+str(dat_file.data_label)+" ("+str(dat_file.data_units)+")'")
	ret.append("set xlabel '"+str(dat_file.y_label)+" ("+str(dat_file.y_units)+")'")
	ret.append("set key top left")
	ret.append("set colors classic")
	if dat_file.logscale_data==True:
		ret.append("set logscale y")
		ret.append("set format y \"%2.0t{/Symbol \\264}10^{%L}\"")
	else:
		ret.append("#set logscale y")
		ret.append("#set format y \"%2.0t{/Symbol \\264}10^{%L}\"")

	if dat_file.logscale_y==True:
		ret.append("set logscale x")
	else:
		ret.append("#set logscale x")

	return ret



