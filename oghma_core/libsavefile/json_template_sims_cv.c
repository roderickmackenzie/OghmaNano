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

int json_template_sims_cv(struct json_obj *obj_sims)
{
	struct json_obj *obj_cv;
	struct json_obj *obj_template;
	struct json_obj *obj_template_config;
	struct json_obj *text;

	obj_cv=json_obj_add(obj_sims,"cv","",JSON_NODE);
	json_obj_add(obj_cv,"icon_","cv",JSON_STRING);

	obj_template=json_obj_add(obj_cv,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","CV",JSON_STRING);
	json_obj_add(obj_template,"icon","cv",JSON_STRING);
	obj_template_config=json_obj_add(obj_template,"config","",JSON_NODE);
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	//config
		json_obj_add(obj_template_config,"cv_start_voltage","-2.0",JSON_DOUBLE);
		json_obj_add(obj_template_config,"cv_stop_voltage","0.5",JSON_DOUBLE);
		json_obj_add(obj_template_config,"cv_dv_step","0.1",JSON_DOUBLE);
		json_obj_add(obj_template_config,"cv_fx","1000",JSON_INT);
		json_obj_add(obj_template_config,"load_type","load",JSON_STRING);
		json_obj_add(obj_template_config,"fxdomain_large_signal","true",JSON_BOOL);
		json_obj_add(obj_template_config,"fxdomain_Rload","0.0",JSON_DOUBLE);
		json_obj_add(obj_template_config,"fxdomain_points","30",JSON_INT);
		json_obj_add(obj_template_config,"fxdomain_n","5",JSON_INT);
		json_obj_add(obj_template_config,"fx_modulation_type","voltage",JSON_STRING);
		json_obj_add(obj_template_config,"fxdomain_measure","measure_current",JSON_STRING);
		json_obj_add(obj_template_config,"fxdomain_voltage_modulation_max","0.01",JSON_DOUBLE);
		json_obj_add(obj_template_config,"fxdomain_light_modulation_depth","0.01",JSON_DOUBLE);
		json_obj_add(obj_template_config,"fxdomain_do_fit","true",JSON_BOOL);
		json_obj_add(obj_template_config,"fxdomain_L","0.0",JSON_DOUBLE);
		json_obj_add(obj_template_config,"periods_to_fit","2",JSON_INT);
		json_obj_add(obj_template_config,"fxdomain_modulation_rolloff_enable","false",JSON_BOOL);
		json_obj_add(obj_template_config,"fxdomain_modulation_rolloff_start_fx","1e3",JSON_DOUBLE);
		json_obj_add(obj_template_config,"fxdomain_modulation_rolloff_speed","1.6026e-05",JSON_DOUBLE);
		json_obj_add(obj_template_config,"fxdomain_norm_tx_function","false",JSON_BOOL);

		//Generation model
		text=json_obj_add(obj_template_config,"text_generation_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_template_config,"charge_carrier_generation_model","transfer_matrix",JSON_STRING);

		//output
		text=json_obj_add(obj_template_config,"text_output_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_template_config,"dump_verbosity","0",JSON_INT);
		json_obj_add(obj_template_config,"dump_screen_verbosity","dump_verbosity_key_results",JSON_STRING);
		json_obj_add(obj_template_config,"dump_sweep_save","none",JSON_STRING);

	return 0;
}
