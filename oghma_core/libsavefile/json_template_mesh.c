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

int json_template_mesh(struct json_obj *obj_root,int x,int y, int z, int t, int l)
{
	struct json_obj *obj_mesh;
	struct json_obj *obj_x;
	struct json_obj *obj_template_x;
	struct json_obj *obj_y;
	struct json_obj *obj_template_y;
	struct json_obj *obj_z;
	struct json_obj *obj_template_z;
	struct json_obj *obj_t;
	struct json_obj *obj_template_t;
	struct json_obj *obj_l;
	struct json_obj *obj_template_l;

	struct json_obj *obj_config;

	obj_mesh=json_obj_add(obj_root,"mesh","",JSON_NODE);
	json_obj_add(obj_mesh,"icon_","mesh",JSON_STRING);

	obj_config=json_obj_add(obj_mesh,"config","",JSON_NODE);
	json_obj_add(obj_config,"remesh_z","true",JSON_BOOL);
	json_obj_add(obj_config,"remesh_x","true",JSON_BOOL);
	json_obj_add(obj_config,"remesh_y","true",JSON_BOOL);

	if (x==TRUE)
	{
		obj_x=json_obj_add(obj_mesh,"mesh_x","",JSON_NODE);
		json_obj_add(obj_x,"enabled","false",JSON_BOOL);
		json_obj_add(obj_x,"auto","false",JSON_BOOL);
		json_obj_add(obj_x,"icon_","x",JSON_STRING);

		obj_template_x=json_obj_add(obj_x,"template","",JSON_TEMPLATE);
		json_obj_add(obj_template_x,"len","0.0032249",JSON_DOUBLE);
		json_obj_add(obj_template_x,"len_u","m",JSON_STRING);
		json_obj_add(obj_template_x,"points","1.0",JSON_DOUBLE);
		json_obj_add(obj_template_x,"mul","1.0",JSON_DOUBLE);
		json_obj_add(obj_template_x,"left_right","left",JSON_STRING);
		json_obj_add(obj_template_x,"id","",JSON_RANDOM_ID);
	}

	if (y==TRUE)
	{
		obj_y=json_obj_add(obj_mesh,"mesh_y","",JSON_NODE);
		json_obj_add(obj_y,"enabled","true",JSON_BOOL);
		json_obj_add(obj_y,"auto","true",JSON_BOOL);
		json_obj_add(obj_y,"icon_","y",JSON_STRING);

		obj_template_y=json_obj_add(obj_y,"template","",JSON_TEMPLATE);
		json_obj_add(obj_template_y,"len","0.0032249",JSON_DOUBLE);
		json_obj_add(obj_template_y,"len_u","m",JSON_STRING);
		json_obj_add(obj_template_y,"points","1.0",JSON_DOUBLE);
		json_obj_add(obj_template_y,"mul","1.0",JSON_DOUBLE);
		json_obj_add(obj_template_y,"left_right","left",JSON_STRING);
		json_obj_add(obj_template_y,"id","",JSON_RANDOM_ID);
	}

	if (z==TRUE)
	{
		obj_z=json_obj_add(obj_mesh,"mesh_z","",JSON_NODE);
		json_obj_add(obj_z,"enabled","false",JSON_BOOL);
		json_obj_add(obj_z,"auto","false",JSON_BOOL);
		json_obj_add(obj_z,"icon_","z",JSON_STRING);

		obj_template_z=json_obj_add(obj_z,"template","",JSON_TEMPLATE);
		json_obj_add(obj_template_z,"len","0.0032249",JSON_DOUBLE);
		json_obj_add(obj_template_z,"len_u","m",JSON_STRING);
		json_obj_add(obj_template_z,"points","1",JSON_INT);
		json_obj_add(obj_template_z,"mul","1.0",JSON_DOUBLE);
		json_obj_add(obj_template_z,"left_right","left",JSON_STRING);
		json_obj_add(obj_template_z,"id","",JSON_RANDOM_ID);
	}

	if (t==TRUE)
	{
		obj_t=json_obj_add(obj_mesh,"mesh_t","",JSON_NODE);
		json_obj_add(obj_t,"enabled","false",JSON_BOOL);
		json_obj_add(obj_t,"auto","false",JSON_BOOL);
		json_obj_add(obj_t,"icon_","t",JSON_STRING);

		obj_template_t=json_obj_add(obj_t,"template","",JSON_TEMPLATE);
		json_obj_add(obj_template_t,"start","220.0",JSON_DOUBLE);
		json_obj_add(obj_template_t,"stop","300.0",JSON_DOUBLE);
		json_obj_add(obj_template_t,"points","7",JSON_INT);
		json_obj_add(obj_template_t,"mul","1.0",JSON_DOUBLE);
		json_obj_add(obj_template_t,"left_right","left",JSON_STRING);
		json_obj_add(obj_template_t,"id","",JSON_RANDOM_ID);
	}

	if (l==TRUE)
	{
		obj_l=json_obj_add(obj_mesh,"mesh_l","",JSON_NODE);
		json_obj_add(obj_l,"enabled","false",JSON_BOOL);
		json_obj_add(obj_l,"auto","false",JSON_BOOL);
		json_obj_add(obj_l,"icon_","lambda",JSON_STRING);

		obj_template_l=json_obj_add(obj_l,"template","",JSON_TEMPLATE);
		json_obj_add(obj_template_l,"start","220",JSON_DOUBLE);
		json_obj_add(obj_template_l,"start","300e-9",JSON_DOUBLE);
		json_obj_add(obj_template_l,"stop","1.4e-6",JSON_DOUBLE);
		json_obj_add(obj_template_l,"start_u","nm",JSON_STRING);
		json_obj_add(obj_template_l,"stop_u","nm",JSON_STRING);
		json_obj_add(obj_template_l,"points","150.0",JSON_DOUBLE);
		json_obj_add(obj_template_l,"mul","1.0",JSON_DOUBLE);
		json_obj_add(obj_template_l,"left_right","left",JSON_STRING);
		json_obj_add(obj_template_l,"id","",JSON_RANDOM_ID);
	}

	return 0;
}
