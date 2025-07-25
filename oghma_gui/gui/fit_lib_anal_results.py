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

## @package fit_lib_anal_results
#  This is the backend to handle fitting
#


import os

import i18n
_ = i18n.language.gettext
from inp import inp
from token_lib import tokens
from math import pow
from math import fabs
from util_latex import latex
from token_lib import tokens
import json
import operator
from lib_html import lib_html

class fit_lib_anal_results:
	def get_fit_quality(self,path):
		f=inp()
		if f.load(os.path.join(path,"fitlog.csv"))==False:
			return -1.0
		last=f.lines[-2].split()

		if len(last)!=2:
			return -1.0

		return float(last[1])

	def anal_get_fit_values(self,simulation_paths,aditional_vars=["parasitic/Shunt resistance"]):

		class sort_result():
			def __init__(self):
				self.vars={}
				self.quality=0.0
		#self.find_sims(search_path)

		vars_from_file={}
		results=[]
		data=all_json_root()
		data.load(os.path.join(simulation_paths[0],"sim.json"))
		for v in data.fits.vars.segments:
			if v.fit_var_enabled==True:
				vars_from_file[v.json_var]=[]

		for p in aditional_vars:
			vars_from_file[p]=[]

		for s in simulation_paths:
			f=inp()
			if f.load(os.path.join(s,"sim.json"))!=False:

				json_data="\n".join(f.lines)
				decode=json.loads(json_data)

				a=sort_result()
				for json_path in list(vars_from_file.keys()):
					val=get_json_obj_from_human_path(decode,json_path)

					a.vars[json_path]=fabs(float(val))
				a.quality=self.get_fit_quality(s)
				a.file=s
				results.append(a)
		results = sorted(results, key=operator.attrgetter('quality'))

		return results

	def cal_avg_and_std(self,results):
		ret={}

		for name,val in results[0].vars.items():
			ret[name]={'avg':0.0,'std':0.0}

		for r in results:
			for name,val in r.vars.items():
				ret[name]['avg']=ret[name]['avg']+val

		for name,val in results[0].vars.items():
			ret[name]['avg']=ret[name]['avg']/len(results)

		for r in results:
			for name,val in r.vars.items():
				#print(name,val)
				ret[name]['std']=ret[name]['std']+pow(val-ret[name]['avg'],2.0)

		for name,val in results[0].vars.items():
			ret[name]['std']=pow(ret[name]['std']/len(results),0.5)

		for name,val in results[0].vars.items():
			print(name,ret[name]['avg'])

		#for r in results:
			
		#	a=""
		#	for v in list(r.vars.keys()):
		#		a=a+" "+str(r.vars[v])
		#	print(a,r.quality)

		return ret

	def transpose_values(self,results):
		data=[]
		ret={}

		for r in results:
			ret={}
			print("1")
			for name,val in r.vars.items():
				ret[name]={'avg':0.0,'std':0.0}
				ret[name]['avg']=val
				#if name=="parasitic/Shunt resistance":
				#	print(name,val)
				
			data.append(ret)

		return data

	def make_latex_table(self,data_sets,avg=True,json_path=os.getcwd(),col_titles=None):
		lx=latex()
		lx.document_start()
		title=[]
		title.append("Parameter")
		n=0
		for a in data_sets:
			if avg==True:
				if col_titles==None:
					title.append("Value")
				else:
					title.append(col_titles[n])
			else:
				title.append("$\sigma,N$")
			n=n+1

		title.append("Units")
		lx.tab_start(title)

		token_lib=tokens()
		
		f=inp()
		f.load(os.path.join(json_path,"sim.json"))
		json_data="\n".join(f.lines)
		decode=json.loads(json_data)

		for name,val in data_sets[0].items():
			json_name=get_json_path_from_human_path(decode,name)
			#print(json_name)
			token=token_lib.find_json(os.path.basename(json_name))
			line=[]
			line.append(token.info)
			for data_set in data_sets:
				if name in data_set:
					if avg==True:
						line.append("$"+lx.number_to_latex(data_set[name]['avg'])+"$")
					else:
						line.append("$"+lx.number_to_latex(data_set[name]['std'])+","+str(len(data_sets[0].items()))+"$")
				else:
					line.append("")

			line.append("$"+token.units+"$")
			lx.tab_add_row(line)

		lx.tab_end()
		lx.latex_document_end()
		return lx

	def make_html_table(self,data_sets,save_file="out.html"):
		lx=lib_html()
		lx.document_start()
		title=[]
		title.append("Parameter")
		for a in data_sets:
			title.append("Value")

		title.append("Units")
		lx.tab_start(title)

		token_lib=tokens()
		
		f=inp()
		f.load(os.path.join(os.getcwd(),"sim.json"))
		json_data="\n".join(f.lines)
		decode=json.loads(json_data)

		for name,val in data_sets[0].items():
			json_name=get_json_path_from_human_path(decode,name)
			#print(json_name)
			token=token_lib.find_json(os.path.basename(json_name))
			line=[]
			line.append(token.info)
			for data_set in data_sets:
				if name in data_set:
					line.append(lx.number_to_html(data_set[name]['avg']))
				else:
					line.append("")

			line.append("$"+token.units+"$")
			lx.tab_add_row(line)

		lx.tab_end()
		lx.document_end()
		lx.save(os.path.join(os.getcwd(),"anal",save_file))

