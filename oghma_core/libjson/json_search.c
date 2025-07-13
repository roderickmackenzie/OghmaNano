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
		//printf("cmp:'%s' '%s'\n",next_obj->name,name);
		if (strcmp(next_obj->name,name)==0)
		{
			return next_obj;

		}
	}

	return NULL;

}

struct json_obj *json_obj_find_by_path(struct json_obj *obj, char *path)
{
	int i;
	//int pos=0;
	char build[200];
	char before_dot[200];
	int first_dot=-1;
	struct json_obj *next_obj=NULL;
	struct json_obj *ret_obj=NULL;

	if (strcmp(path,"")==0)
	{
		return obj;
	}

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
		return NULL;
	}

	if (first_dot!=-1)
	{
		ret_obj=json_obj_find_by_path(next_obj, build);
		if (ret_obj==NULL)
		{
			return NULL;
		}

		return ret_obj;

	}

	return next_obj;

}

int json_get_string(struct simulation *sim,struct json_obj *obj, char *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		strcpy(out,found->data);
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Token %s not found\n",name);
		}	
	}

	return -1;

}

int json_get_hex_string(struct simulation *sim,struct json_obj *obj, char *out,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		strcpy(out,found->data);
		hex_to_string(out);
		return 0;
	}else
	{
		if (stop_on_error==TRUE)
		{
			ewe(sim,"Token %s not found\n",name);
		}	
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
			ewe(sim,"Not found '%s' in '%s'\n",name,obj->name);
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

int json_get_double_fabs(struct simulation *sim,struct json_obj *obj, double *out,char *name,int stop_on_error)
{
	int ret;
	ret=json_get_double(sim,obj, out,name,stop_on_error);
	*out=fabs(*out);
	return ret;
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

int json_get_equation(struct simulation *sim, struct json_obj *obj, struct rpn_equation *equ,char *name,int stop_on_error)
{
	struct json_obj *found;
	found=json_obj_find(obj, name);
	if (found!=NULL)
	{
		strcpy(equ->equ,found->data);
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

int json_calculate_memory(struct json_obj *obj,int *tot)
{
	int i;
	struct json_obj* objs;
	struct json_obj* next_obj;
	*tot+=sizeof(struct json_obj)*obj->max_len;
	*tot+=obj->data_len;

	objs=(struct json_obj* )obj->objs;
	for (i=0;i<obj->len;i++)
	{
		next_obj=&(objs[i]);

		json_calculate_memory(next_obj,tot);
	}

	return 0;
}

struct json_obj *json_search_for_obj_by_uid(struct json_obj *obj, char *value)
{
	struct json_obj *ret;
	ret=json_search_for_token_value(NULL, obj,"id", value);
	return ret;
}

struct json_obj *json_search_for_token_value(char *path, struct json_obj *obj,char *token, char *value)
{
	int i;
	struct json_obj *ret;
	struct json_obj *objs;
	struct json_obj *next_obj;
	objs=(struct json_obj* )obj->objs;

	for (i=0;i<obj->len;i++)
	{
		next_obj=&(objs[i]);
		if (strcmp(next_obj->name,token)==0)
		{
			if (strcmp(next_obj->data,value)==0)
			{
				return obj;
			}
		}
		if (next_obj->data_type==JSON_NODE)
		{
			if (path!=NULL)
			{
				if (strlen(path)!=0)
				{
					strcat(path,".");
				}

				strcat(path,next_obj->name);
			}
			
			ret=json_search_for_token_value(path, next_obj,token, value);
			if (ret!=NULL)
			{
				return ret;
			}

			if (path!=NULL)
			{
				if (str_count_char(path, '.')==0)
				{
					strcpy(path,"");
				}else
				{
					split_reverse(path, '.');
				}
			}
		}
	}

	return NULL;
}

int json_get_cpus(struct simulation *sim,struct json_obj *obj, int *out,char *name,int stop_on_error)
{
	int max_cpus;
	int ret;
	char temp[100];
	if (json_get_string(sim,obj, temp,name,stop_on_error)!=0)
	{
		return -1;
	}

	max_cpus=g_get_max_cpus();
	json_get_string(sim, obj, temp,name,TRUE);

	if (strcmp(temp,"all")==0)
	{
		ret=max_cpus;
	}else
	if (strcmp(temp,"all-div2")==0)
	{
		ret=max_cpus/2;
	}else
	if (strcmp(temp,"all-2")==0)
	{
		ret=max_cpus-2;
		if (ret<0)
		{
			ret=0;
		}
	}else
	{
		sscanf(temp,"%d",&ret);
	}

	if (ret>max_cpus)
	{
		ret=max_cpus;
	}

	*out=ret;

	return 0;
}

//This does not care about time zones, this is to increase platform portability.
int json_get_time_iso8601(struct simulation *sim, struct json_obj *obj, long long *out, char *name, int stop_on_error)
{
    struct tm tm = {0};
    long long unix_time;
    struct json_obj *found;

    found = json_obj_find(obj, name);

    if (found != NULL)
    {
        // Parse ISO8601 format: "YYYY-MM-DDTHH:MM:SSZ"
        int matched = sscanf(found->data, "%4d-%2d-%2dT%2d:%2d:%2dZ",
                             &tm.tm_year, &tm.tm_mon, &tm.tm_mday,
                             &tm.tm_hour, &tm.tm_min, &tm.tm_sec);

        if (matched != 6)
        {
            fprintf(stderr, "Failed to parse timestamp: %s\n", found->data);
            return -1;
        }

        tm.tm_year -= 1900; // struct tm expects years since 1900
        tm.tm_mon  -= 1;    // struct tm expects months 0-11

        // mktime assumes local time, which you're fine with
        unix_time = mktime(&tm);
        *out = unix_time;

        return 0;
    }
    else if (stop_on_error == TRUE)
    {
        ewe(sim, "Not found %s\n", name);
    }

    return -1;
}


