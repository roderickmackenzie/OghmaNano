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

## @package check_lib_in_bash_rc
#  Check the bash rc for the lib path
#

import os
from win_lin import get_platform
from inp import inp
from cal_path import sim_paths

def check_lib_in_bash_rc():
	if get_platform()=="linux":
		if sim_paths.installed_from_deb==True:
			return
		f=inp()
		oghma_installed=-1
		if f.load(os.path.join(sim_paths.get_home_path(),".bashrc"))!=False:
			for i in range(0,len(f.lines)):
				if f.lines[i].startswith("export LD_LIBRARY_PATH")==True and f.lines[i].count("oghma")!=0:
					oghma_installed=i
					if f.lines[i].endswith(sim_paths.get_exe_path()):
						return
		line="export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"+sim_paths.get_exe_path()

		if oghma_installed==-1:
			f.lines.append(line)
		else:
			f.lines[i]=line
		f.save()

