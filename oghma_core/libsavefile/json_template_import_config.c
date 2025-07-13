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

int json_template_import_config(struct json_obj *obj_root,char *name)
{
	struct json_obj *obj_import_config;
	obj_import_config=json_obj_add(obj_root,name,"",JSON_NODE);

	json_obj_add(obj_import_config,"icon_","parasitic",JSON_STRING);

	json_obj_add(obj_import_config,"import_file_path","none",JSON_STRING);
	json_obj_add(obj_import_config,"import_x_combo_pos","9",JSON_INT);
	json_obj_add(obj_import_config,"import_data_combo_pos","5",JSON_INT);
	json_obj_add(obj_import_config,"import_x_spin","0",JSON_INT);
	json_obj_add(obj_import_config,"import_data_spin","1",JSON_INT);
	json_obj_add(obj_import_config,"import_title","Voltage - J",JSON_STRING);
	json_obj_add(obj_import_config,"import_xlabel","Voltage",JSON_STRING);
	json_obj_add(obj_import_config,"import_data_label","J",JSON_STRING);
	json_obj_add(obj_import_config,"import_area","0.104",JSON_DOUBLE);
	json_obj_add(obj_import_config,"import_data_invert","false",JSON_BOOL);
	json_obj_add(obj_import_config,"import_x_invert","false",JSON_BOOL);
	json_obj_add(obj_import_config,"data_file","none",JSON_STRING);
	json_obj_add(obj_import_config,"id","",JSON_RANDOM_ID);
	return 0;
}
