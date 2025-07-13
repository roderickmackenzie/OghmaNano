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

int json_template_gui_config(struct json_obj *obj_main)
{
	struct json_obj *obj_gui_config;
	struct json_obj *obj_interface;
	struct json_obj *obj_main_ribbon;

	obj_gui_config=json_obj_add(obj_main,"gui_config","",JSON_NODE);

	obj_interface=json_obj_add(obj_gui_config,"interface","",JSON_NODE);
	json_obj_add(obj_interface,"bk_r","-1.0",JSON_DOUBLE);
	json_obj_add(obj_interface,"bk_g","-1.0",JSON_DOUBLE);
	json_obj_add(obj_interface,"bk_b","-1.0",JSON_DOUBLE);

	json_obj_add(obj_interface,"col_text_r","-1.0",JSON_DOUBLE);
	json_obj_add(obj_interface,"col_text_g","-1.0",JSON_DOUBLE);
	json_obj_add(obj_interface,"col_text_b","-1.0",JSON_DOUBLE);

	obj_main_ribbon=json_obj_add(obj_gui_config,"main_ribbon","",JSON_NODE);

	json_obj_add(obj_main_ribbon,"thermal_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"sim_mode_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"editors_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"automation_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"electrical_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"optical_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"thermal_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"database_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"cluster_visible","true",JSON_BOOL);
	json_obj_add(obj_main_ribbon,"information_visible","true",JSON_BOOL);

	return 0;
}
