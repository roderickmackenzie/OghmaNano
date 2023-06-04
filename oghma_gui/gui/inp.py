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

## @package inp
#  Used for writing and reading .inp files from .gpvdm archives
#

import os

from win_lin import get_platform
from util_zip import zip_remove_file
from util_zip import write_lines_to_archive
from util_zip import archive_isfile
from util_zip import zip_lsdir

from cal_path import sim_paths
from util_zip import zip_get_raw_data

from util_zip import archive_get_file_time
from util import is_number
import json
from sim_name import sim_name

class inp:

	def __init__(self,file_path=None):
		self.lines=[]
		self.pos=0
		self.zip_file_path=os.getcwd()

		if file_path!=None:
			self.set_file_name(file_path)
		self.json=None

	def tab(self):
		begin=""
		for i in range(0, len(self.lines)):
			self.lines[i]=begin+self.lines[i].lstrip()
			if self.lines[i].count("{")>0:
				begin=begin+"\t"
			if self.lines[i].count("}")>0:
				if len(begin)>0:
					begin=begin[:-1]

	def __str__(self):
		if self.lines==False:
			return ""
		ret=""
		for i in range(0, len(self.lines)):
			ret=ret+self.lines[i]+"\n"

		return ret

	def lsdir(self):
		return zip_lsdir(self.zip_file_path)

	def set_file_name(self,file_path,archive="sim"+sim_name.file_ext,mode="l"):
		if file_path==None:
			return False

		file_name=default_to_sim_path(file_path)

		if file_name.endswith(sim_name.file_ext):		#we are opperating on just the archive
			self.zip_file_path=file_name
			self.file_name=None
			return

		if os.path.dirname(file_path).endswith(sim_name.file_ext):		#/handles a/b/sim.archive/jv.inp
			self.zip_file_path=os.path.dirname(file_path)
		else:
			self.zip_file_path=search_zip_file(file_name,archive)

		self.file_name=os.path.basename(file_name)

	def get_ver(self,file_path):
		self.load(file_path)
		return self.get_token("#ver")

	def check_if_i_can_read(self,file_name):
		try:
			f = open(file_name, "r")
			f.readlines()
			f.close()
			return True
		except:
			return False

	def load(self,file_path,archive="sim.oghma",mode="l"):
		self.set_file_name(file_path,archive=archive,mode=mode)

		if self.file_name!=None:
			self.lines=zip_get_raw_data(file_path,archive=archive,mode=mode)

		if self.lines==False:
			return False

		return self

	def load_json(self,file_path,archive="sim.oghma"):
		if self.load(file_path,archive=archive)==False:
			return False

		if self.lines!=False:
			lines="\n".join(self.lines)
			try:
				self.json=json.loads(lines)
			except:
				return False

		return self.json

	def sync_json_to_lines(self):
		self.lines=json.dumps(self.json).split("\n")

	def isfile(self,file_path,archive="sim"+sim_name.file_ext):
		file_name=default_to_sim_path(file_path)
		
		self.zip_file_name=search_zip_file(file_name,archive)

		return archive_isfile(self.zip_file_name,os.path.basename(file_name))


	def delta_tokens(self,cmp_file):
		missing_in_cmp=[]
		for self_line in self.lines:
			if self_line.startswith("#"):
				for cmp_line in cmp_file.lines:
					found=False
					if self_line==cmp_line:
						found=True
						break
				if found==False:
					missing_in_cmp.append(self_line)

		return missing_in_cmp

	def import_tokens(self,in_file):
		for self_line in self.lines:
			if self_line.startswith("#") and self_line!="#ver" and self_line!="#end":
				in_data=in_file.get_token(self_line)
				if in_data!=False:
					self.replace(self_line,in_data)

	def get_token(self,token):
		if self.lines==False:
			return False

		"""Get the value of a token from a list"""
		for i in range(0, len(self.lines)):
			if self.lines[i]==token:
				if i+1<len(self.lines):
					return self.lines[i+1]
				return False
		return False

	def reset(self):
		self.pos=0

	def get_file_name(self):
		return os.path.join(self.zip_file_path,self.file_name)
	
	def get_tokens(self):
		ret=[]
		for l in self.lines:
			if l.startswith("#"):
				ret.append(l)
		return ret

	def replace_token_name(self,old_token,new_token):
		if type(self.lines)!=list:
			return False

		for i in range(0, len(self.lines)):
			if self.lines[i].startswith(old_token)==True:
				delta=self.lines[i][len(old_token):]
				try:
					int(delta)
				except:
					delta=""

				self.lines[i]=new_token+delta
				#return


	#update a token value
	def set_token(self,token,value):
		return self.replace(token,value)

	def replace(self,token,replace):
		if type(replace)==bool:
			replace=str(replace)

		if type(self.lines)!=list:
			return False

		replaced=False
		if type(replace)==str:
			for i in range(0, len(self.lines)):
				if self.lines[i]==token:
					#print(self.lines[i],token,replace)
					if i+1<len(self.lines):
						self.lines[i+1]=replace
						replaced=True
						break

		if type(replace)==list:
			ret=[]
			i=0
			while(i<len(self.lines)):
				ret.append(self.lines[i])
				if self.lines[i]==token:
					for r in replace:
						ret.append(r)
					for ii in range(i+1,len(self.lines)):
						if self.lines[ii].startswith("#")==True:
							i=ii-1
							break
				i=i+1

			self.lines=ret

		return replaced

	def save(self,mode="l",dest="archive"):
		"""Write save lines to a file"""
		ret= write_lines_to_archive(self.zip_file_path,self.file_name,self.lines,mode=mode,dest=dest)
		return ret

	def append(self,data):
		self.lines.append(data)

	def save_as(self,file_path,archive="sim"+sim_name.file_ext,mode="l",dest="archive"):

		full_path=default_to_sim_path(file_path)
		self.zip_file_path=os.path.join(os.path.dirname(full_path),archive)
		self.file_name=os.path.basename(full_path)

		return self.save(dest=dest)

	def delete(self):
		zip_remove_file(self.zip_file_path,self.file_name)

	def time(self):
		full_file_name=default_to_sim_path(self.file_name)

		if os.path.isfile(full_file_name):
			return os.path.getmtime(full_file_name)

		if os.path.isfile(self.zip_file_path):
			return archive_get_file_time(self.zip_file_path,os.path.basename(self.file_name))

		return -1



def inp_read_next_item(lines,pos):
	"""Read the next item form an inp file"""
	token=lines[pos]
	pos=pos+1
	value=lines[pos]
	pos=pos+1
	return token,value,pos


def inp_replace_token_value(lines,token,replace):
	"""replace the value of a token in a list"""
	if type(lines)!=list:
		return False

	replaced=False
	for i in range(0, len(lines)):
		if lines[i]==token:
			if i+1<len(lines):
				lines[i+1]=replace
				replaced=True
				break

	return replaced


def inp_update_token_value(file_path, token, replace,archive="sim"+sim_name.file_ext,id=""):
	lines=[]

	lines=inp_load_file(file_path,archive=archive)
	if lines==False:
		return False

	ret=inp_replace_token_value(lines,token,replace)
	if ret==False:
		return False


	inp_save(file_path,lines,archive=archive,id=id)

	return True


def default_to_sim_path(file_path):
	"""For file names with no path assume it is in the simulation directory"""
	head,tail=os.path.split(file_path)
	if head=="":
		return os.path.join(sim_paths.get_sim_path(),file_path)
	else:
		return file_path

def search_zip_file(file_name,archive):
	#Assume sim.oghma is in /a/b/c/ where mat.inp is in /a/b/c/mat.inp 
	zip_file_path=os.path.join(os.path.dirname(file_name),archive)
	if os.path.isfile(file_name)==True:
		#we found the file there so we do not care about the arhive 
		return zip_file_path

	#now try back one level
	#Using path /a/b/c/mat.inp look in /a/b/sim.oghma for the sim file
	#if os.path.isfile(zip_file_path)==False:
	#	zip_file_path=os.path.join(os.path.dirname(os.path.dirname(file_name)),archive)

	return zip_file_path

def inp_load_file(file_path,archive="sim"+sim_name.file_ext,mode="l"):
	"""load file"""
	if file_path==None:
		return False

	ret=zip_get_raw_data(default_to_sim_path(file_path),archive=archive,mode=mode)
	return ret

def inp_save(file_path,lines,archive="sim"+sim_name.file_ext,id=""):
	"""Write save lines to a file"""

	full_path=default_to_sim_path(file_path)
	archive_path=os.path.join(os.path.dirname(full_path),archive)
	file_name=os.path.basename(full_path)
	#print("archive",archive_path)
	#print("file",file_name)
	#print(lines)


	ret= write_lines_to_archive(archive_path,file_name,lines)

	return ret

def inp_save_lines_to_file(file_path,lines):
	"""This will save lines to a text file"""
	file_name=default_to_sim_path(file_path)
	dump='\n'.join(lines)

	dump=dump.rstrip("\n")
	dump=dump.encode('utf-8')
	try:
		f=open(file_name, mode='wb')
	except:
		return False
	f.write(dump)
	f.close()

	return True

def inp_search_token_value(lines, token):
	"""Get the value of a token from a list"""
	for i in range(0, len(lines)):
		if lines[i]==token:
			return lines[i+1]

	return False

def inp_get_token_value(file_path, token,archive="sim"+sim_name.file_ext):
	"""Get the value of a token from a file"""


	lines=[]
	lines=inp_load_file(file_path,archive=archive)
	if lines==False:
		return None

	ret=inp_search_token_value(lines, token)
	if ret!=False:
		return ret

	return None

