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

## @package gl_default_shapes
#  The gl_default_shapes class for the OpenGL display.
#

import sys
import os
from math import fabs

import math

from cal_path import sim_paths
from dat_file import dat_file
from vec import vec

class gl_default_shapes():
	def __init__(self):
		shape_path=os.path.join(sim_paths.get_shape_path(),"box","shape.inp")
		if os.path.isfile(shape_path)==True:
			self.box=dat_file()
			self.box.load(shape_path,raw_data=True)
			if self.box.data!=None:
				a=vec()
				min_vec=self.box.gl_triangles_get_min()
				self.box.gl_triangles_sub_vec(min_vec)
				max_vec=self.box.gl_triangles_get_max()
				self.box.gl_triangles_div_vec(max_vec)

