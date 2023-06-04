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

## @package html_latex
#  html helper routines
#

import os

class lib_html:
	def __init__(self):
		self.lines=[]

	def tab_start(self,labels):
		self.lines.append("<table>\n")
		self.lines.append("<tr>\n")
		for l in labels:
			self.lines.append(" <th>"+l+"</th>\n")
		self.lines.append("</tr>\n")

	def tab_add_row(self,values):
		self.lines.append("<tr>\n")
		for v in values:
			self.lines.append("<td>"+v+"</td>\n")
		self.lines.append("</tr>\n")

	def document_start(self):
		self.lines.append("<html>\n")
		self.lines.append("<head>\n")
		self.lines.append("<style>\n")
		self.lines.append("table {\n")
		self.lines.append("  font-family: arial, sans-serif;\n")
		self.lines.append("  border-collapse: collapse;\n")
		self.lines.append("  width: 100%;\n")
		self.lines.append("}\n")
		self.lines.append("\n")
		self.lines.append("td, th {\n")
		self.lines.append("  border: 1px solid #dddddd;\n")
		self.lines.append("  text-align: left;\n")
		self.lines.append("  padding: 8px;\n")
		self.lines.append("}\n")
		self.lines.append("\n")
		self.lines.append("tr:nth-child(even) {\n")
		self.lines.append("  background-color: #dddddd;\n")
		self.lines.append("}\n")
		self.lines.append("</style>\n")
		self.lines.append("</head>\n")
		self.lines.append("<body>\n")


	def document_end(self):
		self.lines.append("</body>\n")
		self.lines.append("</html>\n")

	def tab_end(self):
  		self.lines.append("</table>\n")

	def save(self,file_name):
		self.file_name=file_name
		dir_name=os.path.dirname(file_name)
		if os.path.isdir(dir_name)==False:
			os.mkdir(dir_name)

		out_file=open(file_name,"w")
		out_file.write("\n".join(self.lines))
		out_file.close()


	def number_to_html(self,data):
		if type(data)==str:
			data=float(data)

		if data>0.01 and data<1000.0:
			return "{:.3f}".format(data)

		ret="%1.1e" % data
		if (ret.count('e')!=0):
			a,b=ret.split('e')
			b=b.replace("+","")
			ret=a+"x10<sup>"+b+"</sup>"

		return ret




