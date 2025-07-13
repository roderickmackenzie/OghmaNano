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
#include <sim_struct.h>
#include <math_xy.h>
#include "util.h"
#include "cal_path.h"
#include "oghma_const.h"
#include <log.h>
#include <memory.h>
#include <g_io.h>
#include <math_kern_1d.h>

int math_xy_get_min_max(struct math_xy* in,double *min, double *max)
{
	int i=0;
	if (in->len<=0)
	{
		return -1;
	}

	*min=in->data[0];
	*max=in->data[0];

	for (i=0;i<in->len;i++)
	{
		if (in->data[i]<*min)
		{
			*min=in->data[i];
		}

		if (in->data[i]>*max)
		{
			*max=in->data[i];
		}
	}

	return 0;
}

/**Get the smallest data stored in an math_xy array
@param in input math_xy
*/
int math_xy_get_min(struct math_xy* in,double *ret)
{
	int i=0;
	if (in->len<=0)
	{
		return -1;
	}

	double min=in->data[i];
	for (i=0;i<in->len;i++)
	{
		if (in->data[i]<min) min=in->data[i];
	}
	*ret=min;
	return 0;
}

/**Get maximum value of an math_xy
@param in input math_xy
*/
double math_xy_get_max(struct math_xy* in)
{
double max=0.0;

max=inter_get_max_range(in,0,in->len);

return max;
}

/**Get the position of the smallest data stored in an math_xy array
@param in input math_xy
*/
int inter_get_min_pos(struct math_xy* in)
{
int i=0;
int pos=0;
double min=in->data[i];
for (i=0;i<in->len;i++)
{
	if (in->data[i]<min)
	{
		min=in->data[i];
		pos=i;
	}

}
return pos;
}

/**Get the smallest data stored in an math_xy array
@param in input math_xy
*/
double inter_get_min_range(struct math_xy* in,double min, double max)
{
int i=0;
double ret=in->data[i];
for (i=0;i<in->len;i++)
{
	if ((in->x[i]>min)&&(in->x[i]<max))
	{
		if (in->data[i]<ret) ret=in->data[i];
	}

}
return ret;
}


void math_xy_get_max_and_pos(struct math_xy* in,double *max, double *x)
{
	int i;
	*max=in->data[0];

	for (i=0;i<in->len;i++)
	{
		if (in->data[i]>*max)
		{
			*max=in->data[i];
			*x=in->x[i];
		}
	}
}

double inter_get_max_range(struct math_xy* in,int start, int stop)
{
int i;
double max=0.0;
if (start<in->len)
{
	max=in->data[start];
}

//if (in->len>0) max=in->data[0];
for (i=start;i<stop;i++)
{
	if (in->data[i]>max) max=in->data[i];
}

return max;
}

int inter_get_max_pos(struct math_xy* in)
{
int i;
int pos=0;
double max=in->data[0];
//if (in->len>0) max=in->data[0];
for (i=0;i<in->len;i++)
{
	if (in->data[i]>max)
	{
		max=in->data[i];
		pos=i;
	}
}

return pos;
}
