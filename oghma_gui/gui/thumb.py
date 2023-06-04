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

## @package thumb
#  XWindows thumbnail generator
#

import os
import math

from util_zip import archive_add_file
from cal_path import sim_paths
from win_lin import get_platform
if get_platform()=="linux":
	import cairo

def gen_icon(path,icon_size):
	if get_platform()=="linux":
		#surface = cairo.SVGSurface('example1.svg', icon_size, icon_size)
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, icon_size, icon_size)
		ctx = cairo.Context(surface)

		ctx.scale(icon_size, icon_size)  # Normalizing the canvas

		pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
		pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
		pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity

		ctx.rectangle(0.25, 0.25, 0.5, 0.5)  # Rectangle(x0, y0, x1, y1)
		ctx.set_source(pat)
		ctx.fill()

		ctx.translate(0.1, 0.1)  # Changing the current transformation matrix

		surface.write_to_png(path)  # Output to PNG
		surface.finish()

def thumb_nail_gen():
	if get_platform()=="linux":
		thumb_dir=os.path.join(sim_paths.get_sim_path(),"thumb")
		if os.path.isdir(thumb_dir)==False:
			os.mkdir(thumb_dir)

		for i in [16,32,48,64,128]:
			icon_path=os.path.join(thumb_dir,str(i)+"x"+str(i)+".png")
			gen_icon(icon_path,i)
			archive_add_file(os.path.join(sim_paths.get_sim_path(),"sim.oghma"),icon_path,thumb_dir)

if __name__ == '__main__':
	gen_icon("hello.png",128)

