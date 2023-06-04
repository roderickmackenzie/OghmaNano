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

## @package export_materials
#  Export the materials database to a zip file.
#

import os
import zipfile
from progress_class import progress_class
from process_events import process_events
from cal_path import remove_cwdfrompath

def export_materials(target):
	if target.endswith(".zip")==False:
		target=target+".zip"

	file_list=[]

	progress_window=progress_class()
	progress_window.show()
	progress_window.start()
	process_events()
	mat_files=["alpha.csv","cost.xlsx","dos.inp","fit.inp","data.json","n.csv","pl.inp"]
	for path, dirs, files in os.walk(os.path.join(os.getcwd(),"materials")):
		for file_name in files:
			if file_name in mat_files:
				file_list.append(os.path.join(path,file_name))

	zf = zipfile.ZipFile(target, 'a')

	for i in range(0,len(file_list)):
		cur_file=file_list[i]

		lines=[]
		if os.path.isfile(cur_file):
			f=open(cur_file, mode='rb')
			lines = f.read()
			f.close()


			zf.writestr(remove_cwdfrompath(cur_file), lines)
			progress_window.set_fraction(float(i)/float(len(file_list)))
			progress_window.set_text("Adding"+cur_file[len(os.getcwd()):])
			process_events()

	zf.close()
	progress_window.stop()

