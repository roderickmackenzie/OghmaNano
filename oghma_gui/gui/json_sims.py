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

from json_ray import json_ray
from json_jv import json_jv
from json_suns_jsc import json_suns_jsc
from json_suns_voc import json_suns_voc
from json_base import json_base
from json_pl import json_pl
from json_ce import json_ce
from json_cv import json_cv
from json_eqe import json_eqe
from json_equilibrium import json_equilibrium
from json_fdtd import json_fdtd
from json_mode import json_mode
from json_time_domain import json_time_domain
from json_fx_domain import json_fx_domain
from json_spm import json_spm
from json_transfer_matrix import json_transfer_matrix
from json_exciton import json_exciton

class json_sims(json_base):

	def __init__(self):
		json_base.__init__(self,"sims")
		self.var_list=[]
		self.var_list.append(["jv",json_jv()])
		self.var_list.append(["suns_voc",json_suns_voc()])
		self.var_list.append(["suns_jsc",json_suns_jsc()])
		self.var_list.append(["time_domain",json_time_domain()])
		self.var_list.append(["fx_domain",json_fx_domain()])
		self.var_list.append(["cv",json_cv()])
		self.var_list.append(["ce",json_ce()])
		self.var_list.append(["pl_ss",json_pl()])
		self.var_list.append(["transfer_matrix",json_transfer_matrix()])
		self.var_list.append(["eqe",json_eqe()])
		self.var_list.append(["equilibrium",json_equilibrium()])
		self.var_list.append(["fdtd",json_fdtd()])
		self.var_list.append(["mode",json_mode()])
		self.var_list.append(["ray",json_ray()])
		self.var_list.append(["spm",json_spm()])
		self.var_list.append(["exciton",json_exciton()])

		self.var_list_build()


