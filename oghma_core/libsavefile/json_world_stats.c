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
#include <vec.h>

int json_world_size(struct json *j, struct vec *my_min, struct vec *my_max)
{
	char name[200];
	struct json_obj *json_seg;

	struct json_obj *obj;
	double dx0=-1.0;
	double dx1=-1.0;

	double dy0=-1.0;
	double dy1=-1.0;

	double dz0=-1.0;
	double dz1=-1.0;

	double world_margin_x0=-1.0;
	double world_margin_x1=-1.0;

	double world_margin_y0=-1.0;
	double world_margin_y1=-1.0;

	double world_margin_z0=-1.0;
	double world_margin_z1=-1.0;

	int world_automatic_size;
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);

	my_min->x=1e6;
	my_min->y=1e6;
	my_min->z=1e6;

	my_max->x=-1e6;
	my_max->y=-1e6;
	my_max->z=-1e6;

	obj=json_obj_find_by_path(&(j->obj), "world.config");
	json_get_english(NULL,obj, &world_automatic_size,"world_automatic_size",TRUE);

	if (world_automatic_size==FALSE)
	{
		json_get_double(NULL,obj, &(my_min->x),"world_x0",TRUE);
		json_get_double(NULL,obj, &(my_min->y),"world_y0",TRUE);
		json_get_double(NULL,obj, &(my_min->z),"world_z0",TRUE);

		json_get_double(NULL,obj, &(my_max->x),"world_x1",TRUE);
		json_get_double(NULL,obj, &(my_max->y),"world_y1",TRUE);
		json_get_double(NULL,obj, &(my_max->z),"world_z1",TRUE);

	}else
	{

		//epi
		json_segment_counter_load(&counter,j, "epitaxy");

		while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
		{
			json_world_object_get_min_max(my_min, my_max, json_seg);
		}


		//world
		json_segment_counter_load(&counter,j, "world.world_data");

		while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
		{

			json_get_string(NULL, json_seg, name,"name",TRUE);
			if (strcmp(name,"label")!=0)
			{
				json_world_object_get_min_max(my_min, my_max, json_seg);
			}
		}

		//lights
		json_segment_counter_load(&counter,j, "optical.light_sources.lights");

		while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
		{

			json_get_string(NULL, json_seg, name,"light_illuminate_from",TRUE);
			if (strcmp(name,"xyz")==0)
			{
				json_world_object_get_min_max(my_min, my_max, json_seg);
			}
		}

		//detectors
		json_segment_counter_load(&counter,j, "optical.detectors");

		while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
		{
			json_world_object_get_min_max(my_min, my_max, json_seg);
		}

		json_get_double(NULL,obj, &(world_margin_x0),"world_margin_x0",TRUE);
		json_get_double(NULL,obj, &(world_margin_x1),"world_margin_x1",TRUE);

		json_get_double(NULL,obj, &(world_margin_y0),"world_margin_y0",TRUE);
		json_get_double(NULL,obj, &(world_margin_y1),"world_margin_y1",TRUE);

		json_get_double(NULL,obj, &(world_margin_z0),"world_margin_z0",TRUE);
		json_get_double(NULL,obj, &(world_margin_z1),"world_margin_z1",TRUE);

		dx0=(world_margin_x0-1.0)*(my_max->x-my_min->x);
		dx1=(world_margin_x1-1.0)*(my_max->x-my_min->x);

		dy0=(world_margin_y0-1.0)*(my_max->y-my_min->y);
		dy1=(world_margin_y1-1.0)*(my_max->y-my_min->y);

		dz0=(world_margin_z0-1.0)*(my_max->z-my_min->z);
		dz1=(world_margin_z1-1.0)*(my_max->z-my_min->z);

		my_min->x=my_min->x-dx0;
		my_min->y=my_min->y-dy0;
		my_min->z=my_min->z-dz0;

		my_max->x=my_max->x+dx1;
		my_max->y=my_max->y+dy1;
		my_max->z=my_max->z+dz1;
	}

	return 0;
}

int json_world_electrical_size(struct json *j, struct vec *my_min, struct vec *my_max)
{
	char name[200];
	struct json_obj *json_seg;
	int obj_type;
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	int found=FALSE;
	my_min->x=1e6;
	my_min->y=1e6;
	my_min->z=1e6;

	my_max->x=-1e6;
	my_max->y=-1e6;
	my_max->z=-1e6;


	//epi
	json_segment_counter_load(&counter,j, "epitaxy");

	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_get_english(NULL,json_seg, &obj_type,"obj_type",TRUE);
		if ((obj_type==LAYER_ACTIVE)||(obj_type==LAYER_BHJ))
		{
			json_world_object_get_min_max(my_min, my_max, json_seg);
			found=TRUE;
		}
		
	}

	//world
	json_segment_counter_load(&counter,j, "world.world_data");

	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{

		json_get_string(NULL, json_seg, name,"name",TRUE);
		json_get_english(NULL,json_seg, &obj_type,"obj_type",TRUE);
		if (strcmp(name,"label")!=0)
		{
			if ((obj_type==LAYER_ACTIVE)||(obj_type==LAYER_BHJ))
			{
				json_world_object_get_min_max(my_min, my_max, json_seg);
				found=TRUE;
			}
		}
	}

	if (found==FALSE)
	{
		my_min->x=0.0;
		my_min->y=0.0;
		my_min->z=0.0;

		my_max->x=0.0;
		my_max->y=0.0;
		my_max->z=0.0;
		return -1;
	}

	return 0;
}

int json_world_thermal_size(struct json *j, struct vec *my_min, struct vec *my_max)
{
	char name[200];
	struct json_obj *json_seg;
	int enabled;
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	int found=FALSE;
	my_min->x=1e6;
	my_min->y=1e6;
	my_min->z=1e6;

	my_max->x=-1e6;
	my_max->y=-1e6;
	my_max->z=-1e6;


	//epi
	json_segment_counter_load(&counter,j, "epitaxy");

	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		if (json_get_english(NULL,json_seg, &enabled,"solve_thermal_problem",FALSE)==0)
		{
			if (enabled==TRUE)
			{
				json_world_object_get_min_max(my_min, my_max, json_seg);
				found=TRUE;
			}
		}
		
	}

	//world
	json_segment_counter_load(&counter,j, "world.world_data");

	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{

		json_get_string(NULL, json_seg, name,"name",TRUE);
		if (json_get_english(NULL,json_seg, &enabled,"solve_thermal_problem",FALSE)==0)
		{
			if (strcmp(name,"label")!=0)
			{
				if (enabled==TRUE)
				{
					json_world_object_get_min_max(my_min, my_max, json_seg);
					found=TRUE;
				}
			}
		}
	}

	if (found==FALSE)
	{
		my_min->x=0.0;
		my_min->y=0.0;
		my_min->z=0.0;

		my_max->x=0.0;
		my_max->y=0.0;
		my_max->z=0.0;
		return -1;
	}

	return 0;
}
