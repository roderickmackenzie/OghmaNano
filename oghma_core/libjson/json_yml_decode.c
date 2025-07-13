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

/** @file buffer.c
@brief used to save output files to disk with a nice header, so the user knows what was writtne to them
*/

#include <sys/stat.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>
#include "util.h"
#include "dat_file.h"
#include "cal_path.h"
#include "dump.h"
#include <log.h>
#include <g_io.h>
#include <triangle.h>
#include <triangles.h>
#include <json.h>
#include <color.h>
#include <ctype.h>

int json_yml_decode_line(int *indent,char *pre,char *token,char *data, char *line)
{
	int i;
	int tmp;
	int len=strlen(line);
	int found_alpha=FALSE;
	char c='*';

	int data_pos=0;

	int token_pos=0;
	int token_search_blocked=FALSE;

	token[0]=0;
	data[0]=0;
	pre[0]=0;

	for (i=0;i<len;i++)
	{
		c=line[i];

		//comments
		if (c=='#')
		{
			break;
		}

		if (token_search_blocked==FALSE)
		{
			//pre char search and also detecting first char
			if (found_alpha==FALSE)
			{
				if (c=='-')
				{
					tmp=strlen(pre);
					pre[tmp]=c;
					pre[tmp+1]=0;
				}else
				if (isalpha(c)!=0)		//if a-z A-z
				{
					found_alpha=TRUE;
				}else
				if (isspace(c)==0)	//if not space
				{
					token_search_blocked=TRUE;
				}
				*indent=i;
			}
			//printf("%d %s\n",found_alpha,token);
			if (found_alpha==TRUE)
			{
				if ((isalpha(c)==0)&&(c!='_'))		//It's not a char
				{
					if (c==':')
					{
						//token_found=TRUE;
						data_pos=0;
						data[data_pos]=0;
						token_search_blocked=TRUE;
						continue;
					}else
					{
						//printf("oh here '%c'\n",c);
						token[0]=0;
						token_search_blocked=TRUE;
					}
				}else
				{
					token[token_pos++]=c;
					token[token_pos]=0;
				}
			}
		}	//end token search

		data[data_pos++]=c;
		data[data_pos]=0;
	}

	remove_space_after(data);
	remove_space_before(data);

	//printf("found token: %s\m",token);

	return 0;
}

/*int json_yml_peek_segment(struct json *j)
{
	int i;
	char c;
	for (i=j->pos;i<j->raw_data_len;i++)
	{
		c=j->raw_data[i];

		if (c=='-')
		{
			j->raw_data[i]=" ";
			return 0;
		}

		if (c=='#')
		{
			return -1;
		}

		if (isspace(c)==0)	//If it is not a space or -
		{
			return -1;
		}

		if ((c == '\r')||(c == '\n'))	//If it is new line
		{
			-1;
		}

	}

	return -1;
}*/

int json_yml_remove_dash(struct json *j)
{
	int i;
	char c;
	for (i=j->pos;i<j->raw_data_len;i++)
	{
		c=j->raw_data[i];

		if (c=='-')
		{
			j->raw_data[i]=' ';
			return 0;
		}

	}

	return -1;
}

int json_yml_decode(struct json *j,struct json_obj *obj,int indent_in)
{
	int ret=0;
	char line[STR_MAX];
	char pre[200];
	char token[200];
	char data[200];
	char tmp[100];
	//int in_ref=FALSE;
	int indent;
	int max_len;
	char *data_build=NULL;
	long last_pos=j->pos;
	int segments=0;
	int data_last_len=0;
	struct json_obj *this_obj=NULL;
	strcat_malloc(&data_build,&max_len, "");

	ret=get_line(line,j->raw_data,j->raw_data_len,&j->pos,sizeof(line));
	while(ret!=-1)
	{

		//printf("'%s'\n",line);
		
		json_yml_decode_line(&indent,pre,token,data,line);
		data_last_len=strlen(data_build);
		if (data_last_len>0)
		{
			strcat_malloc(&data_build,&max_len, "\n");
		}
		strcat_malloc(&data_build,&max_len, data);
		//printf("token! %d '%s' '%s'\n",indent,token,data_build);
		//getchar();

		if (strcmp(token,"")!=0)
		{
			//json_obj_add(obj,token,out,guessed_value_type);
			if (this_obj!=NULL)
			{
				if (strcmp(data_build,"")!=0)
				{
					//printf(">>>>\n");
					//json_dump_obj(&(j->obj));
					json_set_data(this_obj,data_build);
					//json_dump_obj(&(j->obj));
					//printf("after2\n");
					//getchar();
				}
			}

			//printf("token! data_build=%s '%s'\n",token,data_build);
			//getchar();
			//printf("indents: %d %d\n",indent,indent_in);

			if (strcmp(pre,"-")==0)		//its a segment
			{
				
				if (indent==indent_in)		//detect another list item on same level
				{
					//printf("----> '%s' %d %p\n",data_build,data_last_len,this_obj);
					if (this_obj!=NULL)					//If we have an open object
					{
						if (strlen(data_build)>0)		//empty what we have built
						{
							data_build[data_last_len]=0;
							json_set_data(this_obj,data_build);
						}
					}
					//printf("new segment same level!\n");

					if (data_build!=NULL)
					{
						free(data_build);
					}

					j->pos=last_pos;
					return 0;
				}else 						//new list item.
				{
					sprintf(tmp,"segment%d",segments++);
					//printf("ADD!!!!!!!!!!!!!!! %s\n",tmp);
					//json_dump_obj(&(j->obj));
					this_obj=json_obj_find(obj, "segments");
					if (this_obj==NULL)
					{
						json_obj_add_int(obj,"segments", segments);
					}else
					{
						json_set_data_int(obj,"segments",segments);
					}
					
					this_obj=json_obj_add(obj,tmp,"",JSON_NODE);
					j->pos=last_pos;
					json_yml_remove_dash(j);		//remove dash and have another go at the line
					//json_dump_obj(&(j->obj));
					//printf("after!\n");
					//getchar();
					int r=json_yml_decode(j,this_obj,indent);
					this_obj=NULL;
					//printf("back to here\n");
					//segments++;
					if (r==-2)
					{
						return 0;
					}
				}

			}else
			if (indent<indent_in)		//detect another list item on same level
			{
				if (this_obj!=NULL)
				{
					if (strlen(data_build)>0)		//empty what we have built
					{
						data_build[data_last_len]=0;
						json_set_data(this_obj,data_build);
					}
				}
				//printf("new segment same level!\n");

				if (data_build!=NULL)
				{
					free(data_build);
				}

				j->pos=last_pos;
				//printf("POP!\n");
				return -2;
			}else
			if (strcmp(data,"")==0)		//its a new node
			{
				this_obj=json_obj_add(obj,token,"",JSON_NODE);
				//printf("NEST!\n");
				int r=json_yml_decode(j,this_obj,indent);
				if (r==-2)
				{
					return 0;
				}
			}else
			if (strcmp(data,"|")==0)		//its a split string
			{
				this_obj=json_obj_add(obj,token,"",JSON_STRING);
				data_build[0]=0;
			}else 							//it has data
			{
				//printf("HERE!\n");
				this_obj=json_obj_add(obj,token,data,JSON_STRING);
				this_obj=NULL;
			}

			data_build[0]=0;
		}

		//json_dump_obj(&(j->obj));
		//printf("indent=%d\n",indent);
		//printf("pre=%s\n",pre);
		//printf("token=%s\n",token);
		//printf("data=%s\n",data);
		//printf("data_build='%s'\n",data_build);

		//getchar();


		last_pos=j->pos;

		//segment_start=json_yml_peek_segment(j);
		ret=get_line(line,j->raw_data,j->raw_data_len,&j->pos,sizeof(line));
	}

	if (this_obj!=NULL)
	{
		if (strlen(data_build)>0)
		{
			json_set_data(this_obj,data_build);
		}
	}

	//json_dump_obj(&(j->obj));

	if (data_build!=NULL)
	{
		free(data_build);
	}

	return 0;

}


