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

## @package json_sims
#  Contains all simulation modes
#


from json_base import json_base
from json_light import json_light
from json_light_sources import json_light_sources
from json_detectors import json_detectors
from json_spctral2 import json_spctral2
from json_lasers import json_lasers
from json_mesh import json_mesh

class json_optical_ray(json_base):
	def __init__(self):
		json_base.__init__(self,"ray")
		self.var_list.append(["rays_display","all"])
		self.var_list_build()


class json_optical_boundary(json_base):
	def __init__(self):
		json_base.__init__(self,"boundary")
		self.var_list.append(["optical_y0","abc"])
		self.var_list.append(["optical_y1","abc"])
		self.var_list.append(["optical_x0","abc"])
		self.var_list.append(["optical_x1","abc"])
		self.var_list.append(["optical_z0","abc"])
		self.var_list.append(["optical_z1","abc"])
		self.var_list_build()

class json_optical(json_base):

	def __init__(self):
		json_base.__init__(self,"optical")
		self.var_list.append(["icon_","optics2"])
		self.var_list.append(["light",json_light()])
		self.var_list.append(["light_sources",json_light_sources()])
		self.var_list.append(["detectors",json_detectors()])
		self.var_list.append(["spctral2",json_spctral2()])
		self.var_list.append(["lasers",json_lasers()])
		self.var_list.append(["boundary",json_optical_boundary()])
		self.var_list.append(["ray",json_optical_ray()])
		self.var_list.append(["mesh",json_mesh(optical=True)])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()

