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

int json_db_electrical_constants(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"electrical_constants","",JSON_NODE);

	json_shape_dos(obj, TRUE);
	json_obj_add(obj,"material_blend","false",JSON_BOOL);
	json_obj_add(obj,"Xi0","-3.0",JSON_DOUBLE);
	json_obj_add(obj,"Eg0","1.0",JSON_DOUBLE);
	json_obj_add(obj,"Xi1","-3.0",JSON_DOUBLE);
	json_obj_add(obj,"Eg1","1.0",JSON_DOUBLE);
	return 0;
}

int json_db_materials(struct json *j)
{
	json_free(j);
	struct json_obj *obj_main;
	struct json_obj *obj_lca;
	struct json_obj *obj_thermal;
	j->is_template=TRUE;

	obj_main=&(j->obj);
	json_obj_add(obj_main,"item_type","material",JSON_STRING);
	json_obj_add(obj_main,"color_r","0.8",JSON_DOUBLE);
	json_obj_add(obj_main,"color_g","0.8",JSON_DOUBLE);
	json_obj_add(obj_main,"color_b","0.8",JSON_DOUBLE);
	json_obj_add(obj_main,"color_alpha","0.8",JSON_DOUBLE);
	json_obj_add(obj_main,"material_type","other",JSON_STRING);
	json_obj_add(obj_main,"status","private",JSON_STRING);
	json_obj_add(obj_main,"changelog","",JSON_STRING);
	json_obj_add(obj_main,"mat_src","",JSON_STRING);

	json_template_import_config(obj_main,"n_import");
	json_template_import_config(obj_main,"alpha_import");
	json_template_import_config(obj_main,"emission_import");

	json_db_electrical_constants(obj_main);

	obj_thermal=json_obj_add(obj_main,"thermal_constants","",JSON_NODE);
	json_obj_add(obj_thermal,"thermal_kl","1.0",JSON_DOUBLE);
	json_obj_add(obj_thermal,"thermal_tau_e","1.0000e-8",JSON_DOUBLE);
	json_obj_add(obj_thermal,"thermal_tau_h","1.0000e-9",JSON_DOUBLE);

	obj_lca=json_obj_add(obj_main,"lca","",JSON_NODE);
	json_obj_add(obj_lca,"lca_density","2400.0",JSON_DOUBLE);
	json_obj_add(obj_lca,"lca_cost","0.47",JSON_DOUBLE);
	json_obj_add(obj_lca,"lca_energy","37450374.430606",JSON_DOUBLE);
	json_obj_add(obj_main,"id","",JSON_RANDOM_ID);

	//json_dump_obj(&(j->obj));

	return 0;
}
