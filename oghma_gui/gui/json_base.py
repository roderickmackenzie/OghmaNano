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

## @package json_base
#  Used to store json_base
#


import os
import json
from str2bool import str2bool
from util import is_number
from util_latex import latex
from util import pygtk_to_latex_subscript
from inp import inp
import codecs
import copy
from bytes2str import bytes2str

def del_keys(dic, del_key):
    dict_foo = dic.copy()
    for field in dict_foo.keys():
        if field == del_key:
            del dic[field]
        if type(dict_foo[field]) == dict:
            del_keys(dic[field], del_key)
    return dic

def isclass(object):
	if "gen_json" in dir(object):
		return True
	return False

class json_base():

	def __init__(self,name,segment_class=False,segment_example=None):
		self.include_name=True
		self.base_name=name
		self.var_list=[]
		self.segment_class=segment_class
		self.segments=[]
		self.loaded=False
		self.latex_allowed=[]
		self.latex_banned=[]
		self.triangles_loaded=False
		self.segments_name=["segments"]
		self.segment_name=["segment"]
		self.f=inp()
		self.segment_examples=[segment_example]
		self.hex=[]

	def import_from_list(self,lines):
		lines="\n".join(lines)
		j_data=json.loads(lines)
		self.load_from_json(j_data)

	def find_enabled_segment(self):
		for sn in self.segments_name:
			for s in getattr(self, sn):
				if s.enabled==True:
					return s

	def import_raw_json(self,json_data):
		self.var_list=[]
		for token, val in json_data.items():
			self.var_list.append([token,val])
		self.var_list_build()

	def import_from_file(self,file_name):
		self.f.load_json(file_name)
		self.import_raw_json(self.f.json)

	def var_list_build(self):
		for l in self.var_list:
			setattr(self, l[0], l[1])
		for s in self.segments_name:
			setattr(self, s, [])
		
	def find_object_by_id(self,want_id):
		if type(want_id)==bytes:
			want_id=bytes2str(want_id)

		for item in self.var_list:
			m=item[0]
			val=getattr(self, m)
			if m=="id":
				if val==want_id:
					return self
			elif isclass(val)==True:
				ret=val.find_object_by_id(want_id)
				if ret!=None:
					return ret

		for sn in self.segments_name:
			for s in getattr(self, sn):
				val=getattr(s, "id","not found")
				if val==want_id:
					return s
				elif isclass(s)==True:
					ret=s.find_object_by_id(want_id)
					if ret!=None:
						return ret
		return None

	def find_object_path_by_id(self,want_id,cur_path=""):
		#print(self.segments_name)
		for item in self.var_list:
			m=item[0]
			val=getattr(self, m)
			if m=="id":
				if val==want_id:
					return self,cur_path
			elif isclass(val)==True:
				ret,new_path=val.find_object_path_by_id(want_id,cur_path=cur_path+"."+m)
				if ret!=None:
					return ret,new_path

		for sn in self.segments_name:
			s_obj=getattr(self, sn)
			#print(sn,s_obj,want_id)
			for s_int in range(0,len(s_obj)):
				val=getattr(s_obj[s_int], "id","not found")
				if val==want_id:
					return s_obj[s_int], cur_path+"."+sn+"["+str(s_int)+"]"
				elif isclass(s_obj[s_int])==True:
					ret,new_path=s_obj[s_int].find_object_path_by_id(want_id,cur_path=cur_path+"."+sn+"["+str(s_int)+"]")
					if ret!=None:
						return ret,new_path
		return None,None

	def pop_object_by_id(self,want_id):
		items=[attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
		for item in items:
			val=getattr(self, item)
			if isclass(val)==True:
				if getattr(val, "pop_object_by_id", None)!=None:
					val.pop_object_by_id(want_id)
			elif type(val)==list:
				for i in range(0,len(val)):
					if isclass(val[i])==True:
						item_id=getattr(val[i], "id", None)
						if item_id==want_id:
							val.pop(i)
							return
						if getattr(val[i], "pop_object_by_id", None)!=None:
							val[i].pop_object_by_id(want_id)

	def fix_identical_uids(self,found):
		for item in self.var_list:
			m=item[0]
			val=getattr(self, m)
			if m=="id":
				if val in found:
					print("warning updated ID",val)
					self.id=self.random_id()
				found.append(val)
			elif isclass(val)==True:
				val.fix_identical_uids(found)

		for sn in self.segments_name:
			for s in getattr(self, sn):
				val=getattr(s, "id",None)
				if val!=None:
					if val in found:
						print("warning updated ID",val)
						s.id=self.random_id()
					found.append(val)
				elif isclass(val)==True:
					val.fix_identical_uids(found)

		#print(found)

	def update_random_ids(self):
		for item in self.var_list:
			m=item[0]
			val=getattr(self, m)
			if m=="id":
				#print(self)
				setattr(self, m, self.random_id()	)
			elif isclass(val)==True:
				try:
					val.update_random_ids()
				except:
					pass

		for sn in self.segments_name:
			for item in getattr(self, sn):
				if isclass(item)==True:
					try:
						val.update_random_ids()
					except:
						pass

	def set_val(self,path,val):
		pointer=self
		path=path.replace("/",".")
		for m in path.split("."):
			last=pointer
			if m.startswith("segment"):
				n=int(m[7:])
				pointer=pointer.segments[n]
			elif m.startswith("layer"):
				n=int(m[5:])
				pointer=pointer.layers[n]
			else:
				pointer=getattr(pointer, m)

		setattr(last, m, val)

	def get_val(self,path):
		pointer=self
		path=path.replace("/",".")
		for m in path.split("."):
			last=pointer
			if m.startswith("segment"):
				n=int(m[7:])
				pointer=pointer.segments[n]
			elif m.startswith("layer"):
				n=int(m[5:])
				pointer=pointer.layers[n]
			else:
				pointer=getattr(pointer, m)

		return pointer

	def gen_json(self,include_bracket=True):
		out=[]

		
		if self.include_name==True:
			name_str="\""+self.base_name+"\":"
		else:
			name_str=""
		if include_bracket==True:
			out.append(name_str +" {")

		for item in self.var_list:
			m=item[0]
			val=getattr(self, m)
			if m.endswith("_")==False:
				if type(val)==str:
					
					val=val.replace("\n","\\n")
					if m in self.hex:
						val=val.encode("utf-8").hex()
					out.append("\t\""+m+"\":\""+val+"\",")
				elif type(val)==int:
					out.append("\t\""+m+"\":"+str(val)+",")
				elif type(val)==float:
					out.append("\t\""+m+"\":"+str(val)+",")
				elif type(val)==bool:
					out.append("\t\""+m+"\":\""+str(val)+"\",")
				elif isclass(val)==True:
					#print(type(val))
					out.extend(val.gen_json())
					out[-1]=out[-1]+","
				else:
					print(m,type(val))

		if self.segment_class==True:
			for sn,item_name in zip(self.segments_name,self.segment_name):
				#print(sn)
				out.append("\""+sn+"\":"+str(len(getattr(self,sn)))+",")
				i=0
				for s in getattr(self,sn):
					s.base_name=item_name+str(i)
					out.extend(s.gen_json())
					out[-1]=out[-1]+","
					i=i+1

		if out[-1].endswith(",")==True:
			out[-1]=out[-1][:-1]
		if include_bracket==True:
			out.append("\t}")

		return out

	def dump_as_latex(self,token_lib=None):
		ret=[]
		class ret_data():
			def __init__(self):
				self.text=""
				self.value=""
				self.units=""
				self.token=item

		for item in self.var_list:
			dump=True
			m=item[0]
			if "all" in self.latex_banned:
				dump=False
				if m in self.latex_allowed:
					dump=True

			if m in self.latex_banned:
				dump=False

			if dump==True:
				value=str(getattr(self, m))
				token_data=token_lib.find_json(m)
				if token_data!=False:

					if is_number(value)==True:
						r=ret_data()
						r.text=token_data.info
						r.value=latex().number_to_latex(value)
						r.units=pygtk_to_latex_subscript(token_data.units)
						r.token=m
						ret.append(r)

		return ret

	def load_from_json(self,data):
		for item in self.var_list:		#add bib items dynamicly
			m=item[0]
			ref_token="ref_"+m
			if ref_token in data:
				if any(e[0] == ref_token for e in data)==False:	#is ref_token in the list already
					from bibtex import json_bib
					bib_item=json_bib(ref_token)
					self.var_list.append([ref_token,bib_item])
				setattr(self, ref_token, bib_item)


		for item in self.var_list:
			m=item[0]
			val=item[1]
			#print(data)
			#print(data[m],type(getattr(self,m)),type(val))
			decoded=False
			if m=="time_domain":
				if 'pulse' in data:
					self.sims.time_domain.load_from_json(data['pulse'])
					decoded=True
			elif m=="fx_domain":
				if "is" in data:
					self.sims.fx_domain.load_from_json(data['is'])
					decoded=True
			elif m=="world":
				if "jv" in data:
					self.sims.jv.load_from_json(data['jv'])
				if "suns_voc" in data:
					self.sims.suns_voc.load_from_json(data['suns_voc'])
				if "suns_jsc" in data:
					self.sims.suns_jsc.load_from_json(data['suns_jsc'])
				if "ce" in data:
					self.sims.ce.load_from_json(data['ce'])

				if "pl_ss" in data:
					self.sims.pl_ss.load_from_json(data['pl_ss'])
				if "eqe" in data:
					self.sims.eqe.load_from_json(data['eqe'])
				if "fdtd" in data:
					self.sims.fdtd.load_from_json(data['fdtd'])
				if "time_domain" in data:
					self.sims.time_domain.load_from_json(data['time_domain'])
				if "fx_domain" in data:
					self.sims.fx_domain.load_from_json(data['fx_domain'])
				if "cv" in data:
					self.sims.cv.load_from_json(data['cv'])
				if "spm" in data:
					self.sims.spm.load_from_json(data['spm'])
				if "transfer_matrix" in data:
					self.sims.transfer_matrix.load_from_json(data['transfer_matrix'])
				if "ray" in data:
					self.sims.ray.load_from_json(data['ray'])
				if "light" in data:
					self.optical.light.load_from_json(data['light'])
				if "light_sources" in data:
					self.optical.light_sources.load_from_json(data['light_sources'])
				if "detectors" in data:
					self.optical.detectors.load_from_json(data['detectors'])
				if "spctral2" in data:
					self.optical.spctral2.load_from_json(data['spctral2'])
				if "lasers" in data:
					self.optical.lasers.load_from_json(data['lasers'])
				if "thermal_boundary" in data:
					self.thermal.thermal_boundary.load_from_json(data['thermal_boundary'])
				if "exciton_boundary" in data:
					self.exciton.exciton_boundary.load_from_json(data['exciton_boundary'])
				if "mesh" in data:
					self.electrical_solver.mesh.load_from_json(data['mesh'])

			if decoded==False:
				if m.startswith("ref_")==False:
					if m in data:
						if type(val)==float:
							try:
								clean_val=float(data[m])
							except:
								clean_val=0.0
							setattr(self, m, clean_val)
						elif type(val)==int:
							try:
								clean_val=int(data[m])
							except:
								clean_val=0
							setattr(self, m, clean_val)
						elif type(val)==bool:
							setattr(self, m, str2bool(data[m]))
						elif type(val)==type(data[m]):
							if m in self.hex:
								data[m]=bytes.fromhex(data[m]).decode('utf-8')
							setattr(self, m, data[m])
						elif type(val)==str:
							setattr(self, m, str(data[m]))
						elif isclass(getattr(self,m))==True:
							getattr(self,m).load_from_json(data[m])


		if self.segment_class==True:
			for sn,item_name,segment_example in zip(self.segments_name,self.segment_name,self.segment_examples):
				setattr(self,sn,[])
				if sn in data:
					segs=data[sn]
					for i in range(0,segs):
						a=copy.deepcopy(segment_example)
						simulation_name=item_name+str(i)
						if simulation_name in data:
							a.load_from_json(data[simulation_name])
							getattr(self,sn).append(a)

		try:
			self.name=data['shape_name']
		except:
			pass

		try:
			self.name=data['english_name']
		except:
			pass

		try:
			self.enabled=str2bool(data['shape_enabled'])
		except:
			pass

	def reload(self):
		if self.f.load_json(self.file_name)!=False:
			self.load_from_json(self.f.json)
			self.last_time=self.f.time()
			self.loaded=True
			self.triangles_loaded=False

	def load(self,file_name):
		self.f.set_file_name(file_name)
		self.file_name=file_name
		self.reload()
		if self.loaded==False:
			return False
		return True

	def random_id(self):
		return "id"+codecs.encode(os.urandom(int(16 / 2)), 'hex').decode()

	def save_as(self,file_name,do_tab=True):
		self.file_name=file_name
		lines=self.gen_json()
		self.f.lines=lines
		if do_tab==True:
			self.f.tab()
		else:
			for i in range(0,len(self.f.lines)):
				self.f.lines[i]=self.f.lines[i].replace("\t","")
		self.f.save_as(file_name)
		self.last_time=self.f.time()

	def save(self,do_tab=True):
		if self.loaded==True:
			lines=self.gen_json()
			self.f.lines=lines
			if do_tab==True:
				self.f.tab()
			else:
				for i in range(0,len(self.f.lines)):
					self.f.lines[i]=self.f.lines[i].replace("\t","")
			self.f.save()
			self.last_time=self.f.time()

	def load_triagles(self):
		for l in self.epi.layers:
			l.load_triangles()
			for s in l.segments:
				s.load_triangles()
				if s.triangles==None:
					s.shape_enabled=False

		for c in self.epi.contacts.segments:
			c.load_triangles()

		for source in self.optical.light_sources.lights.segments:
			source.load_triangles()

		for obj in self.world.world_data.segments:
			obj.load_triangles()
			if obj.triangles==None:
				obj.shape_enabled=False

		self.triangles_loaded=True
