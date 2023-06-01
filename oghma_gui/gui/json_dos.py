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

## @package json_dos
#  Store the cv domain json data
#

from json_base import json_base


class shape_homo_lumo_item(json_base):
	def __init__(self):
		json_base.__init__(self,"shape_homo_lumo_item")
		self.var_list=[]
		self.var_list.append(["function","exp"])
		self.var_list.append(["function_enable",True])
		self.var_list.append(["function_a",4e+20])
		self.var_list.append(["function_b",1e-3])
		self.var_list.append(["function_c",0.0])
		self.var_list_build()

class shape_homo_lumo(json_base):
	def __init__(self,name):
		self.var_list=[]
		json_base.__init__(self,name,segment_class=True,segment_example=shape_homo_lumo_item())
		self.var_list.append(["icon_","electrical"])
		self.var_list.append(["id",self.random_id()])
		self.var_list_build()


	def load_from_json(self,json):				#delete 25th Nov 2024
		self.segments=[]
		nsegments=json['segments']
		for i in range(0,nsegments):
			a=shape_homo_lumo_item()
			if "function"+str(i) in json:
				function_name="function"+str(i)
			else:
				function_name="segment"+str(i)
			a.load_from_json(json[function_name])
			self.segments.append(a)
		try:
			self.id=json['id']
		except:
			pass

class json_dos_config(json_base):
	def __init__(self):
		json_base.__init__(self,"config")
		self.var_list=[]
		self.var_list.append(["mu_tdep_enable",False])
		self.var_list_build()

class json_dos(json_base):

	def gen_var_list(self,material_db=False):
		var_list=[]
		var_list.append(["enabled",False])
		var_list.append(["icon_","electrical"])
		#free carrier
		var_list.append(["text_free_carrier_",""])
		var_list.append(["dd_enabled",True])
		var_list.append(["symmetric_mobility_e","symmetric"])
		var_list.append(["mue_z",1e-15])
		var_list.append(["mue_x",1e-15])
		var_list.append(["mue_y",1.0e-05])
		var_list.append(["mue_delta",0.1])
		var_list.append(["symmetric_mobility_h","symmetric"])
		var_list.append(["muh_z",1e-15])
		var_list.append(["muh_x",1e-15])
		var_list.append(["muh_y",1.0e-05])
		var_list.append(["muh_delta",0.1])
		var_list.append(["Nc",5e25])
		var_list.append(["Nv",5e25])
		if material_db==False:
			var_list.append(["free_to_free_recombination",0.000000e+00])
			var_list.append(["dos_free_carrier_stats","mb_equation"])

		#Non-dynamic srh
		var_list.append(["text_steay_srh_",""])
		var_list.append(["ss_srh_enabled",False])
		var_list.append(["srh_n1",1e20])
		var_list.append(["srh_p1",1e20])
		var_list.append(["srh_tau_n",1e-15])
		var_list.append(["srh_tau_p",1e-15])

		#Dynamic traps
		var_list.append(["text_dynamic_traps_",""])
		if material_db==False:
			var_list.append(["dostype","exponential"])
			var_list.append(["complex_lumo",shape_homo_lumo("complex_lumo")])
			var_list.append(["complex_homo",shape_homo_lumo("complex_homo")])
			var_list.append(["Ntrape",1e20])
			var_list.append(["Ntraph",1e20])
			var_list.append(["Etrape",60e-3])
			var_list.append(["Etraph",60e-3])
			var_list.append(["ion_density",0.0])
			var_list.append(["ion_mobility",0.0])

		if material_db==False:
			var_list.append(["doping_start",0.0])
			var_list.append(["doping_stop",0.0])
			var_list.append(["Na0",0.0])
			var_list.append(["Na1",0.0])
			var_list.append(["Nd0",0.0])
			var_list.append(["Nd1",0.0])
			var_list.append(["nstart",-2.5])
			var_list.append(["nstop",1.0])
			var_list.append(["npoints",1000])
			var_list.append(["pstart",-2.5])
			var_list.append(["pstop",1.0])
			var_list.append(["ppoints",1000])

			var_list.append(["srh_start",-0.5])
			var_list.append(["srhsigman_e",2.131895e-21])
			var_list.append(["srhsigmap_e",3.142822e-22])
			var_list.append(["srhvth_e",1e5])
			var_list.append(["srhsigman_h",3.142822e-22])
			var_list.append(["srhsigmap_h",2.131895e-21])
			var_list.append(["srhvth_h",1e5])
			var_list.append(["srh_bands",5])

			var_list.append(["Esteps",1000])
			var_list.append(["dump_band_structure",0])


			#Auger
			var_list.append(["text_auger_",""])
			var_list.append(["dos_enable_auger",False])
			var_list.append(["dos_auger_Cn",1e-26])
			var_list.append(["dos_auger_Cp",1e-26])

		var_list.append(["text_electro_",""])
		var_list.append(["Xi",1.6])
		var_list.append(["Eg","1.2"])
		var_list.append(["epsilonr",5.0])
		if material_db==False:
			var_list.append(["id",self.random_id()])

		#Exciton solver
		var_list.append(["text_exciton_",""])
		var_list.append(["exciton_enabled",False])
		var_list.append(["exciton_L",1e-08])
		var_list.append(["exciton_tau",1e-10])
		var_list.append(["exciton_kpl",4e9])
		var_list.append(["exciton_kfret",0.0])
		var_list.append(["exciton_alpha",1E-13])
		var_list.append(["exciton_kdis",1e11])

		#singlet solver
		var_list.append(["text_singlet_",""])
		var_list.append(["singlet_enabled",False])
		var_list.append(["singlet_k_fret",1e10])
		var_list.append(["singlet_k_s",8e7])
		var_list.append(["singlet_k_isc",2.2e4])
		var_list.append(["singlet_k_ss",3.5e-18])
		var_list.append(["singlet_k_sp",3.0e-10])
		var_list.append(["singlet_k_st",1.9e-16])
		var_list.append(["singlet_k_dext",1e10])
		var_list.append(["singlet_k_t",6.5e2])
		var_list.append(["singlet_k_tp",2.8e-19])
		var_list.append(["singlet_k_tt",2.2e-18])
		var_list.append(["singlet_k_sd",1e9])
		var_list.append(["singlet_k_iscd",2.2e4])
		var_list.append(["singlet_k_spd",3.0e-16])
		var_list.append(["singlet_k_std",1.9e-16])
		var_list.append(["singlet_k_ssd",9.6e-19])
		var_list.append(["singlet_k_td",6.6e2])
		var_list.append(["singlet_k_ttd",2.4e-21])
		var_list.append(["singlet_k_tpd",5.6e-19])
		#var_list.append(["singlet_zeta",1.4e-11])		#remove as now calculated from singlet_zeta
		var_list.append(["singlet_k_cav",1e12])
		var_list.append(["singlet_beta_sp",1e-4])
		var_list.append(["singlet_C",0.02])
		var_list.append(["singlet_N_dop",4.2e25])
		var_list.append(["singlet_W",2.6e-2])
		#singlet solver+
		var_list.append(["singlet_k_risc",1e5])
		var_list.append(["singlet_sigma_em",5e-20])
		var_list.append(["singlet_sigma_t1tn",1e-20])
		var_list.append(["singlet_sigma_np",2e-20])
		var_list.append(["singlet_a",1e-9])
		var_list.append(["config",json_dos_config()])
		return var_list

	def __init__(self):
		json_base.__init__(self,"shape_dos")
		self.var_list=self.gen_var_list()

		self.var_list_build()


