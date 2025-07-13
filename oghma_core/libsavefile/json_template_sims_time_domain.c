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

int json_template_sims_time_domain(struct json_obj *obj_sims)
{
	struct json_obj *obj_jv;
	struct json_obj *obj_template;
	struct json_obj *obj_config;
	struct json_obj *obj_mesh;
	struct json_obj *obj_template_mesh;
	struct json_obj *text;

	obj_jv=json_obj_add(obj_sims,"time_domain","",JSON_NODE);
	json_obj_add(obj_jv,"icon_","celiv",JSON_STRING);

	obj_template=json_obj_add(obj_jv,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","celiv",JSON_STRING);
	json_obj_add(obj_template,"icon","celiv",JSON_STRING);
	obj_config=json_obj_add(obj_template,"config","",JSON_NODE);
	obj_mesh=json_obj_add(obj_template,"mesh","",JSON_NODE);
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	//config
		json_obj_add(obj_config,"pulse_shift","5e-6",JSON_DOUBLE);
		json_obj_add(obj_config,"load_type","load",JSON_STRING);
		json_obj_add(obj_config,"pulse_L","0.0",JSON_DOUBLE);
		json_obj_add(obj_config,"Rload","0.0",JSON_DOUBLE);
		json_obj_add(obj_config,"pump_laser","green",JSON_STRING);
		json_obj_add(obj_config,"pulse_bias","0.0",JSON_DOUBLE);
		json_obj_add(obj_config,"pulse_subtract_dc","false",JSON_BOOL);
		json_obj_add(obj_config,"start_time","-4e-12",JSON_DOUBLE);
		json_obj_add(obj_config,"fs_laser_time","-1.0",JSON_DOUBLE);

	//dump
		text=json_obj_add(obj_config,"text_output_","",JSON_INT);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_config,"dump_verbosity","1",JSON_INT);
		json_obj_add(obj_config,"dump_energy_space","false",JSON_BOOL);
		json_obj_add(obj_config,"dump_x","0",JSON_INT);
		json_obj_add(obj_config,"dump_y","0",JSON_INT);
		json_obj_add(obj_config,"dump_z","0",JSON_INT);
		json_obj_add(obj_config,"dump_sweep_save","none",JSON_STRING);

	//Generation model
		text=json_obj_add(obj_config,"text_generation_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_config,"charge_carrier_generation_model","transfer_matrix",JSON_STRING);
		json_obj_add(obj_config,"pulse_light_efficiency","1.0",JSON_DOUBLE);

	//mesh
	json_obj_add(obj_mesh,"time_loop","false",JSON_BOOL);
	json_obj_add(obj_mesh,"time_loop_times","4",JSON_INT);
	json_obj_add(obj_mesh,"time_loop_reset_time","false",JSON_BOOL);
	obj_template_mesh=json_obj_add(obj_mesh,"template","",JSON_TEMPLATE);

	json_obj_add(obj_template_mesh,"len","10e-6",JSON_DOUBLE);
	json_obj_add(obj_template_mesh,"dt","0.01e-6",JSON_DOUBLE);
	json_obj_add(obj_template_mesh,"voltage_start","0.0",JSON_DOUBLE);
	json_obj_add(obj_template_mesh,"voltage_stop","0.0",JSON_DOUBLE);
	json_obj_add(obj_template_mesh,"mul","1.0",JSON_DOUBLE);
	json_obj_add(obj_template_mesh,"sun_start","0.0",JSON_DOUBLE);
	json_obj_add(obj_template_mesh,"sun_stop","0.0",JSON_DOUBLE);
	json_obj_add(obj_template_mesh,"laser_start","0.0",JSON_DOUBLE);
	json_obj_add(obj_template_mesh,"laser_stop","0.0",JSON_DOUBLE);

	return 0;
}
