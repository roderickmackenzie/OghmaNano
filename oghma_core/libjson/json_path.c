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
#include <token_lib.h>

int json_path_to_list(struct list* l,char *path)
{
	int i;
	char build[200];
	build[0]=0;
	int pos=0;
	for (i=0;i<strlen(path);i++)
	{
		if (path[i]!='.')
		{
			build[pos]=path[i];
			pos++;
		}else
		{
			build[pos]=0;
			list_add(l,build);
			pos=0;
		}
	}

	if (strlen(build)!=0)
	{
		build[pos]=0;
		list_add(l,build);
	}
	return 0;
}

int json_human_path_to_json(struct json *j, struct hash_list *token_lib,char *json_path,char *human_path)
{
	int i;
	int s;
	int segments;
	struct list l;
	struct json_obj *obj;
	struct json_obj *obj_next;
	struct json_obj *obj_segs;
	struct token_lib_item* token_item;
	char temp[OGHMA_PATH_MAX];
	char temp_name[200];
	int found=FALSE;
	obj=&(j->obj);
	list_init(&l);
	json_path_to_list(&l,human_path);
	strcpy(json_path,"");
	int last_token;
	//printf("I have been fed '%s'\n",human_path);
	for (i=0;i<l.len;i++)
	{
		found=FALSE;
		obj_next=json_obj_find_by_path(obj, l.names[i]);
		//printf("Search '%s'\n",l.names[i]);
		if (obj_next!=NULL)
		{
			strcat(json_path,l.names[i]);
			strcat(json_path,".");
			obj=obj_next;
			found=TRUE;
		}

		if (found==FALSE)
		{
			if (json_get_int(NULL,obj, &segments,"segments",FALSE)==0)
			{
				//printf("segs=%d\n",segments);
				for (s=0;s<segments;s++)
				{
					sprintf(temp,"segment%d",s);
					obj_segs=json_obj_find_by_path(obj, temp);
					json_get_string(NULL,obj_segs, temp_name,"name",TRUE);
					if (strcmp(temp_name,l.names[i])==0)
					{
						strcat(json_path,temp);
						strcat(json_path,".");
						obj=obj_segs;
						found=TRUE;
						break;
					}
					
				}
			}
		}

		if (found==FALSE)
		{
			last_token=0;
			while(1)
			{
				token_item=token_lib_rfind(token_lib,l.names[i],&last_token);
				if (token_item==NULL)
				{
					break;
				}

				obj_next=json_obj_find_by_path(obj, token_item->token);
				if (obj_next!=NULL)
				{
					strcat(json_path,token_item->token);
					strcat(json_path,".");
					obj=obj_next;
					found=TRUE;
				}

			}
		}

		if (found==FALSE)
		{
			printf("lost at %s\n",l.names[i]);
			list_free(&l);
			return -1;
		}
	}
	
	if (strcmp_end(json_path,".")==0)
	{
		json_path[strlen(json_path)-1]=0;
	}
	//printf("return %s\n",json_path);
	list_free(&l);
	return 0;
}


int json_path_to_human_path(struct json *j, struct hash_list *token_lib,char *human_path,char *json_path)
{
	int i;
	struct list l;
	struct json_obj *obj;
	struct json_obj *obj_next;
	struct json_obj *obj_segs;
	struct token_lib_item* token_item;
	char temp_name[200];
	int found=FALSE;
	obj=&(j->obj);
	list_init(&l);
	json_path_to_list(&l,json_path);
	strcpy(human_path,"");
	//printf("I have been fed '%s'\n",json_path);
	for (i=0;i<l.len;i++)
	{
		found=FALSE;
		obj_next=json_obj_find_by_path(obj, l.names[i]);
		//printf("Search '%s'\n",l.names[i]);
		if (obj_next==NULL)
		{
			printf("lost at %s\n",l.names[i]);
			list_free(&l);
			return -1;
		}

		token_item=token_lib_find(token_lib,l.names[i]);
		if (token_item!=NULL)
		{
			strcat(human_path,token_item->english);
			strcat(human_path,".");
			obj=obj_next;
			found=TRUE;
		}

		if (found==FALSE)
		{
			if (strcmp_begin(l.names[i],"segment")==0)
			{
				if (strcmp_begin(l.names[i],"segments")!=0)
				{
					obj_segs=json_obj_find_by_path(obj, l.names[i]);
					if (json_get_string(NULL,obj_segs, temp_name,"name",FALSE)==0)
					{
						strcat(human_path,temp_name);
						strcat(human_path,".");
						obj=obj_segs;
						found=TRUE;
					}
				}
			}
		}


		if (found==FALSE)
		{
			strcat(human_path,l.names[i]);
			strcat(human_path,".");
			obj=obj_next;
		}

	}
	
	if (strcmp_end(human_path,".")==0)
	{
		human_path[strlen(human_path)-1]=0;
	}

	printf("returning: '%s'\n",human_path);
	list_free(&l);
	return 0;
} 
