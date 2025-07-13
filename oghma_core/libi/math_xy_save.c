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

/** @file i.c
	@brief Simple functions to read in scientific data from text files and perform simple maths on the data.
*/
#define _FILE_OFFSET_BITS 64
#define _LARGEFILE_SOURCE
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sim_struct.h>

#include <math_xy.h>
#include "util.h"
#include "cal_path.h"
#include "oghma_const.h"
#include <log.h>
#include <memory.h>
#include <g_io.h>
#include <dat_file.h>




/**Print math_xy to screen
@param in struct to print
*/
void math_xy_dump(struct math_xy* in)
{
	int i=0;
	if (in->branch!=NULL)
	{
		for (i=0;i<in->n_branch;i++)
		{
			math_xy_dump(&(in->branch[i]));
		}
	}

	printf("name:%s\n",in->file_name);
	if ((in->x!=NULL)&&(in->data!=NULL))
	{
		for  (i=0;i<in->len;i++)
		{
			printf("%le %le\n",in->x[i],in->data[i]);
		}
	}else
	{
		printf("No Data\n");
	}

}



/**Save an math_xy to disk and define path
@param in struct to save
@param path path of output file
@param path name of output file
*/	
void inter_save_a(struct math_xy* in,char *path,char *name)
{
	char wholename[PATH_MAX];
	join_path(2, wholename,path,name);
	math_xy_save(in,wholename);
}

void inter_save_seg(struct math_xy* in,char *path,char *name,int seg)
{
FILE *file=NULL;
int i=0;

int count_max=in->len/seg;
int count=0;
char temp[1000];
char file_name[1000];
int file_count=0;
for  (i=0;i<in->len;i++)
{
	if (count==0)
	{
		sprintf(file_name,"%s%d.dat",name,file_count);

		join_path(2, temp,path,file_name);

		file=g_fopen(temp,"w");
		file_count++;
	}
		fprintf(file,"%le",in->x[i]);
		fprintf(file," %le",in->data[i]);
	count++;
	fprintf(file,"\n");

	if (count==count_max)
	{
		fclose(file);
		count=0;
	}

}
if (count!=0) fclose(file);

}


/**Save an math_xy to disk
@param in struct to save
@param name outputfile
*/
int math_xy_save(struct math_xy* in,char *name)
{
	FILE *file;


	file=g_fopen(name,"w");
	if (file==NULL)
	{
		return -1;
	}

	int i=0;
	for  (i=0;i<in->len;i++)
	{
		fprintf(file,"%le %le",in->x[i],in->data[i]);
		if (in->complex_enabled==TRUE)
		{
			fprintf(file," %le",in->imag[i]);
		}
		fprintf(file,"\n");
	}

	fclose(file);

	return 0;
}


