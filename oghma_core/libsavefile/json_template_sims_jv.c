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

int json_template_sims_jv(struct json_obj *obj_sims)
{
	struct json_obj *obj_jv;
	struct json_obj *obj_template;
	struct json_obj *obj_template_config;
	struct json_obj *text;

	obj_jv=json_obj_add(obj_sims,"jv","",JSON_NODE);
	json_obj_add(obj_jv,"icon_","jv",JSON_STRING);

	obj_template=json_obj_add(obj_jv,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","JV\\ncurve",JSON_STRING);
	json_obj_add(obj_template,"icon","jv",JSON_STRING);
	obj_template_config=json_obj_add(obj_template,"config","",JSON_NODE);
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	json_obj_add(obj_template_config,"Vstart","0.0",JSON_DOUBLE);
	json_obj_add(obj_template_config,"Vstop","1.2",JSON_DOUBLE);
	json_obj_add(obj_template_config,"Vstep","0.01",JSON_DOUBLE);
	json_obj_add(obj_template_config,"jv_step_mul","1.00",JSON_DOUBLE);
	json_obj_add(obj_template_config,"jv_use_external_voltage_as_stop","true",JSON_BOOL);
	json_obj_add(obj_template_config,"jv_max_j","1e3",JSON_DOUBLE);
	json_obj_add(obj_template_config,"jv_Rcontact","-1.0",JSON_DOUBLE);
	json_obj_add(obj_template_config,"jv_Rshunt","-1.0",JSON_DOUBLE);
	json_obj_add(obj_template_config,"jv_single_point","false",JSON_BOOL);

	text=json_obj_add(obj_template_config,"text_generation_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_template_config,"jv_light_efficiency","1.0",JSON_DOUBLE);
	json_obj_add(obj_template_config,"charge_carrier_generation_model","transfer_matrix",JSON_STRING);
	json_obj_add(obj_template_config,"eqe_smooth","false",JSON_BOOL);

	text=json_obj_add(obj_template_config,"text_output_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_template_config,"dump_verbosity","1",JSON_INT);
	json_obj_add(obj_template_config,"dump_energy_space","false",JSON_STRING);
	json_obj_add(obj_template_config,"dump_x","0",JSON_INT);
	json_obj_add(obj_template_config,"dump_y","0",JSON_INT);
	json_obj_add(obj_template_config,"dump_z","0",JSON_INT);
	json_obj_add(obj_template_config,"dump_sclc","false",JSON_BOOL);

	json_obj_add(obj_template_config,"dump_sweep_save","none",JSON_STRING);
	//printf("OK!\n");
	//exit(0);

	return 0;
}
