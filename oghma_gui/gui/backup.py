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

## @package backup
#  Backup a simulation
#
#import sys
import os
#import glob
from shutil import copyfile
from json_c import json_c
from safe_delete import safe_delete

def backup(dest,src,notes=""):

	if os.path.isdir(dest)==False:
		os.makedirs(dest)

	data=json_c("folder_backup")
	data.build_template()
	data.save_as(os.path.join(dest,"data.json"))

	for f in os.listdir(src):
		if f.endswith(".inp") or f=="sim.oghma" or f=="sim.json":
			src_file=os.path.join(src,f)
			dst_file=os.path.join(dest,f)
			copyfile(src_file,dst_file)

def backup_restore(dest,src):

	for f in os.listdir(dest):
		if f.endswith(".inp") or f=="sim.oghma" or f=="sim.json":
			safe_delete(os.path.join(dest,f))

	for f in os.listdir(src):
		if f.endswith(".inp") or f=="sim.oghma" or f=="sim.json":
			if f!="data.json":
				src_file=os.path.join(src,f)
				dst_file=os.path.join(dest,f)
				copyfile(src_file,dst_file)


