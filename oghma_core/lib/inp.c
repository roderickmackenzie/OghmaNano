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

/** @file inp.c
	@brief Input file interface, files can be in .oghma files or stand alone files.
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zip.h>
#include <unistd.h>
#include <fcntl.h>
#include "inp.h"
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <list.h>
#include <g_io.h>


void inp_listdir(struct simulation *sim, char *dir_name,struct list *out)
{
char sim_file[PATH_MAX];
int mylen=0;
int i=0;
int err = 0;
char temp[200];

join_path(2,sim_file,dir_name,"sim.oghma");

out->names=(char**)malloc(sizeof(char*)*2000);
out->len=0;

struct zip *z = zip_open(sim_file, 0, &err);

if (z!=NULL)
{
	int files=zip_get_num_files(z);
	for (i=0;i<files;i++)
	{
		strcpy(temp,zip_get_name(z, i, ZIP_FL_UNCHANGED));
		if (list_cmp(out,temp)!=0)
		{
			if ((strcmp(temp,".")!=0)&&(strcmp(temp,"..")!=0))
			{
				mylen=strlen(temp);
				out->names[out->len]=(char*)malloc(sizeof(char)*(mylen+1));
				strcpy(out->names[out->len],temp);
				out->len++;
			}
		}

	}

	zip_close(z);

}

struct find_file find;

if (find_open(&find,dir_name)==0)
{
	while(find_read(&find)==0)
	{
		if ((strcmp(find.file_name,".")!=0)&&(strcmp(find.file_name,"..")!=0))
		{
			mylen=strlen(find.file_name);
			out->names[out->len]=(char*)malloc(sizeof(char)*(mylen+1));
			strcpy(out->names[out->len],find.file_name);
			out->len++;
		}
	}

find_close(&find);

}

}


int inp_isfile(struct simulation *sim,char *full_file_name)
{
FILE *f = g_fopen(full_file_name, "rb");
if (f!=NULL)
{
	sim->files_read++;
	fclose(f);
	return 0;
}else
{
	return zip_is_in_archive(full_file_name);
}
//#endif
return -1;
}


void inp_reset_read(struct simulation *sim,struct inp_file *in)
{
in->pos=0;
}

int inp_get_string(struct simulation *sim,char *out, struct inp_file *in)
{
	if (in->pos>=in->fsize)
	{
		return -1;
	}

	get_line(out,in->data,in->fsize,&in->pos,-1);

	return 0;
}




int inp_read_buffer(struct simulation *sim,char **buf, long *len,char *full_file_name)
{

if (isfile(full_file_name)==0)
{
	if (g_read_file_to_buffer(buf, len,full_file_name,-1)!=0)
	{
		return -1;
	}

	sim->files_read++;
	sim->bytes_read+=*len;
	log_write_file_access(sim,full_file_name,'r');


	return 0;

}else
{
	char zip_path[OGHMA_PATH_MAX];
	char file_path[OGHMA_PATH_MAX];
	char file_name[OGHMA_PATH_MAX];

	get_dir_name_from_path(file_path,full_file_name);
	get_file_name_from_path(file_name,full_file_name,OGHMA_PATH_MAX);

	join_path(2,zip_path,file_path,"sim.oghma");

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
			*len=st.size*sizeof(char);
			*buf = (char *)malloc((*len+1)*sizeof(char));
			sim->bytes_read+=*len;

			//Read the compressed file
			struct zip_file *f = zip_fopen(z, file_name, 0);
			sim->files_read++;
			if (f==NULL)
			{
				free(buf);
				zip_close(z);
				return -1;
			}

			ret=zip_fread(f, *buf, st.size);
			if (ret==-1)
			{
				free(buf);
				zip_fclose(f);
				zip_close(z);
				return -1;
			}

			zip_fclose(f);
			(*buf)[*len]=0;
		}else
		{

			zip_close(z);
		 	return -1;
		}

		zip_close(z);

		return 0;
	}else
	{
		return -1;
	}

}

}

void inp_init(struct simulation *sim,struct inp_file *in)
{
strcpy(in->full_name,"");
in->data=NULL;
in->fsize=0;
in->pos=0;
in->edited=FALSE;
}

int inp_load_from_path(struct simulation *sim,struct inp_file *in,char *path,char *file)
{
int ret=0;
char full_path[OGHMA_PATH_MAX];
join_path(2,full_path,path,file);
ret=inp_load(sim,in,full_path);
return ret;
}

void inp_load_from_buffer(struct simulation *sim,struct inp_file *in,char *file,char *buffer,int len)
{
	in->pos=0;


	if (in->data!=NULL)
	{
		inp_free(sim,in);
	}

	strcpy(in->full_name,file);

	in->fsize=len;
	in->data=malloc((len+1)*sizeof(char));
	memcpy(in->data, buffer, len*sizeof(char));
	in->data[len]=0;
	in->edited=FALSE;

}

int inp_load(struct simulation *sim,struct inp_file *in,char *file)
{
int ret=0;
in->pos=0;
if (strcmp(in->full_name,file)!=0)
{

	if (in->data!=NULL)
	{
		inp_free(sim,in);
	}

	strcpy(in->full_name,file);
	if (inp_read_buffer(sim,&(in->data),&(in->fsize),file)!=0)
	{
		ret= -1;
	}

	in->edited=FALSE;
}

return ret;
}


void inp_replace_double(struct simulation *sim,struct inp_file *in,char *token, double value)
{
	char temp[100];
	sprintf(temp,"%le",value);
	inp_replace(sim,in,token,temp);
}

void inp_replace(struct simulation *sim,struct inp_file *in,char *token, char *text)
{
inp_replace_offset(sim,in,token, text,0);
}


void inp_replace_offset(struct simulation *sim,struct inp_file *in,char *token, char *text,int offset)
{
int i=0;
char *temp = malloc(in->fsize + 100);
memset(temp, 0, in->fsize + 100);
//char *line;
int len=0;
long pos=0;
int ret=0;
char line[in->fsize + 100];

ret=get_line(line,in->data,in->fsize,&pos,-1);

int found=FALSE;

while(ret!=-1)
{
	if (strcmp(line,token)!=0)
	{
		strcat(temp,line);
		strcat(temp,"\n");
	}else
	{
		strcat(temp,line);
		strcat(temp,"\n");

		for (i=0;i<offset;i++)
		{
			ret=get_line(line,in->data,in->fsize,&pos,-1);
			strcat(temp,line);
			strcat(temp,"\n");
		}

		strcat(temp,text);
		strcat(temp,"\n");
		ret=get_line(line,in->data,in->fsize,&pos,-1);
		found=TRUE;
	}
	ret=get_line(line,in->data,in->fsize,&pos,-1);
}


len=strlen(temp);
in->fsize=len;

if (found==TRUE)
{
	in->edited=TRUE;
}

in->data=realloc(in->data,(len+1)*sizeof(char));
memcpy(in->data, temp, (len+1)*sizeof(char));

if (in->data[len]!=0)
{
	ewe(sim,"String not ended\n");
}
free(temp);
}



int inp_save(struct simulation *sim,struct inp_file *in)
{
int ret=0;
if (in->edited==TRUE)
{
	ret=zip_write_buffer(sim,in->full_name,in->data, in->fsize);
	in->edited=FALSE;
}

return ret;
}

void inp_free(struct simulation *sim,struct inp_file *in)
{

	inp_save(sim,in);

	free(in->data);
	inp_init(sim,in);
}

int inp_search_gdouble(struct simulation *sim,struct inp_file *in,gdouble* out,char* token)
{
char temp[200];
double tmp;
if (inp_search(sim,temp,in,token)==0)
{
	if (str_isnumber(temp)==FALSE)
	{
		printf_log(sim,"warning:  '%s' %s %s is not a number.\n",temp,token,in->full_name);
		getchar();
	}

	sscanf(temp,"%le",&tmp);
	*out=tmp;
	//printf("oh %Le %s\n",*out,token);
	return 0;
}
return -1;
//ewe(sim,"token %s not found in file %s\n",token,in->full_name);
}

int inp_search_double(struct simulation *sim,struct inp_file *in,double* out,char* token)
{
char temp[200];
if (inp_search(sim,temp,in,token)==0)
{
	if (str_isnumber(temp)==FALSE)
	{
		printf_log(sim,"'%s' is not a number.\n",temp);
	}
	sscanf(temp,"%le",out);
	return 0;
}
return -1;
}


void inp_search_int(struct simulation *sim,struct inp_file *in,int* out,char* token)
{
char temp[200];
if (inp_search(sim,temp,in,token)==0)
{
	if (str_isnumber(temp)==FALSE)
	{
		printf_log(sim,"'%s' is not a number.\n",temp);
	}

	sscanf(temp,"%d",out);
	return;
}
ewe(sim,"token %s not found in file %s\n",token,in->full_name);
}


void inp_search_string(struct simulation *sim,struct inp_file *in,char* out,char* token)
{
if (inp_search(sim,out,in,token)==0)
{
	return;
}
ewe(sim,"token %s not found in file %s\n",token,in->full_name);
}

void inp_check(struct simulation *sim,struct inp_file *in,double ver)
{
	char line[4000];
	double read_ver=0.0;
	long pos=0;
	int ret=0;
	inp_reset_read(sim,in);

	ret=get_line(line,in->data,in->fsize,&pos,-1);

	while(ret!=-1)
	{
		//printf(">>>>>>>%s\n",line);
		if (strcmp(line,"#ver")==0)
		{
			ret=get_line(line,in->data,in->fsize,&pos,-1);

			//printf(">>>>>>>%s\n",line);
			sscanf(line,"%lf",&(read_ver));

			if (ver!=read_ver)
			{
				ewe(sim,"File compatibility problem %s >%s< >%s< >%lf<\n",in->full_name,in->data,line,ver);

			}
			ret=get_line(line,in->data,in->fsize,&pos,-1);

			if ((ret==-1)||(strcmp(line,"#end")!=0))
			{
				ewe(sim,"#end token missing %s\n",in->full_name);
			}

			inp_reset_read(sim,in);
			return;
		}

		ret=get_line(line,in->data,in->fsize,&pos,-1);
	}

ewe(sim,"Token #ver not found in %s\n",in->full_name);
return;
}


int inp_search(struct simulation *sim,char* out,struct inp_file *in,char *token)
{
	char line[2000];
	long pos=0;
	int ret=0;
	inp_reset_read(sim,in);

	if (in->fsize>0)
	{
		if (in->data[0]!='#')
		{
			return -1;
		}
	}

	ret=get_line(line,in->data,in->fsize,&pos,-1);

	while(ret!=-1)
	{

		if (strcmp(line,token)==0)
		{
			ret=get_line(line,in->data,in->fsize,&pos,-1);
			//printf("1:%s %d\n",line,ret);
			if (ret==-1)
			{
				ewe(sim,"inp_search_offset");
			}
			strcpy(out,line);
			return 0;
		}

		ret=get_line(line,in->data,in->fsize,&pos,-1);
		//printf("2:%d\n",ret);

	}

return -1;
}


int inp_search_english(struct simulation *sim,struct inp_file *in,char *token)
{
	char line[4000];
	int ret=0;
	long pos=0;
	inp_reset_read(sim,in);
	ret=get_line(line,in->data,in->fsize,&pos,-1);

	while(ret!=-1)
	{

		if (strcmp(line,token)==0)
		{
			ret=get_line(line,in->data,in->fsize,&pos,-1);
			return english_to_bin(sim,line);
		}

		ret=get_line(line,in->data,in->fsize,&pos,-1);
	}
ewe(sim,"Token %s not found in file %s",token,in->full_name);
exit(0);
return -1;
}

