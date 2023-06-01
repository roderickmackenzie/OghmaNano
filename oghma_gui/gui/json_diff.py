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

## @package json_diff
# Diff two json objects
#

def json_diff(obj0,obj1,path=""):
	ret=[]
	for obj in obj0:
		if type(obj0[obj])==dict:
			if path!="":
				new_path=path+"."+obj
			else:
				new_path=obj

			my_ret=json_diff(obj0[obj],obj1,path=new_path)
			ret.extend(my_ret)
		else:
			if path!="":
				cur_path=path+"."+obj
				pointer=obj1
				for seg in cur_path.split("."):
					#print(pointer,seg)
					pointer=pointer[seg]
			else:							#This is to deal with items in the root of the tree which are not a dic
				pointer=obj1[obj]	
				cur_path=obj

			if pointer!=obj0[obj]:
				ret.append(cur_path)

	return ret


