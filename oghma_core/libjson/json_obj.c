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
#include <rand.h>

void json_obj_init(struct json_obj *obj)
{
	strcpy(obj->name,"");
	obj->len=0;
	obj->max_len=0;
	obj->objs=NULL;
	obj->data=NULL;
	obj->data_len=0;
	obj->data_type=-1;
	obj->data_flags=0;
	obj->json_template=NULL;
}

void json_obj_realloc(struct json_obj *obj)
{
	if (obj->len>=obj->max_len)
	{
		if (obj->max_len==0)
		{
			obj->max_len=8;
		}else
		{
			obj->max_len*=2;
		}
		obj->objs=(struct json_obj*)realloc(obj->objs,sizeof(struct json_obj)*obj->max_len);
		//reallocs++;
	}

}

struct json_obj * json_obj_add(struct json_obj *obj,char *name,char *data, int data_type)
{
	struct json_obj *objs;
	struct json_obj *obj_next;

	if (data_type==JSON_TEMPLATE)
	{
		json_obj_add(obj,"segments","0",JSON_INT);
		obj->json_template=malloc(sizeof(struct json_obj));
		obj_next=(struct json_obj *)obj->json_template;
		json_obj_init(obj_next);
		strcpy(obj_next->name,name);
		obj_next->data_type=JSON_NODE;
		return obj_next;
	}

	json_obj_realloc(obj);

	objs=(struct json_obj* )obj->objs;
	obj_next=&(objs[obj->len]);
	json_obj_init(obj_next);

	strcpy(obj_next->name,name);
	obj_next->data_type=data_type;

	if (strlen(obj_next->name)>40)
	{
		printf("This json reader can't handel tokens over 40 chars in length\n");
		exit(0);
	}

	if (obj_next->data!=NULL)
	{
		printf("json memory error\n");
		exit(0);
	}

	if (data_type==JSON_RANDOM_ID)
	{
		json_set_data(obj_next,"          ");
		rand_hex(NULL, obj_next->data,16);
	}else
	if (data_type==JSON_DAT_FILE)
	{
		json_set_data_dat_file(obj_next);
	}else
	{
		json_set_data(obj_next,data);
	}
	obj->len++;
	//printf("reallocs: %d\n",reallocs);
	return obj_next;
}

struct json_obj * json_obj_add_int(struct json_obj *obj,char *name, int data)
{
	char tmp[STR_MAX];
	struct json_obj *ret;
	sprintf(tmp,"%d",data);
	ret=json_obj_add(obj,name,tmp, JSON_INT);
	return ret;
}

struct json_obj * json_obj_add_double(struct json_obj *obj,char *name, double data)
{
	char tmp[STR_MAX];
	struct json_obj *ret;
	sprintf(tmp,"%le",data);
	ret=json_obj_add(obj,name,tmp, JSON_DOUBLE);
	return ret;
}

struct json_obj * json_obj_add_long_long(struct json_obj *obj,char *name, long long data)
{
	char tmp[STR_MAX];
	struct json_obj *ret;
	sprintf(tmp,"%lld",data);
	ret=json_obj_add(obj,name,tmp, JSON_LONG_LONG);
	return ret;
}

struct json_obj * json_obj_add_bool(struct json_obj *obj,char *name, int data)
{
	char tmp[STR_MAX];
	struct json_obj *ret;
	if (data==TRUE)
	{
		strcpy(tmp,"true");
	}else
	{
		strcpy(tmp,"false");
	}

	ret=json_obj_add(obj,name,tmp, JSON_BOOL);
	return ret;
}

struct json_obj * json_obj_add_string(struct json_obj *obj,char *name, char *data)
{
	struct json_obj *ret;
	ret=json_obj_add(obj,name, data, JSON_STRING);
	return ret;
}

void json_obj_cpy_data(struct json_obj *out,struct json_obj *in)
{
	//printf("here %s\n",in->name);

	out->len=in->len;
	out->max_len=in->max_len;
	//printf("1\n");
	strcpy(out->name,in->name);
	//printf("2\n");
	out->json_template=NULL;
	out->data_len=in->data_len;
	out->data=NULL;

	out->data_type=in->data_type;
	out->data_flags=in->data_flags;

	if (in->data_type==JSON_DAT_FILE)
	{
		json_set_data_dat_file(out);
	}else
	{
		if (in->data!=NULL)
		{
			out->data=malloc((in->data_len)*sizeof(char));
			memcpy(out->data, in->data, in->data_len);
		}
	}

	if (out->max_len>0)
	{
		out->objs=(struct json_obj*)malloc(sizeof(struct json_obj)*out->max_len);
	}

	if (in->json_template!=NULL)
	{
		out->json_template=(struct json_obj*)malloc(sizeof(struct json_obj)*out->max_len);
		json_obj_cpy((struct json_obj*)out->json_template,(struct json_obj*)in->json_template);
	}
}

void json_obj_cpy(struct json_obj *out,struct json_obj *in)
{

	int i;
	json_obj_cpy_data(out,in);

	struct json_obj *objs_in;
	struct json_obj *objs_out;

	struct json_obj *obj_in;
	struct json_obj *obj_out;

	objs_in=(struct json_obj* )in->objs;
	objs_out=(struct json_obj* )out->objs;

	for (i=0;i<in->len;i++)
	{
		obj_in=&(objs_in[i]);
		obj_out=&(objs_out[i]);

		json_obj_cpy(obj_out,obj_in);

	}

}


