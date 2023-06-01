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

## @package json_contacts
#  Back end to deal with contacts.
#

from shape import shape
from json_base import json_base

class contact(shape):
	def __init__(self):
		super().__init__()
		self.var_list.append(["position","top"])
		self.var_list.append(["applied_voltage_type","constant"])
		self.var_list.append(["applied_voltage",-2.0])
		self.var_list.append(["contact_resistance_sq",0.0])
		self.var_list.append(["shunt_resistance_sq",0.0])
		self.var_list.append(["np",1e20])
		self.var_list.append(["charge_type","electron"])
		self.var_list.append(["physical_model","ohmic"])
		self.var_list.append(["ve0",1e5])
		self.var_list.append(["vh0",1e5])
		self.var_list_build()
		self.latex_banned=["all"]
		self.latex_allowed=["np"]

class json_contacts(json_base):

	def __init__(self):
		self.this_is_the_contact_class=None
		json_base.__init__(self,"contacts",segment_class=True)

	def em(self):
		self.load()
		self.changed.emit()

	def load_json(self,json):
		self.segments=[]
		if "ncontacts" in json:
			ncontacts=json['ncontacts']
			for n in range(0,ncontacts):
				contact_name="contact"+str(n)
				c=contact()
				c.decode_from_json(json[contact_name])

				self.segments.append(c)

		if "segments" in json:
			ncontacts=json['segments']
			for n in range(0,ncontacts):
				contact_name="segment"+str(n)
				c=contact()
				c.decode_from_json(json[contact_name])

				self.segments.append(c)

	def print():
		for s in self.segments:
			print(s.x0, s.dx,s.depth,s.contact_applied_voltage,s.contact_applied_voltage_type)

	def clear():
		self.segments=[]

	def get_layers_with_contacts(self):
		layers=[]
		for c in self.segments:
			if c.position not in layers:
				layers.append(c.position)

		return layers

	def insert(self,pos):
		s=contact()
		s.position="top"
		s._applied_voltage="ground"
		s.np=1e25
		s.physical_model="ohmic"
		s.contact_resistance_sq="0.0"
		s.shunt_resistance_sq="1e7"
		s.ve0=1e7
		s.vh0=1e7
		s.charge_type="electron"
		s.name="new_contact"
		s.type="box"
		self.segments.insert(pos,s)
		return self.segments[pos]

