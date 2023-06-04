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

import os
import fnmatch
import numpy
import shutil

from cal_path import get_base_material_path
from util_zip import zip_remove_file
from math import sqrt
from n_to_rgb import n_to_rgb
import yaml
from bibtex import bibtex
from dat_file import dat_file
from yml_to_dat_file import yml_to_dat_file
from json_material_db_item import json_material_db_item


def process_yml_file(dest,yml_src_file):
	print("src:",yml_src_file)
	print("dst:",dest)
	lam=[]
	n=[]
	alpha=[]
	settings_stream=open(yml_src_file, 'r')
	print("Importing",yml_src_file,dest)
	settingsMap=yaml.safe_load(settings_stream)

	alpha,n=yml_to_dat_file(settingsMap)

	r=0.5
	g=0.5
	b=0.5

	if n!=False and alpha!=False:
		alpha.y_len=len(alpha.y_scale)
		n.y_len=len(n.y_scale)
		r,g,b=n_to_rgb(n.y_scale,n.data[0][0],alpha.y_scale,alpha.data[0][0])

		if os.path.isdir(dest)==False:
			os.makedirs(dest)

		a=json_material_db_item()

		a.color_r=round(r,2)
		a.color_g=round(g,2)
		a.color_b=round(b,2)
		a.save_as(os.path.join(dest,"data.json"))

		alpha.save(os.path.join(dest,"alpha.csv"))
		n.save(os.path.join(dest,"n.csv"))

		#do refs
		b=bibtex()

		new_ref=b.new()
		new_ref.token="alpha"
		new_ref.type="article"
		new_ref.unformatted=settingsMap['REFERENCES']

		new_ref=b.new()
		new_ref.token="n"
		new_ref.type="article"
		new_ref.unformatted=settingsMap['REFERENCES']

		b.save_as(os.path.join(dest,"mat.bib"))
	else:
		print("no")



	return


def clean_and_order_path(path):
	path=path.split(os.sep)
	if path[0]=="database":
		path=path[1:]

	if path[0]=="data":
		path=path[1:]

	path=os.path.sep.join(path)
	path=path.replace(" ","_")
	path=path.replace("(","_")
	path=path.replace(")","_")
	return path
	
def yml_nk_db_sync(search_path):
	for root, dirnames, filenames in os.walk(search_path):
		for file_name in fnmatch.filter(filenames, '*.yml'):
			yml_file=os.path.join(root, file_name)

			rel_path=os.path.relpath(yml_file, search_path)[:-4]
			decoded_path=clean_and_order_path(rel_path)
			dest=os.path.join(get_base_material_path(),"refractive_index_db",decoded_path)
			process_yml_file(dest,yml_file)

	return
