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

void math_xy_add_to_hist(struct math_xy* in,double pos,double value)
{
	int ii=0;
	double min=in->x[0];
	double max=in->x[in->len-1];
	double dx=(max-min)/((double)in->len);

	ii=(int)((pos-min)/dx);

	if (ii<in->len)
	{
		if (ii>=0)
		{
			in->data[ii]+=value;
		}
	}

}

void math_xy_add_to_hist_log10(struct math_xy* in,double pos,double value)
{
	int ii=0;
	double min=log10(in->x[0]);
	double max=log10(in->x[in->len-1]);
	double dx=(max-min)/((double)in->len);

	ii=(int)((log10(pos)-min)/dx);

	if (ii<in->len)
	{
		if (ii>=0)
		{
			in->data[ii]+=value;
		}
	}

}

int math_xy_make_hist(struct math_xy* out,struct math_xy* in, int bins)
{
	int i;
	double min;
	double max;
	double point_val=1.0/in->len;
	if (math_xy_get_min_max(in,&min,&max)!=0)
	{
		return -1;
	}

	math_xy_init_mesh(out,bins,min,max);

	for (i=0;i<in->len;i++)
	{
		math_xy_add_to_hist(out,in->data[i],point_val);
	}

	return 0;
}
