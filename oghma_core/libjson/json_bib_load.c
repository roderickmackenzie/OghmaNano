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
#include <savefile.h>

int json_bib_get_uid(char *uid,char *line)
{
	int pos=-1;
	int len=-1;
	if (strcmp_begin(line,"@article")==0)
	{
		if (strcmp_end(line,",")==0)
		{
			pos=str_get_char_first_pos(line,'{');
			strcpy(uid,line+pos+1);
			len=strlen(uid);
			uid[len-1]=0;
			return 0;
		}
	}

	return -1;
}

int json_bib_get_token(char *token,char *line)
{
	char temp[STR_MAX];
	int pos=-1;
	strcpy(temp,line);
	pos=str_get_char_first_pos(temp,'=');
	if (pos==-1)
	{
		return -1;
	}

	temp[pos]=0;
	remove_space_after(temp);
	remove_space_before(temp);
	strcpy(token,temp);
	return 0;
}

int json_bib_get_value(char *value,char *line)
{
	char temp[STR_MAX];
	int pos=-1;
	strcpy(temp,line);
	pos=str_get_char_first_pos(temp,'=');
	if (pos==-1)
	{
		return -1;
	}
	str_remove_before(temp, '=');
	remove_space_after(temp);
	remove_space_before(temp);

	str_remove_before(temp, '{');
	split_reverse(temp, '}');
	strcpy(value,temp);
	return 0;
}

int json_bib_decode(struct json *j,struct json_obj *obj_a)
{
	int ret=0;
	char line[STR_MAX];
	int in_ref=FALSE;
	long pos=0;
	int bra_ket=0;
	char temp[STR_MAX];
	char token[STR_MAX];
	char value[STR_MAX];
	struct json_obj *obj=&(j->obj);
	struct json_obj *json_bib_entry;
	struct json_obj *json_bib_item;


	ret=get_line(line,j->raw_data,j->raw_data_len,&pos,sizeof(line));
	while(ret!=-1)
	{
		if (ret>0)
		{
			remove_space_after(line);
			remove_space_before(line);
		}

		if (strcmp_begin(line,"@article")==0)
		{
			if (in_ref==TRUE)
			{
				return -1;
			}

			json_bib_get_uid(temp,line);
			//printf("\n\nID: %s\n",temp);
			json_bib_entry=json_obj_add(obj,temp,"",JSON_NODE);
			json_template_bib(json_bib_entry);
			//json_obj_all_free(json_bib_entry);
			//json_obj_cpy(json_bib_entry,obj->json_template);
			strcpy(json_bib_entry->name,temp);
			in_ref=TRUE;
		}
		bra_ket+=str_count_char(line, '{')-str_count_char(line, '}');

		if (in_ref==TRUE)
		{
			if (json_bib_get_token(token,line)==0)
			{

				if (json_bib_get_value(value,line)==0)
				{
					//json_dump_obj(json_bib_entry);
					json_bib_item=json_obj_find(json_bib_entry, token);
					if (json_bib_item!=NULL)
					{
						json_set_data_string(json_bib_entry,token,value);
					}
					//printf("%s %p|",token,json_bib_item);
					//printf("%s\n",value);
				}
			}
		}
		if (bra_ket==0)
		{
			in_ref=FALSE;
		}

		//printf("'%s' %d\n",line,bra_ket);

		ret=get_line(line,j->raw_data,j->raw_data_len,&pos,sizeof(line));
	}

	//json_dump_obj(&(j->obj));
	return 0;

}


