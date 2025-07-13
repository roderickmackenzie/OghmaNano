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

/** @file josn_free.c
	@brief Json free objects
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
#include <memory.h>
#include <rand.h>
#include <dat_file.h>

void json_free(struct json *j)
{
	json_obj_all_free(&(j->obj));
	free_1d((void **)&(j->raw_data));
	json_obj_all_free(&(j->bib_template));
	json_init(j);

}


void json_obj_free(struct json_obj *obj)
{
	int i;
	struct json_obj *objs;
	struct json_obj *next_obj;
	objs=(struct json_obj* )obj->objs;
	for (i=0;i<obj->len;i++)
	{
		next_obj=&(objs[i]);
		if (next_obj->data!=NULL)
		{
			free_1d((void **)&(next_obj->data));
		}
	}

	if (obj->objs!=NULL)
	{
		//printf("'%s'\n",obj->name);
		free_1d((void **)&(obj->objs));
	}
	obj->len=0;
	obj->max_len=0;

	free_1d((void **)&(obj->json_template));

}

void json_obj_all_free(struct json_obj *obj)
{
	int i;
	//printf("enter\n");
	struct json_obj *objs;
	struct json_obj *next_obj;
	objs=(struct json_obj* )obj->objs;

	for (i=0;i<obj->len;i++)
	{
		next_obj=&(objs[i]);
		//printf("free: '%s'\n",next_obj->name);
		if (next_obj->data_type==JSON_NODE)
		{
			json_obj_all_free(next_obj);
		}else
		if (next_obj->data_type==JSON_DAT_FILE)
		{
			//printf("here!? %p %d %d\n",next_obj->data,next_obj->data_len,sizeof(struct dat_file));
			//dat_file_dump_info((struct dat_file*)next_obj->data);
			dat_file_free((struct dat_file*)(next_obj->data));
			//printf("not here!?\n");
		}
	}

	if (obj->json_template!=NULL)
	{
		json_obj_all_free((struct json_obj *)obj->json_template);
	}

	json_obj_free(obj);

}



