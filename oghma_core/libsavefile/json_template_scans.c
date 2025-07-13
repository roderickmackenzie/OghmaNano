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

int json_template_scans(struct json_obj *obj_main)
{
	struct json_obj *obj_scans;
	struct json_obj *obj_scans_config;
	struct json_obj *obj_scan_optimizer;
	struct json_obj *obj_scans_template;
	struct json_obj *obj_scan_line_template;

	obj_scans=json_obj_add(obj_main,"scans","",JSON_NODE);
	json_obj_add(obj_scans,"icon_","scan",JSON_STRING);

	obj_scans_config=json_obj_add(obj_scans,"config","",JSON_NODE);
	json_obj_add(obj_scans_config,"none","none",JSON_STRING);

	obj_scans_template=json_obj_add(obj_scans,"template","",JSON_TEMPLATE);
	json_obj_add(obj_scans_template,"name","name",JSON_STRING);
	json_obj_add(obj_scans_template,"icon","scan",JSON_STRING);
	obj_scan_optimizer=json_obj_add(obj_scans_template,"scan_optimizer","",JSON_NODE);
	json_obj_add(obj_scans_template,"id","",JSON_RANDOM_ID);

	json_obj_add(obj_scan_optimizer,"enabled","false",JSON_BOOL);
	json_obj_add(obj_scan_optimizer,"scan_optimizer_dump_at_end","false",JSON_BOOL);
	json_obj_add(obj_scan_optimizer,"scan_optimizer_dump_n_steps","300",JSON_INT);

	obj_scan_line_template=json_obj_add(obj_scans_template,"template","",JSON_TEMPLATE);

	json_obj_add(obj_scan_line_template,"human_var","Paramter to change",JSON_STRING);
	json_obj_add(obj_scan_line_template,"values","values",JSON_STRING_HEX);
	json_obj_add(obj_scan_line_template,"opp","scan",JSON_STRING_HEX);
	json_obj_add(obj_scan_line_template,"token_json","Paramter to change",JSON_STRING);
	json_obj_add(obj_scan_line_template,"token_json1", "token_json1",JSON_STRING);

	return 0;
}
