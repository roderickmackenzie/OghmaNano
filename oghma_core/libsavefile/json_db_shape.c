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


int json_shape_db_threshold(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"threshold","",JSON_NODE);
	json_obj_add(obj,"threshold_enabled","false", JSON_BOOL);
	json_obj_add(obj,"threshold_value","200", JSON_INT);

	return 0;
}

int json_shape_saw_wave(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"saw_wave","",JSON_NODE);
	json_obj_add(obj,"shape_saw_offset","0", JSON_INT);
	json_obj_add(obj,"shape_saw_length","50", JSON_INT);
	json_obj_add(obj,"shape_saw_type","saw_wave",JSON_STRING);

	return 0;
}

int json_shape_db_blur(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"blur","",JSON_NODE);
	json_obj_add(obj,"shape_import_blur_enabled","false", JSON_BOOL);
	json_obj_add(obj,"shape_import_blur","10", JSON_INT);
	json_obj_add(obj,"mesh_show","true", JSON_BOOL);
	json_obj_add(obj,"mesh_gen_nx","20", JSON_INT);
	json_obj_add(obj,"mesh_gen_ny","20", JSON_INT);
	json_obj_add(obj,"mesh_gen_opp","node_reduce",JSON_STRING);
	json_obj_add(obj,"mesh_min_ang","25", JSON_INT);

	return 0;
}

int json_shape_db_mesh(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"mesh","",JSON_NODE);
	json_obj_add(obj,"mesh_show","true", JSON_BOOL);
	json_obj_add(obj,"mesh_gen_nx","20", JSON_INT);
	json_obj_add(obj,"mesh_gen_ny","20", JSON_INT);
	json_obj_add(obj,"mesh_gen_opp","node_reduce",JSON_STRING);
	json_obj_add(obj,"mesh_min_ang","25", JSON_INT);

	return 0;
}

int json_shape_boundary(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"boundary","",JSON_NODE);
	json_obj_add(obj,"boundary_enabled","false", JSON_BOOL);
	json_obj_add(obj,"image_boundary_x0","0", JSON_INT);
	json_obj_add(obj,"image_boundary_x0_color","1.0,1.0,1.0,1.0",JSON_STRING);
	json_obj_add(obj,"image_boundary_x1","0", JSON_INT);
	json_obj_add(obj,"image_boundary_x1_color","1.0,1.0,1.0,1.0",JSON_STRING);
	json_obj_add(obj,"image_boundary_y0","0", JSON_INT);
	json_obj_add(obj,"image_boundary_y0_color","1.0,1.0,1.0,1.0",JSON_STRING);
	json_obj_add(obj,"image_boundary_y1","0", JSON_INT);
	json_obj_add(obj,"image_boundary_y1_color","1.0,1.0,1.0,1.0",JSON_STRING);

	return 0;
}

int json_shape_db_item_import(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"import_config","",JSON_NODE);
	json_obj_add(obj,"shape_import_y_norm","false", JSON_BOOL);
	json_obj_add(obj,"shape_import_z_norm","false", JSON_BOOL);
	json_obj_add(obj,"shape_import_y_norm_percent","2.0", JSON_DOUBLE);
	json_obj_add(obj,"shape_import_rotate","0.0", JSON_DOUBLE);

	return 0;
}

int json_shape_db_item_lens(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"lens","",JSON_NODE);
	json_obj_add(obj,"lens_type","convex",JSON_STRING);
	json_obj_add(obj,"lens_size","1.0", JSON_DOUBLE);

	return 0;
}

int json_shape_db_item_xtal(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"xtal","",JSON_NODE);

	json_obj_add(obj,"xtal_dr","10", JSON_INT);
	json_obj_add(obj,"xtal_dx","30", JSON_INT);
	json_obj_add(obj,"xtal_dy","30", JSON_INT);
	json_obj_add(obj,"xtal_offset","30", JSON_INT);

	return 0;
}

int json_shape_db_item_honeycomb(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"honeycomb","",JSON_NODE);

	json_obj_add(obj,"honeycomb_dx","30.0", JSON_DOUBLE);
	json_obj_add(obj,"honeycomb_dy","30.0", JSON_DOUBLE);
	json_obj_add(obj,"honeycomb_x_shift","0", JSON_INT);
	json_obj_add(obj,"honeycomb_y_shift","0", JSON_INT);
	json_obj_add(obj,"honeycomb_line_width","10", JSON_INT);
	json_obj_add(obj,"honeycomb_rotate","0.0", JSON_DOUBLE);

	return 0;
}

int json_shape_db_item_gaus(struct json_obj *obj_main)
{
	struct json_obj *obj;
	obj=json_obj_add(obj_main,"gauss","",JSON_NODE);

	json_obj_add(obj,"gauss_sigma","100.0", JSON_DOUBLE);
	json_obj_add(obj,"gauss_offset_x","0", JSON_INT);
	json_obj_add(obj,"gauss_offset_y","0", JSON_INT);
	json_obj_add(obj,"gauss_invert","false", JSON_BOOL);
	return 0;
}

int json_db_shape(struct json *j)
{
	json_free(j);
	struct json_obj *obj_main;
	j->is_template=TRUE;

	obj_main=&(j->obj);

	json_obj_add(obj_main,"item_type","shape",JSON_STRING);
	json_obj_add(obj_main,"color_r","0.8",JSON_DOUBLE);
	json_obj_add(obj_main,"color_g","0.8",JSON_DOUBLE);
	json_obj_add(obj_main,"color_b","0.8",JSON_DOUBLE);
	json_obj_add(obj_main,"image_ylen","200",JSON_INT);
	json_obj_add(obj_main,"image_xlen","200",JSON_INT);
	json_obj_add(obj_main,"color_alpha","0.8",JSON_DOUBLE);

	json_obj_add(obj_main,"shape_type0_enable","false",JSON_BOOL);
	json_obj_add(obj_main,"shape_type0","box",JSON_STRING);
	json_obj_add(obj_main,"shape_type1_enable","false",JSON_BOOL);
	json_obj_add(obj_main,"shape_type1","box",JSON_STRING);

	json_obj_add(obj_main,"status","private",JSON_STRING);

	json_shape_db_item_gaus(obj_main);
	json_shape_db_item_honeycomb(obj_main);
	json_shape_db_item_xtal(obj_main);
	json_shape_db_item_lens(obj_main);

	json_shape_db_item_import(obj_main);
	json_shape_boundary(obj_main);
	json_shape_db_mesh(obj_main);

	json_shape_db_blur(obj_main);
	json_shape_saw_wave(obj_main);
	json_shape_db_threshold(obj_main);

	json_obj_add(obj_main,"id","",JSON_RANDOM_ID);

	//json_dump_obj(&(j->obj));

	return 0;
}
