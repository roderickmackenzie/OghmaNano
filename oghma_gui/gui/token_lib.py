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
#   THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#   SOFTWARE.
#

## @package token_lib
#  A library of all tokens used in the model.
#

from cal_path import sim_paths
from hash_list import hash_list
from hash_list import c_list
import ctypes
from bytes2str import str2bytes
from bytes2str import bytes2str

lib={}
lib_r={}
lib_json={}
fast_lib=hash_list()
dll_lib=sim_paths.get_dll_py()

class token_lib_item(ctypes.Structure):
	_fields_ = [('token', ctypes.c_char * 100),
				('english', ctypes.c_char * 100),
				('widget', ctypes.c_char * 100),
				('units_widget', ctypes.c_char * 100),
				('units', ctypes.c_char * 100),
				('log', ctypes.c_int ),
				('hidden',ctypes.c_int),
				('hide_on_token',c_list),
				('hide_on_value',c_list),
				('show_on_token',c_list),
				('show_on_value',c_list),
				('default_token',c_list),
				('default_value',c_list),
				('pack',c_list)]

class my_data():
	def __init__(self,b,info,widget):
		self.units=b
		self.info=info
		self.defaults=None
		self.widget=widget
		self.units_widget="QLabel"
		self.hidden=False
		self.hide_on_token_eq=None
		self.show_on_token_eq=None
		self.pack=[]
		self.token=""


def ctoken_to_python_token(token):
	a=my_data(bytes2str(token.units),_(bytes2str(token.english)),bytes2str(token.widget))
	a.token=bytes2str(token.token)
	a.hidden=bool(token.hidden)
	a.units_widget=bytes2str(token.units_widget)
	#When all the tokens are gone these two need to be embedded in C
	if token.show_on_token.len>0:
		a.show_on_token_eq=[]
		for i in range(0,token.show_on_token.len):
			t=ctypes.create_string_buffer(400)
			val=ctypes.create_string_buffer(400)
			dll_lib.token_lib_get_show_on(ctypes.byref(token),t,val,i)
			tok=bytes2str(val.value)
			if tok.lower()=="false":
				tok=False
			elif tok.lower()=="true":
				tok=True
			a.show_on_token_eq.append([bytes2str(t.value),tok])

	if token.hide_on_token.len>0:
		a.hide_on_token_eq=[]
		for i in range(0,token.hide_on_token.len):
			t=ctypes.create_string_buffer(400)
			val=ctypes.create_string_buffer(400)
			dll_lib.token_lib_get_hide_on(ctypes.byref(token),t,val,i)
			tok=bytes2str(val.value)
			if tok.lower()=="false":
				tok=False
			elif tok.lower()=="true":
				tok=True
			a.hide_on_token_eq.append([bytes2str(t.value),tok])
		if token=="mun_z":
			print(a.hide_on_token_eq)

	if token.default_token.len>0:
		a.defaults=[]
		for i in range(0,token.default_token.len):
			t=ctypes.create_string_buffer(400)
			val=ctypes.create_string_buffer(400)
			dll_lib.token_lib_get_default(ctypes.byref(token),t,val,i)
			a.defaults.append([bytes2str(t.value),bytes2str(val.value)])

	if token.pack.len>0:
		a.pack=[]
		for i in range(0,token.pack.len):
			t=ctypes.create_string_buffer(400)
			dll_lib.token_lib_get_pack(ctypes.byref(token),t,i)
			a.pack.append(str(bytes2str(t.value)))
	return a


def build_token_lib():
	global fast_list
	global lib
	dll_lib.token_lib_init(ctypes.byref(fast_lib))
	dll_lib.token_lib_build(ctypes.byref(fast_lib))
	#dll_lib.token_lib_dump(ctypes.byref(fast_lib))

class tokens:

	def __init__(self):
		global lib
		global dll_lib
		dll_lib.token_lib_find.restype = ctypes.c_void_p
		if len(lib)==0:
			build_token_lib()

	def get_fast_lib(self):
		return fast_lib

	def find(self,token):
		global lib
		global dll_lib
		search_token=token.strip()
		ret=dll_lib.token_lib_find(ctypes.byref(fast_lib),ctypes.c_char_p(str2bytes(search_token)))
		if ret!=None:
			tok = token_lib_item.from_address(ret)	
			return ctoken_to_python_token(tok)

		return False

	def find_json(self,token):
		global lib
		global lib_json
		search_token=token.strip()
		if search_token.count(".")!=0:
			search_token=search_token.split(".")[-1]

		dll_find=self.find(token)
		if dll_find!=False:
			return dll_find

		return False

	def reverse_lookup(self,english):
		global lib
		global lib_r
		global dll_lib

		english=english.strip()

		ret=dll_lib.token_lib_rfind(ctypes.byref(fast_lib),ctypes.c_char_p(str2bytes(english)),None)
		if ret!=None:
			tok = token_lib_item.from_address(ret)
			ret=ctoken_to_python_token(tok)
			return ret

		return False

			

