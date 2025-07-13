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

void gobble(struct json *j)
{
	while(j->pos<j->raw_data_len)
	{
		if (isspace(j->raw_data[j->pos])==0)	//If it is not white space
		{
			return;
		}

		j->pos++;

	}

	j->pos=j->raw_data_len-1;
	
}

int json_remove_last_item_from_path(struct json *j)
{
	int ff;
	int removed=0;
	for (ff=strlen(j->path)-1;ff>0;ff--)
	{
		if (j->path[ff]=='.')
		{
			j->path[ff]=0;
			removed=1;
			break;
		}
	}

	if (removed==0)
	{
		strcpy(j->path,"");
	}

	return 0;
}

void skip_past_next_ket(struct json *j)
{
	int sum=1;
	while(j->pos<j->raw_data_len)
	{
		if (j->raw_data[j->pos]=='}')	//If it is not white space
		{
			sum--;
		}else
		if (j->raw_data[j->pos]=='{')	//If it is not white space
		{
			sum++;
		}

		j->pos++;

		if (sum==0)
		{
			return;
		}

	}

	j->pos=j->raw_data_len-1;
	
}

void skip_array(struct json *j)
{
	if (j->raw_data[j->pos]=='[')
	{
		while(j->pos<j->raw_data_len)
		{
			if (j->raw_data[j->pos]==']')
			{
				j->pos++;
				if (j->pos>=j->raw_data_len)
				{
					j->pos=j->raw_data_len-1;
				}
				return;
			}

			j->pos++;
		}	
	}

	return;
}

void get_name(char *out,struct json *j)
{
	int i=0;
	strcpy(out,"");
	if (j->raw_data[j->pos]=='\"')
	{
		j->pos++;
	}else
	{
		printf("error no \" found '%c'\n",j->raw_data[j->pos]);
	}

	while(j->pos<j->raw_data_len)
	{
	//printf("%c\n",j->raw_data[j->pos]);
	//getchar();
		if (j->raw_data[j->pos]=='\"')
		{
			j->pos++;
			gobble(j);
			//getchar();
			if (j->raw_data[j->pos]==':')
			{
				j->pos++;
				return;
			}else
			{
				printf("Json error '%s'\n",out);
				exit(0);
			}
		}

		out[i]=j->raw_data[j->pos];
		out[i+1]=0;
		i++;
		j->pos++;

	}

	return;
}

void get_value(char *out,struct json *j, int debug,int *value_type)
{
	int i=0;
	strcpy(out,"");

	//Copy until , or }
	int in_quote=FALSE;
	while(j->pos<j->raw_data_len)
	{

		//This is to allow } and , inside of quotes.

		if (j->raw_data[j->pos]=='"')
		{
			if (j->pos>0)
			{
				if (j->raw_data[j->pos-1]!='\\')
				{
					in_quote = TRUE-in_quote;		//Flip between 1 and 0;
				}
			}
		}

		if (in_quote==FALSE)
		{
			if ((j->raw_data[j->pos]=='}')||(j->raw_data[j->pos]==','))
			{
				break;
			}
		}
		
		out[i]=j->raw_data[j->pos];

		if (i>STR_MAX)
		{
			out[i]=0;
			printf("json.c: The string is too long so far I have: '%s'.\n",out);
			exit(0);
		}
		i++;

		j->pos++;

	}
	out[i]=0;

	//Now try to remove the first and last quote if they exist
	//printf("%s\n",out);
	//printf("'%s'\n",out);
	if (remove_quotes(out)==0)
	{
		*value_type=JSON_STRING;
	}else
	{
		*value_type=JSON_INT;
	}
	//getchar();
	return;
}

void print_next_10(char *out,struct json *j)
{
	int i=0;

	while(j->pos<j->raw_data_len)
	{
		printf(">%c %d\n",j->raw_data[j->pos+i],j->raw_data[j->pos+i]);
		i++;

		if (i>10)
		{
			break;
		}
	}
}

int json_decode(struct json *j,struct json_obj *obj)
{
	//printf("'>>%d'\n",j->pos);
	int i;
	char token[100];
	char out[STR_MAX];
	int debug=FALSE;
	int decoded=FALSE;
	int guessed_value_type;
	struct json_obj *next_obj;
	struct json_obj *tmp_obj;
	gobble(j);
	//printf("OBJs: %p\n",obj->objs);
	//printf("'>>%d %d'\n",j->pos,j->is_template);
	if (j->raw_data[j->pos]=='{')
	{
		j->pos++;
	}else
	{
		j->level++;
	}
	//int step=FALSE;
	//printf("::%s\n",j->path);
	for (i=0;i<1000;i++)
	{
		gobble(j);
		get_name(token,j);
		//printf("TOKEN:%s\n",token);
		//if (strcmp(token,"html_link")==0)
		//{
		//	debug=TRUE;
		//}
		json_compat(j,token,NULL);		//compat layer

		gobble(j);

		skip_array(j);

		if (j->raw_data[j->pos]=='{')
		{
			if (strlen(j->path)!=0)
			{
				strcat(j->path,".");
			}
			strcat(j->path,token);
			
			j->pos++;
			gobble(j);
			//printf("%s %s %c\n",token,j->path,j->raw_data[j->pos]);
			//getchar();
			//printf(">> %c 1:'%c' 2:'%c' 3:'%c'\n",j->raw_data[j->pos-2],j->raw_data[j->pos-1],j->raw_data[j->pos],j->raw_data[j->pos+1]);
			//json_dump_buffer(j);
			if (j->is_template==TRUE)
			{
				//printf("TEMPLATE %s\n",token);
				next_obj=json_obj_find(obj,token);
				//printf(">%s %p\n",token,obj);
				//json_dump_obj(obj);

				if (next_obj!=NULL)
				{
					json_decode(j,next_obj);
				}else
				{
					decoded=FALSE;
					//printf("%s %s\n",j->path,token);
					if (obj->json_template!=NULL)
					{
						//json_compat(j,token,NULL);
						if (strcmp_begin(token,"segment")==0)
						{
							if (strcmp_begin(token,"segments")!=0)
							{
								//printf("copy %s\n",token);
								next_obj=json_obj_add(obj,token,"",JSON_NODE);
								json_obj_all_free(next_obj);
								json_obj_cpy(next_obj,obj->json_template);
								strcpy(next_obj->name,token);
								//json_dump_obj(next_obj);
								json_decode(j,next_obj);
								decoded=TRUE;

							}
						}
					}

					if (strcmp_begin(token,"bib_")==0)
					{
						next_obj=json_add_bib_item(j, obj, token);
						json_decode(j,next_obj);
						decoded=TRUE;
					}

					if (decoded==FALSE)
					{
						//printf("SKIP!\n");
						skip_past_next_ket(j);
						json_remove_last_item_from_path(j);
					}
				}

			}else
			{

				next_obj=json_obj_add(obj,token,"",JSON_NODE);
				//printf("DECODE\n");
				json_decode(j,next_obj);
			}
			//json_dump_buffer(j);
			//printf("I am about to decode another\n");
			//getchar();
			
			//get_name(token,j);
			strcpy(out,"none");
		}else
		{
			//if (debug==TRUE)
			//{
			//	printf("%s token=|%s|\n",j->path,token);
			//}
			get_value(out,j,debug,&guessed_value_type);
			json_compat(j,token,out);

			if (j->is_template==TRUE)
			{
				tmp_obj=json_obj_find(obj,token);
				//printf("%s %p\n",token,tmp_obj);
				//json_dump_obj(obj);
				if (tmp_obj!=NULL)
				{
					if (tmp_obj->data_type==JSON_STRING_HEX)
					{
						hex_to_string(out);
					}
					json_set_data(tmp_obj,out);
				}
			}else
			{
				json_obj_add(obj,token,out,guessed_value_type);
			}
			//if (debug==TRUE)
			//{
			//	printf("value=|%s|\n",out);
			//}
			//print_next_10(out,j);
			//getchar();
			//tmp_obj=
			
			//printf("%d\n",guessed_value_type);
			//getchar();
		}

		if (j->level==-1)
		{
			//printf("level=0 exit!!!!!!!!!\n");
			return 0;
		}

		//if (strcmp(j->path,"sim")==0)
		//{
		//	printf("%d: path=%s %s=|%s|\n",j->level,j->path,token,out);
		//}
		gobble(j);

		if (j->raw_data[j->pos]==',')
		{
			j->pos++;
		}

		if (j->raw_data[j->pos]=='}')
		{
			//printf("yes\n");
			j->pos++;
			if (j->raw_data[j->pos]==',')
			{
				j->pos++;
			}
			j->level--;
			json_remove_last_item_from_path(j);
			//printf("exit here!!!!!!!!!\n");

			return 0;
		}

	}
	return 0;

}

int json_load_from_path(struct simulation *sim,struct json *j,char *path,char *file_name)
{
	char full_file_name[PATH_MAX];
	join_path(2,full_file_name,path,file_name);
	//printf("%s\n",full_file_name);
	return json_load(sim,j,full_file_name);
}

int json_load(struct simulation *sim,struct json *j,char *full_file_name)
{
	int ret;
	strcpy(j->file_path,full_file_name);
	if (strcmp_end(full_file_name,".bib")==0)
	{
		j->bib_file=TRUE;
	}else
	if (strcmp_end(full_file_name,".yml")==0)
	{
		j->yml_file=TRUE;
	}

	//printf("%s\n",full_file_name);
	//getchar();
	if (isfile(full_file_name)==0)
	{
		ret=g_read_file_to_buffer(&(j->raw_data), &j->raw_data_len,full_file_name,-1);

		if (ret!=0)
		{
			j->pos=0;
			return ret;
		}

		if (sim!=NULL)
		{
			sim->files_read++;
			sim->bytes_read+=j->raw_data_len;
			log_write_file_access(sim,full_file_name,'r');
		}

		if (j->bib_file==TRUE)
		{
			json_bib_decode(j,&(j->obj));
		}else
		if (j->yml_file==TRUE)
		{
			json_yml_decode(j,&(j->obj),0);
		}else
		{
			json_decode(j,&(j->obj));
		}

		free_1d((void **)&(j->raw_data));
		//json_dump_obj(&(j->obj));
		//getchar();
		j->pos=0;
		return 0;

	}
	else
	{	
		char zip_path[OGHMA_PATH_MAX];
		char file_path[OGHMA_PATH_MAX];
		char file_name[OGHMA_PATH_MAX];

		get_dir_name(file_path,full_file_name);
		get_file_name_from_path(file_name,full_file_name,1000);

		join_path(2,zip_path,file_path,"sim.oghma");
		//printf("OK %s\n",zip_path);
		int err = 0;
		struct zip *z = zip_open(zip_path, 0, &err);

		if (z!=NULL)
		{
			//Search for the file of given name
			struct zip_stat st;
			zip_stat_init(&st);
			int ret=zip_stat(z, file_name, 0, &st);

			if (ret==0)
			{
				//Alloc memory for its uncompressed contents
				j->raw_data_len=st.size*sizeof(char);
				j->raw_data = (char *)malloc((j->raw_data_len+1)*sizeof(char));
				if (sim!=NULL)
				{
					sim->bytes_read+=j->raw_data_len;
				}

				//Read the compressed file
				struct zip_file *f = zip_fopen(z, file_name, 0);

				if (sim!=NULL)
				{
					sim->files_read++;
				}

				if (f==NULL)
				{
					free_1d((void **)&(j->raw_data));
					zip_close(z);
					j->pos=0;
					return -1;
				}

				ret=zip_fread(f, j->raw_data, st.size);
				if (ret==-1)
				{
					free_1d((void **)&(j->raw_data));
					zip_fclose(f);
					zip_close(z);
					j->pos=0;
					return -1;
				}

				zip_fclose(f);
				j->raw_data[j->raw_data_len]=0;
			}else
			{

				zip_close(z);
				j->pos=0;
			 	return -1;
			}

			zip_close(z);

			if (j->bib_file==TRUE)
			{
				json_bib_decode(j,&(j->obj));
			}else
			if (j->yml_file==TRUE)
			{
				json_yml_decode(j,&(j->obj),0);
			}else
			{
				json_decode(j,&(j->obj));
			}

			free_1d((void **)&(j->raw_data));
			j->pos=0;
			return 0;
		}

	}

	return -1;
}
