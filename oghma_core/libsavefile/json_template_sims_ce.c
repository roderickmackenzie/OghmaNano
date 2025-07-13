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


int json_template_sims_ce(struct json_obj *obj_sims)
{
	struct json_obj *obj_ce;
	struct json_obj *obj_template;
	struct json_obj *obj_template_config;
	struct json_obj *text;

	obj_ce=json_obj_add(obj_sims,"ce","",JSON_NODE);
	json_obj_add(obj_ce,"icon_","ce",JSON_STRING);

	obj_template=json_obj_add(obj_ce,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","Charge\\nExtraction",JSON_STRING);
	json_obj_add(obj_template,"icon","ce",JSON_STRING);
	obj_template_config=json_obj_add(obj_template,"config","",JSON_NODE);
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	json_obj_add(obj_template_config,"ce_start_sun","0.01",JSON_DOUBLE);
	json_obj_add(obj_template_config,"ce_stop_sun","10.0",JSON_DOUBLE);
	json_obj_add(obj_template_config,"ce_number_of_simulations","10.0",JSON_DOUBLE);
	json_obj_add(obj_template_config,"ce_on_time","1e-6",JSON_DOUBLE);
	json_obj_add(obj_template_config,"ce_off_time","1.0",JSON_DOUBLE);
	json_obj_add(obj_template_config,"load_type","open_circuit",JSON_STRING);

	//dump
	text=json_obj_add(obj_template_config,"text_output_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_template_config,"dump_verbosity","1",JSON_DOUBLE);
	json_obj_add(obj_template_config,"dump_screen_verbosity","dump_verbosity_key_results",JSON_STRING);
	return 0;
}
