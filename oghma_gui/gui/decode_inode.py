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

## @package dir_decode
#  Functions to find out what type of directory we have
#



import os
from inp import inp
from inode import inode
from str2bool import str2bool
import json
from icon_lib import icon_get
from bytes2str import bytes2str
from bytes2str import str2bytes
from cal_path import sim_paths
import ctypes

def decode_inode_from_json(ret,decode):
	#This needs removing as we already have a C equivlent
	try:
		ret.type=str2bytes(decode['item_type'])
	except:
		pass

	try:
		ret.icon=str2bytes(decode['icon'])
	except:
		pass

	try:
		ret.hidden=str2bytes(str2bool(decode['hidden']))
	except:
		pass

	try:
		ret.sub_icon=str2bytes(decode['sub_icon'])
	except:
		pass

	try:
		ret.display_name=str2bytes(decode['name'])
	except:
		pass

	try:
		ret.display_name=str2bytes(decode['english_name'])
	except:
		pass

	try:
		ret.hide_this_json_file=str2bool(decode['hide_this_json_file'])
	except:
		pass

	try:
		ret.view_type=decode['view_type']
	except:
		pass

	return ret

def decode_inode(file_name):
	ret=inode()
	ret.file_name=str2bytes(os.path.basename(file_name))
	ext=""
	try:
		ext=os.path.splitext(file_name)[1]
	except:
		pass

	if file_name.endswith(".oghma"):
		f=inp()
		if f.load_json(os.path.join(os.path.dirname(file_name),"sim.json"),archive=os.path.basename(file_name))!=False:
			decode_inode_from_json(ret,f.json)
	else:
		sim_paths.get_dll_py().decode_inode(ctypes.byref(ret), ctypes.c_char_p(str2bytes(file_name)))


	if ret.icon==b"":
		if icon_get(ext)!=False:	
			ret.icon=str2bytes(ext)
		else:
			ret.icon=b"misc"

	return ret
	
