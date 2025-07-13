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

## @package detectors_editor
#  Main window for settign up detectors
#

import i18n
_ = i18n.language.gettext

from vec import vec
from experiment_bin import experiment_bin
from global_objects import global_object_run
from json_c import json_tree_c

class detectors_editor(experiment_bin):

	def __init__(self,data=None):
		experiment_bin.__init__(self,"tab_jv",window_save_name="detectors_editor", window_title=_("Optical detectors editor"),json_search_path="optical.detectors")
		self.bin=json_tree_c()
		self.notebook.currentChanged.connect(self.switch_page)
		self.switch_page()
		self.changed.connect(self.callback_changed)
		self.fixup_new=self.my_fixup_new

	def switch_page(self):
		self.notebook.currentWidget()

	def callback_changed(self):
		global_object_run("gl_force_redraw")

	def my_fixup_new(self,json_path):
		world_min=vec()
		world_max=vec()
		self.bin.json_world_size(world_min,world_max)

		dx=world_max.x-world_min.x
		dy=(world_max.y-world_min.y)/100.0
		dz=world_max.z-world_min.z

		self.bin.set_token_value(json_path,"dx",dx)
		self.bin.set_token_value(json_path,"dy",dy)
		self.bin.set_token_value(json_path,"dz",dz)
		self.bin.set_token_value(json_path,"moveable",True)

		self.bin.set_token_value(json_path,"color_r",0.0)
		self.bin.set_token_value(json_path,"color_g",1.0)
		self.bin.set_token_value(json_path,"color_b",0.0)
		self.bin.set_token_value(json_path,"color_alpha",0.5)

