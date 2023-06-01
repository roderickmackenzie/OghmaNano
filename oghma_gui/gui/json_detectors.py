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

## @package json_detectors
#  Store the information on the optical detectors
#


from json_base import json_base
from json_world_object import json_world_object

class json_detector(json_base,json_world_object):

	def __init__(self):
		json_base.__init__(self,"detector")
		json_world_object.__init__(self)
		self.var_list.append(["name","Detector"])
		self.var_list.append(["icon","jv"])
		self.var_list.append(["text_detector",""])
		self.var_list.append(["viewpoint_nx",8])
		self.var_list.append(["viewpoint_nz",8])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()
		self.color_r=0.8
		self.color_g=0.0
		self.color_b=0.8
		self.color_alpha=1.0


class json_detectors(json_base):

	def __init__(self):
		json_base.__init__(self,"detectors",segment_class=True,segment_example=json_detector())


