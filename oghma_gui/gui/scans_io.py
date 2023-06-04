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

## @package scans_io
#  IO functions for the scanning simulation parameters.
#


import os


from progress_class import progress_class
from process_events import process_events

from error_dlg import error_dlg

import i18n
_ = i18n.language.gettext

from yes_no_cancel_dlg import yes_no_cancel_dlg

from util_zip import archive_add_dir
from inp import inp
from scan_io import scan_io
from safe_delete import safe_delete
from decode_inode import decode_inode
from clean_sim import ask_to_delete

class scans_io:

	def __init__(self,path):
		self.path=path
		self.parent_window=None
		self.interactive=True

	def get_scan_dirs(self):
		scan_dirs=[]
		f=inp(file_path=os.path.join(self.path,"sim.oghma"))
		ls=f.lsdir()

		for scan_file in ls:
			f_name=os.path.join(self.path,scan_file)
			ret=decode_inode(f_name)
			if ret.type=="scan":
				scan_dirs.append(f_name)


		return scan_dirs

	def delete(self,scan_name):
		full_file_name=os.path.join(self.path,scan_name)
		if scan_io().is_scan_dir(full_file_name)==True:
			safe_delete(full_file_name,allow_dir_removal=True)


	def clean_all(self):
		dirs_to_del=[]
		scans=self.get_scan_dirs()
		for scan_dir in scans:
			listing=os.listdir(scan_dir)

			for sub_dir in listing:
				full_path=os.path.join(scan_dir, sub_dir)
				if os.path.isdir(full_path)==True:
					dirs_to_del.append(full_path)
		print(dirs_to_del)
		ask_to_delete(self.parent_window,dirs_to_del,interactive=True)


