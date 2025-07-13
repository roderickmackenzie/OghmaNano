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

## @package global_objects
#  Allows functions to be called accross calsses.
#


global_objects=[]
blocked=False
class objects:
	name=""
	object_pointer=None

def global_object_register(name,pointer):
	global global_objects
	found=False
	for i in range(0,len(global_objects)):
		if global_objects[i].name==name:
			global_objects[i].object_pointer=pointer
			found=True

	if found==False:
		a=objects()
		a.name=name
		a.object_pointer=pointer
		global_objects.append(a)
		

def global_object_get(name):
	global global_objects
	for i in range(0,len(global_objects)):
		if global_objects[i].name==name:
			return global_objects[i].object_pointer

	print("name",name,"not found")
	#sys.exit()

def global_object_run(name):
	global blocked
	if blocked==True:
		return
	global global_objects
	for i in range(0,len(global_objects)):
		if global_objects[i].name==name:
			blocked=True
			try:
				global_objects[i].object_pointer()
			except:
				pass
			blocked=False
			return

	
def global_isobject(name):
	global global_objects
	for i in range(0,len(global_objects)):
		if global_objects[i].name==name:
			return True

	return False

def global_object_delete(name):
	global global_objects
	for i in range(0,len(global_objects)):
		if global_objects[i].name==name:
			del global_objects[i]
			return
