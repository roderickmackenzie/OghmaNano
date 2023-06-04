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
from scans_io import scans_io

from util_zip import zip_lsdir
from util_zip import zip_remove_file
from util_zip import archive_copy_file

from cal_path import get_materials_path
from util_zip import extract_file_from_archive

from progress_class import progress_class
from process_events import process_events
import re
from cal_path import sim_paths
from inp import inp

class file_type():
	JUST_COPY=0
	IGNORE=3

	
	def __init__(self,name="fit_data",dest="archive",copy_opp=JUST_COPY,base_file="",needed=True):
		self.name=name
		self.dest=dest
		self.copy_opp=copy_opp
		self.base_file=base_file
		self.needed=needed		#needed in every simulation
		if base_file=="":
			self.base_file=name
		if name.endswith(".inp")==True:
			self.index_file=False
		else:
			self.index_file=True

file_list=[]

file_list.append(file_type(name="genrate",dest="file",copy_opp=file_type().JUST_COPY))
file_list.append(file_type(name="sim.json",dest="archive",copy_opp=file_type().JUST_COPY))
file_list.append(file_type(name="fit_error_delta",dest="file",copy_opp=file_type().JUST_COPY))
file_list.append(file_type(name="fit_error_exp",dest="file",copy_opp=file_type().JUST_COPY))
file_list.append(file_type(name="fit_error_sim",dest="file",copy_opp=file_type().JUST_COPY))
file_list.append(file_type(name="fit_data",dest="file",copy_opp=file_type().JUST_COPY))
file_list.append(file_type(name="json.bib",copy_opp=file_type().JUST_COPY))

def get_file_info(file_name):
	match = re.match(r"([a-z_]+)([0-9]+)(.inp)", file_name, re.I)
	if match==None:
		match = re.match(r"([a-z_]+)([0-9]+)(.dat)", file_name, re.I)

	if match!=None:
		for i in range(0,len(file_list)):
			if file_list[i].name==match.groups()[0]:
				return file_list[i]
	
	for i in range(0,len(file_list)):
		if file_list[i].name==file_name:
			return file_list[i]
		
	return False


def merge_archives(src_archive,dest_archive,only_over_write):
	pass

	progress_window=progress_class()
	progress_window.show()
	progress_window.start()

	process_events()

	dest_path=os.path.dirname(dest_archive)

	ls=zip_lsdir(src_archive)

	#copy files without checking ver

	for i in range(0,len(ls)):
		info=get_file_info(ls[i])
		if info!=False:
			if info.copy_opp==file_type().JUST_COPY:
				#print(ls[i])
				archive_copy_file(dest_archive,ls[i],src_archive,ls[i],dest=info.dest)
		elif ls[i].endswith(".m"):
			archive_copy_file(dest_archive,ls[i],src_archive,ls[i],dest="file")

		progress_window.set_fraction(float(i)/float(len(ls)))
		progress_window.set_text("Importing "+ls[i])
		process_events()

	#if you find a materials directory in the archive try to merge it
	for i in range(0,len(ls)):
		zip_dir_name=ls[i].split("/")
		if zip_dir_name[0]=="materials":
			dest=os.path.join(os.path.dirname(get_materials_path()))
			#print("Try to read",src_archive,ls[i],dest)
			extract_file_from_archive(dest,src_archive,ls[i])

		if zip_dir_name[0]=="sim":
			extract_file_from_archive(dest_path,src_archive,ls[i])

		if zip_dir_name[0]=="calibrate":
			extract_file_from_archive(dest_path,src_archive,ls[i])

	#search for scan directories
	scan_dirs=[]
	for i in range(0,len(ls)):
		if ls[i].endswith("oghma_gui_config.inp"):
			scan_dirs.append(os.path.dirname(ls[i]))

	#extract scan directories
	for i in range(0,len(ls)):
		for ii in range(0,len(scan_dirs)):
			if ls[i].startswith(scan_dirs[ii])==True:
				#print("Try to read",src_archive,ls[i])
				extract_file_from_archive(dest_path,src_archive,ls[i])

	progress_window.stop()

def import_archive(src_archive,dest_archive,only_over_write):
	src_dir=os.path.dirname(src_archive)
	dest_dir=os.path.dirname(dest_archive)

	if src_archive.endswith('.json') and dest_archive.endswith('.oghma'):
		archive_copy_file(dest_archive,"sim.json",src_archive,os.path.basename(src_archive),dest="archive")
		return

	if src_archive.endswith('.oghma')==False:
		print("I can only import from .oghma files you asked me to import:")
		print(src_archive)
		return

	if dest_archive.endswith('.oghma')==False:
		print("I can only import to .oghma files")
		print(dest_archive)
		return

	merge_archives(src_archive,dest_archive,only_over_write)


