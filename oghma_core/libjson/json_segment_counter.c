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

int json_segment_counter_init(struct json_segment_counter *data)
{
	strcpy(data->path,"");
	strcpy(data->item,"");
	strcpy(data->item_path,"");
	return 0;
}

int json_segment_counter_load(struct json_segment_counter *data,struct json *j,char *path)
{
	strcpy(data->path,path);
	data->segments=json_obj_find_by_path(&(j->obj), path);
	if (data->segments==NULL)
	{
		printf("segment not found %s\n ",path);
	}
	data->i=0;
	json_get_int(NULL, data->segments, &(data->max),"segments",TRUE);

	return 0;
}

int json_segment_counter_load_from_obj(struct json_segment_counter *data,struct json_obj *obj)
{
	strcpy(data->path,"");
	if (json_get_int(NULL, data->segments, &(data->max),"segments",FALSE)!=0)
	{
		return -1;	
	}

	data->segments=obj;
	data->i=0;

	return 0;
}

struct json_obj *json_segment_counter_get_next(struct json_segment_counter *data)
{
	struct json_obj *json_seg;
	if (data->i>=data->max)
	{
		return NULL;
	}

	if (data->segments==NULL)
	{
		printf("you have not loaded the segments into the sgment counter\n");
		return NULL;		
	}

	sprintf(data->item,"segment%d",data->i);
	strcpy(data->item_path,data->path);
	if (strcmp(data->path,"")!=0)
	{
		strcat(data->item_path,".");
	}
	strcat(data->item_path,data->item);

	json_seg=json_obj_find(data->segments, data->item);

	if (json_seg==NULL)
	{
		printf("Object '%s' in '%s' not found\n",data->item,data->path);
		return NULL;
	}
	data->i++;
	return json_seg;
}



