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

## @package oghma_local
#  JV experiment editor
#
import os
import i18n
_ = i18n.language.gettext

from experiment import experiment
from cal_path import sim_paths
from clone_materials import clone_materials
from win_lin import get_platform
import shutil
from progress_class import progress_class
from process_events import process_events

class oghma_local:

	def do_cpy(self,progress_window=None,just_count=False,all_files=100):
		total=0
		total=clone_materials(sim_paths.get_materials_path(), sim_paths.get_base_material_path(),"material",progress_window=progress_window,total=total, just_count=just_count,all_files=all_files)

		total=clone_materials(sim_paths.get_shape_path(), sim_paths.get_base_shape_path(),"shape",progress_window=progress_window,total=total, just_count=just_count,all_files=all_files)

		if os.path.isdir(sim_paths.get_scripts_path())==False:
			shutil.copytree(sim_paths.get_base_scripts_path(), sim_paths.get_scripts_path() ,symlinks=True)

		total=clone_materials(sim_paths.get_filters_path(), sim_paths.get_base_filters_path(),"filter",progress_window=progress_window,total=total, just_count=just_count,all_files=all_files)

		total=clone_materials(sim_paths.get_spectra_path(), sim_paths.get_base_spectra_path(),"spectra",progress_window=progress_window,total=total, just_count=just_count,all_files=all_files)

		return total

	def oghma_local_setup(self):
		if sim_paths.get_use_json_local_root()==True:
			total=self.do_cpy(just_count=True)
			if total>0:
				progress_window=progress_class()
				progress_window.setWindowTitle(_("Copying files and configuring"))
				progress_window.start(offset=False)

				process_events()
				if get_platform()=="wine":
					path=sim_paths.get_wine_home_dir()
					if path!=False:
						wine_json_local_root=os.path.join(path,"json_local_root")
						if os.path.isdir(wine_json_local_root)==False:
							os.symlink(sim_paths.get_user_settings_dir(), wine_json_local_root, target_is_directory=True)
				
				self.do_cpy(progress_window=progress_window,just_count=False,all_files=total)

				progress_window.start()
				progress_window.stop()

