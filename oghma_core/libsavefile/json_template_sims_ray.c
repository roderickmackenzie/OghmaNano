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

int json_template_sims_ray(struct json_obj *obj_sims)
{
	struct json_obj *obj_ray;
	struct json_obj *obj_template;
	struct json_obj *obj_template_config;
	struct json_obj *text;

	obj_ray=json_obj_add(obj_sims,"ray","",JSON_NODE);
	json_obj_add(obj_ray,"icon_","ray",JSON_STRING);

	obj_template=json_obj_add(obj_ray,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","Ray\ntrace",JSON_STRING);
	json_obj_add(obj_template,"icon","ray",JSON_STRING);
	obj_template_config=json_obj_add(obj_template,"config","",JSON_NODE);
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	text=json_obj_add(obj_template_config,"text_ray_run_control_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_template_config,"ray_auto_run","ray_run_once",JSON_STRING);
	json_obj_add(obj_template_config,"ray_auto_run_n","5",JSON_INT);
	text=json_obj_add(obj_template_config,"text_ray_solver_control_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_template_config,"ray_min_intensity","0.01",JSON_DOUBLE);
	json_obj_add(obj_template_config,"ray_max_bounce","7",JSON_INT);
	json_obj_add(obj_template_config,"ray_sim_reflected","true",JSON_BOOL);
	json_obj_add(obj_template_config,"ray_sim_transmitted","true",JSON_BOOL);
	text=json_obj_add(obj_template_config,"text_ray_output_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_template_config,"ray_dump_abs_profile","false",JSON_BOOL);
	json_obj_add(obj_template_config,"ray_escape_bins","20",JSON_INT);
	json_obj_add(obj_template_config,"dump_verbosity","1",JSON_INT);

	return 0;
}
