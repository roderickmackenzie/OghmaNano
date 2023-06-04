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
from plot_window import plot_window

window=None

destroy=False

def set_plot_auto_close(value):
	global destroy
	destroy=value

def plot_gen(input_files,plot_labels,config_file):

	if (len(input_files)==1):
		if os.path.splitext(input_files[0])[1]==".plot":
			plot_file=input_files[0]
			cmd = 'gnuplot -persist '+plot_file
			os.system(cmd)
			return

	global window
	global destroy
	if window!=None:
		if window.shown==True:
			if destroy==True:
				window.input_files=input_files
				window.plot.load_data(input_files)
				window.plot.set_labels(plot_labels)
				window.plot.do_plot()
				window.plot.fig.canvas.draw()
				window.window.present()
				window.window.set_keep_above(True)
				return

	window=plot_window()
	window.init(input_files,plot_labels)


