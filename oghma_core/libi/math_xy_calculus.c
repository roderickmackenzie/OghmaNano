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

static int unused __attribute__((unused));
static char* unused_pchar __attribute__((unused));

/**Integrate the data
@param in the structure to integrate
*/
double inter_intergrate(struct math_xy* in)
{
int i;
double tn=0.0;
double tp=0.0;
//double t=0.0;
double dt=0.0;
//double Eomega=0.0;
double sum=0.0;
double n;

	for (i=0;i<in->len;i++)
	{

		if (i==0)
		{
			tn=in->x[i];
		}else
		{
			tn=in->x[i-1];
		}

		if (i==in->len-1)
		{
			tp=in->x[i];
		}else
		{
			tp=in->x[i+1];
		}

		n=in->data[i];
		dt=fabs((tp-tn)/2.0);

		sum+=n*dt;


	}
return sum;
}

/**Integrate the data between limits
@param in the structure to integrate
@param from lower limit
@param from upper limit
*/
double inter_intergrate_lim(struct math_xy* in,double from, double to)
{
int i;
double tn=0.0;
double tp=0.0;
//double t=0.0;
double dt=0.0;
//double Eomega=0.0;
double sum=0.0;
double n;

	for (i=0;i<in->len;i++)
	{

		if (i==0)
		{
			tn=in->x[i];
		}else
		{
			tn=in->x[i-1];
		}

		if (i==in->len-1)
		{
			tp=in->x[i];
		}else
		{
			tp=in->x[i+1];
		}

		n=in->data[i];
		dt=fabs((tp-tn)/2.0);

		if (tn>from) sum+=n*dt;
		if (tn>to) break;

	}

return sum;
}



