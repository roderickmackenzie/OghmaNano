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

## @package dat_file
#  Load and dump a dat file into a dat class
#

import re

class dat_file_decode():

	def col_name_to_pos(self,lines,col,known_col_sep):
		if known_col_sep==None:
			return col

		if type(col)==float:
			return col

		for i in range(0, len(lines)):
			s,label=self.decode_line(lines[i],known_col_sep=known_col_sep)
			if col in s:
				return s.index(col)

		return False

	def decode_line(self,line,known_col_sep=None):
		label=False
		line=re.sub(' +',' ',line)

		if known_col_sep!=None:
			s=line.split(known_col_sep)
			return s,False

		line=re.sub('\t',' ',line)

		#check for labels at the end of the line
		if len(line)>0:
			if line[0]!="#":
				if line.count("#")>0:
					label=line.split("#")[1]
					line=line.split("#")[0]

		line=line.replace(', ', ' ')	#remove comman in csv files
		line=line.replace(',', '.')		#Remove European commas
		s=line.split()
			
		return s,label


