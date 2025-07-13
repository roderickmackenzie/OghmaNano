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

/** @file josn.c
	@brief Json file decoder
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>
#include <ctype.h>
#include <g_io.h>
#include <util_str.h>
#include <memory.h>
#include <zip.h>

struct json_obj * json_clip_start(struct json *j,char *paste_object_type)
{
	struct json_obj *obj_paste_data;
	json_obj_add_string(&(j->obj),"type","paste_object");
	json_obj_add_string(&(j->obj),"sub_type",paste_object_type);
	obj_paste_data=json_obj_add(&(j->obj),"paste_data","",JSON_NODE);
	json_obj_add_int(obj_paste_data,"segments",0);
	return obj_paste_data;
}

struct json_obj * json_clip_add_data(struct json *j,struct json_obj *data)
{
	int segments;
	char name[20];
	struct json_obj *obj_paste_data;
	struct json_obj *obj_segment;
	obj_paste_data=json_obj_find_by_path(&(j->obj), "paste_data");

	json_get_int(NULL, obj_paste_data, &segments,"segments",FALSE);

	sprintf(name,"segment%d",segments);
	obj_segment=json_obj_add(obj_paste_data,name,"",JSON_NODE);
	json_obj_cpy(obj_segment,data);

	//json_set_data_string(obj_segment,"name",name);
	strcpy(obj_segment->name,name);
	//json_dump_obj(obj_segment);

	segments++;

	json_set_data_int(obj_paste_data,"segments",segments);
	return obj_paste_data;
}


int json_copy_to_clipboard(struct json *j, struct json_string *buf, char *path,char *paste_object_type, int *segments, int n_segments)
{
	int i;
	char temp_str[100];
	struct json_dump_settings settings;
	json_dump_settings_init(&settings);
	struct json build;
	struct json_obj *main_obj;
	struct json_obj *obj;

	json_init(&build);

	main_obj=json_obj_find_by_path(&(j->obj), path);
	if (main_obj==NULL)
	{
		printf("object %s not found\n",path);
		return -1;
	}

	if (strcmp(paste_object_type,"")==0)
	{
		json_clip_start(&build,"unknown");
	}else
	{
		json_clip_start(&build,paste_object_type);
	}

	if (segments==NULL)
	{
		json_clip_add_data(&build,main_obj);
		json_dump_to_string(buf,&(build.obj),0,&settings);

	}else
	{
		for (i=0;i<n_segments;i++)
		{
			sprintf(temp_str,"segment%d",segments[i]);
			obj=json_obj_find(main_obj, temp_str);
			if (obj!=NULL)
			{
				json_clip_add_data(&build,obj);
			}

		}

		json_dump_to_string(buf,&(build.obj),0,&settings);
	}

	json_free(&build);

	return 0;
}
