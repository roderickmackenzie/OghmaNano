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

## @package scan_human_labels
#  A class to turn the .inp into human labels
#
#import sys
from token_lib import tokens
from epitaxy import get_epi

import json


def json_get_val(json_data,path):
	try:
		pointer=json_data
		for seg in path.split("."):
			pointer=pointer[seg]
		return pointer
	except:
		return None

#this should be merged to use get_json_path_from_human_path
def set_json_from_human_path(json,path,val):
	pointer=json
	s=path.replace('\\','.')		#These are old, don't use any more
	s=path.replace('/','.')
	s=s.split(".")
	for token in s:
		found=False
		if token.startswith("segments[") and token.endswith("]"):
			token="segment"+token[len("segments["):-1]

		if token in pointer:
			true_token=token
			found=True
		
		if found==False:
			for json_obj in pointer:
				sub_obj=pointer[json_obj]
				name=False
				try:
					name=sub_obj['name']
				except:
					pass

				if name!=False:
					if name==token:
						true_token=json_obj
						found=True
						break

		if found==False:
			lib_token=tokens().reverse_lookup(token)
			if lib_token!=False:
				token=lib_token.token
				if token in pointer:
					true_token=token
					found=True

				
		if found==False:
			print("lost at ",token,tokens().reverse_lookup(token))
			return False
		else:
			#print(true_token)
			last_pointer=pointer
			pointer=pointer[true_token]

	if found==True:
		last_pointer[true_token]=val

def get_json_path_from_human_path(json_in,path):
	if type(json_in)!=dict:
		json_in=json.loads("\n".join(json_in.gen_json()))

	pointer=json_in
	s=path.replace('\\','.')		#These are old, don't use any more
	s=s.replace('/','.')
	s=s.split(".")
	out_path=[]

	for token in s:
		found=False
		#print(">",token)
		if token in pointer:
			true_token=token
			found=True

		if found==False:
			for json_obj in pointer:
				sub_obj=pointer[json_obj]
				name=False
				try:
					name=sub_obj['name']
				except:
					pass

				if name!=False:
					if name==token:
						true_token=json_obj
						found=True
						break

		if found==False:
			lib_token=tokens().reverse_lookup(token)
			#print(lib_token)
			if lib_token!=False:
				token=lib_token.token
				if token in pointer:
					true_token=token
					found=True

		if token.startswith("segments[") and token.endswith("]"):
			val=token[9:-1]
			true_token="segment"+val
			found=True

		if found==False:
			print("lost at2 |",token,"|",tokens().reverse_lookup(token),"|",s)
			#print(pointer)
			print("lost")
			return False
		else:
			#print(true_token)
			out_path.append(true_token)
			pointer=pointer[true_token]

	if found==True:
		return ".".join(out_path)

def get_json_obj_from_human_path(json,path):
	json_path=get_json_path_from_human_path(json,path)
	pointer=json
	s=json_path.split(".")
	found=True
	for token in s:
		try:
			pointer=pointer[token]
			found=True
		except:
			found=False

	if found==True:
		return pointer
	return False

def get_python_path_from_human_path(json,path):
	json_path=get_json_path_from_human_path(json,path)
	split_path =json_path.split(".")
	converted=[]
	for s in split_path:
		if s.startswith("layer"):
			s="layers["+str(s[5:])+"]"
		elif s.startswith("segment"):
			s="segments["+str(s[7:])+"]"
		converted.append(s)

	converted=".".join(converted)

	if len(converted)>0:
		converted="."+converted

	return "json_root()"+converted

