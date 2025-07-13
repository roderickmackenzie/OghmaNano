# 
# General-purpose Photovoltaic Device Model oghma-nano.com - a drift diffusion
# base/Shockley-Read-Hall model for 1st, 2nd and 3rd generation solarcells.
# The model can simulate OLEDs, Perovskite cells, and OFETs.
# 
# Copyright 2008-2022 Roderick C. I. MacKenzie https://www.oghma-nano.com
# r.c.i.mackenzie at googlemail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
# 

import os
import sys
import shutil
try:
	from dialog import Dialog
except:
	from menu import Dialog

from shutil import copyfile
from shutil import rmtree
from util import copytree
from install import do_install

def find_installed_dir(src_path,search_name,directory=True):
	found=[]
	for root, dirs, files in os.walk(src_path):
		for name in list(set(files + dirs)) :
			if directory==True:
				dir_name=os.path.dirname(os.path.join(root, name))
				if dir_name.endswith(search_name):
					if dir_name not in found:
						found.append(dir_name)
			if directory==False:
				file_name=os.path.join(root, name)
				if os.path.isfile(file_name)==True:
					if file_name.endswith(search_name):
						if file_name not in found:
							found.append(file_name)
	print(found)
	if len(found)==0:
		return None

	return min(found, key=len) 

def intelligent_move(dest_root,search_path,target,directory=True):
	src=find_installed_dir(search_path,target,directory=directory)
	if src==None:
		print("not found",target)
		return

	if os.path.isdir(src)==True:
		for f in os.listdir(src):
			dest=os.path.join(dest_root,f)
			src_file=os.path.join(src,f)
			if os.path.isdir(os.path.dirname(dest))==False:
				os.makedirs(os.path.dirname(dest))
			print("move",src_file)
			shutil.move(src_file,dest)
	else:
		shutil.move(src,dest_root)

def flat_install(d):

	pub_path=os.path.join(os.getcwd(),"pub")
	output_path=os.path.join(pub_path,"build")
	flat_path=os.path.join(pub_path,"flat")
	flat_path_plugins=os.path.join(flat_path,"plugins")
	flat_path_inp_template=os.path.join(flat_path,"inp_template")
	flat_path_docs=os.path.join(flat_path,"docs")
	flat_path_device_lib=os.path.join(flat_path,"device_lib")
	flat_path_licenses=os.path.join(flat_path,"licenses")

	#asdsd

	if os.path.isdir(pub_path)==True:
		rmtree(pub_path)

	do_install(d,output_path)

	#This needs fixing
	intelligent_move(flat_path,output_path,"oghma_core")
	intelligent_move(flat_path_licenses,output_path,"licenses")

	intelligent_move(flat_path,output_path,"oghma_data")
	intelligent_move(flat_path_device_lib,output_path,"device_lib")
	intelligent_move(flat_path,output_path,"oghma_gui")

	intelligent_move(flat_path_plugins,output_path,"plugins")
	intelligent_move(flat_path,output_path,"icons")
	intelligent_move(flat_path_docs,output_path,"doc")
	intelligent_move(flat_path,output_path,"man")
	intelligent_move(flat_path_inp_template,output_path,"inp_template")
	intelligent_move(flat_path,output_path,"applications")
	intelligent_move(flat_path,output_path,"mime")
	intelligent_move(flat_path,output_path,"video")
	#The bin file
	intelligent_move(flat_path,output_path,"oghma_core",directory=False)
	intelligent_move(flat_path,output_path,"oghma_core.exe",directory=False)
	intelligent_move(flat_path,output_path,"liboghma_core.dll",directory=False)
	intelligent_move(flat_path,output_path,"liboghma_core.so",directory=False)
	intelligent_move(flat_path,output_path,"liboghma_fdtd.dll",directory=False)
	intelligent_move(flat_path,output_path,"liboghma_fdtd.so",directory=False)
	intelligent_move(flat_path,output_path,"liboghma_py.dll",directory=False)
	intelligent_move(flat_path,output_path,"liboghma_py.so",directory=False)

	os.symlink("gui/oghmanano.py",os.path.join(flat_path,"oghmanano"))
	#os.symlink("gui/oghma_tool.py",os.path.join(flat_path,"oghma_tool"))


	#shutil.copytree("./oghma_data/materials", os.path.join(output_path,"materials"), symlinks=False)
	#shutil.copytree("./oghma_data/spectra", os.path.join(output_path,"spectra"), symlinks=False)
	return flat_path
