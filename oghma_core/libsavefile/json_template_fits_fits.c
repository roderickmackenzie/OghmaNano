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

void json_template_fits_config(struct json_obj *obj_fit_fits)
{
	struct json_obj *obj_fits_config;

	obj_fits_config=json_obj_add(obj_fit_fits,"config","",JSON_NODE);
	json_obj_add(obj_fits_config,"enabled","true",JSON_BOOL);
	json_obj_add(obj_fits_config,"sim_data","jv.csv",JSON_STRING);
	json_obj_add(obj_fits_config,"fit_name","jv_light_0h",JSON_STRING);	//in Jul 2026
	json_obj_add(obj_fits_config,"fit_error_mul","1.0",JSON_DOUBLE);
	json_obj_add(obj_fits_config,"time_shift","0.0",JSON_DOUBLE);
	json_obj_add(obj_fits_config,"fit_shift_y","0.0",JSON_DOUBLE);
	json_obj_add(obj_fits_config,"start","0.0",JSON_DOUBLE);
	json_obj_add(obj_fits_config,"stop","0.85",JSON_DOUBLE);
	json_obj_add(obj_fits_config,"log_x","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"log_y","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"log_y_keep_sign","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"fit_invert_simulation_y","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"fit_subtract_lowest_point","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"fit_set_first_point_to_zero","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"fit_1st_deriv","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"fit_norm_data_at","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"fit_norm_x_point","0.5",JSON_DOUBLE);
	json_obj_add(obj_fits_config,"fit_set_error_to_zero_before","-100.0",JSON_DOUBLE);
	json_obj_add(obj_fits_config,"fit_hidden","false",JSON_BOOL);
	json_obj_add(obj_fits_config,"fit_against","self",JSON_STRING);
	json_obj_add(obj_fits_config,"id","",JSON_RANDOM_ID);
}

void json_template_fits_patch(struct json_obj *obj_fit_fits)
{
	struct json_obj *obj_fits_patch;
	struct json_obj *obj_fits_patch_template;

	obj_fits_patch=json_obj_add(obj_fit_fits,"fit_patch","",JSON_NODE);
	obj_fits_patch_template=json_obj_add(obj_fits_patch,"template","",JSON_TEMPLATE);
	json_obj_add(obj_fits_patch_template,"json_path","one/two/three",JSON_STRING);
	json_obj_add(obj_fits_patch_template,"human_path","one/two/three",JSON_STRING);
	json_obj_add(obj_fits_patch_template,"val","jv@jv",JSON_STRING);
	json_obj_add(obj_fits_patch_template,"id","",JSON_RANDOM_ID);
}

int json_template_fits_fits(struct json_obj *obj_fits)
{
	struct json_obj *obj_fit_fits;
	struct json_obj *obj_template;

	obj_fit_fits=json_obj_add(obj_fits,"fits","",JSON_NODE);
	json_obj_add(obj_fit_fits,"icon_","fit",JSON_STRING);

	obj_template=json_obj_add(obj_fit_fits,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","none",JSON_STRING);
	json_template_fits_patch(obj_template);
	json_template_fits_duplicate(obj_template);
	json_template_fits_config(obj_template);
	json_template_import_config(obj_template,"import_config");
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);
	return 0;
}
