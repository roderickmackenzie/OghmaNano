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

## @package export_archive
#  Export the simulation to an archive.
#

import os
import zipfile
from progress_class import progress_class
from process_events import process_events
from cal_path import remove_simpathfrompath

from cal_path import sim_paths

def export_archive(target,everything):
	if target.endswith(".oghma")==False:
		target=target+".oghma"

	file_list=[]

	progress_window=progress_class()
	progress_window.show()
	progress_window.start()
	process_events()

	if everything==True:
		for path, dirs, files in os.walk(sim_paths.get_sim_path()):
			for file_name in files:
				if file_name.endswith(".inp") or file_name.endswith(".dat") or file_name.endswith(".csv"):
					file_list.append(os.path.join(path,file_name))
	else:
		files=os.listdir(sim_paths.get_sim_path())
		for file_name in files:
			if file_name.endswith(".inp"):
				file_list.append(os.path.join(sim_paths.get_sim_path(),file_name))

	zf = zipfile.ZipFile(target, 'a')

	for i in range(0,len(file_list)):
		cur_file=file_list[i]

		lines=[]
		if os.path.isfile(cur_file):
			try:
				f=open(cur_file, mode='rb')
				lines = f.read()
				f.close()


				zf.writestr(remove_simpathfrompath(cur_file), lines)
			except:
				print(_("Can't open file ")+cur_file)

			progress_window.set_fraction(float(i)/float(len(file_list)))
			progress_window.set_text("Adding"+cur_file[len(sim_paths.get_sim_path()):])
			process_events()

	src_zf = zipfile.ZipFile(os.path.join(sim_paths.get_sim_path(),"sim.oghma"), 'r')

	for file_name in src_zf.namelist():
		if file_name not in zf.namelist():
			#print "adding from archive",file_name
			lines=src_zf.read(file_name)
			zf.writestr(file_name, lines)

	zf.close()
	src_zf.close()
	progress_window.stop()

