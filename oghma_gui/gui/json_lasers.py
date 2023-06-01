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

## @package json_lasers
#  Store the cv domain json data
#

from json_base import json_base


class json_laser_config(json_base):

	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["laserwavelength",520e-9])
		self.var_list.append(["spotx",5e-3])
		self.var_list.append(["spoty",5e-3])
		self.var_list.append(["pulseJ",5e-14])
		self.var_list.append(["laser_pulse_width",5e-9])
		self.var_list.append(["laser_photon_efficiency",1.0])
		self.var_list_build()



class json_laser(json_base):

	def __init__(self):
		json_base.__init__(self,"laser_segment")
		self.var_list=[]
		self.var_list.append(["name","Green"])
		self.var_list.append(["icon","laser"])
		self.var_list.append(["config",json_laser_config()])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


class json_lasers(json_base):

	def __init__(self):
		json_base.__init__(self,"lasers",segment_class=True,segment_example=json_laser())


