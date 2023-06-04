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

from experiment import experiment
from global_objects import global_object_run
from json_root import json_root

class detectors_editor(experiment):


	def __init__(self,data=None):
		experiment.__init__(self,"detectors_tab",window_save_name="detectors_editor", window_title=_("Optical detectors editor"),json_search_path="json_root().optical.detectors")

		self.base_json_obj="from json_detectors import json_detector"
		self.notebook.currentChanged.connect(self.switch_page)
		self.switch_page()
		self.changed.connect(self.callback_changed)
		self.fixup_new=self.my_fixup_new

	def switch_page(self):
		self.notebook.currentWidget()
		#self.tb_lasers.update(tab.data)

	def callback_changed(self):
		global_object_run("gl_force_redraw")

	def my_fixup_new(self,a):
		world_min,world_max=json_root().get_world_size()
		a.dx=world_max.x-world_min.x
		a.dy=(world_max.y-world_min.y)/100.0
		a.dz=world_max.z-world_min.z


