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

## @package plot
#  These are mainly used by the scan widget.
#  This needs rewriting
#

from token_lib import tokens
from util_zip import zip_get_data_file

def check_info_file(search_string):
	files=["sim_info.dat"]
	if files.count(search_string)> 0:
		return True
	else:
		return False


def plot_populate_plot_token(data_file,file_name):
	if file_name!=None:
		ret=data_file.load_only_info(file_name)

		if ret==True:
			return True

	#check to see if I have been provided with a token

	if data_file!=None:
		my_token_lib=tokens()
		result0=my_token_lib.find(data_file.tag0)
		result1=my_token_lib.find(data_file.tag1)
		print("one=",data_file.tag0,result0)
		print("two=",data_file.tag1,result1)
		if result0!=False:
			data_file.x_label=result0.info
			data_file.x_units=result0.units
			data_file.x_mul=result0.number_mul

			data_file.data_label=result1.info
			data_file.data_units=result1.units
			data_file.data_mul=result1.number_mul

			data_file.title=result0.info+" "+result1.info

			print("Found tokens",data_file.tag0,data_file.tag1)
			return True
		else:
			print("Tokens not found",data_file.tag0,data_file.tag1)

	return False


