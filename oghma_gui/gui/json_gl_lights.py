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

## @package json_jv
#  Store the cv domain json data
#


from json_base import json_base
from json_world_object import json_world_object

class json_gl_light(json_base,json_world_object):

	def __init__(self):
		json_base.__init__(self,"gl_light")
		json_world_object.__init__(self)
		self.var_list_build()

class json_gl_lights(json_base):
	def __init__(self):
		json_base.__init__(self,"gl_lights",segment_class=True,segment_example=json_gl_light())
		self.safe_init(0)

	def load_from_json(self,json):
		self.var_list=[]
		segs=0
		try:
			segs=json['segments']
		except:
			pass

		if self.safe_init(segs)==False:
			self.segments=[]
			for i in range(0,segs):
				a=json_gl_light()
				simulation_name="segment"+str(i)
				a.load_from_json(json[simulation_name])
				self.segments.append(a)

	def safe_init(self,segs):
		if segs!=6:
			self.segments=[]
			l=json_gl_light()
			l.x0=0
			l.y0=5
			l.z0=-10
			self.segments.append(l)

			l=json_gl_light()
			l.x0=0
			l.y0=-5
			l.z0=-10
			self.segments.append(l)


			l=json_gl_light()
			l.x0=0
			l.y0=5
			l.z0=10
			self.segments.append(l)

			l=json_gl_light()
			l.x0=0
			l.y0=-5
			l.z0=10
			self.segments.append(l)

			l=json_gl_light()
			l.x0=-10
			l.y0=-5
			l.z0=0
			self.segments.append(l)

			l=json_gl_light()
			l.x0=10
			l.y0=-5
			l.z0=0
			self.segments.append(l)

			return True
		return False

