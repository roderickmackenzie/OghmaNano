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

## @package import_archive
#  Logic to import .oghma files, even if they are in an older fromat.
#


import os
import shutil
use_gui=False
try:
	from progress_class import progress_class
	from process_events import process_events
	use_gui=True
except:
	pass

def copy_device(src_json, dest_dir,setup_sim_to_run=False):
	src_dir=os.path.dirname(src_json)
	if src_json.endswith("sim.json")==False:
		if os.path.isdir(dest_dir)==False:
			os.makedirs(dest_dir)
		dst_file_name = os.path.basename(src_json)
		if setup_sim_to_run==True:
			dst_file_name="sim.json"
		shutil.copyfile(src_json,os.path.join(dest_dir,dst_file_name))
		return					

	if use_gui==True:
		progress_window=progress_class()
		progress_window.show()
		progress_window.start()

	banned=["data.json"]
	allowed_files=[".json",".inp",".bib",".py",".m"]
	for root, dirs, files in os.walk(src_dir):
		if "sim" in root.split(os.sep):
			continue

		for file in files:
			file_root, file_extension = os.path.splitext(file)
			if file not in banned:
				if file_extension in allowed_files:
					src_file_path = os.path.join(root, file)

					relative_path = os.path.relpath(root, src_dir)
					dest_path = os.path.join(dest_dir, relative_path)

					os.makedirs(dest_path, exist_ok=True)

					shutil.copy2(src_file_path, os.path.join(dest_path, file))

					print(f"Copied: {src_file_path} to {os.path.join(dest_path, file)}")

					if use_gui==True:
						progress_window.pulse()
						progress_window.set_text("Importing "+src_file_path)
						process_events()

	if use_gui==True:
		process_events()
		progress_window.stop()

