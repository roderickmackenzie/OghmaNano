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

import re

import i18n
_ = i18n.language.gettext
import time

class my_data():
	token=""
	units=""
	info=""
	def __init__(self,b,info,widget,defaults=None,units_widget="QLabel",min=None,max=None,hidden=False,hide_on_token_eq=None,show_on_token_eq=None,pack=[]):
		self.units=b
		self.info=info
		self.defaults=defaults
		self.widget=widget
		self.units_widget=units_widget
		self.hidden=hidden
		self.hide_on_token_eq=hide_on_token_eq
		self.show_on_token_eq=show_on_token_eq
		self.min=min
		self.max=max
		self.pack=pack


lib={}
lib_r={}
lib_json={}

def build_token_lib():
	global lib
	#light.inp
	lib['lstop']=my_data("m",_("Lambda stop"),"QLineEdit")

	lib['light_file_generation']=my_data("file_name",_("File containing generation rate"),"g_select")

	lib['Dphotoneff']=my_data("0-1",_("Photon efficiency"),"QLineEdit",min=0.001,max=1.2)
	lib['light_file_qe_spectra']=my_data("au",_("QE spectra file"),"QLineEdit")

	lib['light_spectrum']=my_data("au",_("Light spectrum"),"tb_spectrum")
	lib['light_multiplyer']=my_data("au",_("Light multiplyer"),"QLineEdit")

	#sim_info.dat from light
	lib['J_photo']=my_data("Am^{-2}",_("Photo current density"),"QLineEdit")
	lib['I_photo']=my_data("A",_("Photo current"),"QLineEdit")

	#filter
	lib['filter_enabled']=my_data("au",_("Invert"),"gtkswitch")
	lib['filter_material']=my_data("...",_("Optical filter material"),"g_select_filter" ,units_widget="QPushButton")
	lib['filter_db']=my_data("0-1000dB",_("dB"),"QLineEdit")
	lib['filter_local_ground_view_factor']=my_data(_("Degrees"),"Local ground view factor","QLineEdit")
	lib['filter_invert']=my_data("au",_("Invert"),"gtkswitch")

	#light sources
	lib['light_external_n']=my_data("Refractive index",_("n"),"QLineEdit")
	lib['light_illuminate_from']=my_data("au",_("Illuminate from"),"QComboBoxLang",defaults=[[("y0"),_("Top (y0)")],[("y1"),_("Bottom (y1)")],[("x0"),_("Left (x0)")],[("x1"),_("Right (x1)")],[("z0"),_("Front (z0)")],[("z1"),_("Back (z1)")],[("xyz"),_("xyz")]])

	#generic
	lib['log_fit']=my_data(_("True/False"),_("Log fit"),"gtkswitch")
	lib['human_var']=my_data(_("Select"),_("Select"),"g_select")
	lib['human_path']=my_data(_("Select"),_("Select"),"g_select")
	lib['fit_var_enabled']=my_data(_("True/False"),_("Enable fit variable"),"gtkswitch")
	lib['duplicate_var_enabled']=my_data(_("True/False"),_("Enable fit variable"),"gtkswitch")
	lib['opp']=my_data("au",_("Opperation"),"QComboBox",defaults=[])

	#ml
	lib['ml_sim_enabled']=my_data(_("True/False"),_("Enable fit variable"),"gtkswitch")
	lib['ml_patch_enabled']=my_data(_("True/False"),_("Enable fit variable"),"gtkswitch")
	lib['random_var_enabled']=my_data(_("True/False"),_("Enable fit variable"),"gtkswitch")
	lib['ml_output_vector_item_enabled']=my_data(_("True/False"),_("Enable vector"),"gtkswitch")
	lib['ml_edit_sim']=my_data("file_name",_("Edit patch"),"tab_button")
	lib['ml_edit_vectors']=my_data("file_name",_("Edit vectors"),"tab_button")
	lib['ml_number_of_archives']=my_data("au",_("Number of archives"),"QLineEdit")
	lib['ml_sims_per_archive']=my_data("au",_("Simulations per archive"),"QLineEdit")
	lib['random_distribution']=my_data("type",_("Random distribution"),"QComboBoxLang",defaults=[[("log"),_("Log")],["linear",_("Linear")]])
	lib['ml_archive_path']=my_data("au",_("Archive path"),"QLineEdit")
	lib['ml_vector_file_name']=my_data("au",_("Vector file name"),"QLineEdit")

	#fit duplicate
	#lib['enabled']=my_data(_("True/False"),_("Enabled"),"gtkswitch")
	lib['human_src']=my_data(_("Select"),_("Select"),"g_select")
	lib['human_dest']=my_data(_("Select"),_("Select"),"g_select")
	lib['multiplier']=my_data(_("multiplier"),_("Multiplier"),"QLineEdit")
	lib['json_src']=my_data(_("json_src"),_("json_src"),"QLineEdit")
	lib['json_dest']=my_data(_("json_dest"),_("json_dest"),"QLineEdit")

	#fit rules
	lib['human_x']=my_data(_("Select"),_("Select"),"g_select")
	lib['human_y']=my_data(_("Select"),_("Select"),"g_select")
	lib['fit_rule_enabled']=my_data(_("Select"),_("Select"),"gtkswitch")
	#laser?.inp
	lib['laserwavelength']=my_data("m",_("Laser wavelength"),"QLineEdit")
	lib['laser_pulse_width']=my_data("s",_("Length of pulse"),"QLineEdit")
	lib['spotx']=my_data("m",_("Spot size x"),"QLineEdit")
	lib['spoty']=my_data("m",_("Spot size y"),"QLineEdit")
	lib['pulseJ']=my_data("J",_("Energy in pulse"),"QLineEdit")
	lib['laser_photon_efficiency']=my_data("0-1",_("Efficiency of photons"),"QLineEdit")

	#layer widget
	lib['solve_optical_problem']=my_data("type",_("Solve optical problem"),"QComboBoxLang",defaults=[[("yes_nk"),_("Yes - n/k")],[("yes_k"),_("Yes - k")],["false",_("No")]])
	lib['solve_thermal_problem']=my_data("type",_("Solve optical problem"),"QComboBoxLang",defaults=[[("true"),_("Yes")],["false",_("No")]])
	lib['layer_type']=my_data("type",_("Layer type"),"QComboBoxLang",defaults=[[("contact"),_("contact")],["active",_("active layer")],["other",_("other")]])

	lib['optical_thickness']=my_data("m",_("Optical thickness"),"QLineEdit")
	lib['optical_thickness_enabled']=my_data(_("au"),_("Enabled"),"gtkswitch")


	#dos?.inp
	##free carriers
	lib['dos_free_carrier_stats']=my_data("type",_("Free carrier statistics"),"QComboBoxLang",defaults=[[("mb_equation"),_("Maxwell Boltzmann - analytic")],["mb_look_up_table_analytic",_("Maxwell Boltzmann - numerical+analytic")],["mb_look_up_table",_("Maxwell Boltzmann - full numerical")],["fd_look_up_table",_("Ferm-Dirac - numerical")]],hide_on_token_eq=[["dd_enabled",False]])

	lib['text_free_carrier_']=my_data("",_("<b>Free carriers</b>"),"QLabel",hide_on_token_eq=[["dd_enabled",False]])
	lib['Nc']=my_data("m^{-3}",_("Effective density of free electron states (@300K)"),"QLineEdit",min=1e10,max=1e27,hide_on_token_eq=[["dd_enabled",False]] )
	lib['Nv']=my_data("m^{-3}",_("Effective density of free hole states (@300K)"),"QLineEdit",min=1e10,max=1e27,hide_on_token_eq=[["dd_enabled",False]] )

	lib['symmetric_mobility_e']=my_data("m^{2}V^{-1}s^{-1}",_("Electron mobility"),"mobility_widget",min=1.0,max=1e-1,defaults=[True], hide_on_token_eq=[["dd_enabled",False]])
	lib['symmetric_mobility_h']=my_data("m^{2}V^{-1}s^{-1}",_("Hole mobility"),"mobility_widget",min=1.0,max=1e-14, defaults=[False], hide_on_token_eq=[["dd_enabled",False]] )

	lib['mue_z']=my_data("m^{2}V^{-1}s^{-1}",_("Electron mobility z"),"mobility_widget",min=1.0,max=1e-1,hidden=True)
	lib['mue_x']=my_data("m^{2}V^{-1}s^{-1}",_("Electron mobility x"),"mobility_widget",min=1.0,max=1e-1,hidden=True)
	lib['mue_y']=my_data("m^{2}V^{-1}s^{-1}",_("Electron mobility y"),"mobility_widget",min=1.0,max=1e-1,hidden=True)
	lib['mue_delta']=my_data("eV","Electron activation (\u0394)","QLineEdit",hide_on_token_eq=[["config.mu_tdep_enable",False]] )
	lib['muh_z']=my_data("m^{2}V^{-1}s^{-1}",_("Hole mobility z"),"mobility_widget",min=1.0,max=1e-1,hidden=True)
	lib['muh_x']=my_data("m^{2}V^{-1}s^{-1}",_("Hole mobility x"),"mobility_widget",min=1.0,max=1e-1,hidden=True)
	lib['muh_y']=my_data("m^{2}V^{-1}s^{-1}",_("Hole mobility y"),"mobility_widget",min=1.0,max=1e-1,hidden=True)
	lib['muh_delta']=my_data("eV","Hole activation (\u0394)","QLineEdit",hide_on_token_eq=[["config.mu_tdep_enable",False]] )
	lib['mu_tdep_enable']=my_data(_("au"),_("Enable T dependent free carrier mob"),"gtkswitch")

	##Non dynamic SRH
	lib['text_steay_srh_']=my_data("",_("<b>Equilibrium SRH traps</b>"),"QLabel",hide_on_token_eq=[["ss_srh_enabled",False]])
	lib['srh_n1']=my_data("m^{-3}",_("n_{1}"),"QLineEdit",min=1e10,max=1e27,hide_on_token_eq=[["ss_srh_enabled",False]] )
	lib['srh_p1']=my_data("m^{-3}",_("p_{1}"),"QLineEdit",min=1e10,max=1e27,hide_on_token_eq=[["ss_srh_enabled",False]] )
	lib['srh_tau_n']=my_data("s^{-1}",_("tau_{n}"),"QLineEdit",min=1e10,max=1e27,hide_on_token_eq=[["ss_srh_enabled",False]] )
	lib['srh_tau_p']=my_data("s^{-1}",_("tau_{p}"),"QLineEdit",min=1e10,max=1e27,hide_on_token_eq=[["ss_srh_enabled",False]] )

	##Dynamic SRH
	lib['text_dynamic_traps_']=my_data("",_("<b>Non-equilibrium SRH traps</b>"),"QLabel",hide_on_token_eq=[["srh_bands",0]])
	lib['srh_bands']=my_data("bands",_("Number of traps"),"QLineEdit",hide_on_token_eq=[["srh_bands",0]])
	lib['dostype']=my_data("Edit",_("DoS distribution"),"generic_switch",units_widget="QPushButton",defaults=[[_("Complex"),"complex"],[_("Exponential"),"exponential"]],hide_on_token_eq=[["srh_bands",0]])
	lib['Ntrape']=my_data("m^{-3} eV^{-1}",_("Electron trap density"),"QLineEdit",min=1e10,max=1e27,hide_on_token_eq=[["dostype","complex"],["srh_bands",0]] )
	lib['Ntraph']=my_data("m^{-3} eV^{-1}",_("Hole trap density"),"QLineEdit",min=1e10,max=1e27,hide_on_token_eq=[["dostype","complex"],["srh_bands",0]] )
	lib['Etrape']=my_data("eV",_("Electron tail slope"),"QLineEdit",min=20e-3,max=150e-3,hide_on_token_eq=[["dostype","complex"],["srh_bands",0]] )
	lib['Etraph']=my_data("eV",_("Hole tail slope"),"QLineEdit",min=20e-3,max=150e-3,hide_on_token_eq=[["dostype","complex"],["srh_bands",0]] )

	lib['srhsigman_e']=my_data("m^{-2}",_("Free electron to Trapped electron"),"QLineEdit",min=1e-27,max=1e-15,hide_on_token_eq=[["srh_bands",0]] )
	lib['srhsigmap_e']=my_data("m^{-2}",_("Trapped electron to Free hole"),"QLineEdit",min=1e-27,max=1e-15,hide_on_token_eq=[["srh_bands",0]] )
	lib['srhsigman_h']=my_data("m^{-2}",_("Trapped hole to Free electron"),"QLineEdit",min=1e-27,max=1e-15,hide_on_token_eq=[["srh_bands",0]] )
	lib['srhsigmap_h']=my_data("m^{-2}",_("Free hole to Trapped hole"),"QLineEdit",min=1e-27,max=1e-15,hide_on_token_eq=[["srh_bands",0]])


	lib['function']=my_data("au",_("Function"),"QComboBoxLang",defaults=[["exp",_("Exponential")],["gaus",_("Gaussian")],["lorentzian",_("Lorentzian")]])
	lib['function_enable']=my_data(_("True/False"),_("Enable/Disable"),"gtkswitch")

	##Exciton
	lib['text_exciton_']=my_data("",_("<b>Excitons</b>"),"QLabel",hide_on_token_eq=[["exciton_enabled",False]])
	lib['exciton_L']=my_data("m",_("Scattering length"), "QLineEdit", hide_on_token_eq=[["exciton_enabled",False]])
	lib['exciton_tau']=my_data("m",_("Life time"), "QLineEdit", hide_on_token_eq=[["exciton_enabled",False]])
	lib['exciton_kpl']=my_data("s^{-1}",_("k_{pl}"),"QLineEdit", hide_on_token_eq=[["exciton_enabled",False]])
	lib['exciton_kfret']=my_data("s^{-1}",_("k_{fret}"),"QLineEdit",hide_on_token_eq=[["exciton_enabled",False]])
	lib['exciton_alpha']=my_data("m^{3} s^{-1}",_("k_{alpha}"),"QLineEdit",hide_on_token_eq=[["exciton_enabled",False]])
	lib['exciton_kdis']=my_data("s^{-1}",_("k_{dis}"),"QLineEdit",hide_on_token_eq=[["exciton_enabled",False]])

	lib['exciton_max_ittr']=my_data("au",_("Max itterations"),"QLineEdit")
	lib['exciton_min_error']=my_data("au",_("Convergence error"),"QLineEdit")

	##Optical boundaries
	lib['optical_y0']=my_data("au",_("Boundary condition for y_{min}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["abc",_("ABC")],["periodic",_("Periodic")]])
	lib['optical_y1']=my_data("au",_("Boundary condition for y_{max}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["abc",_("ABC")],["periodic",_("Periodic")]])
	lib['optical_x0']=my_data("au",_("Boundary condition for x_{min}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["abc",_("ABC")],["periodic",_("Periodic")]])
	lib['optical_x1']=my_data("au",_("Boundary condition for x_{max}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["abc",_("ABC")],["periodic",_("Periodic")]])
	lib['optical_z0']=my_data("au",_("Boundary condition for z_{min}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["abc",_("ABC")],["periodic",_("Periodic")]])
	lib['optical_z1']=my_data("au",_("Boundary condition for z_{max}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["abc",_("ABC")],["periodic",_("Periodic")]])

	##General boundries
	lib['y0_boundry']=my_data("au",_("Boundary condition for y_{min}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["neumann",_("Neumann (==0)")],["heatsink",_("Heatsink")]])
	lib['y1_boundry']=my_data("au",_("Boundary condition for y_{max}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["neumann",_("Neumann (==0)")],["heatsink",_("Heatsink")]])
	lib['x0_boundry']=my_data("au",_("Boundary condition for x_{min}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["neumann",_("Neumann (==0)")],["heatsink",_("Heatsink")]])
	lib['x1_boundry']=my_data("au",_("Boundary condition for x_{max}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["neumann",_("Neumann (==0)")],["heatsink",_("Heatsink")]])
	lib['z0_boundry']=my_data("au",_("Boundary condition for z_{min}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["neumann",_("Neumann (==0)")],["heatsink",_("Heatsink")]])
	lib['z1_boundry']=my_data("au",_("Boundary condition for z_{max}"),"QComboBoxLang",defaults=[["dirichlet",_("Dirichlet")],["neumann",_("Neumann (==0)")],["heatsink",_("Heatsink")]])

	##Exciton boundaries
	lib['n_y0']=my_data("m^{-3}",_("Exciton density at y_{min}"),"QLineEdit",  hide_on_token_eq=[["y0_boundry", "neumann"]])
	lib['heatsink_y0']=my_data("W m^{-}K^{-1}",_("Conductivity of heat sink y_{min}"),"QLineEdit", hide_on_token_eq=[["y0_boundry", "neumann"],["y0_boundry", "dirichlet"],["thermal",False]])
	lib['heatsink_length_y0']=my_data("m",_("Heat sink length y_{min}"),"QLineEdit",  hide_on_token_eq=[["y0_boundry", "neumann"],["y0_boundry", "dirichlet"]])

	lib['n_y1']=my_data("m^{-3}",_("Exciton density at y_{max}"),"QLineEdit",  hide_on_token_eq=[["y1_boundry", "neumann"],["y1_boundry", "heatsink"]])
	lib['heatsink_y1']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink y_{max}"),"QLineEdit",  hide_on_token_eq=[["y1_boundry", "neumann"],["y1_boundry", "dirichlet"]])
	lib['heatsink_length_y1']=my_data("m",_("Heat sink length y_{max}"),"QLineEdit",  hide_on_token_eq=[["y1_boundry", "neumann"],["y1_boundry", "dirichlet"]])

	lib['n_x0']=my_data("m^{-3}",_("Exciton density at x_{min}"),"QLineEdit",  hide_on_token_eq=[["x0_boundry", "neumann"]])
	lib['heatsink_x0']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink x_{min}"),"QLineEdit",  hide_on_token_eq=[["x0_boundry", "neumann"],["x0_boundry", "dirichlet"],["thermal",False]])
	lib['heatsink_length_x0']=my_data("m",_("Heat sink length x_{min}"),"QLineEdit",  hide_on_token_eq=[["x0_boundry", "neumann"],["x0_boundry", "dirichlet"]])

	lib['n_x1']=my_data("m^{-3}",_("Exciton density at x_{max}"),"QLineEdit",  hide_on_token_eq=[["x1_boundry", "neumann"]])
	lib['heatsink_x1']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink x_{max}"),"QLineEdit", hide_on_token_eq=[["x1_boundry", "neumann"],["x1_boundry", "dirichlet"],["thermal",False]])
	lib['heatsink_length_x1']=my_data("m",_("Heat sink length x_{max}"),"QLineEdit",  hide_on_token_eq=[["x1_boundry", "neumann"],["x1_boundry", "dirichlet"]])

	lib['n_z0']=my_data("Kelvin",_("Device temperature at z_{min}"),"QLineEdit",  hide_on_token_eq=[["z0_boundry", "neumann"]])
	lib['heatsink_z0']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink z_{min}"),"QLineEdit", hide_on_token_eq=[["z0_boundry", "neumann"],["z0_boundry", "dirichlet"],["thermal",False]])
	lib['heatsink_length_z0']=my_data("m",_("Heat sink length z_{min}"),"QLineEdit",  hide_on_token_eq=[["z0_boundry", "neumann"],["z0_boundry", "dirichlet"]])

	lib['n_z1']=my_data("m^{-3}",_("Exciton density at z_{max}"),"QLineEdit",  hide_on_token_eq=[["z1_boundry", "neumann"]])
	lib['heatsink_z1']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink z_{max}"),"QLineEdit",  hide_on_token_eq=[["z1_boundry", "neumann"],["z1_boundry", "dirichlet"],["thermal",False]])
	lib['heatsink_length_z1']=my_data("m",_("Heat sink length z_{max}"),"QLineEdit",  hide_on_token_eq=[["z1_boundry", "neumann"],["z1_boundry", "dirichlet"]])

	##auger
	lib['text_auger_']=my_data("",_("<b>Auger recombination</b>"),"QLabel",hide_on_token_eq=[["dos_enable_auger",False]])
	lib['dos_auger_Cn']=my_data("m^{6}s^{-1}",_("Auger C_{n}"),"QLineEdit",min=1e-30,max=1e-10,hide_on_token_eq=[["dos_enable_auger",False]] )
	lib['dos_auger_Cp']=my_data("m^{6}s^{-1}",_("Auger C_{p}"),"QLineEdit",min=1e-30,max=1e-10,hide_on_token_eq=[["dos_enable_auger",False]] )



	lib['T_start']=my_data("K",_("Start temperature"),"QLineEdit")
	lib['T_stop']=my_data("K",_("Stop temperature"),"QLineEdit")
	lib['T_steps']=my_data("au",_("Temperature steps"),"QLineEdit")


	lib['ion_density']=my_data("m^{-3}",_("Perovskite ion density"),"QLineEdit",min=1e10,max=1e27,hidden=True)
	#lib['ion_mobility']=my_data("m^{2}V^{-1}s^{-1}",_("Perovskite ion mobility"),1.0,"QLineEdit")

	lib['doping_start']=my_data("m^{-3}",_("Doping density (x=0)"),"QLineEdit",min=1.0,max=1e27,hidden=True)
	lib['doping_stop']=my_data("m^{-3}",_("Doping density (x=max)"),"QLineEdit",min=1.0,max=1e27,hidden=True)


	lib['free_to_free_recombination']=my_data("m^{3}s^{-1}",_("n_{free} to p_{free} Recombination rate constant"),"QLineEdit",min=1e-27,max=1e-15, hide_on_token_eq=[["dd_enabled",False]] )

	lib['text_electro_']=my_data("",_("<b>Electrostatics</b>"),"QLabel")
	lib['Eg']=my_data("eV",_("Eg"),"QLineEdit")
	lib['Xi']=my_data("eV",_("Xi"),"QLineEdit")
	lib['epsilonr']=my_data("au",_("Relative permittivity"),"QLineEdit",min=1.0,max=10.0 )

	##Exciton
	lib['text_singlet_']=my_data("",_("<b>Excited states</b>"),"QLabel",hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_fret']=my_data("s^{-1}",_("Forster transfer rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_s']=my_data("s^{-1}",_("Host singlet-exciton decay rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_isc']=my_data("s^{-1}",_("Host inter-system crossing rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_ss']=my_data("m^{3} s^{-1}",_("Host singlet-singlet annihilation (SSA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_sp']=my_data("m^{3} s^{-1}",_("Host singlet-polaron annihilation (SPA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_st']=my_data("m^{3} s^{-1}",_("Host singlet-triplet annihilation (STA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_dext']=my_data("s^{-1}",_("Dexter transfer rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_t']=my_data("s^{-1}",_("Host triplet decay rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_tp']=my_data("m^{3} s^{-1}",_("Host triplet-polaron annihilation (TPA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_tt']=my_data("m^{3} s^{-1}",_("Host triplet-triplet annihilation (TTA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_sd']=my_data("s^{-1}",_("Dopant singlet-exciton decay rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_iscd']=my_data("s^{-1}",_("Dopant inter-system crossing rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_spd']=my_data("m^{3} s^{-1}",_("Dopant singlet-polaron annihilation (SPA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_std']=my_data("m^{3} s^{-1}",_("Dopant singlet-triplet annihilation (STA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_ssd']=my_data("m^{3} s^{-1}",_("Dopant singlet-singlet annihilation (SSA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_td']=my_data("s^{-1}",_("Dopant triplet decay rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_ttd']=my_data("m^{3} s^{-1}",_("Dopant triplet-triplet annihilation (TTA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_tpd']=my_data("m^{3} s^{-1}",_("Dopant triplet-polaron annihilation (TPA) rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_gamma']=my_data("au",_("Confinement factor"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_zeta']=my_data("m^{3} s^{-1}",_("\u03BE Stimulated emission gain coefficient"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_k_cav']=my_data("s^{-1}",_("Cavity photon decay rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_beta_sp']=my_data("au",_("Spontaneous emission factor"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_C']=my_data("0.0-1.0",_("Dopant concentration"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_N_dop']=my_data("m^{-3}",_("Density of guest molecules"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_W']=my_data("0.0-1.0",_("Spectral overlap"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	#singlet solver+
	lib['singlet_k_risc']=my_data("s^{-1}",_("k_{RISC} Reverse Inter-System crossing rate"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_sigma_em']=my_data("m^{-1}",_("\u03C3_{em} Stimulated Emission cross section"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_sigma_t1tn']=my_data("m^{-1}",_("\u03C3_{t1tn} Triplet Absorption cross section"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_sigma_np']=my_data("m^{-1}",_("\u03C3_{n,p} Polaron Absorption cross section"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])
	lib['singlet_a']=my_data("m}",_("e-h separation distance"), "QLineEdit", hide_on_token_eq=[["singlet_enabled",False]])


	#materials database
	#electrical constants
	lib['material_blend']=my_data(_("True/False"),_("Blended material"),"gtkswitch" )
	lib['Eg0']=my_data("eV",_("Eg_{0}"),"QLineEdit")
	lib['Xi0']=my_data("eV",_("Xi_{0}"),"QLineEdit")
	lib['Eg1']=my_data("eV",_("Eg_{1}"),"QLineEdit",hide_on_token_eq=[["material_blend",False]])
	lib['Xi1']=my_data("eV",_("Xi_{1}"),"QLineEdit",hide_on_token_eq=[["material_blend",False]])

	#thermal constants
	lib['thermal_kl']=my_data("W m^{-1} C^{-1}",_("Thermal conductivity"),"QLineEdit")
	lib['thermal_tau_e']=my_data("s",_("Electron relaxation time"),"QLineEdit")
	lib['thermal_tau_h']=my_data("s",_("Hole relaxation time"),"QLineEdit")

	#lca
	lib['lca_density']=my_data("Kg m^{-3}",_("Density"),"QLineEdit")
	lib['lca_cost']=my_data(" $/Kg",_("Cost per Kg"),"QLineEdit")
	lib['lca_energy']=my_data("J/Kg",_("Energy per Kg"),"QLineEdit")

	#electrical?.inp
	lib['electrical_component']=my_data("type",_("Component"),"QComboBoxLang",defaults=[[("resistance"),_("Resistance")],["diode",_("Diode")],["link",_("Link")]])
	lib['electrical_shunt']=my_data("Ohm  m",_("Shunt resistivity"),"QLineEdit",min=0.1,max=1e20, hide_on_token_eq=[["electrical_component","resistance"],["electrical_component","link"]] )

	lib['electrical_symmetrical_resistance']=my_data("Ohm m",_("Series resistivity"),"mobility_widget", defaults=[False] )

	lib['electrical_series_z']=my_data("Ohm m",_("Series resistivity z"),"mobility_widget",min=1.0,max=1e-1,hidden=True)
	lib['electrical_series_x']=my_data("Ohm m",_("Series resistivity x"),"mobility_widget",min=1.0,max=1e-1,hidden=True)
	lib['electrical_series_y']=my_data("Ohm m",_("Series resistivity y"),"mobility_widget",min=1.0,max=1e-1,hidden=True)

	lib['electrical_n']=my_data("au",_("Layer ideality factor"),"QLineEdit",min=0.0,max=1.0, hide_on_token_eq=[["electrical_component","resistance"],["electrical_component","link"]] )
	lib['electrical_J0']=my_data("A m^{-2}",_("Reverse bias current"),"QLineEdit",min=0.0,max=1e6, hide_on_token_eq=[["electrical_component","resistance"],["electrical_component","link"]] )
	lib['electrical_enable_generation']=my_data(_("True/False"),_("Enable optical charge\ncarrier generation"),"gtkswitch", hide_on_token_eq=[["electrical_component","resistance"],["electrical_component","link"]] )


	#spm?.inp
	lib['spm_voltage']=my_data("V",_("Applied voltage"),"QLineEdit")
	lib['spm_scan_section']=my_data("su",_("Scan section"),"QComboBoxLang",defaults=[[("spm_whole_device"),_("Whole device")],["spm_box",_("Box section")],["spm_x_cut",_("x-Scan")]])
	lib['spm_x0']=my_data("m",_("x-start"),"QLineEdit",hide_on_token_eq=[["spm_scan_section","spm_whole_device"],["spm_scan_section","spm_x_cut"]])
	lib['spm_z0']=my_data("m",_("z-start"),"QLineEdit",hide_on_token_eq=[["spm_scan_section","spm_whole_device"],["spm_scan_section","spm_x_cut"]])
	lib['spm_x1']=my_data("m",_("x-stop"),"QLineEdit",hide_on_token_eq=[["spm_scan_section","spm_whole_device"],["spm_scan_section","spm_x_cut"]])
	lib['spm_z1']=my_data("m",_("z-stop"),"QLineEdit",hide_on_token_eq=[["spm_scan_section","spm_whole_device"],["spm_scan_section","spm_x_cut"]])

	#scan
	lib['scan_optimizer_dump_at_end']=my_data(_("True/False"),_("Dump only at end"),"gtkswitch")
	lib['scan_optimizer_dump_n_steps']=my_data("steps",_("Dump every n steps"),"QLineEdit", hide_on_token_eq=[["scan_optimizer_dump_at_end",True]])

	#shape?.inp
	lib['shape_type']=my_data(_("Edit"),_("Shape type"),"g_select_shape",units_widget="QPushButton")

	lib['rotate_y']=my_data("degrees",_("Rotate around y-axis"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]], pack=[_("Rotate"),_("y-axis"),_("x-axis")])
	lib['rotate_x']=my_data("degrees",_("Rotate around x-axis"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])

	lib['dx']=my_data("m",_("dx of the object"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]],pack=["xyz size","dx","dy","dz"])
	lib['dy']=my_data("m",_("dy of the object"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])
	lib['dz']=my_data("m",_("dz of the object"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])

	lib['dx_padding']=my_data("m",_("dx padding"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]],pack=[ _("padding"),"dx","dy","dz"])
	lib['dy_padding']=my_data("m",_("dy padding"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])
	lib['dz_padding']=my_data("m",_("dz padding"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])

	lib['shape_hidden']=my_data("au",_("Hidden"),"gtkswitch")
	lib['shape_nx']=my_data("au",_("Number of objects x"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]],pack=[_("Number of objects"),"x","y","z"])
	lib['shape_ny']=my_data("au",_("Number of objects y"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])
	lib['shape_nz']=my_data("au",_("Number of objects z"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])
	lib['text_object_']=my_data("",_("<b>Object</b>"),"QLabel",show_on_token_eq=[["light_illuminate_from","xyz"]])
	lib['text_attributes_']=my_data("",_("<b>Attributes</b>"),"QLabel")

	lib['x0']=my_data("m",_("x offset"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]],pack=[_("Offset"),"x","y","z"])
	lib['y0']=my_data("m",_("y offset"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])
	lib['z0']=my_data("m",_("z offset"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"]])
	lib['html_link']=my_data(_("au"),_("Web page link"),"QLineEdit")
	lib['label']=my_data(_("au"),_("Text label"),"QLineEdit")
	lib['image_path']=my_data(_("au"),_("Texture"),"QLineEdit")
	lib['shape_dos']=my_data(_("Edit"),_("Drift diffusion"),"shape_dos_switch",units_widget="QPushButton")
	lib['shape_electrical']=my_data(_("Edit"),_("Circuit model\nparameters"),"shape_electrical_switch",units_widget="QPushButton")
	lib['optical_material']=my_data(_("Edit"),_("Optical material"),"g_select_material" ,units_widget="QPushButton")
	lib['color_r']=my_data("rgb",_("Color"),"QColorPicker")

	#interface?.inp
	lib['interface_model']=my_data("type",_("Interface model"),"QComboBoxLang",defaults=[[("none"),_("None")],["recombination",_("Free-to-Free")],["recombination_srh",_("Free-to-trap (SRH)")]])
	lib['interface_eh_tau']=my_data("m^{3}s^{-1}",_("Recombination constant"),"QLineEdit",hide_on_token_eq=[["interface_model","none"]])

	lib['interface_left_doping_enabled']=my_data(_("True/False"),_("Interface doping LHS"),"gtkswitch")
	lib['interface_left_doping']=my_data("m^{-3}",_("Doping LHS"),"QLineEdit", hide_on_token_eq=[["interface_left_doping_enabled",False]])

	lib['interface_tunnel_e']=my_data(_("True/False"),_("Electron tunneling"),"gtkswitch")
	lib['interface_Ge']=my_data("m^{3}s^{-1}",_("Electron tunneling (T)"),"QLineEdit", hide_on_token_eq=[["interface_tunnel_e",False]])


	lib['interface_tunnel_h']=my_data(_("True/False"),_("Hole tunneling"),"gtkswitch")
	lib['interface_Gh']=my_data("m^{3}s^{-1}",_("Hole tunneling (T)"),"QLineEdit", hide_on_token_eq=[["interface_tunnel_h",False]])

	lib['interface_right_doping_enabled']=my_data(_("True/False"),_("Interface doping RHS"),"gtkswitch")
	lib['interface_right_doping']=my_data("m^{-3}",_("Doping RHS"),"QLineEdit", hide_on_token_eq=[["interface_right_doping_enabled",False]])


	#stark.inp
	lib['stark_startime']=my_data("s",_("startime"),"QLineEdit")
	lib['stark_ea_factor']=my_data("au",_("ea_factor"),"QLineEdit")
	lib['stark_Np']=my_data("1/0",_("Np"),"QLineEdit")
	lib['stark_den']=my_data("1/0",_("den"),"QLineEdit")
	lib['stark_externalv']=my_data("V",_("externalv"),"QLineEdit")
	lib['stark_dt_neg_time']=my_data("s",_("dt_neg_time"),"QLineEdit")
	lib['stark_dt']=my_data("s",_("dt"),"QLineEdit")
	lib['stark_dt_mull']=my_data("au",_("dt_mull"),"QLineEdit")
	lib['stark_stop']=my_data("s",_("stop"),"QLineEdit")
	lib['stark_stark']=my_data("1/0",_("stark"),"QLineEdit")
	lib['stark_lasereff']=my_data("1/0",_("lasereff"),"QLineEdit")
	lib['stark_probe_wavelength']=my_data("nm",_("wavelength"),1e9,"QLineEdit")
	lib['stark_sim_contacts']=my_data("1/0",_("sim_contacts"),"QLineEdit")

	#ref / bib
	lib['url']=my_data("au",_("Website"),"QLineEdit")
	lib['author']=my_data("au",_("Author"),"QLineEdit")
	lib['journal']=my_data("au",_("Journal"),"QLineEdit")
	lib['title']=my_data("au",_("Title"),"QLineEdit")
	lib['volume']=my_data("au",_("Volume"),"QLineEdit")
	lib['pages']=my_data("au",_("Pages"),"QLineEdit")
	lib['year']=my_data("au",_("Year"),"QLineEdit")
	lib['DOI']=my_data("au",_("DOI"),"QLineEdit")
	lib['booktitle']=my_data("au",_("Book title"),"QLineEdit")
	lib['publisher']=my_data("au",_("Publisher"),"QLineEdit")
	lib['isbn']=my_data("au",_("ISBN"),"QLineEdit")
	lib['unformatted']=my_data("au",_("Scraped text"),"QLineEdit")

	#pulse?.inp
	lib['pulse_shift']=my_data("s","Shift of TPC signal","QLineEdit")
	lib['Rshort_pulse']=my_data("Ohms",_("R_{short}"),"QLineEdit")
	lib['pulse_bias']=my_data("V",_("V_{bias}"),"QLineEdit")
	lib['pulse_light_efficiency']=my_data("au",_("Efficiency of light"),"QLineEdit")
	lib['pulse_subtract_dc']=my_data(_("True/False"),_("subtract DC"),"gtkswitch")
	lib['Rload']=my_data("Ohms",_("External load resistor"),"QLineEdit")

	#mat.inp
	lib['material_type']=my_data("type",_("Material type"),"QComboBoxLang",defaults=[[("organic"),_("Organic")],["oxide",_("Oxide")],["inorganic",_("Inorganic")],["metal",_("Metal")],["other",_("Other")]])
	lib['mat_alpha']=my_data("0-1",_("Transparency"),"QLineEdit")
	lib['status']=my_data("type",_("Privicy options"),"QComboBoxLang",defaults=[[("public"),_("Public - everyone")],[("public_internal"),_("Public - within org")],["private",_("Private - never publish")]])
	lib['changelog']=my_data("au",_("Change log"),"QChangeLog")

	#jv.inp
	lib['jv_step_mul']=my_data("0-2.0",_("JV voltage step multiplyer"),"QLineEdit")
	lib['jv_max_j']=my_data("A m^{-2}",_("Maximum current density"),"QLineEdit")
	lib['jv_light_efficiency']=my_data("au",_("JV curve photon generation efficiency"),"QLineEdit")
	lib['jv_pmax_n']=my_data("m^{-3}",_("Average carrier density at P_{max}"),"QLineEdit")
	lib['Vstart']=my_data("V",_("Start voltage"),"QLineEdit")
	lib['Vstop']=my_data("V",_("Stop voltage"),"QLineEdit")
	lib['Vstep']=my_data("V",_("Voltage step"),"QLineEdit")
	lib['jv_single_point']=my_data(_("True/False"),_("Single point"),"gtkswitch")
	lib['jv_use_external_voltage_as_stop']=my_data(_("True/False"),_("Use external\nvoltage as stop"),"gtkswitch")
	lib['text_output_']=my_data("",_("<b>Output</b>"),"QLabel")
	lib['dump_energy_space']=my_data("au",_("Dump trap distribution"),"QComboBoxLang",defaults=[[("false"),_("False")],["energy_space_map",_("Energy space map")],["single_mesh_point",_("Single mesh point")]],hide_on_token_eq=[["dump_verbosity", -1],["dump_verbosity", 0]])
	lib['dump_x']=my_data("au",_("x-position"),"QLineEdit",show_on_token_eq=[["dump_energy_space","single_mesh_point"]],hide_on_token_eq=[["dump_verbosity", -1],["dump_verbosity", 0]])
	lib['dump_y']=my_data("au",_("y-position"),"QLineEdit",show_on_token_eq=[["dump_energy_space","single_mesh_point"]],hide_on_token_eq=[["dump_verbosity", -1],["dump_verbosity", 0]])
	lib['dump_z']=my_data("au",_("z-position"),"QLineEdit",show_on_token_eq=[["dump_energy_space","single_mesh_point"]],hide_on_token_eq=[["dump_verbosity", -1],["dump_verbosity", 0]])


	#sim_info.dat (jv plugin
	lib['voc']=my_data("V",_("V_{oc}"),"QLineEdit")
	lib['jv_vbi']=my_data("V",_("V_{bi}"),"QLineEdit")
	lib['pce']=my_data("Percent",_("Power conversion efficiency (PCE)"),"QLineEdit")
	lib['ff']=my_data("a.u.",_("Fill factor"),"QLineEdit")
	lib['Pmax']=my_data("W m^{-2}",_("Max power"),"QLineEdit")
	lib['v_pmax']=my_data("V",_("Voltage at max power"),"QLineEdit")
	lib['j_pmax']=my_data("Am^{-2}",_("Current density at max power"),"QLineEdit")

	lib['voc_nt']=my_data("m^{-3}",_("Trapped electrons at Voc"),"QLineEdit")
	lib['voc_pt']=my_data("m^{-3}",_("Trapped holes at Voc"),"QLineEdit")
	lib['voc_nf']=my_data("m^{-3}",_("Free electrons at Voc"),"QLineEdit")
	lib['voc_pf']=my_data("m^{-3}",_("Free holes at Voc"),"QLineEdit")
	lib['voc_np_tot']=my_data("m^{-3}",_("Total carriers (n+p)/2 at Voc"),"QLineEdit")

	lib['voc_R']=my_data("m^{-3}s^{-1}",_("Recombination rate at Voc"),"QLineEdit")
	lib['voc_J']=my_data("A m^{-2}",_("Current density at Voc"),"QLineEdit")
	lib['jsc']=my_data("A m^{-2}",_("J_{sc}"),"QLineEdit")

	#mu
	lib['mue_pmax']=my_data("m^{2}V^{-1}s^{-1}",_("Electron mobility at P_{max}"),"QLineEdit")
	lib['muh_pmax']=my_data("m^{2}V^{-1}s^{-1}",_("Hole mobility at P_{max}"),"QLineEdit")
	lib['mu_jsc']=my_data("m^{2}V^{-1}s^{-1}",_("Average mobility as J_{sc}"),"QLineEdit")
	lib['mu_pmax']=my_data("m^{2}V^{-1}s^{-1}",_("Average mobility at P_{max}"),"QLineEdit")
	lib['mu_voc']=my_data("m^{2}V^{-1}s^{-1}",_("Average mobility at V_{oc}"),"QLineEdit")

	#theta

	lib['theta_srh_free']=my_data("au",_("Theta_{SRH} - free P_{max}"),"QLineEdit")
	lib['theta_srh_free_trap']=my_data("au",_("Theta_{SRH} - free-trap P_{max}"),"QLineEdit")
	#tau
	lib['tau_pmax']=my_data("s",_("Recombination time constant"),"QLineEdit")
	lib['tau_voc']=my_data("s",_("Recombination time constant at Voc"),"QLineEdit")
	lib['device_C']=my_data("F",_("Device capacitance"),"QLineEdit")



	#sim_info.dat (optics plugin
	lib['light_photons_in_active_layer']=my_data("m^{-2}",_("Photos absorbed in active layer"),"QLineEdit")


	#object_stats.dat (optics plugin
	lib['object_stats.dat']=my_data("#Rp[0-9]","m",_("Peak height Rp"),"QLineEdit")
	lib['object_stats.dat']=my_data("#Rq[0-9]","m",_("RMS height Rq"),"QLineEdit")
	lib['object_stats.dat']=my_data("#Ra[0-9]","m",_("Average height Ra"),"QLineEdit")

	#cv?.inp
	lib['cv_start_voltage']=my_data("Volts",_("Start voltage"),"QLineEdit")
	lib['cv_stop_voltage']=my_data("Volts",_("Stop voltage"),"QLineEdit")
	lib['cv_dv_step']=my_data("Volts",_("dV step"),"QLineEdit")
	lib['cv_fx']=my_data("Hz",_("Frequency"),"QLineEdit")


	#sim_info.dat (equlibrium
	lib['left_holes']=my_data("m^{-3}",_("Left hole density"),"QLineEdit")
	lib['left_electrons']=my_data("m^{-3}",_("Left electron density"),"QLineEdit")
	lib['right_holes']=my_data("m^{-3}",_("Right hole density"),"QLineEdit")
	lib['right_electrons']=my_data("m^{-3}",_("Right electron density"),"QLineEdit")
	lib['Vbi']=my_data("m^{-3}",_("Built in potential"),"QLineEdit")
	lib['electron_affinity_left']=my_data("eV",_("Electron affinity left"),"QLineEdit")
	lib['electron_affinity_right']=my_data("eV",_("Electron affinity right"),"QLineEdit")

	#server.inp
	lib['text_cpu']=my_data("au",_("<b>CPU</b>"),"QLabel")
	lib['core_max_threads']=my_data("au",_("Number of threads used by the backend"),"QLineEdit")
	lib['max_core_instances']=my_data("au",_("Maximum number of core instances"),"QLineEdit")

	lib['server_stall_time']=my_data("au","Stall time","QLineEdit")
	lib['server_exit_on_dos_error']=my_data("","","QLineEdit")
	lib['server_max_run_time']=my_data("s","Max fit run time","QLineEdit")
	lib['server_min_cpus']=my_data("au","Min cpus","QLineEdit")
	lib['server_steel']=my_data("au","Steel CPUs","QLineEdit")

	lib['port']=my_data("au","Cluster port","QLineEdit")
	lib['path_to_src']=my_data("au",_("Path to source code"),"QLineEdit")
	lib['path_to_libs']=my_data("au",_("Path to compiled libs for cluster"),"QLineEdit")
	lib['make_command']=my_data("au",_("Make command"),"QLineEdit")
	lib['exe_name']=my_data("au",_("exe name"),"QLineEdit")
	lib['server_use_dos_disk_cache']=my_data(_("True/False"),_("Store DoS on disk"),"gtkswitch")
	lib['text_gpu']=my_data("au",_("<b>GPU</b>"),"QLabel")


	#cluster.inp
	lib['cluster_user_name']=my_data("au","User name","QLineEdit")
	lib['cluster_ip']=my_data("au","Cluster IP","QLineEdit")
	lib['cluster_master_ip']=my_data("au","Cluster master IP","QLineEdit")
	lib['cluster_cluster_dir']=my_data("au",_("Remote cluster directory"),"QLineEdit")
	lib['cluster_node_list']=my_data("au",_("Remote node list"),"QLineEdit")
	lib['cluster_iv']=my_data("au",_("IV"),"QLineEdit")
	lib['cluster_key']=my_data("au",_("Key"),"QLineEdit")

	#triangle mesh editor
	lib['mesh_gen_nx']=my_data("au",_("x-triangles"),"QLineEdit")
	lib['mesh_gen_ny']=my_data("au",_("y-triangles"),"QLineEdit")
	lib['mesh_gen_opp']=my_data("au",_("Method"),"QComboBoxLang",defaults=[["node_reduce",_("Node reduce")],["square_mesh_gen",_("No reduce")]])
	lib['mesh_min_ang']=my_data("au",_("Min allowable angle"),"QLineEdit")

	lib['shape_import_blur']=my_data("width pixels",_("Gaussian blur"),"QLineEdit")
	lib['shape_import_y_norm_percent']=my_data("percent",_("Percent of histogram to ignore"),"QLineEdit")

	lib['gauss_sigma']=my_data("pixels",_("Sigma of gaussian"),"QLineEdit")
	lib['gauss_offset_x']=my_data("pixels",_("Gaussian offset x"),"QLineEdit")
	lib['gauss_offset_y']=my_data("pixels",_("Gaussian offset y"),"QLineEdit")
	lib['gauss_invert']=my_data(_("True/False"),"Invert","gtkswitch")

	lib['shape_type0_enable']=my_data(_("True/False"),"Enable shape0","gtkswitch")
	lib['shape_type0']=my_data(_("Edit"),_("Shape type"),"g_select_shape",units_widget="QPushButton",  hide_on_token_eq=[["shape_type0_enable", False]])
	lib['shape_type1_enable']=my_data(_("True/False"),"Enable shape1","gtkswitch")
	lib['shape_type1']=my_data(_("Edit"),_("Shape type"),"g_select_shape",units_widget="QPushButton",  hide_on_token_eq=[["shape_type1_enable", False]])

	#honeycomb
	lib['honeycomb_dx']=my_data("pixels",_("dx of Honeycomb"),"QLineEdit")
	lib['honeycomb_dy']=my_data("pixels",_("dy of Honeycomb"),"QLineEdit")
	lib['honeycomb_line_width']=my_data("pixels",_("Line width"),"QLineEdit")
	lib['honeycomb_x_shift']=my_data("pixels",_("x shift"),"QLineEdit")
	lib['honeycomb_y_shift']=my_data("pixels",_("y shift"),"QLineEdit")
	lib['honeycomb_rotate']=my_data("pixels",_("Rotate"),"QLineEdit")
	lib['image_ylen']=my_data("pixels",_("y size"),"QLineEdit")
	lib['image_xlen']=my_data("pixels",_("x size"),"QLineEdit")

	#threshold
	lib['threshold_value']=my_data("0-255",_("Threshold value"),"QLineEdit")

	#xtal
	lib['xtal_dr']=my_data("pixels",_("dr"),"QLineEdit")
	lib['xtal_dx']=my_data("pixels",_("dx"),"QLineEdit")
	lib['xtal_dy']=my_data("pixels",_("dy"),"QLineEdit")
	lib['xtal_offset']=my_data("pixels",_("offset"),"QLineEdit")

	#lens
	lib['lens_type']=my_data("au",_("Lens type"),"QComboBoxLang",defaults=[["convex",_("Convex")],["concave",_("Concave")]])
	lib['lens_size']=my_data("au",_("Lens size"),"QLineEdit")

	#saw wave
	lib['shape_saw_offset']=my_data("pixels",_("Offset"),"QLineEdit")
	lib['shape_saw_length']=my_data("pixels",_("length"),"QLineEdit")
	lib['shape_saw_type']=my_data("au",_("Waveform"),"QComboBoxLang",defaults=[["square_wave",_("Square")],["saw_wave",_("Saw wave")]])
	#honeycomb
	lib['shape_import_blur']=my_data("pixels",_("pixels"),"QLineEdit")


	#boundary
	lib['image_boundary_x0']=my_data("pixels",_("Boundary x0"),"QLineEdit")
	lib['image_boundary_x0_color']=my_data("rgb",_("Color"),"QColorPicker_one_line")
	lib['image_boundary_x1']=my_data("pixels",_("Boundary x1"),"QLineEdit")
	lib['image_boundary_x1_color']=my_data("rgb",_("Color"),"QColorPicker_one_line")
	lib['image_boundary_y0']=my_data("pixels",_("Boundary y0"),"QLineEdit")
	lib['image_boundary_y0_color']=my_data("rgb",_("Color"),"QColorPicker_one_line")
	lib['image_boundary_y1']=my_data("pixels",_("Boundary y1"),"QLineEdit")
	lib['image_boundary_y1_color']=my_data("rgb",_("Color"),"QColorPicker_one_line")

	#math.inp
	lib['text_newton_first_itt']=my_data("au",_("<b>Fist iteration</b>"),"QLabel")
	lib['maxelectricalitt_first']=my_data("au",_("Max Electrical iterations (first step)"),"QLineEdit")
	lib['electricalclamp_first']=my_data("au",_("Electrical clamp (first step)"),"QLineEdit")
	lib['math_electrical_error_first']=my_data("au",_("Desired solver error (first step)"),"QLineEdit")
	lib['newton_first_temperature_ramp']=my_data(_("True/False"),"Ramp temperature","gtkswitch")

	lib['text_newton_later_itt']=my_data("au",_("<b>Later iterations</b>"),"QLabel")
	lib['maxelectricalitt']=my_data("au",_("Max electrical iterations"),"QLineEdit")
	lib['electricalclamp']=my_data("au",_("Electrical clamp"),"QLineEdit")
	lib['electricalerror']=my_data("au",_("Desired solver error"),"QLineEdit")


	lib['text_newton_exit_strategy']=my_data("au",_("<b>Exit strategy</b>"),"QLabel")
	lib['newton_clever_exit']=my_data(_("True/False"),"Newton solver clever exit","gtkswitch")
	lib['newton_min_itt']=my_data("au",_("Newton minimum iterations"),"QLineEdit")

	lib['text_newton_solver_type']=my_data("au",_("<b>Solver type</b>"),"QLabel")
	lib['complex_solver_name']=my_data(_("dll name"),_("Complex matrix solver to use"),"QLineEdit")

	lib['math_stop_on_convergence_problem']=my_data(_("True/False"),_("Quit on convergence problem"),"gtkswitch")
	lib['math_stop_on_inverted_fermi_level']=my_data(_("True/False"),_("Quit on inverted Fermi-level"),"gtkswitch")
	lib['text_newton_output']=my_data("au",_("<b>Output</b>"),"QLabel")

	#pos
	lib['pos_max_ittr']=my_data("au",_("Poisson solver max iterations"),"QLineEdit")
	lib['pos_min_error']=my_data("au",_("Desired solver error"),"QLineEdit")
	lib['posclamp']=my_data("au",_("Poisson clamping"),"QLineEdit")
	lib['math_enable_pos_solver']=my_data(_("True/False"),_("Enable poisson solver"),"gtkswitch")
	lib['pos_dump_verbosity']=my_data("au",_("Output verbosity to disk"),"QComboBoxLang",defaults=[["0",_("Nothing")],[("1"),_("Write everything to disk")]])

	lib['solver_name']=my_data(_("dll name"),_("Matrix solver"),"QComboBoxNewtonSelect",defaults=["umfpack","external_solver","csparse","superlu","nr_d","nr_ld"])

	lib['newton_name']=my_data(_("dll name"),_("Newton solver to use"),"QComboBoxNewtonSelect",defaults=["none","newton_2d","newton_norm","newton","poisson_2d"])
	lib['math_t0']=my_data("au",_("Slotboom T0"),"QLineEdit")
	lib['math_d0']=my_data("au",_("Slotboom D0"),"QLineEdit")
	lib['math_n0']=my_data("au",_("Slotboom n0"),"QLineEdit")
	lib['math_current_calc_at']=my_data("au",_("Calculate current at"), "QComboBoxLang",defaults=[["contacts",_("Contacts")],["mid_point",_("Mid point")],["avg",_("Average")]])

	lib['kl_in_newton']=my_data("au",_("Solve Kirchhoff's current law in Newton solver"),"gtkswitch")


	#fit.inp
	lib['sim_data']=my_data(_("filename"),"Simulation file to fit against","QLineEdit")
	lib['time_shift']=my_data("s","Shift experimental x","QLineEdit")
	lib['fit_shift_y']=my_data("s","Shift experimental y","QLineEdit")
	lib['start']=my_data("s","Fit x start","QLineEdit")
	lib['stop']=my_data("s","Fit x stop","QLineEdit")
	lib['log_x']=my_data(_("True/False"),_("log x"),"gtkswitch")
	lib['log_y']=my_data(_("True/False"),_("log y"),"gtkswitch")
	lib['log_y_keep_sign']=my_data(_("True/False"),_("Keep sign for log y "),"gtkswitch")
	lib['fit_invert_simulation_y']=my_data(_("True/False"),_("Invert simulated data (y)"),"gtkswitch")
	lib['fit_subtract_lowest_point']=my_data(_("True/False"),_("Subtract lowest point"),"gtkswitch")
	lib['fit_set_first_point_to_zero']=my_data(_("True/False"),_("Set first point to zero"),"gtkswitch")
	lib['fit_1st_deriv']=my_data(_("True/False"),_("Fit df(x)/dx"),"gtkswitch")
	lib['fit_against']=my_data( "au", _("Fit against simulation"),"QComboBoxLang")
	lib['fit_error_mul']=my_data("au",_("Fit error multiplyer"),"QLineEdit")
	lib['fit_randomize']=my_data(_("True/False"),_("Randomize fit"),"gtkswitch")
	lib['fit_random_reset_ittr']=my_data("au",_("Number of iterations between random reset"),"QLineEdit")
	lib['fit_stall_steps']=my_data("au",_("Stall steps"),"QLineEdit")
	lib['fit_disable_reset_at']=my_data("au",_("Disable reset at level"),"QLineEdit")
	lib['fit_converge_error']=my_data("au",_("Fit define convergence"),"QLineEdit")
	lib['fit_enable_simple_reset']=my_data("au",_("Enable simplex reset"),"gtkswitch")
	lib['fit_enable_simple_reset']=my_data("au",_("Simplex reset steps"),"gtkswitch")
	lib['fit_method']=my_data("au",_("Fiting method"),"QComboBox",defaults=["simplex","newton"])
	lib['fit_simplexmul']=my_data("au",_("Start simplex step multiplication"),"QLineEdit")
	lib['fit_simplex_reset']=my_data("au",_("Simplex reset steps"),"QLineEdit")
	lib['fit_set_error_to_zero_before']=my_data("au",_("Set error to zero before"),"QLineEdit")
	lib['fit_dump_snapshots']=my_data(_("True/False"),_("Enable snapshots during fit"),"gtkswitch")
	lib['fit_norm_data_at']=my_data(_("True/False"),_("Normalize data at x point"),"gtkswitch")
	lib['fit_norm_x_point']=my_data("au",_("Point to normalize"),"QLineEdit", hide_on_token_eq=[["fit_norm_data_at", False]])

	lib['banned_enabled']=my_data("au",_("File or token banned"),"gtkswitch")


	#eqe.inp
	lib['eqe_voltage']=my_data("V",_("EQE Voltage"),"QLineEdit")
	lib['eqe_light_power2']=my_data("Suns",_("Optical power"),"QLineEdit",  hide_on_token_eq=[["eqe_single_light_point", False]])
	lib['eqe_single_light_point']=my_data("au",_("Single optical power"),"gtkswitch")
	lib['eqe_suns_start']=my_data("Suns",_("Optical power start"),"QLineEdit",  hide_on_token_eq=[["eqe_single_light_point", True]])
	lib['eqe_suns_stop']=my_data("Suns",_("Optical power stop"),"QLineEdit",  hide_on_token_eq=[["eqe_single_light_point", True]])
	lib['eqe_wavelength']=my_data("m",_("Wavelength"),"QLineEdit",  hide_on_token_eq=[["eqe_single_light_point", True]])
	lib['eqe_use_electrical_dos']=my_data("m",_("Use electrical DoS at low energy"),"gtkswitch")

	#mode
	lib['mode_max_ittr']=my_data("au",_("Max iterations "),"QLineEdit")
	lib['mode_stop_error']=my_data("au",_("Stop error"),"QLineEdit")
	lib['mode_max_eigenmode_x']=my_data("au",_("Number of x eigenmodes"),"QLineEdit")
	lib['mode_max_eigenmode_y']=my_data("au",_("Number of y eigenmodes"),"QLineEdit")
	lib['mode_te_tm']=my_data("au",_("TE/TM"),"QComboBoxLang",defaults=[["TE",_("Transverse Electric (TE)")],["TM",_("Transverse Magnetic (TM)")]], hide_on_token_eq=[["thermal",False]])
	lib['mode_only_fundamental']=my_data(_("True/False"),_("Find only fundamental"),"gtkswitch")

	#thermal.inp
	lib['thermal_model_type']=my_data("au",_("Thermal model type"),"QComboBoxLang",defaults=[["thermal_hydrodynamic",_("Hydrodynamic")],["thermal_lattice",_("Lattice heat")]], hide_on_token_eq=[["thermal",False]])

	lib['Ty0']=my_data("Kelvin",_("Device temperature at y_{min}"),"QLineEdit",  hide_on_token_eq=[["y0_boundry", "neumann"]])
	lib['heatsink_y0']=my_data("W m^{-}K^{-1}",_("Conductivity of heat sink y_{min}"),"QLineEdit",  hide_on_token_eq=[["y0_boundry", "neumann"],["y0_boundry", "dirichlet"], ["thermal",False]])
	lib['heatsink_length_y0']=my_data("m",_("Heat sink length y_{min}"),"QLineEdit",  hide_on_token_eq=[["y0_boundry", "neumann"],["y0_boundry", "dirichlet"]])

	lib['Ty1']=my_data("Kelvin",_("Device temperature at y_{max}"),"QLineEdit",  hide_on_token_eq=[["y1_boundry", "neumann"]])
	lib['heatsink_y1']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink y_{max}"),"QLineEdit",  hide_on_token_eq=[["y1_boundry", "neumann"],["y1_boundry", "dirichlet"],["thermal",False]])
	lib['heatsink_length_y1']=my_data("m",_("Heat sink length y_{max}"),"QLineEdit",  hide_on_token_eq=[["y1_boundry", "neumann"],["y1_boundry", "dirichlet"]])

	lib['Tx0']=my_data("Kelvin",_("Device temperature at x_{min}"),"QLineEdit",  hide_on_token_eq=[["x0_boundry", "neumann"]])
	lib['heatsink_x0']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink x_{min}"),"QLineEdit", hide_on_token_eq=[["x0_boundry", "neumann"],["x0_boundry", "dirichlet"],["thermal",False]])
	lib['heatsink_length_x0']=my_data("m",_("Heat sink length x_{min}"),"QLineEdit",  hide_on_token_eq=[["x0_boundry", "neumann"],["x0_boundry", "dirichlet"]])

	lib['Tx1']=my_data("Kelvin",_("Device temperature at x_{max}"),"QLineEdit",  hide_on_token_eq=[["x1_boundry", "neumann"]])
	lib['heatsink_x1']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink x_{max}"),"QLineEdit", hide_on_token_eq=[["x1_boundry", "neumann"],["x1_boundry", "dirichlet"], ["thermal",False]])
	lib['heatsink_length_x1']=my_data("m",_("Heat sink length x_{max}"),"QLineEdit",  hide_on_token_eq=[["x1_boundry", "neumann"],["x1_boundry", "dirichlet"]])

	lib['Tz0']=my_data("Kelvin",_("Device temperature at z_{min}"),"QLineEdit",  hide_on_token_eq=[["z0_boundry", "neumann"]])
	lib['heatsink_z0']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink z_{min}"),"QLineEdit",  hide_on_token_eq=[["z0_boundry", "neumann"],["z0_boundry", "dirichlet"],["thermal",False]])
	lib['heatsink_length_z0']=my_data("m",_("Heat sink length z_{min}"),"QLineEdit",  hide_on_token_eq=[["z0_boundry", "neumann"],["z0_boundry", "dirichlet"]])

	lib['Tz1']=my_data("Kelvin",_("Device temperature at z_{max}"),"QLineEdit",  hide_on_token_eq=[["z1_boundry", "neumann"]])
	lib['heatsink_z1']=my_data("W m^{-2}K^{-1}",_("Conductivity of heat sink z_{max}"),"QLineEdit", hide_on_token_eq=[["z1_boundry", "neumann"],["z1_boundry", "dirichlet"], ["thermal",False]])
	lib['heatsink_length_z1']=my_data("m",_("Heat sink length z_{max}"),"QLineEdit",  hide_on_token_eq=[["z1_boundry", "neumann"],["z1_boundry", "dirichlet"]])


	lib['thermal_l']=my_data(_("True/False"),_("Lattice heat model"),"gtkswitch",hide_on_token_eq=[["thermal_model_type", "thermal_lattice"], ["thermal",False]])
	lib['thermal_e']=my_data(_("True/False"),_("Electron heat model"),"gtkswitch",hide_on_token_eq=[["thermal_model_type", "thermal_lattice"],["thermal",False]])
	lib['thermal_h']=my_data(_("True/False"),_("Hole heat model"),"gtkswitch",hide_on_token_eq=[["thermal_model_type", "thermal_lattice"],["thermal",False]])

	lib['thermal_max_ittr']=my_data("au",_("Max thermal solver iterations"),"QLineEdit")
	lib['thermal_min_error']=my_data("au",_("Desired thermal error"),"QLineEdit")

	lib['T_mesh_force']=my_data(_("True/False"),_("Force use of thermal mesh"),"gtkswitch")
	lib['T_min']=my_data("Kelvin",_("Minimum device temperature"),"QLineEdit" )
	lib['T_max']=my_data("Kelvin",_("Maximum device temperature"),"QLineEdit" )
	lib['Tpoints']=my_data("points",_("Thermal mesh points"),"QLineEdit" )


	#electrical.inp
	lib['electrical_y0_boundry']=my_data("au",_("Boundary condition for y_{min}"),"QComboBoxLang",defaults=[["neumann",_("Neumann (==0)")],["interpolate",_("Interpolate")],["constant",_("Constant")]])
	lib['electrical_y1_boundry']=my_data("au",_("Boundary condition for y_{max}"),"QComboBoxLang",defaults=[["neumann",_("Neumann (==0)")],["interpolate",_("Interpolate")],["constant",_("Constant")]])
	lib['electrical_x0_boundry']=my_data("au",_("Boundary condition for x_{min}"),"QComboBoxLang",defaults=[["neumann",_("Neumann (==0)")],["interpolate",_("Interpolate")],["constant",_("Constant")]])
	lib['electrical_x1_boundry']=my_data("au",_("Boundary condition for x_{max}"),"QComboBoxLang",defaults=[["neumann",_("Neumann (==0)")],["interpolate",_("Interpolate")],["constant",_("Constant")]])

	lib['electrical_y0']=my_data("V",_("Boundary value for y_{min}"),"QLineEdit",hide_on_token_eq=[["electrical_y0_boundry", "neumann"],["electrical_y0_boundry", "interpolate"]])
	lib['electrical_y1']=my_data("V",_("Boundary value for y_{max}"),"QLineEdit",hide_on_token_eq=[["electrical_y1_boundry", "neumann"],["electrical_y1_boundry", "interpolate"]])

	lib['electrical_x0']=my_data("V",_("Boundary value for x_{min}"),"QLineEdit",hide_on_token_eq=[["electrical_x0_boundry", "neumann"],["electrical_x0_boundry", "interpolate"]])
	lib['electrical_x1']=my_data("V",_("Boundary value for x_{max}"),"QLineEdit",hide_on_token_eq=[["electrical_x1_boundry", "neumann"],["electrical_x1_boundry", "interpolate"]])

	lib['thermal_couple_to_electrical_solver']=my_data(_("True/False"),_("Couple to electrical solver"),"gtkswitch")


	#dump.inp
	lib['dump_slices']=my_data(_("True/False"),_("Dump slices"),"gtkswitch")
	lib['dump_dynamic']=my_data(_("True/False"),_("Dump dynamic"),"gtkswitch")
	lib['dump_write_out_band_structure']=my_data(_("True/False"),_("Write out band structure"),"gtkswitch")
	lib['dump_write_converge']=my_data(_("True/False"),_("Write newton solver convergence to disk"),"gtkswitch")
	lib['dump_print_pos_error']=my_data(_("True/False"),_("Print poisson solver convergence"),"gtkswitch")
	lib['dump_norm_time_to_one']=my_data(_("True/False"),_("Normalize output x-time to one"),"gtkswitch")
	lib['dump_built_in_voltage']=my_data(_("True/False"),_("Dump the built in voltage."),"gtkswitch")
	lib['dump_optical_probe_spectrum']=my_data(_("True/False"),_("Dump optical probe spectrum"),"gtkswitch")
	lib['dump_file_access_log']=my_data(_("True/False"),_("Write file access log to disk."),"gtkswitch")
	lib['dump_write_headers']=my_data(_("True/False"),_("Write headers to output files"),"gtkswitch")
	lib['dump_first_guess']=my_data(_("True/False"),_("Write first guess to equations"),"gtkswitch")
	lib['dump_log_level']=my_data("au",_("Log verbocity"),"QComboBoxLang",defaults=[[("none"),_("None")],["screen",_("Screen")],["disk",_("Disk")],["screen_and_disk",_("Screen and disk")]])
	lib['dump_log_level']=my_data("au",_("Log verbocity"),"QComboBoxLang",defaults=[[("none"),_("None")],["screen",_("Screen")],["disk",_("Disk")],["screen_and_disk",_("Screen and disk")]])
	lib['dump_dynamic_pl_energy']=my_data(_("True/False"),_("PL dump Energy"),"gtkswitch")
	lib['dump_remove_dos_cache']=my_data(_("True/False"),_("Clean up DoS cache files"),"gtkswitch")
	lib['dump_binary']=my_data(_("True/False"),_("Write binary data where possible"),"gtkswitch")

	#probe
	lib['probe_enabled']=my_data(_("True/False"),_("Probe enabled"),"gtkswitch")
	lib['probe_type']=my_data("m^{-3}",_("Probe type"),"g_probe_type")

	#pl_ss?.inp
	lib['pl_mode']=my_data("au",_("Device state"),"QComboBoxLang",defaults=[[("voc"),_("Voc")],["Jsc",_("Jsc")]])

	#ray

	lib['text_ray_run_control_']=my_data("",_("<b>Run control</b>"),"QLabel")
	lib['text_ray_solver_control_']=my_data("",_("<b>Solver control</b>"),"QLabel")
	lib['text_ray_output_']=my_data("",_("<b>Output</b>"),"QLabel")
	lib['ray_dump_abs_profile']=my_data(_("True/False"),_("Dump absorption profile"),"gtkswitch")
	lib['ray_auto_run']=my_data("au",_("Run the ray tracer"),"QComboBoxLang",defaults=[[("ray_run_never"),_("Never")],["ray_run_once",_("Once per simulation")],["ray_run_step",_("Each simulation step")],["ray_run_step_n",_("Every nth simulation step")]])
	lib['ray_auto_run_n']=my_data("au",_("Each n steps"),"QLineEdit",show_on_token_eq=[["ray_auto_run","ray_run_step_n"]])
	lib['ray_theta_steps']=my_data("au",_("Theta steps"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"],["pl_emission_enabled",True]])
	lib['ray_theta_start']=my_data("Degrees",_("Theta start"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"],["pl_emission_enabled",True]])
	lib['ray_theta_stop']=my_data("Degrees",_("Theta stop"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"],["pl_emission_enabled",True]])

	lib['ray_phi_steps']=my_data("au",_("Phi steps"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"],["pl_emission_enabled",True]])
	lib['ray_phi_start']=my_data("Degrees",_("Phi start"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"],["pl_emission_enabled",True]])
	lib['ray_phi_stop']=my_data("Degrees",_("Phi stop"),"QLineEdit",show_on_token_eq=[["light_illuminate_from","xyz"],["pl_emission_enabled",True]])

	lib['ray_escape_bins']=my_data("au",_("Escape bins"),"QLineEdit")

	lib['ray_auto_wavelength_range']=my_data(_("True/False"),_("Automatic wavelength range"),"gtkswitch")
	
	lib['ray_emission_source']=my_data("au",_("Emit from"),"QComboBoxLang",defaults=[["ray_emission_single_point",_("Center of each layer")],[("ray_emission_electrical_mesh"),_("Each electrical mesh point")],["ray_emission_every_x_point",_("Center of y slice")]],hide_on_token_eq=[["pl_emission_enabled",False]])
	lib['ray_super_sample_x']=my_data("au",_("Super sample x"),"gtkswitch",show_on_token_eq=[["ray_emission_source","ray_emission_every_x_point"]])
	lib['ray_super_sample_x_points']=my_data("au",_("Super sample x points"),"QLineEdit", show_on_token_eq=[["ray_super_sample_x",True]])

	lib['text_ray_tracing']=my_data("au",_("<b>Ray tracing</b>"),"QLabel")

	lib['ray_min_intensity']=my_data("au",_("Minimum ray intensity"),"QLineEdit")
	lib['ray_max_bounce']=my_data("au",_("Maximum number of bounces"),"QLineEdit")

	lib['ray_sim_transmitted']=my_data(_("True/False"),_("Simulate transmitted rays"),"gtkswitch")
	lib['ray_sim_reflected']=my_data(_("True/False"),_("Simulate reflected rays"),"gtkswitch")

	#viewpoint.inp
	lib['viewpoint_nx']=my_data("au",_("Mesh points x"),"QLineEdit")
	lib['viewpoint_nz']=my_data("au",_("Mesh points z"),"QLineEdit")

	lib['text_detector']=my_data("au",_("<b>Detector</b>"),"QLabel")

	#led.inp
	lib['led_extract_eff']=my_data("0.0-1.0",_("LED extraction efficiency"),"QLineEdit")

	#device.inp
	#lib['invert_applied_bias']=my_data("au",_("Invert applied bias"),"gtkswitch")
	#lib['lcharge']=my_data("m^{-3}",_("Charge on left contact"),"QLineEdit")
	#lib['rcharge']=my_data("m^{-3}",_("Charge on right contact"),"QLineEdit")

	#parasitic.inp
	lib['Rshunt']=my_data("Ohms m^{2}",_("Shunt resistance"),"QLineEdit",min=1e-3,max=1e6)
	lib['Rcontact']=my_data("Ohms",_("Series resistance"),"QLineEdit",min=1.0,max=200)
	lib['otherlayers']=my_data("m",_("Other layers"),"QLineEdit")
	lib['test_param']=my_data("m",_("debug (ignore)"),"QLineEdit",hidden=True)

	#contacts.inp
	lib['np']=my_data("m^{-3}",_("Contact charge density"),"energy_to_charge")
	lib['position']=my_data("au",_("Contact position"),"QComboBoxLang",defaults=[[("top"),_("top")],[("bottom"),_("bottom")],[("right"),_("right")],[("left"),_("left")]])
	lib['applied_voltage']=my_data("m^{-3}",_("Applied voltage"),"g_applied_voltage")
	lib['charge_type']=my_data("au",_("Charge type"),"QComboBoxLang",defaults=[[("electron"),_("Electron")],[("hole"),_("Hole")]])
	lib['physical_model']=my_data("au",_("Physical model"),"QComboBoxLang",defaults=[[("ohmic"),_("Ohmic")],[("schottky"),_("Schottky")]])


	#mesh?.inp
	lib['remesh_x']=my_data("au",_("Automatic remesh x"),"gtkswitch")
	lib['remesh_y']=my_data("au",_("Automatic remesh y"),"gtkswitch")
	lib['remesh_z']=my_data("au",_("Automatic remesh z"),"gtkswitch")
	lib['left_right']=my_data("au",_("Left/Right"),"QComboBoxLang",defaults=[[("left"),_("Left")],[("right"),_("Right")]])

	#pl?.inp
	lib['pl_fe_fh']=my_data("0.0-1.0",_("n_{free} to p_{free} photon generation efficiency"),"QLineEdit",hide_on_token_eq=[["pl_use_experimental_emission_spectra",True],["pl_emission_enabled",False]])
	lib['pl_fe_te']=my_data("0.0-1.0",_("n_{free} to n_{trap} photon generation efficiency"),"QLineEdit",hide_on_token_eq=[["pl_use_experimental_emission_spectra",True],["pl_emission_enabled",False]])
	lib['pl_te_fh']=my_data("0.0-1.0",_("n_{trap} to p_{free} photon generation efficiency"),"QLineEdit",hide_on_token_eq=[["pl_use_experimental_emission_spectra",True],["pl_emission_enabled",False]])
	lib['pl_th_fe']=my_data("0.0-1.0",_("p_{trap} to n_{free} photon generation efficiency"),"QLineEdit",hide_on_token_eq=[["pl_use_experimental_emission_spectra",True],["pl_emission_enabled",False]])
	lib['pl_fh_th']=my_data("0.0-1.0",_("p_{free} to p_{trap} photon generation efficiency"),"QLineEdit",hide_on_token_eq=[["pl_use_experimental_emission_spectra",True],["pl_emission_enabled",False]])
	lib['pl_input_spectrum']=my_data(_("Edit"),_("Experimental emission spectra"),"g_select_material" ,units_widget="QPushButton", hide_on_token_eq=[["pl_emission_enabled",False],["pl_use_experimental_emission_spectra",False]])
	lib['icon']=my_data(_("Icon"),_("Edit"),"icon_widget" ,units_widget="QPushButton")
	lib['pl_experimental_emission_efficiency']=my_data("0.0-1.0",_("Experimental emission efficiency"),"QLineEdit", hide_on_token_eq=[["pl_emission_enabled",False],["pl_use_experimental_emission_spectra",False]])

#pl_experimental_emission_efficiency

	lib['pl_use_experimental_emission_spectra']=my_data(_("True/False"),_("Use experimental emission spectra"),"gtkswitch",hide_on_token_eq=[["pl_emission_enabled",False]])

	#fxdomain?.inp
	lib['is_Vexternal']=my_data("Volts",_("V_{external}"),"QLineEdit",hide_on_token_eq=[["load_type","open_circuit"]])
	lib['fxdomain_Rload']=my_data("Ohms",_("Load resistor"),"QLineEdit",hide_on_token_eq=[["load_type","open_circuit"]])
	lib['fxdomain_points']=my_data("au",_("fx domain mesh points"),"QLineEdit",hide_on_token_eq=[["fxdomain_large_signal","small_signal"]])
	lib['fxdomain_n']=my_data("au",_("Cycles to simulate"),"QLineEdit",hide_on_token_eq=[["fxdomain_large_signal","small_signal"]])
	lib['fxdomain_voltage_modulation_max']=my_data("V",_("Voltage modulation depth"),"QLineEdit",hide_on_token_eq=[["fx_modulation_type","optical"],["fxdomain_large_signal","small_signal"]])

	lib['fx_modulation_type']=my_data("au",_("Excite with"),"QComboBoxLang",defaults=[[("voltage"),_("Voltage")],[("optical"),_("Light")]])
	lib['fxdomain_measure']=my_data("au",_("Measure"),"QComboBoxLang",defaults=[[("measure_voltage"),_("Voltage")],[("measure_current"),_("Current")]])
	lib['fxdomain_light_modulation_depth']=my_data("au",_("Light modulation depth"),"QLineEdit",hide_on_token_eq=[["fx_modulation_type","voltage"]])

	lib['fxdomain_do_fit']=my_data("au",_("Run fit after simulation"),"gtkswitch",hide_on_token_eq=[["fxdomain_large_signal","small_signal"],["fxdomain_large_signal","fourier"]])
	lib['periods_to_fit']=my_data("au",_("Periods to fit"),"QLineEdit",hide_on_token_eq=[["fxdomain_large_signal","small_signal"],["fxdomain_large_signal","fourier"]])

	lib['fxdomain_norm_tx_function']=my_data("au",_("Normalize transfer functon by light intensity"),"gtkswitch",hide_on_token_eq=[["fx_modulation_type","voltage"]])

	lib['fxdomain_r']=my_data("",_("Re(i)"),"QLineEdit")
	lib['fxdomain_i']=my_data("V",_("Im(i)"),"QLineEdit")
	lib['fxdomain_Jr']=my_data("Am^{-2}",_("Re(J)"),"QLineEdit")
	lib['fxdomain_Ji']=my_data("Am^{-2}",_("Im(J)"),"QLineEdit")
	lib['fxdomain_fx']=my_data("Hz",_("fx"),"QLineEdit")
	lib['fxdomain_delta_i']=my_data("s",_("di"),"QLineEdit")
	lib['fxdomain_delta_g']=my_data("s",_("dmodulation"),"QLineEdit")
	lib['fxdomain_delta_phase']=my_data("rads",_("dphase"),"QLineEdit")
	lib['fxdomain_large_signal']=my_data("au",_("Simulation type"),"QComboBoxLang",defaults=[[("large_signal"),_("Large signal")],[("fourier"),_("Fourier")]])


 
	#node_list.inp
	lib['node_list']=my_data("au",_("Node list"),"QChangeLog")

	#crypto.inp
	lib['iv']=my_data("au",_("Initialization vector"),"QLineEdit")
	lib['key']=my_data("au",_("Cryptographic key"),"QLineEdit")

	#fit.inp
	lib['simplexmul']=my_data("au","simplex mull","QLineEdit")
	lib['simplex_reset']=my_data("au","Reset steps","QLineEdit")
	lib['dummy_var0']=my_data("au","Dummy var 0","QLineEdit")
	lib['dummy_var1']=my_data("au","Dummy var 1","QLineEdit")
	lib['dummy_var2']=my_data("au","Dummy var 2","QLineEdit")
	lib['dummy_var3']=my_data("au","Dummy var 3","QLineEdit")
	lib['dummy_var4']=my_data("au","Dummy var 4","QLineEdit")
	lib['dummy_var5']=my_data("au","Dummy var 5","QLineEdit")
	lib['dummy_var6']=my_data("au","Dummy var 6","QLineEdit")
	lib['dummy_var7']=my_data("au","Dummy var 7","QLineEdit")

	#
	lib['Psun']=my_data("Sun",_("Intensity of the sun"),"QLineEdit",hidden=True)

	lib['saturation_n0']=my_data("#saturation_n0",_("#saturation_n0"),"QLineEdit")
	lib['saturation_rate']=my_data("#saturation_rate",_("#saturation_rate"),"QLineEdit")
	lib['imps_saturate']=my_data("#imps_saturate",_("#imps_saturate"),"QLineEdit")


	lib['simplephotondensity']=my_data("m^{-2}s^{-1}",_("Photon density"),"QLineEdit")
	lib['simple_alpha']=my_data("m^{-1}",_("Absorption of material"),"QLineEdit")
	lib['simmode']=my_data("au",_("#simmode"),"QLineEdit")

	lib['function']=my_data("au",_("#function"),"QLineEdit")
	lib['Vexternal']=my_data("V",_("start voltage"),"QLineEdit")
	lib['Vmax']=my_data("V",_("Max voltage"),"QLineEdit")
	lib['invert_current']=my_data(_("True/False"),_("Invert output"),"QLineEdit")


	lib['use_capacitor']=my_data("1/0",_("Use capacitor"),"QComboBox",defaults=["1","0"])


	#
	lib['Rshort_imps']=my_data("Ohms",_("R_{short}"),"QLineEdit")
	lib['imps_sun']=my_data("1=1 Sun",_("Backgroud light bias"),"QLineEdit")
	lib['imps_modulation_max']=my_data("1=1 Sun",_("Modulation depth"),"QLineEdit")
	lib['imps_modulation_fx']=my_data("Hz",_("Modulation frequency"),"QLineEdit")
	lib['high_sun_scale']=my_data("au",_("High light multiplyer"),"QLineEdit")



	lib['imps_r']=my_data("Amps",_("Re(i)"),"QLineEdit")
	lib['imps_i']=my_data("Amps",_("Im(i)"),"QLineEdit")
	lib['imps_Jr']=my_data("Amps $m^{-2}$",_("Re(J)"),"QLineEdit")
	lib['imps_Ji']=my_data("Amps $m^{-2}$",_("Im(J)"),"QLineEdit")
	lib['imps_fx']=my_data("Hz",_("Frequency"),"QLineEdit")
	lib['imps_delta_i']=my_data("s",_("Phase shift"),"QLineEdit")
	lib['imps_delta_g']=my_data("s",_("Phase shift"),"QLineEdit")
	lib['imps_delta_phase']=my_data("s",_("Phase shift"),"QLineEdit")
	lib['imps_points']=my_data("s",_("points"),"QLineEdit")
	lib['imps_n']=my_data("s",_("Wavelengths to simulate"),"QLineEdit")
	lib['imps_Vexternal']=my_data("Volts",_("External voltage"),"QLineEdit")

	lib['Cext']=my_data("C",_("External C"),"QLineEdit")
	lib['Rext']=my_data("Ohms",_("External R"),"QLineEdit")

	lib['Rscope']=my_data("Ohms",_("Resistance of scope"),"QLineEdit")

	#suns_voc
	lib['sun_voc_single_point']=my_data("True/False",_("Single point"),"gtkswitch")
	lib['sun_voc_Psun_start']=my_data("Suns",_("Start intensity"),"QLineEdit")
	lib['sun_voc_Psun_stop']=my_data("Suns",_("Stop intensity"),"QLineEdit")
	lib['sun_voc_Psun_mul']=my_data("au",_("step multiplier"),"QLineEdit")

	#suns_jsc
	lib['sunstart']=my_data("Suns",_("Start intensity"), "QLineEdit")
	lib['sunstop']=my_data("Suns",_("Stop intensity"), "QLineEdit")
	lib['sundp']=my_data("au",_("Step"), "QLineEdit")
	lib['sundpmul']=my_data("au",_("step multiplier"), "QLineEdit")

	lib['simplephotondensity']=my_data("m^{-2}s^{-1}",_("Photon Flux"),"QLineEdit")
	lib['simple_alpha']=my_data("m^{-1}",_("Absorption"),"QLineEdit")
	lib['xlen']=my_data("m",_("device width"),"QLineEdit")
	lib['zlen']=my_data("m",_("device breadth"),"QLineEdit")

	lib['voc_J_to_Jr']=my_data("au","Ratio of conduction current to recombination current","QLineEdit")

	lib['voc_i']=my_data("au",_("Current"),"QLineEdit")



	lib['max_nfree_to_ptrap']=my_data("m^{-3}s^{-1}","nfree_to_ptrap","QLineEdit")
	lib['max_pfree_to_ntrap']=my_data("m^{-3}s^{-1}","max_pfree_to_ntrap","QLineEdit")
	lib['max_nrelax']=my_data("m^{-3}s^{-1}","max_nrelax","QLineEdit")
	lib['max_prelax']=my_data("m^{-3}s^{-1}","max_prelax","QLineEdit")

	lib['max_nfree']=my_data("m^{-3}","max_nfree","QLineEdit")
	lib['max_pfree']=my_data("m^{-3}","max_pfree","QLineEdit")
	lib['max_ntrap']=my_data("m^{-3}","max_ntrap","QLineEdit")
	lib['max_ptrap']=my_data("m^{-3}","max_ptrap","QLineEdit")
	lib['alpha_max_reduction']=my_data("m^{-1}","alpha_max_reduction","QLineEdit")
	lib['alpha_max_increase']=my_data("m^{-1}","alpha_max_increase","QLineEdit")

	lib['srh_n_r1']=my_data("m^{-3}s^{-1}","srh electron rate 1","QLineEdit")
	lib['srh_n_r2']=my_data("m^{-3}s^{-1}","srh electron rate 2","QLineEdit")
	lib['srh_n_r3']=my_data("m^{-3}s^{-1}","srh electron rate 3","QLineEdit")
	lib['srh_n_r4']=my_data("m^{-3}s^{-1}","srh electron rate 4","QLineEdit")

	lib['srh_p_r1']=my_data("m^{-3}s^{-1}","srh hole rate 1","QLineEdit")
	lib['srh_p_r2']=my_data("m^{-3}s^{-1}","srh hole rate 2","QLineEdit")
	lib['srh_p_r3']=my_data("m^{-3}s^{-1}","srh hole rate 3","QLineEdit")
	lib['srh_p_r4']=my_data("m^{-3}s^{-1}","srh hole rate 4","QLineEdit")

	lib['band_bend_max']=my_data("percent","band bend max","QLineEdit")

	#ce
	lib['ce_start_sun']=my_data(_("au"),_("Start light intensity"),"QLineEdit")
	lib['ce_stop_sun']=my_data(_("au"),_("Stop light intensity"),"QLineEdit")
	lib['ce_number_of_simulations']=my_data(_("au"),_("Numer of steps"),"QLineEdit")
	lib['ce_on_time']=my_data(_("au"),_("CE light on time"),"QLineEdit")
	lib['ce_off_time']=my_data(_("au"),_("CE light off time"),"QLineEdit")


	#world
	lib['world_automatic_size']=my_data(_("True/False"),_("Automatic world size"),"gtkswitch")
	lib['world_fills_mesh']=my_data(_("True/False"),_("World fills mesh"),"gtkswitch")
	lib['world_x0']=my_data("m",_("x0"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",True]])
	lib['world_x1']=my_data("m",_("x1"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",True]])
	lib['world_y0']=my_data("m",_("y0"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",True]])
	lib['world_y1']=my_data("m",_("y1"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",True]])
	lib['world_z0']=my_data("m",_("z0"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",True]])
	lib['world_z1']=my_data("m",_("z1"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",True]])
	lib['world_margin_x0']=my_data("decimal",_("margin x0"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",False]])
	lib['world_margin_x1']=my_data("decimal",_("margin x1"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",False]])
	lib['world_margin_y0']=my_data("decimal",_("margin y0"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",False]])
	lib['world_margin_y1']=my_data("decimal",_("margin y1"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",False]])
	lib['world_margin_z0']=my_data("decimal",_("margin z0"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",False]])
	lib['world_margin_z1']=my_data("decimal",_("margin z1"),"QLineEdit",hide_on_token_eq=[["world_automatic_size",False]])

	#
	lib['layer0']=my_data("m",_("Active layer width"),"QLineEdit")
	lib['stark_saturate']=my_data("au","Stark saturate","QLineEdit")

	lib['n_mul']=my_data("au","n mul","QLineEdit")
	lib['alpha_mul']=my_data("m^{-1}","Alpha mul","QLineEdit")


	#time_mesh_config*.inp
	lib['time_loop_times']=my_data("au","Times to repeat","QLineEdit")
	lib['time_loop_reset_time']=my_data("au",_("Reset time to zero each cycle"),"gtkswitch")

	#fdtd.inp
	lib['use_gpu']=my_data("au",_("OpenCL GPU acceleration"),"gtkswitch")
	lib['gpu_name']=my_data("au",_("GPU name"),"QComboBoxOpenCL")
	lib['text_excitation']=my_data("",_("<b>Excitation type</b>"),"QLabel")
	lib['fdtd_excitation_type']=my_data("au",_("FDTD Slice"),"QComboBoxLang",defaults=[["fdtd_sin",_("Sin")],["fdtd_pulse",_("Pulse")]])
	lib['fdtd_lambda_start']=my_data("m",_("Start wavelength"),"QLineEdit",show_on_token_eq=[["fdtd_excitation_type","fdtd_sin"]])
	lib['fdtd_lambda_stop']=my_data("m",_("Stop wavelength"),"QLineEdit",show_on_token_eq=[["fdtd_excitation_type","fdtd_sin"]])
	lib['fdtd_lambda_points']=my_data("m",_("Wavelength steps"),"QLineEdit",show_on_token_eq=[["fdtd_excitation_type","fdtd_sin"]])
	lib['fdtd_pulse_length']=my_data("steps",_("Pulse length"),"QLineEdit",show_on_token_eq=[["fdtd_excitation_type","fdtd_pulse"]])
	lib['fdtd_excite_Ex']=my_data("steps",_("Excite Ex"),"gtkswitch")
	lib['fdtd_excite_Ey']=my_data("steps",_("Excite Ey"),"gtkswitch")
	lib['fdtd_excite_Ez']=my_data("steps",_("Excite Ez"),"gtkswitch")


	lib['text_fdtd_mesh']=my_data("",_("<b>FDTD mesh</b>"),"QLabel")
	lib['fdtd_xzy']=my_data("au",_("FDTD Slice"),"QComboBoxLang",defaults=[["zy",_("zy")],["zx",_("zx")],["xy",_("xy")]])
	lib['fdtd_zlen']=my_data("m",_("Mesh points z"),"QLineEdit",hide_on_token_eq=[["fdtd_xzy","xy"]])
	lib['fdtd_xlen']=my_data("m",_("Mesh points x"),"QLineEdit",hide_on_token_eq=[["fdtd_xzy","zy"]])
	lib['fdtd_ylen']=my_data("m",_("Mesh points y"),"QLineEdit",hide_on_token_eq=[["fdtd_xzy","zx"]])
	lib['fdtd_use_gnuplot']=my_data("au",_("Use gnuplot to visualize"),"gtkswitch")

	lib['text_fdtd_time']=my_data("",_("<b>Simulation time</b>"),"QLabel")
	lib['fdtd_max_time']=my_data("s",_("Stop time"),"QLineEdit")
	lib['fdtd_max_steps']=my_data("m",_("Max steps"),"QLineEdit")

	#any files
	lib['dump_verbosity']=my_data("au",_("Output verbosity to disk"),"QComboBoxLang",defaults=[["-1",_("Nothing")],["0",_("Key results")],[("1"),_("Write everything to disk")],[("2"),_("Write everything to disk every 2nd step")],[("5"),_("Write everything to disk every 5th step")],[("10"),_("Write everything to disk every 10th step")]])
	lib['dump_screen_verbosity']=my_data( "au", _("Output verbosity to screen"),"QComboBoxLang",defaults=[[("dump_verbosity_everything"),_("Show lots")],["dump_verbosity_key_results",_("Show key results")]])

	lib['solver_verbosity']=my_data( "au", _("Solver output verbosity"),"QComboBoxLang",defaults=[[("solver_verbosity_nothing"),_("Nothing")],["solver_verbosity_at_end",_("As answers are found")],["solver_verbosity_every_step",_("Each step")]])

	#circuit diagram
	lib['name0']=my_data("name",_("Name"),"QLineEdit")
	lib['com_R']=my_data("Ohms",_("Resistor"),"QLineEdit")
	lib['com_C']=my_data("F",_("Capacitor"),"QLineEdit")
	lib['com_L']=my_data("H",_("Inductance"),"QLineEdit")
	lib['com_I0']=my_data("Apms",_("I0"),"QLineEdit")
	lib['com_a']=my_data("V",_("V_{0}"),"QLineEdit")
	lib['com_b']=my_data("V",_("d"),"QLineEdit")
	lib['com_c']=my_data("au",_("m"),"QLineEdit")
	lib['com_nid']=my_data("(a.u.)",_("Ideality factor"),"QLineEdit")
	lib['com_layer']=my_data("(a.u.)",_("Layer"),"QComboBoxLayers")
	lib['comp']=my_data( "au", _("Component"),"QComboBoxLang",defaults=[[("diode"),_("Diode")],[("capacitor"),_("Capacitor")],[("wire"),_("Wire")],[("resistor"),_("Resistor")],[("vsource"),_("Source")],[("ground"),_("Ground")],[("bat"),_("Voltage source")],[("pointer"),_("Pointer")],[("power"),_("Power law")]])

	#gl
	lib['xRot']=my_data("Deg",_("x rotation"),"QLineEdit")
	lib['yRot']=my_data("Deg",_("y rotation"),"QLineEdit")
	lib['zRot']=my_data("Deg",_("z rotation"),"QLineEdit")
	lib['x_pos']=my_data("au",_("x pos"),"QLineEdit")
	lib['y_pos']=my_data("au",_("y pos"),"QLineEdit")
	lib['zoom']=my_data("au",_("zoom"),"QLineEdit")

def build_token_lib_r():
	global lib
	global lib_r
	global lib_json
	for item in lib:
		c=lib[item]
		c.token=item
		lib_r[c.info]=item

		end_token=item.split('.')[-1]
		lib_json[end_token]=item

class tokens:

	def __init__(self):
		global lib
		if len(lib)==0:
			build_token_lib()
			build_token_lib_r()

	def find(self,token):
		global lib
		search_token=token.strip()
		if search_token in lib:
			ret=lib[search_token]
			return ret 
		else:
			return False

		return False

	def find_json(self,token):
		global lib
		global lib_json
		search_token=token.strip()

		if search_token in lib_json:
			token=lib_json[search_token]
			ret=lib[token]
			return ret
		else:
			return False

		return False

	def reverse_lookup(self,english):
		global lib
		global lib_r

		english=english.strip()
		if english in lib_r:
			token=lib_r[english]
			return lib[token]
		else:
			return False

		return False

			

