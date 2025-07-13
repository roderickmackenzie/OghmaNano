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

int json_template_sims_mode(struct json_obj *obj_sims)
{
	struct json_obj *obj_mode;
	struct json_obj *obj_template;
	struct json_obj *obj_template_config;

	obj_mode=json_obj_add(obj_sims,"mode","",JSON_NODE);
	json_obj_add(obj_mode,"icon_","mode",JSON_STRING);

	obj_template=json_obj_add(obj_mode,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","Mode",JSON_STRING);
	json_obj_add(obj_template,"icon","mode_fiber",JSON_STRING);
	obj_template_config=json_obj_add(obj_template,"config","",JSON_NODE);
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	json_obj_add(obj_template_config,"mode_max_ittr","25",JSON_INT);
	json_obj_add(obj_template_config,"mode_stop_error","10.0",JSON_DOUBLE);
	json_obj_add(obj_template_config,"mode_max_eigenmode_x","5",JSON_INT);
	json_obj_add(obj_template_config,"mode_max_eigenmode_y","5",JSON_INT);
	json_obj_add(obj_template_config,"mode_te_tm","TE",JSON_STRING);
	json_obj_add(obj_template_config,"mode_only_fundamental","false",JSON_BOOL);

	return 0;
}
