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
#include <memory.h>
#include <shape_struct.h>
#include <color.h>

int json_world_object(struct json_obj *obj)
{
	struct json_obj *text;
	struct json_obj *triangles;
	struct json_obj *bhj_data;

	json_obj_add(obj,"enabled","true",JSON_BOOL);
	text=json_obj_add(obj,"text_object_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;

	json_obj_add(obj,"obj_type","other",JSON_STRING);

	json_obj_add(obj,"x0","0.0",JSON_DOUBLE);
	json_obj_add(obj,"y0","0.0",JSON_DOUBLE);
	json_obj_add(obj,"z0","0.0",JSON_DOUBLE);
	json_obj_add(obj,"x0_u","m",JSON_STRING);
	json_obj_add(obj,"y0_u","m",JSON_STRING);
	json_obj_add(obj,"z0_u","m",JSON_STRING);

	json_obj_add(obj,"dx","0.0",JSON_DOUBLE);
	json_obj_add(obj,"dy","0.0",JSON_DOUBLE);
	json_obj_add(obj,"dz","0.0",JSON_DOUBLE);
	json_obj_add(obj,"dx_u","m",JSON_STRING);
	json_obj_add(obj,"dy_u","m",JSON_STRING);
	json_obj_add(obj,"dz_u","m",JSON_STRING);

	json_obj_add(obj,"dx_padding","0.0",JSON_DOUBLE);
	json_obj_add(obj,"dy_padding","0.0",JSON_DOUBLE);
	json_obj_add(obj,"dz_padding","0.0",JSON_DOUBLE);
	json_obj_add(obj,"dx_padding_u","m",JSON_STRING);
	json_obj_add(obj,"dy_padding_u","m",JSON_STRING);
	json_obj_add(obj,"dz_padding_u","m",JSON_STRING);

	json_obj_add(obj,"shape_nx","1",JSON_INT);
	json_obj_add(obj,"shape_ny","1",JSON_INT);
	json_obj_add(obj,"shape_nz","1",JSON_INT);

	json_obj_add(obj,"rotate_y","0.0",JSON_DOUBLE);
	json_obj_add(obj,"rotate_x","0.0",JSON_DOUBLE);
	json_obj_add(obj,"shape_type","box",JSON_STRING);

	text=json_obj_add(obj,"text_attributes_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;

	json_obj_add(obj,"color_r","0.8",JSON_DOUBLE);
	json_obj_add(obj,"color_g","0.8",JSON_DOUBLE);
	json_obj_add(obj,"color_b","0.8",JSON_DOUBLE);
	json_obj_add(obj,"color_alpha","0.8",JSON_DOUBLE);

	json_obj_add(obj,"name","none",JSON_STRING);
	json_obj_add(obj,"html_link","",JSON_STRING);
	json_obj_add(obj,"label","",JSON_STRING);
	json_obj_add(obj,"image_path","",JSON_STRING);

	json_obj_add(obj,"g_x0","1.0",JSON_DOUBLE);
	json_obj_add(obj,"g_y0","1.0",JSON_DOUBLE);
	json_obj_add(obj,"g_x1","1.0",JSON_DOUBLE);
	json_obj_add(obj,"g_y1","1.0",JSON_DOUBLE);

	triangles=json_obj_add(obj,"triangles","",JSON_DAT_FILE);
	triangles->data_flags=JSON_PRIVATE;

	bhj_data=json_obj_add(obj,"bhj_data","",JSON_DAT_FILE);
	bhj_data->data_flags=JSON_PRIVATE;

	json_obj_add(obj,"id","",JSON_RANDOM_ID);

	return 0;
}

int json_world_object_expand_xyz0(struct vec **xyz,int *count,struct json_obj *obj)
{
	int c=0;
	int z,x,y;
	struct vec *v;


	struct shape s;
	json_populate_shape_from_json_world_object(&s, obj);

	*count=s.nz*s.nx*s.ny;

	if (*count==0)
	{
		return -1;
	}

	malloc_1d((void **)xyz,*count,sizeof(struct vec));
	
	for (z=0;z<s.nz;z++)
	{
		for (x=0;x<s.nx;x++)
		{
			for (y=0;y<s.ny;y++)
			{
				v=&((*xyz)[c]);
				v->x=(s.x0+(s.dx+s.dx_padding)*((double)x));
				v->y=(s.y0+(s.dy+s.dy_padding)*((double)y));
				v->z=(s.z0+(s.dz+s.dz_padding)*((double)z));
				c++;
			}

		}
	}

	return 0;

}

int json_world_object_get_min_max(struct vec *my_min, struct vec *my_max, struct json_obj *obj)
{
	struct shape s;
	double z,x,y;
	json_populate_shape_from_json_world_object(&s, obj);

	//x
	if (s.x0<my_min->x)
	{
		my_min->x=s.x0;
	}

	x=s.x0+s.dx*(double)s.nx+s.dx_padding*((double)s.nx-1.0);

	if (x>my_max->x)
	{
		my_max->x=x;
	}

	//y
	if (s.y0<my_min->y)
	{
		my_min->y=s.y0;
	}

	y=s.y0+s.dy*(double)s.ny+s.dy_padding*((double)s.ny-1.0);

	if (y>my_max->y)
	{
		my_max->y=y;
	}

	//z
	if (s.z0<my_min->z)
	{
		my_min->z=s.z0;
	}

	z=s.z0+s.dz*(double)s.nz+s.dz_padding*((double)s.nz-1.0);

	if (z>my_max->z)
	{
		my_max->z=z;
	}
	
	return 0;
}

int json_populate_shape_from_json_world_object(struct shape *s, struct json_obj *obj)
{
	json_get_english(NULL,obj, &(s->enabled),"enabled",TRUE);

	json_get_double(NULL,obj, &s->dx,"dx",TRUE);
	json_get_double(NULL,obj, &s->dy,"dy",TRUE);
	json_get_double(NULL,obj, &s->dz,"dz",TRUE);

	json_get_double(NULL,obj, &s->dx_padding,"dx_padding",TRUE);
	json_get_double(NULL,obj, &s->dy_padding,"dy_padding",TRUE);
	json_get_double(NULL,obj, &s->dz_padding,"dz_padding",TRUE);

	json_get_int(NULL,obj, &(s->nx),"shape_nx",TRUE);
	json_get_int(NULL,obj, &(s->ny),"shape_ny",TRUE);
	json_get_int(NULL,obj, &(s->nz),"shape_nz",TRUE);

	json_get_string(NULL, obj, s->name,"name",TRUE);

	json_get_double(NULL,obj, &(s->x0),"x0",TRUE);
	json_get_double(NULL,obj, &(s->z0),"z0",TRUE);
	json_get_double(NULL,obj, &(s->y0),"y0",TRUE);

	json_get_double(NULL,obj, &s->rotate_y,"rotate_y",TRUE);
	json_get_double(NULL,obj, &s->rotate_x,"rotate_x",TRUE);

	obj_color_load_from_json(&(s->color),obj);

	json_get_string(NULL, obj, s->shape_type,"shape_type",TRUE);

	json_get_string(NULL, obj, s->id,"id",TRUE);

	return 0;
}

int json_save_shape_to_world_object(struct json_obj *obj, struct shape *s)
{
	json_set_data_bool(obj, "enabled",s->enabled);

	json_set_data_double(obj, "dx",s->dx);
	json_set_data_double(obj, "dy",s->dy);
	json_set_data_double(obj, "dz",s->dz);

	json_set_data_double(obj, "dx_padding",s->dx_padding);
	json_set_data_double(obj, "dy_padding",s->dy_padding);
	json_set_data_double(obj, "dz_padding",s->dz_padding);

	json_set_data_int(obj, "shape_nx",s->nx);
	json_set_data_int(obj, "shape_ny",s->ny);
	json_set_data_int(obj, "shape_nz",s->nz);

	json_set_data_string(obj, "name",s->name);

	json_set_data_double(obj, "x0",s->x0);
	json_set_data_double(obj, "z0",s->z0);
	json_set_data_double(obj, "y0",s->y0);

	json_set_data_double(obj, "rotate_y",s->rotate_y);
	json_set_data_double(obj, "rotate_x",s->rotate_x);

	obj_color_save_to_json(obj,&(s->color));

	json_set_data_string(obj, "shape_type",s->shape_type);

	json_set_data_string(obj, "id",s->id);
	return 0;
}

