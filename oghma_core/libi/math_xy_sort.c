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
#include <enabled_libs.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <math_xy.h>
#include "util.h"
#include "cal_path.h"
#include "oghma_const.h"
#include <log.h>
#include <memory.h>
#include <g_io.h>
#include <math_kern_1d.h>


int inter_sort_compare(const void *a, const void *b)
{
double aa = *(double*)a;
double bb = *(double*)b;

if (aa < bb) return -1;
if (aa > bb) return  1;

return 0;
}

/**Do a quick search
@param in input structure
*/
int inter_sort(struct math_xy* in)
{
	int i=0;
	double *data;
	if (in->len<=0)
	{
		return -1;
	}

	if (in->sorted_x==TRUE)
	{
		return 0;
	}

	data=(double *)malloc(in->len*2*sizeof(double));

	for (i=0;i<in->len;i++)
	{
		data[i*2]=in->x[i];
		data[(i*2)+1]=in->data[i];
	}

	qsort(data, in->len, sizeof(double)*2, inter_sort_compare);

	for (i=0;i<in->len;i++)
	{
		in->x[i]=data[i*2];
		in->data[i]=data[(i*2)+1];
	}

	free(data);
	return 0;
}

int math_xy_sort_just_x(struct math_xy* in)
{
	if (in->len<=0)
	{
		return -1;
	}

	if (in->sorted_x==TRUE)
	{
		return 0;
	}

	qsort(in->x, in->len, sizeof(double), inter_sort_compare);

	return 0;
}

int math_xy_is_sorted(struct math_xy* in)
{
	int y;
	double last_val;
	in->sorted_x=TRUE;
	for  (y=0;y<in->len;y++)
	{
		if (y!=0)
		{
			if (last_val>in->x[y])
			{
				in->sorted_x=FALSE;
				return -1;
			}
		}
		last_val=in->x[y];
	}

	return 0;
}
