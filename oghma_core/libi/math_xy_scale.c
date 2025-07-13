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

/**Perform log10 on data in math_xy and keep the sign
@param in input math_xy
*/
void math_xy_log_y_m(struct math_xy* in)
{
int i;
double mull=1.0;

for (i=0;i<in->len;i++)
{
	mull=1.0;
	if (in->data[i]<0.0) mull= -1.0;
	in->data[i]=log10(fabs(in->data[i]))*mull;
}
}

/**Perform log10 on data in math_xy
@param in input math_xy
*/
void math_xy_log_y(struct math_xy* in)
{
int i;
for (i=0;i<in->len;i++)
{
	in->data[i]=log10(fabs(in->data[i]));
}
}
/**Perform log10 on x axis in math_xy
@param in input math_xy
*/
void math_xy_log_x(struct math_xy* in)
{
	int i;
	for (i=0;i<in->len;i++)
	{
		if (in->x[i]>0.0) in->x[i]=log10(fabs(in->x[i]));
	}
}

void math_xy_log_x_m(struct math_xy* in)
{
	int i;
	double mull=1.0;
	for (i=0;i<in->len;i++)
	{
		mull=1.0;
		if (in->x[i]<0.0) mull= -1.0;
		if (in->x[i]>0.0) in->x[i]=mull*log10(fabs(in->x[i]));
	}
}
