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

int json_template_dump(struct json_obj *obj_main)
{
	struct json_obj *obj_dump;
	struct json_obj *obj_template;
	struct json_obj *obj_banned_files;
	struct json_obj *obj_noise;
	struct json_obj *obj_probes;
	struct json_obj *obj_probe_block_template;
	struct json_obj *obj_probe_item_template;
	struct json_obj *obj_probe_node;

	obj_dump=json_obj_add(obj_main,"dump","",JSON_NODE);
	json_obj_add(obj_dump,"icon_","hdd_custom",JSON_STRING);

	json_obj_add(obj_dump,"dump_probes","true",JSON_BOOL);
	json_obj_add(obj_dump,"dump_write_converge","true",JSON_BOOL);
	json_obj_add(obj_dump,"dump_norm_time_to_one","false",JSON_BOOL);
	json_obj_add(obj_dump,"dump_norm_y_axis","false",JSON_BOOL);
	json_obj_add(obj_dump,"dump_write_out_band_structure","false",JSON_BOOL);
	json_obj_add(obj_dump,"dump_first_guess","false",JSON_BOOL);
	json_obj_add(obj_dump,"dump_log_level","screen_and_disk",JSON_STRING);
	json_obj_add(obj_dump,"dump_optical_probe","false",JSON_BOOL);
	json_obj_add(obj_dump,"dump_optical_probe_spectrum","false",JSON_BOOL);
	json_obj_add(obj_dump,"dump_print_text","0",JSON_INT);
	json_obj_add(obj_dump,"dump_write_headers","true",JSON_BOOL);
	json_obj_add(obj_dump,"dump_remove_dos_cache","false",JSON_BOOL);
	json_obj_add(obj_dump,"dump_dynamic_pl_energy","false",JSON_BOOL);
	json_obj_add(obj_dump,"dump_binary","true",JSON_BOOL);

	//bannded files
	obj_banned_files=json_obj_add(obj_dump,"banned_files","",JSON_NODE);

	obj_template=json_obj_add(obj_banned_files,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"banned_enabled","true",JSON_BOOL);
	json_obj_add(obj_template,"banned_file_name","jv.csv",JSON_STRING);

	obj_noise=json_obj_add(obj_dump,"noise","",JSON_NODE);

	obj_template=json_obj_add(obj_noise,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"noise_enabled","true",JSON_BOOL);
	json_obj_add(obj_template,"noise_file_name","jv.csv",JSON_STRING);
	json_obj_add(obj_template,"noise_sigma","0.1",JSON_DOUBLE);

	//probes
	obj_probes=json_obj_add(obj_dump,"probes","",JSON_NODE);

	obj_probe_block_template=json_obj_add(obj_probes,"template","",JSON_TEMPLATE);
	json_obj_add(obj_probe_block_template,"name","probe",JSON_STRING);
	json_obj_add(obj_probe_block_template,"icon_","map_pin",JSON_STRING);
	obj_probe_node=json_obj_add(obj_probe_block_template,"probes","",JSON_NODE);
	json_obj_add(obj_probe_block_template,"id","",JSON_RANDOM_ID);

	obj_probe_item_template=json_obj_add(obj_probe_node,"template","",JSON_TEMPLATE);
	json_obj_add(obj_probe_item_template,"probe_enabled","true",JSON_BOOL);
	json_obj_add(obj_probe_item_template,"probe_type","point",JSON_STRING);
	json_obj_add(obj_probe_item_template,"file_name","Ec.csv",JSON_STRING);
	json_obj_add(obj_probe_item_template,"px","0",JSON_INT);
	json_obj_add(obj_probe_item_template,"py","0",JSON_INT);
	json_obj_add(obj_probe_item_template,"pz","0",JSON_INT);

	json_obj_add(obj_probe_item_template,"py_double","1.0",JSON_DOUBLE);

	json_obj_add(obj_probe_item_template,"id","",JSON_RANDOM_ID);

	return 0;
}
