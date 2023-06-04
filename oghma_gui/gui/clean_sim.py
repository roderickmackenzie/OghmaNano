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

## @package clean_sim
#  Clean the simulation
#

#import sys
import os
from cal_path import sim_paths
from safe_delete import safe_delete

#import glob


def clean_sim_dir(path,clean_exp_data=True):
	if clean_exp_data==True:
		for f in os.listdir(path):
			full_path=os.path.join(path,f)
			if f.startswith("fit_data")==True:
				if f.endswith(".inp")==True:
					os.unlink(full_path)


def delete_files(dirs_to_del,parent_window=None):
	if parent_window!=None:
		from yes_no_cancel_dlg import yes_no_cancel_dlg
		from progress_class import progress_class
		from process_events import process_events

		progress_window=progress_class()
		progress_window.show()
		progress_window.start()

		process_events()
	
	for i in range(0, len(dirs_to_del)):
		safe_delete(dirs_to_del[i],allow_dir_removal=True)
		if parent_window!=None:
			progress_window.set_fraction(float(i)/float(len(dirs_to_del)))
			progress_window.set_text("Deleting"+dirs_to_del[i])
			process_events()

	if parent_window!=None:
		progress_window.stop()


def ask_to_delete(parent_window,dirs_to_del,interactive=True):
	if len(dirs_to_del)!=0:

		if interactive==True:
			from yes_no_cancel_dlg import yes_no_cancel_dlg
			text_del_dirs=""
			n=0
			for dir_item in dirs_to_del:
				text_del_dirs=text_del_dirs+dir_item+"\n"
				if n>15:
					text_del_dirs=text_del_dirs+_("and ")+str(len(dirs_to_del)-30)+_(" more.")
					break
				n=n+1

			text=_("Should I delete these files?:\n")+"\n"+text_del_dirs

			response = yes_no_cancel_dlg(parent_window,text)

			if response == "yes":
				delete_files(dirs_to_del,parent_window)
				return "yes"
			elif response == "no":
				return "no"
			elif response == "cancel":
				return "cancel"
		else:
			delete_files(dirs_to_del,parent_window)
