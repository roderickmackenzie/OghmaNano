//
// OghmaNano - Organic and hybrid Material Nano Simulation tool
// Copyright (C) 2008-2022 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
//
// https://www.oghma-nano.com
// 
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense, 
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
// THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
// SOFTWARE.
// 

/** @file sim.c
@brief init sim structure
*/


#include <enabled_libs.h>
#include <json.h>
#include <savefile.h>

int json_shape_heat(struct json_obj *obj)
{
	struct json_obj *obj_heat;
	obj_heat=json_obj_add(obj,"shape_heat","",JSON_NODE);
	json_obj_add(obj_heat,"thermal_kl","1.0",JSON_DOUBLE);
	json_obj_add(obj_heat,"thermal_tau_e","1.0",JSON_DOUBLE);
	json_obj_add(obj_heat,"thermal_tau_h","1.0",JSON_DOUBLE);

	return 0;
}

int json_shape_pl(struct json_obj *obj)
{
	struct json_obj *obj_pl;
	struct json_obj *text;
	obj_pl=json_obj_add(obj,"shape_pl","",JSON_NODE);
	json_obj_add(obj_pl,"pl_emission_enabled","false",JSON_BOOL);
	json_obj_add(obj_pl,"pl_use_experimental_emission_spectra","false",JSON_BOOL);
	json_obj_add(obj_pl,"pl_f2f","true",JSON_BOOL);
	json_obj_add(obj_pl,"pl_f2t","false",JSON_BOOL);
	json_obj_add(obj_pl,"pl_input_spectrum","none",JSON_STRING);
	json_obj_add(obj_pl,"pl_experimental_emission_efficiency","1.0",JSON_DOUBLE);
	json_obj_add(obj_pl,"pl_fe_fh","1.0",JSON_DOUBLE);
	json_obj_add(obj_pl,"pl_fe_te","1.0",JSON_DOUBLE);
	json_obj_add(obj_pl,"pl_te_fh","1.0",JSON_DOUBLE);
	json_obj_add(obj_pl,"pl_th_fe","1.0",JSON_DOUBLE);
	json_obj_add(obj_pl,"pl_fh_th","1.0",JSON_DOUBLE);
	text=json_obj_add(obj_pl,"text_ray_tracing","false",JSON_BOOL);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_pl,"ray_theta_steps","200",JSON_INT);
	json_obj_add(obj_pl,"ray_theta_start","0",JSON_INT);
	json_obj_add(obj_pl,"ray_theta_stop","360",JSON_INT);
	json_obj_add(obj_pl,"ray_phi_steps","5",JSON_INT);
	json_obj_add(obj_pl,"ray_phi_start","0",JSON_INT);
	json_obj_add(obj_pl,"ray_phi_stop","360",JSON_INT);
	json_obj_add(obj_pl,"ray_emission_source","ray_emission_single_point",JSON_STRING);
	json_obj_add(obj_pl,"ray_super_sample_x","false",JSON_BOOL);
	json_obj_add(obj_pl,"ray_super_sample_x_points","4",JSON_INT);

	return 0;
}

int json_shape_electrical(struct json_obj *obj)
{
	struct json_obj *obj_electrical;
	obj_electrical=json_obj_add(obj,"shape_electrical","",JSON_NODE);
	json_obj_add(obj_electrical,"electrical_component","resistance",JSON_STRING);
	json_obj_add(obj_electrical,"electrical_shunt","1e6",JSON_DOUBLE);
	json_obj_add(obj_electrical,"electrical_symmetrical_resistance","symmetric",JSON_STRING);
	json_obj_add(obj_electrical,"electrical_series_z","0.24390",JSON_DOUBLE);
	json_obj_add(obj_electrical,"electrical_series_x","0.24390",JSON_DOUBLE);
	json_obj_add(obj_electrical,"electrical_series_y","1e-8",JSON_DOUBLE);
	json_obj_add(obj_electrical,"electrical_n","1.2",JSON_DOUBLE);
	json_obj_add(obj_electrical,"electrical_J0","0.5e-8",JSON_DOUBLE);
	json_obj_add(obj_electrical,"electrical_enable_generation","false",JSON_BOOL);
	json_obj_add(obj_electrical,"id","",JSON_RANDOM_ID);

	return 0;
}


int json_dos_complex(struct json_obj *obj_dos, char *name)
{
	struct json_obj *obj_dos_complex;
	struct json_obj *obj_template;
	obj_dos_complex=json_obj_add(obj_dos,name,"",JSON_NODE);
	//json_obj_add(obj_dos_complex,"icon_","electrical",JSON_STRING);
	json_obj_add(obj_dos_complex,"id","",JSON_RANDOM_ID);

	obj_template=json_obj_add(obj_dos_complex,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"function","a*exp((E-Ec)/b)",JSON_STRING);
	json_obj_add(obj_template,"function_enable","true",JSON_BOOL);
	json_obj_add(obj_template,"function_a","4e+20",JSON_DOUBLE);
	json_obj_add(obj_template,"function_b","60e-3",JSON_DOUBLE);
	json_obj_add(obj_template,"function_c","0.0",JSON_DOUBLE);

	return 0;
}

int json_shape_dos(struct json_obj *obj, int material_db)
{
	struct json_obj *obj_dos;
	struct json_obj *text;
	struct json_obj *obj_dos_config;
	if (material_db==FALSE)
	{
		obj_dos=json_obj_add(obj,"shape_dos","",JSON_NODE);
	}else
	{
		obj_dos=obj;
	}
	//dos
		//json_obj_add(obj_dos,"icon_","electrical",JSON_STRING);

		//free carrier
		text=json_obj_add(obj_dos,"text_free_carrier_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_dos,"dd_enabled","true",JSON_BOOL);
		json_obj_add(obj_dos,"symmetric_mobility_e","symmetric",JSON_STRING);
		json_obj_add(obj_dos,"mue_z","1e-15",JSON_STRING);
		json_obj_add(obj_dos,"mue_x","1e-15",JSON_STRING);
		json_obj_add(obj_dos,"mue_y","1.0e-05",JSON_STRING);
		json_obj_add(obj_dos,"mue_delta","0.1",JSON_DOUBLE);
		json_obj_add(obj_dos,"symmetric_mobility_h","symmetric",JSON_STRING);
		json_obj_add(obj_dos,"muh_z","1e-15",JSON_STRING);
		json_obj_add(obj_dos,"muh_x","1e-15",JSON_STRING);
		json_obj_add(obj_dos,"muh_y","1.0e-05",JSON_STRING);
		json_obj_add(obj_dos,"muh_delta","0.1",JSON_DOUBLE);
		json_obj_add(obj_dos,"Nc","5e25",JSON_DOUBLE);
		json_obj_add(obj_dos,"Nv","5e25",JSON_DOUBLE);

		if (material_db==FALSE)
		{
			json_obj_add(obj_dos,"free_to_free_recombination","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"f2f_lambda","1.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"dos_free_carrier_stats","mb_equation",JSON_STRING);
		}

		//Non-dynamic srh
		text=json_obj_add(obj_dos,"text_steay_srh_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_dos,"ss_srh_enabled","false",JSON_BOOL);
		json_obj_add(obj_dos,"srh_n1","1e20",JSON_DOUBLE);
		json_obj_add(obj_dos,"srh_p1","1e20",JSON_DOUBLE);
		json_obj_add(obj_dos,"srh_tau_n","1e-15",JSON_DOUBLE);
		json_obj_add(obj_dos,"srh_tau_p","1e-15",JSON_DOUBLE);

		//Dynamic traps
		text=json_obj_add(obj_dos,"text_dynamic_traps_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		if (material_db==FALSE)
		{
			json_obj_add(obj_dos,"dostype","exponential",JSON_STRING);
			json_dos_complex(obj_dos, "complex_lumo");
			json_dos_complex(obj_dos, "complex_homo");
			json_obj_add(obj_dos,"Ntrape","1e20",JSON_DOUBLE);
			json_obj_add(obj_dos,"Ntraph","1e20",JSON_DOUBLE);
			json_obj_add(obj_dos,"Etrape","60e-3",JSON_DOUBLE);
			json_obj_add(obj_dos,"Etraph","60e-3",JSON_DOUBLE);
			json_obj_add(obj_dos,"ion_density","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"ion_mobility","0.0",JSON_DOUBLE);
		}

		if (material_db==FALSE)
		{
			json_obj_add(obj_dos,"doping_start","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"doping_stop","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"Na0","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"Na1","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"Nd0","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"Nd1","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"nstart","-2.5",JSON_DOUBLE);
			json_obj_add(obj_dos,"nstop","1.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"npoints","1000",JSON_DOUBLE);
			json_obj_add(obj_dos,"pstart","-2.5",JSON_DOUBLE);
			json_obj_add(obj_dos,"pstop","1.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"ppoints","1000",JSON_DOUBLE);

			json_obj_add(obj_dos,"srh_stop","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"srh_start","-0.5",JSON_DOUBLE);
			json_obj_add(obj_dos,"srhsigman_e","2.131895e-21",JSON_DOUBLE);
			json_obj_add(obj_dos,"srhsigmap_e","3.142822e-22",JSON_DOUBLE);
			json_obj_add(obj_dos,"srhvth_e","1e5",JSON_DOUBLE);
			json_obj_add(obj_dos,"srhsigman_h","3.142822e-22",JSON_DOUBLE);
			json_obj_add(obj_dos,"srhsigmap_h","2.131895e-21",JSON_DOUBLE);
			json_obj_add(obj_dos,"srhvth_h","1e5",JSON_DOUBLE);
			json_obj_add(obj_dos,"srh_bands","5",JSON_INT);

			json_obj_add(obj_dos,"Esteps","1000",JSON_DOUBLE);
			json_obj_add(obj_dos,"dump_band_structure","0",JSON_INT);


			//Auger
			text=json_obj_add(obj_dos,"text_auger_","",JSON_STRING);
			text->data_flags=JSON_PRIVATE;
			json_obj_add(obj_dos,"dos_enable_auger","false",JSON_BOOL);
			json_obj_add(obj_dos,"dos_auger_Cn","1e-26",JSON_DOUBLE);
			json_obj_add(obj_dos,"dos_auger_Cp","1e-26",JSON_DOUBLE);
		}

		text=json_obj_add(obj_dos,"text_electro_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_dos,"Xi","1.6",JSON_STRING);
		json_obj_add(obj_dos,"Eg","1.2",JSON_STRING);
		json_obj_add(obj_dos,"epsilonr","5.0",JSON_DOUBLE);

		if (material_db==FALSE)
		{
			json_obj_add(obj_dos,"id","",JSON_RANDOM_ID);
		}

		if (material_db==FALSE)
		{
			//Exciton solver
			text=json_obj_add(obj_dos,"text_exciton_","",JSON_STRING);
			text->data_flags=JSON_PRIVATE;
			json_obj_add(obj_dos,"exciton_enabled","false",JSON_BOOL);
			json_obj_add(obj_dos,"exciton_L","1e-08",JSON_DOUBLE);
			json_obj_add(obj_dos,"exciton_tau","1e-10",JSON_DOUBLE);
			json_obj_add(obj_dos,"exciton_kpl","4e9",JSON_DOUBLE);
			json_obj_add(obj_dos,"exciton_kfret","0.0",JSON_DOUBLE);
			json_obj_add(obj_dos,"exciton_alpha","1e-13",JSON_DOUBLE);
			json_obj_add(obj_dos,"exciton_kdis","1e11",JSON_DOUBLE);

			//singlet solver
			text=json_obj_add(obj_dos,"text_singlet_","",JSON_STRING);
			text->data_flags=JSON_PRIVATE;
			json_obj_add(obj_dos,"singlet_enabled","false",JSON_BOOL);
			json_obj_add(obj_dos,"singlet_k_fret","1e10",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_s","8e7",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_isc","2.2e4",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_ss","3.5e-18",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_sp","3.0e-10",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_st","1.9e-16",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_dext","1e10",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_t","6.5e2",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_tp","2.8e-19",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_tt","2.2e-18",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_sd","1e9",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_iscd","2.2e4",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_spd","3.0e-16",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_std","1.9e-16",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_ssd","9.6e-19",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_td","6.6e2",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_ttd","2.4e-21",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_tpd","5.6e-19",JSON_DOUBLE);

			json_obj_add(obj_dos,"singlet_C","0.02",JSON_DOUBLE);

			json_obj_add(obj_dos,"singlet_W","2.6e-2",JSON_DOUBLE);

			json_obj_add(obj_dos,"singlet_k_risc","1e5",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_sigma_em","5e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_sigma_t1tn","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_sigma_np","2e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_a","1e-9",JSON_DOUBLE);

			text=json_obj_add(obj_dos,"text_photon_rate_","",JSON_STRING);
			text->data_flags=JSON_PRIVATE;
			json_obj_add(obj_dos,"singlet_photon_enabled","false",JSON_BOOL);
			json_obj_add(obj_dos,"singlet_beta_sp","1e-4",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_k_cav","1e12",JSON_DOUBLE);
			json_obj_add(obj_dos,"singlet_N_dop","4.2e25",JSON_DOUBLE);

			//singlet_opv solver
			text=json_obj_add(obj_dos,"text_singlet_opv_","",JSON_STRING);
			text->data_flags=JSON_PRIVATE;
			json_obj_add(obj_dos,"singlet_opv_enabled","false",JSON_BOOL);
			json_obj_add(obj_dos,"opv_k_d_s","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_isc","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_risc","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_tta","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_sta","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_ssa","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_alpha","0.25",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_fs","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_dt","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_ft","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_dct","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_isc_ct","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_risc_ct","1e-20",JSON_DOUBLE);
			json_obj_add(obj_dos,"opv_k_f","1e-20",JSON_DOUBLE);

			obj_dos_config=json_obj_add(obj_dos,"config","",JSON_NODE);
			json_obj_add(obj_dos_config,"mu_tdep_enable","false",JSON_BOOL);
			json_obj_add(obj_dos_config,"f2f_lambda_enable","false",JSON_BOOL);
		}
	return 0;
}

int json_shape0(struct json_obj *obj)
{
	struct json_obj *text;
	struct json_obj *obj_display_options;

	json_world_object(obj);

	//optical
		text=json_obj_add(obj,"text_optical_attributes_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;

		json_obj_add(obj,"optical_material","blends/p3htpcbm",JSON_STRING);
		json_obj_add(obj,"Gnp","0.0",JSON_DOUBLE);
		json_obj_add(obj,"optical_thickness","0.0",JSON_DOUBLE);
		json_obj_add(obj,"optical_thickness_u","m",JSON_STRING);
		json_obj_add(obj,"optical_thickness_enabled","false",JSON_BOOL);
		json_obj_add(obj,"Dphotoneff","1.0",JSON_DOUBLE);

	obj_display_options=json_obj_add(obj,"display_options","",JSON_NODE);
	json_obj_add(obj_display_options,"show_solid","true",JSON_BOOL);
	json_obj_add(obj_display_options,"show_mesh","true",JSON_BOOL);
	json_obj_add(obj_display_options,"show_cut_through_x","false",JSON_BOOL);
	json_obj_add(obj_display_options,"show_cut_through_y","false",JSON_BOOL);
	json_obj_add(obj_display_options,"hidden","false",JSON_BOOL);

	text=json_obj_add(obj,"text_electrical_attributes_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
		json_shape_dos(obj,FALSE);

		json_shape_electrical(obj);
		json_obj_add(obj,"bhj","default",JSON_STRING);

	json_shape_pl(obj);
	json_shape_heat(obj);

	

	json_obj_add(obj,"moveable","false",JSON_BOOL);

	return 0;
}

int json_shape(struct json_obj *obj)
{
	struct json_obj *obj_template_shape_inside;
	json_shape0(obj);
	obj_template_shape_inside=json_obj_add(obj,"template","",JSON_TEMPLATE);
	json_shape0(obj_template_shape_inside);
	json_obj_add(obj_template_shape_inside,"segments","0",JSON_INT);
	return 0;
}


int json_get_shape_from_segment_path(struct shape *s, struct json *j, char *path,int n)
{
	char temp[200];
	struct json_obj *json_segment;
	struct json_obj *json_segments;
	json_segments=json_obj_find_by_path(&(j->obj), path);

	sprintf(temp,"segment%d",n);

	json_segment=json_obj_find(json_segments, temp);
	if (json_segment==NULL)
	{
		//printf("json_get_shape_from_segment_path: Object %s not found\n",temp);
		return -1;
	}

	json_populate_shape_from_json_world_object(s, json_segment);

	return 0;
}
