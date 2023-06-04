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

## @package fxexperiment
#  Main fx domain experiment window
#

from fxexperiment_tab import fxexperiment_tab

from icon_lib import icon_get

import i18n
_ = i18n.language.gettext

#window
from util import wrap_text
from experiment import experiment
from fxexperiment_tab import fxexperiment_tab


class fxexperiment(experiment):


	def __init__(self):
		experiment.__init__(self,"fxexperiment_tab",window_save_name="fx_domain_experiment", window_title=_("Frequency domain experiment window"),json_search_path="json_root().sims.fx_domain")

		#w=self.ribbon_simulation()
		#self.ribbon.addTab(w,_("Simulation"))

		self.notebook.currentChanged.connect(self.switch_page)
		self.switch_page()



	def switch_page(self):
		self.notebook.currentWidget()
		#self.tb_lasers.update(tab.data)

