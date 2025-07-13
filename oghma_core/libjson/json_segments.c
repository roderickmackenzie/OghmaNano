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

/** @file josn_dump.c
	@brief Json file decoder
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zip.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <inp.h>
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>

int json_segments_renumber(struct json_obj *root_node)
{
	int i;
	struct json_obj *objs;
	struct json_obj *obj_tmp;
	struct json_obj *segment_obj;

	objs=(struct json_obj* )root_node->objs;
	int seg=0;
	for (i=0;i<root_node->len;i++)
	{
		obj_tmp=&(objs[i]);
		if (strcmp_begin(obj_tmp->name,"segment")==0)
		{
			if (strcmp_begin(obj_tmp->name,"segments")!=0)
			{
				sprintf(obj_tmp->name,"segment%d",seg);
				seg++;
			}
		}

	}

	segment_obj=json_obj_find(root_node, "segments");
	sprintf(segment_obj->data,"%d",seg);
	return 0;
}

//This will swap but preserver the order of the segments
int json_segments_move_last_to_pos(struct json_obj *root_node, int i0)
{
	int segments;
	char name_seg0[20];
	char name_seg1[20];
	char name_seg_last[20];
	struct json_obj *obj_seg0;
	struct json_obj *obj_seg1;
	struct json_obj *obj_last;
	struct json_obj tmp;

	json_get_int(NULL, root_node, &segments,"segments",FALSE);

	sprintf(name_seg_last,"segment%d",segments-1);
	obj_last=json_obj_find(root_node, name_seg_last);
	memcpy(&tmp,obj_last,sizeof(struct json_obj));

	sprintf(name_seg0,"segment%d",i0);
	obj_seg0=json_obj_find(root_node, name_seg0);
	sprintf(name_seg1,"segment%d",i0+1);
	obj_seg1=json_obj_find(root_node, name_seg1);

	memcpy(obj_seg1,obj_seg0,sizeof(struct json_obj)*(segments-i0-1));

	memcpy(obj_seg0,&tmp,sizeof(struct json_obj));

	json_segments_renumber(root_node);

	return 0;
}

//This will swap and just renumber the segments
int json_segments_swap(struct json_obj *root_node, int i0, int i1)
{
	char name_seg0[20];
	char name_seg1[20];
	struct json_obj tmp;
	struct json_obj *obj_seg0;
	struct json_obj *obj_seg1;

	sprintf(name_seg0,"segment%d",i0);
	sprintf(name_seg1,"segment%d",i1);

	obj_seg0=json_obj_find(root_node, name_seg0);
	obj_seg1=json_obj_find(root_node, name_seg1);

	memcpy(&tmp,obj_seg0,sizeof(struct json_obj));
	memcpy(obj_seg0,obj_seg1,sizeof(struct json_obj));
	memcpy(obj_seg1,&tmp,sizeof(struct json_obj));

	json_segments_renumber(root_node);
	//json_dump_obj(root_node);
	return 0;
}

int json_clear_segments(struct json_obj *root_node)
{
	int i;
	int write_pos;
	struct json_obj *objs;
	struct json_obj *obj_tmp;
	struct json_obj *segment_obj;

	objs=(struct json_obj* )root_node->objs;
	for (i=0;i<root_node->len;i++)
	{
		obj_tmp=&(objs[i]);
		if (strcmp_begin(obj_tmp->name,"segment")==0)
		{
			if (strcmp_begin(obj_tmp->name,"segments")!=0)
			{
				json_obj_all_free(obj_tmp);
				obj_tmp->max_len=-2;		//signified it is deleted
			}
		}
	}
	
	write_pos=0;
	for (i=0;i<root_node->len;i++)
	{
		obj_tmp=&(objs[i]);

		if (obj_tmp->max_len!=-2)
		{
			if (write_pos!=i)
			{
				memcpy(&(objs[write_pos]), obj_tmp, sizeof(struct json_obj));
			}
			write_pos++;
		}

	}

	root_node->len=write_pos;

	segment_obj=json_obj_find(root_node, "segments");
	strcpy(segment_obj->data,"0");

	return 0;
}

struct json_obj *json_segments_add(struct json_obj *obj,char *human_name, int pos)
{
	struct json_obj *new_segment;
	int segments;
	char new_segment_name[100];
	struct json_obj *next_obj;

	if (obj->json_template==NULL)
	{
		printf("json_segments_add: not a template\n");
		return NULL;
	}
	if (json_get_int(NULL, obj, &segments,"segments",FALSE)==-1)
	{
		printf("json_segments_add: no segments\n");
		return NULL;
	}

	sprintf(new_segment_name,"segment%d",segments);

	segments++;
	json_set_data_int(obj,"segments",segments);

	next_obj=json_obj_add(obj,new_segment_name,"",JSON_NODE);
	json_obj_all_free(next_obj);
	json_obj_cpy(next_obj,obj->json_template);
	strcpy(next_obj->name,new_segment_name);

	if (human_name!=NULL)
	{
		if (strcmp(human_name,"")!=0)
		{
			json_set_data_string(next_obj,"name",human_name);
		}
	}

	json_update_random_ids(next_obj);

	if (pos!=-1)
	{
		json_segments_move_last_to_pos(obj, pos);
		sprintf(new_segment_name,"segment%d",pos);
	}

	new_segment=json_obj_find_by_path(obj, new_segment_name);
	//json_dump_obj(obj);
	return new_segment;
}

struct json_obj *json_segments_add_by_path(struct json_obj *root_obj,char *path,char *human_name, int pos)
{
	struct json_obj *ret;
	struct json_obj *obj;

	obj=json_obj_find_by_path(root_obj, path);
	if (obj==NULL)
	{
		return NULL;
	}
	ret=json_segments_add(obj,human_name, pos);
	if (ret==NULL)
	{
		return NULL;
	}

	return ret;
}

struct json_obj *json_segments_find_by_name(struct json_obj *search_obj,char *name_in)
{
	int i;
	int segments;
	char temp_str[STR_MAX];
	struct json_obj *obj;
	if (json_get_int(NULL,search_obj, &segments,"segments",FALSE)!=0)
	{
		return NULL;
	}

	for (i=0;i<segments;i++)
	{
		sprintf(temp_str,"segment%d",i);
		obj=json_obj_find(search_obj, temp_str);
		if (obj==NULL)
		{
			printf("json_find_segment_by_name: Object %s not found\n",temp_str);
			return NULL;
		}

		json_get_string(NULL, obj, temp_str,"name",TRUE);
		if (strcmp(name_in,temp_str)==0)
		{
			return obj;
		}
	}

	return NULL;
}

int json_delete_segment(struct json_obj *root_node, char *segment_name)
{

	if (json_obj_delete_node(root_node, segment_name)==-1)
	{
		return -1;
	}

	json_segments_renumber(root_node);
	return 0;
}
