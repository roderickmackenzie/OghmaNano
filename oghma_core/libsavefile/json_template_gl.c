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

int json_gl_flyby(struct json_obj *obj)
{
	json_obj_add(obj,"enabled","false",JSON_BOOL);

	json_obj_add(obj,"xRot","25.0",JSON_DOUBLE);
	json_obj_add(obj,"yRot","1.0",JSON_DOUBLE);
	json_obj_add(obj,"zRot","0.0",JSON_DOUBLE);

	json_obj_add(obj,"x_pos","0.0",JSON_DOUBLE);
	json_obj_add(obj,"y_pos","0.0",JSON_DOUBLE);
	json_obj_add(obj,"zoom","16.0",JSON_DOUBLE);

	json_obj_add(obj,"name","view",JSON_STRING);
	json_obj_add(obj,"id","",JSON_RANDOM_ID);

	return 0;
}

int json_template_gl(struct json_obj *obj_main)
{
	struct json_obj *obj_gl;

	struct json_obj *obj_flybys;
	struct json_obj *obj_flybys_template;

	struct json_obj *obj_gl_lights;
	struct json_obj *obj_gl_lights_template;

	obj_gl=json_obj_add(obj_main,"gl","",JSON_NODE);

	obj_flybys=json_obj_add(obj_gl,"flybys","",JSON_NODE);
	obj_flybys_template=json_obj_add(obj_flybys,"template","",JSON_TEMPLATE);
	json_gl_flyby(obj_flybys_template);


	obj_gl_lights=json_obj_add(obj_gl,"gl_lights","",JSON_NODE);
	obj_gl_lights_template=json_obj_add(obj_gl_lights,"template","",JSON_TEMPLATE);
	json_gl_light_object(obj_gl_lights_template);


	//obj_template=json_obj_add(obj_epitaxy,"template","",JSON_TEMPLATE);
	//json_obj_add(obj_template,"icon","jv",JSON_STRING);
	//json_world_object(obj_template);

	return 0;
}
