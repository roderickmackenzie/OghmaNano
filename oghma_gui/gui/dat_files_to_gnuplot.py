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

def dat_file_to_gnuplot_header(dat_file):
	ret=[]
	ret.append("set title '"+str(dat_file.title)+"'")
	ret.append("set ylabel '"+str(dat_file.data_label)+" ("+str(dat_file.data_units)+")'")
	ret.append("set xlabel '"+str(dat_file.y_label)+" ("+str(dat_file.y_units)+")'")
	ret.append("set key top left")
	ret.append("set colors classic")
	if dat_file.logdata==True:
		ret.append("set logscale y")
		ret.append("set format y \"%2.0t{/Symbol \\264}10^{%L}\"")
	else:
		ret.append("#set logscale y")
		ret.append("#set format y \"%2.0t{/Symbol \\264}10^{%L}\"")

	if dat_file.logy==True:
		ret.append("set logscale x")
	else:
		ret.append("#set logscale x")

	return ret

def dat_files_to_gnuplot(out_dir,data):
	os.mkdir(out_dir)
	data_dir=os.path.join(out_dir,"data")
	os.mkdir(data_dir)

	makefile=[]
	makefile.append("main:")
	makefile.append("	gnuplot plot.plot >plot.eps")
	makefile.append("	gs -dNOPAUSE -r600 -dEPSCrop -sDEVICE=jpeg -sOutputFile=plot.jpg plot.eps -c quit")
	makefile.append("	xdg-open plot.jpg")
	inp_save_lines_to_file(os.path.join(out_dir,"makefile"),makefile)

	plotfile=[]
	plotfile.append("set term postscript eps enhanced color solid \"Helvetica\" 25")
	plotfile.extend(dat_file_to_gnuplot_header(data[0]))

	plotfile.append("plot \\")

	for i in range(0,len(data)):
		d=data[i]
		d.save_as_txt(os.path.join(data_dir,str(i)+".txt"))
		file_path=os.path.join("data",str(i)+".txt")
		file_path=str(d.file_name)
		line="'"+file_path+"' using ($1):($2) with lp title '"+str(d.key_text)+"'"
		#print(i,len(data))
		if i<len(data)-1:
			line=line+",\\"

		plotfile.append(line)

	inp_save_lines_to_file(os.path.join(out_dir,"plot.plot"),plotfile)

def dat_files_to_gnuplot_files(out_dir,data):
	if os.path.isdir(out_dir)==False:
		os.mkdir(out_dir)
	data_dir=os.path.join(out_dir,"data")

	if os.path.isdir(data_dir)==False:
		os.mkdir(data_dir)

	makefile=[]
	makefile.append("main:")
	for i in range(0,len(data)):
		makefile.append("	gnuplot "+str(i)+".plot >"+str(i)+".eps")
		makefile.append("	gs -dNOPAUSE -r600 -dEPSCrop -sDEVICE=jpeg -sOutputFile="+str(i)+".jpg "+str(i)+".eps -c quit")
		makefile.append("")

	inp_save_lines_to_file(os.path.join(out_dir,"makefile"),makefile)

	for i in range(0,len(data)):
		plotfile=[]
		plotfile.append("set term postscript eps enhanced color solid \"Helvetica\" 25")
		plotfile.extend(dat_file_to_gnuplot_header(data[i]))

		d=data[i]
		d.save_as_txt(os.path.join(data_dir,str(i)+".txt"))
		file_path=os.path.join("data",str(i)+".txt")
		#file_path=d.file_name
		line="plot '"+file_path+"' using ($1):($2) with lp title '"+d.key_text+"'"

		plotfile.append(line)

		inp_save_lines_to_file(os.path.join(out_dir,str(i)+".plot"),plotfile)
