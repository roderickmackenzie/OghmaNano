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

/** @file i_mem.c
	@brief Memory management for i.c
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
#include <math_xy.h>
#include <memory.h>


/**Initialize a 1D math_xy
@param in input math_xy
*/
void math_xy_init(struct math_xy* in)
{
	in->x=NULL;
	in->data=NULL;
	in->imag=NULL;

	in->complex_enabled=FALSE;
	in->len=-1;
	in->max_len=-1;
	in->sorted_x=FALSE;
	in->file_name=NULL;

	in->n_branch=-1;
	in->branch=NULL;
}


/**Make a copy of one math_xy
@param in input math_xy
@param output math_xy
@param alloc initialize the memory in the output math_xy
*/
void math_xy_cpy(struct math_xy* out,struct math_xy* orig,int alloc)
{
	int i;
	if (alloc==TRUE)
	{
		math_xy_free(out);
		math_xy_malloc(out,orig->len);
	}

	out->len=orig->len;

	for  (i=0;i<orig->len;i++)
	{
		out->x[i]=orig->x[i];
		out->data[i]=orig->data[i];
	}


}

/**Free the structure holding the data
@param in The structure holding the data
*/
void math_xy_free(struct math_xy* in)
{
	int i;
	if (in->branch!=NULL)
	{
		for (i=0;i<in->n_branch;i++)
		{
			math_xy_free(&(in->branch[i]));
		}
	}

	free_1d((void *)&(in->x));
	free_1d((void *)&(in->data));
	free_1d((void *)&(in->imag));
	free_1d((void *)&(in->branch));
	free_1d((void *)&(in->file_name));

	math_xy_init(in);
}


void inter_append(struct math_xy* in,double x,double y)
{
	if (in->x==NULL)
	{
		math_xy_malloc(in,100);
	}

	in->x[in->len]=x;
	in->data[in->len]=y;
	in->len++;

	if ((in->max_len-in->len)<10)
	{
		in->max_len+=100;
		inter_realloc(in,in->max_len);
	}

}

int math_xy_duplicate_last(struct math_xy* in, double x)
{
	if (in->x==NULL)
	{
		math_xy_malloc(in,100);
	}

	if (in->len>0)
	{
		in->x[in->len]=x;
		in->data[in->len]=in->data[in->len-1];
		in->len++;
	}else
	{
		return -1;
	}

	if ((in->max_len-in->len)<10)
	{
		in->max_len+=100;
		inter_realloc(in,in->max_len);
	}

	return 0;
}

/**Change the size of an allocated math_xy
@param in inout math_xy
@param len new length
*/
void inter_realloc(struct math_xy* in,int len)
{
	in->x=(double *)realloc (in->x,len*sizeof(double));
	in->data=(double *)realloc (in->data,len*sizeof(double));
}


/**Allocate math_xy as a 1D array
@param in the array to allocate
@param m number of coloums
@param len length of data to store in the array
*/
void math_xy_malloc(struct math_xy* in,int len)
{
	if (in->x!=NULL)
	{
		printf("math_xy_malloc error in->x!=NULL\n");
		getchar();
	}

	if (in->data!=NULL)
	{
		printf("math_xy_malloc error in->data!=NULL\n");
		getchar();
	}

	in->len=0;
	in->max_len=len;

	if (in->file_name==NULL)
	{
		malloc_1d((void **)&(in->file_name),OGHMA_PATH_MAX, sizeof(char));
		strcpy(in->file_name,"new");
	}

	if (in->max_len>0)
	{
		malloc_1d((void **)&(in->x),in->max_len, sizeof(double));
		malloc_1d((void **)&(in->data),in->max_len, sizeof(double));

		if (in->complex_enabled==TRUE)
		{
			malloc_1d((void **)&(in->imag),in->max_len, sizeof(double));
		}
	}
}

void math_xy_malloc_branch(struct math_xy* in,int len)
{
	int i;
	in->n_branch=len;
	malloc_1d((void **)&(in->branch),in->n_branch, sizeof(struct math_xy));
	for (i=0;i<in->n_branch;i++)
	{
		math_xy_init(&(in->branch[i]));
	}
}

int math_xy_init_mesh(struct math_xy* in,int len,double min,double max)
{
	int i;
	math_xy_malloc(in,len);
	in->len=len;
	memset(in->data, 0, in->len*sizeof(double));
	double pos=min;
	double dx=(max-min)/((double)in->len);

	for (i=0;i<in->len;i++)
	{
		in->x[i]=pos;
		pos+=dx;
	}

	return 0;
}

int math_xy_init_mesh_log10(struct math_xy* in,int len,double min,double max)
{
	int i;
	math_xy_malloc(in,len);
	in->len=len;
	memset(in->data, 0, in->len*sizeof(double));
	double pos=log10(min);
	double dx=(log10(max)-log10(min))/((double)in->len);

	for (i=0;i<in->len;i++)
	{
		in->x[i]=pow(10.0,pos);
		pos+=dx;
	}

	return 0;
}
