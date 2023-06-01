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

/** @file josn_search.c
	@brief Search the json tree
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "inp.h"
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>

struct json_obj *json_obj_find(struct json_obj *obj, char *name)
{
	int i;

	struct json_obj *objs;
	struct json_obj *next_obj;
	objs=(struct json_obj* )obj->objs;
	for (i=0;i<obj->len;i++)
	{
		next_obj=&(objs[i]);

		if (strcmp(next_obj->name,name)==0)
		{
			return next_obj;

		}
	}

	return NULL;

}

struct json_obj *json_obj_find_by_path(struct simulation *sim,struct json_obj *obj, char *path)
{
	int i;
	//int pos=0;
	char build[200];
	char before_dot[200];
	int first_dot=-1;
	struct json_obj *next_obj=NULL;
	struct json_obj *ret_obj=NULL;
	//printf("%s\n",path);
	strcpy(before_dot,path);
	for (i=0;i<strlen(path);i++)
	{
		if ((path[i]=='.')||(path[i]=='/')||(path[i]=='\\'))
		{
			first_dot=i;
			before_dot[i]=0;
			break;
		}
	}

	if (first_dot!=-1)
	{
		strcpy(build,path+first_dot+1);
	}else
	{
		strcpy(build,"none");
	}

	//getchar();
	//printf("called:%s %s\n",build,before_dot);
	next_obj=json_obj_find(obj, before_dot);
	if (next_obj==NULL)
	{
		return NULL;//ewe(sim,"object %s %s not found",before_dot,build);
	}

	if (first_dot!=-1)
	{
		ret_obj=json_obj_find_by_path(sim,next_obj, build);
		if (ret_obj==NULL)
		{
			return NULL;//ewe(sim,"object %s\n not found",build);
		}

		return ret_obj;

	}

	return next_obj;

}

int json_get_string(struct simulation *sim,struct json_obj *obj, char *out,char *name)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		strcpy(out,found->data);
		return 0;
	}else
	{
		ewe(sim,"Token %s not found\n",name);
	}

	return -1;

}

int json_is_token(struct json_obj *obj,char *name)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		return 0;
	}

	return -1;

}

int json_get_int(struct simulation *sim,struct json_obj *obj, int *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		sscanf(found->data,"%d",out);
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Not found %s\n",name);
		}
	}

	return -1;

}

int json_get_long_long(struct simulation *sim,struct json_obj *obj, long long *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		//printf("%s %s\n",name,found->data);
		//
			sscanf(found->data,"%lld",out);
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Not found %s\n",name);
		}
	}
	return -1;

}

int json_get_long_double(struct simulation *sim,struct json_obj *obj, gdouble *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	double tmp;
	if (found!=NULL)
	{
		//printf("%s %s\n",name,found->data);
		sscanf(found->data,"%le",&tmp);
		*out=tmp;
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Not found %s\n",name);
		}
	}
	return -1;

}

int json_get_long(struct simulation *sim,struct json_obj *obj, long *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	long tmp;
	if (found!=NULL)
	{
		//printf("%s %s\n",name,found->data);
		sscanf(found->data,"%ld",&tmp);
		*out=tmp;
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Not found %s\n",name);
		}
	}
	return -1;

}

int json_get_double(struct simulation *sim,struct json_obj *obj, double *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		//printf("%s %s\n",name,found->data);
		sscanf(found->data,"%le",out);
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Not found %s\n",name);
		}
	}
	return -1;

}

int json_get_float(struct simulation *sim,struct json_obj *obj, float *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		//printf("%s %s\n",name,found->data);
		sscanf(found->data,"%e",out);
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Not found %s\n",name);
		}
	}
	return -1;

}

int json_get_english(struct simulation *sim,struct json_obj *obj, int *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		*out=english_to_bin(sim,found->data);
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Not found %s\n",name);
		}
	}

	return -1;

}



