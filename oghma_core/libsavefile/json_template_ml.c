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

void json_ml_patch(struct json_obj *obj_root)
{
	struct json_obj *obj_ml_patch;
	struct json_obj *obj_ml_patch_template;

	obj_ml_patch=json_obj_add(obj_root,"ml_patch","",JSON_NODE);
	obj_ml_patch_template=json_obj_add(obj_ml_patch,"template","",JSON_TEMPLATE);
	json_obj_add(obj_ml_patch_template,"ml_patch_enabled","true",JSON_BOOL);
	json_obj_add(obj_ml_patch_template,"json_var","one/two/three",JSON_STRING);
	json_obj_add(obj_ml_patch_template,"human_var","one/two/three",JSON_STRING);
	json_obj_add(obj_ml_patch_template,"ml_patch_val","value",JSON_STRING);
	json_obj_add(obj_ml_patch_template,"id","",JSON_RANDOM_ID);
}

int json_template_ml(struct json_obj *obj_main)
{
	struct json_obj *obj_ml;
	struct json_obj *obj_template_ml;
	struct json_obj *obj_ml_random;
	struct json_obj *obj_ml_random_template;
	struct json_obj *obj_duplicate;
	struct json_obj *obj_duplicate_template;
	struct json_obj *obj_ml_sims;
	struct json_obj *obj_ml_sims_template;
	struct json_obj *obj_ml_config;
	struct json_obj *obj_ml_output_vectors;
	struct json_obj *obj_ml_output_vectors_template;

	obj_ml=json_obj_add(obj_main,"ml","",JSON_NODE);
	json_obj_add(obj_ml,"icon_","ml",JSON_STRING);

	obj_template_ml=json_obj_add(obj_ml,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template_ml,"name","ML",JSON_STRING);
	json_obj_add(obj_template_ml,"icon_","ml",JSON_STRING);

	//random
	obj_ml_random=json_obj_add(obj_template_ml,"ml_random","",JSON_NODE);
	obj_ml_random_template=json_obj_add(obj_ml_random,"template","",JSON_TEMPLATE);
	json_obj_add(obj_ml_random_template,"random_var_enabled","true",JSON_BOOL);
	json_obj_add(obj_ml_random_template,"json_var","one/two/three",JSON_STRING);
	json_obj_add(obj_ml_random_template,"human_var","one/two/three",JSON_STRING);
	json_obj_add(obj_ml_random_template,"min","0.0",JSON_DOUBLE);
	json_obj_add(obj_ml_random_template,"max","1.0",JSON_DOUBLE);
	json_obj_add(obj_ml_random_template,"random_distribution","log",JSON_STRING);
	json_obj_add(obj_ml_random_template,"id","",JSON_RANDOM_ID);

	//patch
	json_ml_patch(obj_template_ml);

	//duplicate
	obj_duplicate=json_obj_add(obj_template_ml,"duplicate","",JSON_NODE);
	obj_duplicate_template=json_obj_add(obj_duplicate,"template","",JSON_TEMPLATE);
	json_obj_add(obj_duplicate_template,"duplicate_var_enabled","true",JSON_BOOL);
	json_obj_add(obj_duplicate_template,"human_src","one/two/three",JSON_STRING);
	json_obj_add(obj_duplicate_template,"human_dest","one/two/three",JSON_STRING);
	json_obj_add(obj_duplicate_template,"multiplier","x",JSON_STRING);
	json_obj_add(obj_duplicate_template,"json_src","one/two/three",JSON_STRING);
	json_obj_add(obj_duplicate_template,"json_dest","one/two/three",JSON_STRING);
	json_obj_add(obj_duplicate_template,"id","",JSON_RANDOM_ID);

	//sims
	obj_ml_sims=json_obj_add(obj_template_ml,"ml_sims","",JSON_NODE);
	obj_ml_sims_template=json_obj_add(obj_ml_sims,"template","",JSON_TEMPLATE);
	json_obj_add(obj_ml_sims_template,"ml_sim_enabled","true",JSON_BOOL);
	json_obj_add(obj_ml_sims_template,"sim_name","light_1.0",JSON_STRING);
	json_ml_patch(obj_ml_sims_template);
	json_obj_add(obj_ml_sims_template,"id","",JSON_RANDOM_ID);

	//sims/ml_output_vectors
	obj_ml_output_vectors=json_obj_add(obj_ml_sims_template,"ml_output_vectors","",JSON_NODE);
	obj_ml_output_vectors_template=json_obj_add(obj_ml_output_vectors,"template","",JSON_TEMPLATE);
	json_obj_add(obj_ml_output_vectors_template,"ml_output_vector_item_enabled","true",JSON_BOOL);
	json_obj_add(obj_ml_output_vectors_template,"file_name","jv.dat",JSON_STRING);
	json_obj_add(obj_ml_output_vectors_template,"ml_token_name","vec",JSON_STRING);
	json_obj_add(obj_ml_output_vectors_template,"vectors","0.0,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0",JSON_STRING);
	json_template_import_config(obj_ml_output_vectors_template,"import_config");
	json_obj_add(obj_ml_output_vectors_template,"id","",JSON_RANDOM_ID);

	//config
	obj_ml_config=json_obj_add(obj_template_ml,"ml_config","",JSON_NODE);
	json_obj_add(obj_ml_config,"ml_number_of_archives","400",JSON_INT);
	json_obj_add(obj_ml_config,"ml_sims_per_archive","40",JSON_INT);
	json_obj_add(obj_ml_config,"ml_archive_path","cwd",JSON_STRING);
	json_obj_add(obj_ml_config,"ml_vector_file_name","vectors.json",JSON_STRING);
	json_obj_add(obj_ml_config,"ml_crash_time","4.0",JSON_DOUBLE);
	json_obj_add(obj_ml_config,"ml_build_vectors_when_done","false",JSON_BOOL);
	json_obj_add(obj_ml_config,"id","",JSON_RANDOM_ID);

	json_template_ml_networks(obj_template_ml);
	json_obj_add(obj_template_ml,"id","",JSON_RANDOM_ID);
	//json_dump_obj(obj_ml);

	return 0;
}
