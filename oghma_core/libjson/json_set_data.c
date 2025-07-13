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

/** @file josn_init.c
	@brief Json file decoder
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "oghma_const.h"
#include <log.h>
#include <json.h>
#include <memory.h>
#include <dat_file.h>

void json_set_data(struct json_obj *obj,char *data)
{
	int len;
	free_1d((void **)&(obj->data));
	len=strlen(data);
	obj->data_len=len+10;
	obj->data=malloc((obj->data_len)*sizeof(char));
	strcpy(obj->data,data);
	obj->data[len]=0;
}

void json_set_data_dat_file(struct json_obj *obj)
{
	free_1d((void **)&(obj->data));

	obj->data_len=sizeof(struct dat_file);
	obj->data=(char *)malloc(obj->data_len);
	dat_file_init((struct dat_file*)obj->data);
	//obj->data=NULL;
}

int json_set_data_double(struct json_obj *main_obj,char *token,double value)
{
	char temp[200];
	struct json_obj *obj;
	obj=json_obj_find(main_obj, token);
	if (obj==NULL)
	{
		return -1;
	}
	
	sprintf(temp,"%le",value);
	json_set_data(obj,temp);
	return 0;
}

int json_set_data_string(struct json_obj *main_obj,char *token,char *value)
{

	struct json_obj *obj;
	obj=json_obj_find(main_obj, token);
	if (obj==NULL)
	{
		return -1;
	}

	json_set_data(obj,value);
	return 0;
}

int json_set_data_int(struct json_obj *main_obj,char *token,int value)
{
	char temp[200];
	struct json_obj *obj;
	obj=json_obj_find(main_obj, token);
	if (obj==NULL)
	{
		return -1;
	}
	
	sprintf(temp,"%d",value);
	json_set_data(obj,temp);
	return 0;
}

int json_set_data_long_long(struct json_obj *main_obj,char *token,long long value)
{
	char temp[200];
	struct json_obj *obj;
	obj=json_obj_find(main_obj, token);
	if (obj==NULL)
	{
		return -1;
	}
	
	sprintf(temp,"%lld",value);
	json_set_data(obj,temp);
	return 0;
}

int json_set_data_bool(struct json_obj *main_obj,char *token,int value)
{
	char temp[200];
	struct json_obj *obj;
	obj=json_obj_find(main_obj, token);
	if (obj==NULL)
	{
		return -1;
	}

	if (value==TRUE)
	{
		strcpy(temp,"true");
	}else
	{
		strcpy(temp,"false");
	}

	json_set_data(obj,temp);
	return 0;
}
