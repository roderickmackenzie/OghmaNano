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

## @package scan_ml
#  ML framework.
#

import os

from safe_delete import safe_delete

from math import log10

import i18n
_ = i18n.language.gettext

from progress_class import progress_class
from process_events import process_events
from server import server_break
from util_zip import zip_lsdir
from util_zip import extract_dir_from_archive

import zipfile
import random
import string
import numpy as np
from gui_util import yes_no_dlg
from scan_io import scan_io
from yes_no_cancel_dlg import yes_no_cancel_dlg
from json_root import json_root
from json_root import all_json_root
from inp import inp
from scan_human_labels import get_json_path_from_human_path
from scan_human_labels import json_get_val

from json_base import json_base
from json_diff import json_diff
import json
from dat_file import dat_file
from cal_path import sim_paths

def make_vector_from_file(file_name,x_values):
	if os.path.isfile(file_name)==True:
		f=open(file_name,'r')
		lines = f.readlines()
		f.close()
	else:
		return False

	x=[]
	y=[]
	for i in range(0,len(lines)):
		if lines[i].startswith("#")==False:

			if lines[i].count("nan")!=0:
				return False

			if lines[i].count("inf")!=0:
				return False

			r=lines[i].split()
			if len(r)==2:
				try:
					x.append(float(r[0]))
					y.append(float(r[1]))
				except:
					return False
	

	x, y = zip(*sorted(zip(x, y)))

	if x_values==None:
		return y

	r=np.interp(x_values,x,y)
	return r

def get_vectors(file_name,x_values):

	data=make_vector_from_file(file_name,x_values)

	if type(data)==bool:
		if data==False:
			return False


	n=[]
	for i in range(0,len(data)):
		#print(data[i])
		r=float(data[i])

		n.append(r)
	#print(n)

	s=""
	for ii in range(0,len(n)):
		s=s+'{:e}'.format(float(n[ii]))+" "

	return s



class ml_vectors:

	def __init__(self):
		pass
			
	def json_get_ml_tokens(self,archive_path,sub_sim):
		zf = zipfile.ZipFile(archive_path, 'r')
		items=zf.namelist()
		sims=[]
		for file_name in items:
			if file_name.endswith("sim.json"):
				if os.path.basename(os.path.dirname(file_name))==sub_sim:
					sims.append(file_name)

		read_lines0 = zf.read(sims[0])
		read_lines1 = zf.read(sims[1])
		json_data0=json.loads(read_lines0)
		json_data1=json.loads(read_lines1)
		print(sims[0])
		print(sims[1])

		zf.close()
		return json_diff(json_data0,json_data1)


	def make_tmp_dir(self):
		rnd = [random.choice(string.ascii_letters + string.digits) for n in range(0,32)]
		rnd = "".join(rnd)
		tmp_dir="/dev/shm/oghma_"+rnd
		if os.path.isdir(tmp_dir)==True:
			safe_delete(tmp_dir,allow_dir_removal=True)

		os.mkdir(tmp_dir)

		return tmp_dir

	def build_vector(self,scan_dir,data):
		output_file=os.path.join(scan_dir,data.ml_config.ml_vector_file_name)

		error_file=open(os.path.join(scan_dir,"errors.dat"),'w')
		error_file.write("")
		error_file.close()

		out_json=open(output_file,'wb')
		out_json.write(str.encode("{\n"))
		out_json.write(str.encode("\"item_type\":\"ml_vectors\",\n"))

		progress_window=progress_class()
		progress_window.show()
		progress_window.start()


		archives=[]
		for archive_name in os.listdir(scan_dir):
			if archive_name.startswith("archive")==True and archive_name.endswith(".zip")==True:
				archives.append(archive_name)

		sub_sims=[]
		for item in data.ml_sims.segments:
			if item.ml_sim_enabled==True:
				sub_sims.append(item.sim_name)

		self.ml_tokens=[]
		for item in data.ml_random.segments:
			self.ml_tokens.append(item.json_var.replace("/","."))

		done=0

		errors=0


		for archive_name in archives:

			if archive_name.startswith("archive")==True and archive_name.endswith(".zip")==True:

				archive_path=os.path.join(scan_dir,archive_name)


				zf = zipfile.ZipFile(archive_path, 'r')
				simulations=zip_lsdir(archive_path,zf=zf,sub_dir="/")

				for simulation in simulations:

					tmp_dir="oghma_"+simulation

					extract_dir_from_archive(tmp_dir,"",simulation,zf=zf)
					
					written=False

					error=False

					base=json_base(simulation)
				
					base.val_list=[]
					base.var_list.append(["params",json_base("params")])
					for sub_sim in sub_sims:
						base.var_list.append([sub_sim,json_base(sub_sim)])
					base.var_list_build()


					sub_sim_folder=None

					for sub_sim in sub_sims:
						sub_sim_folder=os.path.join(tmp_dir,sub_sim)

						d=all_json_root()
						#print(os.path.join(sub_sim_folder,"sim.json"))
						if d.load(os.path.join(sub_sim_folder,"sim.json"))==False:
							error=True
							break

						sim_mode=d.sim.simmode.lower().split("@")[1]

						light=d.optical.light.Psun

						
						for c in data.ml_sims.segments[sub_sims.index(sub_sim)].ml_output_vectors.segments:
							if c.ml_output_vector_item_enabled==True:
								vector_path=os.path.join(tmp_dir,sub_sim,c.file_name)
								ret=get_vectors(vector_path,[float(i) for i in c.vectors.split(",")])
								if ret==False:
									error=True
									error_file=open(os.path.join(scan_dir,"errors.dat"),'a')
									error_file.write(archive_path+"\\"+simulation+","+sub_sim+"\n")
									error_file.close()
									break
								getattr(base,sub_sim).var_list.append([c.ml_token_name,ret])

						if sim_mode=="jv" and light>0.0:
							f=inp()
							json_data=f.load_json(os.path.join(tmp_dir,sub_sim,"sim_info.dat"))
							tokens=["pce","ff", "voc", "voc_R", "jsc", "theta_srh_free", "theta_srh_free_trap"]
							tokens.append("mu_jsc")
							tokens.append("mu_pmax")
							tokens.append("mu_voc")
							tokens.append("mu_geom_jsc")
							tokens.append("mu_geom_pmax")
							tokens.append("mu_geom_voc")
							tokens.append("mu_geom_micro_jsc")
							tokens.append("mu_geom_micro_pmax")
							tokens.append("mu_geom_micro_voc")
							tokens.append("mue_jsc")
							tokens.append("muh_jsc")
							tokens.append("mue_pmax")
							tokens.append("muh_pmax")
							tokens.append("tau_voc")
							tokens.append("tau_pmax")
							tokens.append("tau_all_voc")
							tokens.append("tau_all_pmax")

							tokens.append("theta_srh_free")
							tokens.append("theta_srh_free_trap")
							tokens.append("theta_jsc")
							tokens.append("theta_voc")
							tokens.append("theta_pmax")

							for t in tokens:
								val=json_get_val(json_data,t)
								if val==None:
									error=True
									break
								getattr(base,sub_sim).var_list.append([t,val])

					f=inp()
					json_file_name=os.path.join(tmp_dir,sub_sims[0],"sim.json")
					json_data=f.load_json(json_file_name)

					base.params.var_list=[]
					for token_path in self.ml_tokens:
						temp=str(json_get_val(json_data,token_path))
						base.params.var_list.append([token_path,temp])
						#print(simulation,token_path,temp,json_file_name)

					#print(v,error)
					if error==False:
						base.params.var_list_build()
						for sub_sim in sub_sims:
							getattr(base,sub_sim).var_list_build()
						base.var_list_build()
						out_json.write(str.encode("\n".join(base.gen_json())+",\n"))
						written=True
					else:
						errors=errors+1

					done=done+1

					progress_window.set_fraction(float(done)/float(len(simulations)*len(archives)))
					if written==True:
						progress_window.set_text(simulation)
					else:
						progress_window.set_text("                         /Last error: "+simulation+" tot errors="+str(errors)+" "+str(round(100.0*errors/done,1))+"%")

					progress_window.set_text(simulation)

					process_events()
					#return

					safe_delete(tmp_dir,allow_dir_removal=True)

		out_json.seek(-2, os.SEEK_END)
		out_json.write(str.encode("\n}"))
		out_json.close()
		progress_window.stop()
		os.chdir(sim_paths.get_sim_path())


