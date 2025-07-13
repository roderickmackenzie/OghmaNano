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
#include <time.h>

int json_dump_obj_string_from_path(struct json_string *buf,struct json *j, char *json_path)
{
	struct json_obj *obj;
	char path[OGHMA_PATH_MAX];
	char tmp[OGHMA_PATH_MAX+10];
	struct json_dump_settings settings;
	json_dump_settings_init(&settings);
	settings.show_private=FALSE;

	if (strcmp(json_path,"")==0)
	{
		obj=&(j->obj);

	}else
	{
		strcpy(path,json_path);
		str_split_end(path, '.');

		obj=json_obj_find_by_path(&(j->obj), json_path);
		if (obj==NULL)
		{
			return -1;
		}
	}

	sprintf(tmp,"\"%s\": {\n",path);
	json_string_cat(buf,tmp);

	json_dump(obj,buf,0,&settings);
	remove_comma(buf);

	json_string_cat(buf,"\n\t}");
	return 0;
}

int json_dump_tokens_from_path(struct json_string *buf,struct json *j, char *json_path)
{
	int i;
	struct json_obj *objs;
	struct json_obj *next_obj;
	struct json_dump_settings settings;
	json_dump_settings_init(&settings);
	settings.show_private=FALSE;

	struct json_obj *obj;

	if (strcmp(json_path,"")==0)
	{
		obj=&(j->obj);

	}else
	{
		obj=json_obj_find_by_path(&(j->obj), json_path);
		if (obj==NULL)
		{
			return -1;
		}
	}

	if (obj->data_type!=JSON_NODE)
	{
		return -1;
	}

	objs=(struct json_obj* )obj->objs;
	for (i=0;i<obj->len;i++)
	{
		next_obj=&(objs[i]);

		json_string_cat(buf,next_obj->name);
		json_string_cat(buf,"\n");
	}

	json_string_del_last_chars(buf,1);

	return 0;
}

int json_get_token_value_from_path(struct json_string *buf,int *data_type,struct json *j, char *json_path, char *token)
{
	struct json_obj *found;
	struct json_obj *obj;
	obj=json_obj_find_by_path(&(j->obj), json_path);
	if (obj==NULL)
	{
		return -1;
	}

	found=json_obj_find(obj, token);
	if (found==NULL)
	{
		return -1;
	}

	json_string_cat(buf,found->data);

	*data_type=found->data_type;

	return 0;
}

int json_is_token_from_path(struct json *j, char *json_path, char *token)
{
	struct json_obj *found;
	struct json_obj *obj;
	obj=json_obj_find_by_path(&(j->obj), json_path);
	if (obj==NULL)
	{
		return -1;
	}

	if (strcmp(token,"")==0)
	{
		return 0;
	}

	found=json_obj_find(obj, token);
	if (found==NULL)
	{
		return -1;
	}

	return 0;
}

int json_set_token_value_using_path(struct json *j, char *json_path, char *token, char *value)
{
	int ret;
	struct json_obj *obj;
	obj=json_obj_find_by_path(&(j->obj), json_path);
	if (obj==NULL)
	{
		return -1;
	}

	ret=json_set_data_string(obj,token, value);

	return ret;
}

int json_get_all_sim_modes(struct json_string *buf,struct json *j)
{
	int i;
	int ii;
	int added=0;
	int segments;
	struct json_obj *obj;
	struct json_obj *objs;
	struct json_obj *sims;
	struct json_obj *sim;
	char temp_str[100];
	sims=json_obj_find(&(j->obj), "sims");
	if (sims==NULL)
	{
		printf("sims not found\n");
		return -1;
	}
	objs=sims->objs;
	//printf("%d\n",sims->len);
	
	for (i=0;i<sims->len;i++)
	{
		sim=&(objs[i]);

		json_get_int(NULL,sim, &segments,"segments",TRUE);
		added=0;
		for (ii=0;ii<segments;ii++)
		{
			sprintf(temp_str,"segment%d",ii);
			obj=json_obj_find(sim, temp_str);
			if (obj==NULL)
			{
				printf("json_get_all_sim_modes: Object %s not found\n",temp_str);
				return -1;
			}
			//uid,name,icon,segment,module
			json_get_string(NULL, obj, temp_str,"id",TRUE);
			json_string_cat(buf,temp_str);
			json_string_cat(buf,"|");
			json_get_string(NULL, obj, temp_str,"name",TRUE);
			json_string_cat(buf,temp_str);
			json_string_cat(buf,"|");
			json_get_string(NULL, obj, temp_str,"icon",TRUE);
			json_string_cat(buf,temp_str);
			json_string_cat(buf,"|");
			sprintf(temp_str,"segment%d",ii);
			json_string_cat(buf,temp_str);
			json_string_cat(buf,"|");
			json_string_cat(buf,sim->name);
			json_string_cat(buf,"*");
			added++;
		}

		if (added>0)
		{
			if (i!=sims->len-1)
			{
				json_string_cat(buf,"vline*");
			}
		}

	}

	if (buf->pos>2)
	{
		//printf("'%s %c'\n",buf->data,buf->data[buf->pos-1]);
		if (buf->data[buf->pos-1]=='*')
		{
			buf->data[buf->pos-1]=0;
		}
	}
	if (buf->pos<=0)
	{
		return -1;
	}
	return 0;
}

int json_delete_token_using_path(struct json *j, char *json_path, char *token)
{
	int ret;
	struct json_obj *obj;
	obj=json_obj_find_by_path(&(j->obj), json_path);
	if (obj==NULL)
	{
		return -1;
	}

	ret=json_obj_delete_node(obj, token);

	return ret;
}

struct json_obj *json_add_bib_item_at_path(struct json *j, char *json_path, char *token)
{

	struct json_obj *obj;
	struct json_obj *bib_obj;
	obj=json_obj_find_by_path(&(j->obj), json_path);
	if (obj==NULL)
	{
		return NULL;
	}

	bib_obj=json_add_bib_item(j, obj, token);

	return bib_obj;
}

int json_search_for_token_value_in_path(char *path, struct json *j, char *token, char *value)
{
	struct json_obj *ret=NULL;
	char path_tmp[OGHMA_PATH_MAX];
	struct json_obj *obj;
	strcpy(path_tmp,path);
	obj=json_obj_find_by_path(&(j->obj), path_tmp);

	if (obj==NULL)
	{
		return -1;
	}

	ret=json_search_for_token_value(path_tmp, obj, token, value);
	//printf("found> %s %s\n",path_tmp,value);
	if (ret!=NULL)
	{
		strcpy(path,path_tmp);
		return 0;
	}else
	{
		strcpy(path,"not found");
		return -1;
	}
	return -1;
}

int json_py_add_segment(char *new_segment_path, char *path,struct json *j,char *human_name, int pos)
{
	struct json_obj *ret;

	ret=json_segments_add_by_path(&(j->obj),path,human_name, pos);
	if (ret==NULL)
	{
		return -1;
	}

	strcpy(new_segment_path,path);
	strcat(new_segment_path,".");
	strcat(new_segment_path,ret->name);

	return 0;
}

int json_delete_segment_by_path(struct json *j, char *path, char *segment_name)
{
	int ret=0;
	struct json_obj *obj;
	obj=json_obj_find_by_path(&(j->obj), path);

	if (obj==NULL)
	{
		return -1;
	}

	ret=json_delete_segment(obj, segment_name);

	return ret;
}

int json_clone_segment(char *new_segment_path, char *root_path,char *src_segment, struct json *j,char *new_human_name)
{
	int segments;
	char new_segment_name[100];
	struct json_obj *obj_root;
	struct json_obj *next_obj;
	struct json_obj *obj_src_segment;
	struct json_obj *segment_obj;
	struct json_obj *segment_obj_human_name;

	obj_root=json_obj_find_by_path(&(j->obj), root_path);

	if (obj_root==NULL)
	{
		//printf("1\n");
		return -1;
	}

	obj_src_segment=json_obj_find_by_path(obj_root, src_segment);
	if (obj_src_segment==NULL)
	{
		//printf("2 %s\n",src_segment);
		return -1;
	}

	if (json_get_int(NULL, obj_root, &segments,"segments",FALSE)==-1)
	{
		//printf("3\n");
		return -1;
	}

	sprintf(new_segment_name,"segment%d",segments);

	segments++;
	segment_obj=json_obj_find(obj_root, "segments");
	sprintf(segment_obj->data,"%d",segments);

	next_obj=json_obj_add(obj_root,new_segment_name,"",JSON_NODE);
	json_obj_all_free(next_obj);
	json_obj_cpy(next_obj,obj_src_segment);
	strcpy(next_obj->name,new_segment_name);

	strcpy(new_segment_path,root_path);
	strcat(new_segment_path,".");
	strcat(new_segment_path,new_segment_name);

	segment_obj_human_name=json_obj_find(next_obj, "name");
	strcpy(segment_obj_human_name->data,new_human_name);

	json_update_random_ids(next_obj);

	return 0;
}

int json_py_add_obj_double(struct json *j,char *root_path,char *token, double value)
{
	struct json_obj *obj_root;
	obj_root=json_obj_find_by_path(&(j->obj), root_path);
	json_obj_add_double(obj_root,token,value);
	return 0;
}

int json_py_add_obj_int(struct json *j,char *root_path,char *token, int value)
{
	char tmp[400];
	struct json_obj *obj_root;
	obj_root=json_obj_find_by_path(&(j->obj), root_path);
	sprintf(tmp,"%d",value);
	json_obj_add_int(obj_root,token,value);
	return 0;
}

int json_py_add_obj_bool(struct json *j,char *root_path,char *token, int value)
{
	struct json_obj *obj_root;
	obj_root=json_obj_find_by_path(&(j->obj), root_path);
	json_obj_add_bool(obj_root,token,value);
	return 0;
}

int json_py_add_obj_string(struct json *j,char *root_path,char *token, char *value)
{
	struct json_obj *obj_root;
	obj_root=json_obj_find_by_path(&(j->obj), root_path);
	json_obj_add_string(obj_root,token,value);
	return 0;
}

int json_py_segments_swap(struct json *j,char *root_path,int i0, int i1)
{
	struct json_obj *obj_root;

	obj_root=json_obj_find_by_path(&(j->obj), root_path);

	if (obj_root==NULL)
	{
		return -1;
	}

	json_segments_swap(obj_root, i0, i1);

	return 0;
}

int json_py_import_json_to_obj(struct json *j,char *path,char *import_json_as_text)
{
	int len;

	struct json_obj *obj;

	obj=json_obj_find_by_path(&(j->obj), path);

	if (obj==NULL)
	{
		return -1;
	}

	len=strlen(import_json_as_text);

	json_import_ojb_from_buffer(j,obj,import_json_as_text,len);

	json_update_random_ids(obj);

	return 0;
}

int json_py_init_rand()
{
	srand(time(NULL));
	return 0;
}

int json_py_to_latex(struct json_string *buf,struct json *j, char *json_path,struct hash_list *token_lib)
{
	struct json_obj *obj;

	obj=json_obj_find_by_path(&(j->obj), json_path);

	if (obj==NULL)
	{
		return -1;
	}

	json_to_latex(buf,obj,token_lib);

	return 0;
}

int json_py_isnode(struct json *j, char *json_path)
{
	struct json_obj *obj;
	obj=json_obj_find_by_path(&(j->obj), json_path);
	if (obj==NULL)
	{
		return -1;
	}

	if (obj->data_type==JSON_NODE)
	{
		return 0;
	}

	return -1;
}

int json_py_clear_segments(struct json *j, char *json_path)
{
	int ret;
	struct json_obj *obj;
	//printf("%s\n",json_path);
	obj=json_obj_find_by_path(&(j->obj), json_path);
	if (obj==NULL)
	{
		return -1;
	}

	ret=json_clear_segments(obj);
	return ret;
}



