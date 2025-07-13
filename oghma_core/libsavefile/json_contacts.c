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
#include <string.h>
#include <json.h>
#include <savefile.h>
#include <util.h>

int get_top_contact_layer(struct json *j)
{
	int l=0;
	char obj_type[100];
	struct json_obj *json_seg;
	struct json_segment_counter counter;

	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy");

	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_get_string(NULL, json_seg, obj_type,"obj_type",TRUE);
		if (strcmp(obj_type,"contact")==0)
		{
			return l;
		}
		l++;

		if (l>counter.max/2)
		{
			break;
		}
	}

	return -1;
}

int get_btm_contact_layer(struct json *j)
{
	int i;
	int segments;
	char temp[100];
	char obj_type[100];
	struct json_obj *json_seg;
	struct json_obj *json_epitaxy;
	json_epitaxy=json_obj_find_by_path(&(j->obj), "epitaxy");

	json_get_int(NULL, json_epitaxy, &segments,"segments",TRUE);

	for (i=segments-1;i>=0;i--)
	{
		sprintf(temp,"segment%d",i);
		json_seg=json_obj_find(json_epitaxy, temp);

		if (json_seg==NULL)
		{
			ewe(NULL,"Object contact %s not found\n",temp);
		}

		json_get_string(NULL, json_seg, obj_type,"obj_type",TRUE);

		if (strcmp(obj_type,"contact")==0)
		{
			return i;
		}

		if (i<segments/2)
		{
			break;
		}
	}
	
	return -1;
}

int json_fixup_new_contact_size(struct json *j,char *contact_path)
{
	int segments;
	struct vec my_min;
	struct vec my_max;
	struct json_obj *json_contact;
	struct json_obj *json_epitaxy;

	struct vec delta;


	json_epitaxy=json_obj_find_by_path(&(j->obj), "epitaxy");
	if (json_epitaxy==NULL)
	{
		return -1;
	}

	json_contact=json_obj_find_by_path(&(j->obj), contact_path);
	if (json_contact==NULL)
	{
		return -1;
	}

	json_get_int(NULL, json_epitaxy, &segments,"segments",TRUE);

	if (segments==0)
	{
		json_world_size(j, &my_min, &my_max);
		vec_cpy(&delta,&my_max);
		vec_sub(&delta,&my_min);
		json_set_data_double(json_contact,"dy",delta.y*0.2);
		json_set_data_double(json_contact,"dx",delta.x*0.2);
		json_set_data_double(json_contact,"dz",delta.z);
	}else
	{
		//needs filling in
	}

	return 0;
}

int json_fixup_contacts(struct json *j)
{
	struct vec my_min;
	struct vec my_max;
	double dy;
	char  position[100];
	struct json_obj *json_contact;
	struct json_obj *json_contact_data;
	struct json_segment_counter counter;

	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy.contacts");
	json_world_electrical_size(j, &my_min, &my_max);

	while((json_contact=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_set_data_string(json_contact,"obj_type", "contact");

		json_get_double(NULL,json_contact,&dy,"dy",TRUE);

		json_contact_data=json_obj_find_by_path(json_contact, "contact");
		json_get_string(NULL, json_contact_data, position,"position",TRUE);

		//move to the correct position

		if (strcmp(position,"top")==0)
		{
			json_set_data_double(json_contact,"y0",my_min.y-dy);
		}else
		if (strcmp(position,"bottom")==0)
		{
			json_set_data_double(json_contact,"y0",my_max.y);
		}
	}

	return 0;

}
