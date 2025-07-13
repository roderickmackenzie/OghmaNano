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

int json_dump_settings_init(struct json_dump_settings *settings)
{
	settings->show_private=FALSE;
	settings->show_templates=FALSE;
	return 0;
}

void remove_comma(struct json_string *buf)
{
	int i;
	int len=buf->pos;
	for (i=len-1;i>0;i--)
	{
		if (buf->data[i]==',')
		{
			buf->data[i]=0;
			buf->pos=i;
			return;
		} 
	}

}

int json_save(struct json *j)
{
	int ret;
	ret=json_save_as(NULL,j->file_path,j);
	return ret;
}

int json_save_as(struct simulation *sim,char *file_name,struct json *j)
{
	int ret;
	int level=0;
	struct json_string s;
	struct json_dump_settings settings;
	json_dump_settings_init(&settings);
	settings.show_private=FALSE;
	json_string_init(&s);

	if (j->compact==TRUE)
	{
		s.compact=TRUE;
		level=-1;
	}else
	{
		level=0;
	}

	if (j->bib_file==FALSE)
	{
		json_dump_to_string(&s,&(j->obj),level,&settings);
	}else
	{
		json_dump_bib_to_string(&s,&(j->obj),&settings);
	}
	ret=zip_write_buffer(sim,file_name,s.data, s.pos);
	json_string_free(&s);

	return ret;
}

int json_obj_save_as(struct simulation *sim,char *file_name,struct json_obj *j)
{
	int ret;
	struct json_dump_settings settings;
	json_dump_settings_init(&settings);
	struct json_string s;
	json_string_init(&s);
	json_dump_to_string(&s,j,0,&settings);
	ret=zip_write_buffer(sim,file_name,s.data, s.pos);
	json_string_free(&s);
	return ret;
}



void json_dump_to_string(struct json_string *buf,struct json_obj *obj,int level, struct json_dump_settings *settings)
{
	json_string_cat(buf,"{\n");
	json_dump(obj,buf,level,settings);
	remove_comma(buf);
	json_string_cat(buf,"\n}\n");
}

void tabs(struct json_string *buf,int number)
{
	if (buf->compact==TRUE)
	{
		return;
	}

	int i;
	char temp[200];
	if (number!=-1)
	{
		for (i=0;i<number;i++)
		{
			temp[i]='\t';
		}
		temp[number]=0;
		json_string_cat(buf,temp);
	}
}

void json_dump_obj(struct json_obj *obj)
{
	struct json_string s;
	struct json_dump_settings settings;
	json_dump_settings_init(&settings);
	json_string_init(&s);
	settings.show_templates=TRUE;
	settings.show_private=TRUE;
	printf("name: %s\n",obj->name);
	printf("len: %d\n",obj->len);
	printf("max_len: %d\n",obj->max_len);
	printf("objs: %p\n",obj->objs);
	printf("data (addr): %p\n",obj->data);
	printf("data: %s\n",obj->data);
	printf("data_len: %d\n",obj->data_len);
	printf("data_type: %d\n",obj->data_type);
	json_dump_to_string(&s,obj,0,&settings);
	printf("%s\n",s.data);
	json_string_free(&s);
}

void json_dump(struct json_obj *obj,struct json_string *buf, int level, struct json_dump_settings *settings)
{
	int i;
	int add=TRUE;
	int add_quotes=FALSE;
	char *temp;
	if (level!=-1)
	{
		level++;
	}
	struct json_obj *objs;
	struct json_obj *next_obj;
	objs=(struct json_obj* )obj->objs;
	for (i=0;i<obj->len;i++)
	{
		next_obj=&(objs[i]);

		if (next_obj->data_type==JSON_NODE)
		{
			tabs(buf,level);

			json_string_cat(buf,"\"");
			json_string_cat(buf,next_obj->name);
			json_string_cat(buf,"\": {\n");

			json_dump(next_obj,buf,level,settings);

			if (settings->show_templates==TRUE)
			{
				if (next_obj->json_template!=NULL)
				{
					char temp[100];
					struct json_obj *my_template=(struct json_obj *)(next_obj->json_template);
					sprintf(temp,"len: %d %d %s\n",my_template->data_len,my_template->len,my_template->name);
					tabs(buf,level+1);
					json_string_cat(buf,temp);

					tabs(buf,level+1);
					json_string_cat(buf,"\"");
					json_string_cat(buf,((struct json_obj *)(next_obj->json_template))->name);
					json_string_cat(buf,"\": {\n");
					json_dump(next_obj->json_template,buf,level+1,settings);
					remove_comma(buf);
					json_string_cat(buf,"\n");
					tabs(buf,level+1);
					json_string_cat(buf,"\t},\n");
				}
			}

			remove_comma(buf);
			if (buf->compact==FALSE)
			{
				json_string_cat(buf,"\n");
				tabs(buf,level);
				json_string_cat(buf,"\t},\n");
			}else
			{
				json_string_cat(buf,"},");
			}


			//printf("'%s' %d\n",buf,*buf_pos);
			//getchar();
		}else
		{
			add=TRUE;
			if (settings->show_private==FALSE)
			{
				if (next_obj->data_flags & JSON_PRIVATE)
				{
					add=FALSE;
				}
			}
			//printf("%s %d %x\n",next_obj->name,add,next_obj->data_flags);
			if (add==TRUE)
			{
				add_quotes=FALSE;
				if (next_obj->data_type==JSON_STRING)
				{
					add_quotes=TRUE;
				}else
				if (next_obj->data_type==JSON_STRING_HEX)
				{
					add_quotes=TRUE;
				}else
				if (next_obj->data_type==JSON_RANDOM_ID)
				{
					add_quotes=TRUE;
				}else
				if (next_obj->data_type==JSON_BOOL)
				{
					add_quotes=TRUE;
				}else
				if (next_obj->data_type==JSON_DAT_FILE)
				{
					add_quotes=TRUE;
				}else
				if (strcmp(next_obj->data,"")==0)
				{
					add_quotes=TRUE;
				}

				tabs(buf,level);

				json_string_cat(buf,"\"");
				json_string_cat(buf,next_obj->name);
				json_string_cat(buf,"\":");

				if (add_quotes==TRUE)
				{
					json_string_cat(buf,"\"");
				}

				if (next_obj->data!=NULL)
				{
					if (next_obj->data_type==JSON_STRING_HEX)
					{
						temp=malloc(next_obj->data_len*3*sizeof(char));
						string_to_hex(temp,next_obj->data);
						json_string_cat(buf,temp);
						free(temp);
					}else
					if (next_obj->data_type==JSON_DAT_FILE)
					{
						json_string_cat(buf,"data_not_shown");
					}else
					{
						json_string_cat(buf,next_obj->data);
					}
				}else
				{
					json_string_cat(buf,"NULL");
				}

				if (add_quotes==TRUE)
				{
					json_string_cat(buf,"\"");
				}

				json_string_cat(buf,",\n");
			}

		}
	}
	if (level!=-1)
	{
		level--;
	}
}

void json_dump_buffer(struct json *j)
{
	int pos=0;
	while(pos<j->raw_data_len)
	{
		if (j->pos!=pos)
		{
			printf("%c",j->raw_data[pos]);
		}else
		{
			printf("*");
		break;
		}

		pos++;
	}
	
}

void json_dump_all(struct json *j)
{
	struct json_string s;
	struct json_dump_settings settings;
	json_dump_settings_init(&settings);
	json_string_init(&s);
	settings.show_templates=FALSE;
	settings.show_private=FALSE;
	//printf("file_path: %s\n",j->file_path);
	//printf("compact: %d\n",j->compact);
	//printf("is_template: %d\n",j->is_template);

	json_dump_to_string(&s,&(j->obj),0,&settings);
	printf("%s\n",s.data);
	json_string_free(&s);
}



