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

/**Divide one array by the other they must be of the same length/x-asis
@param in opperand one, then result
@param in opperand two

*/
int math_xy_div(struct math_xy* one,struct math_xy* two)
{
	int i;
	double a;
	double b;
	double c;
	double d;

	if (one->branch!=NULL)
	{
		for (i=0;i<one->n_branch;i++)
		{
			math_xy_div(&(one->branch[i]),two);
		}
	}

	if (one->len<=0)
	{
		return -1;
	}

	if (one->len!=two->len)
	{
		printf("The arrays are not the same length\n");
		return -1;
	}

	if (one->complex_enabled==TRUE)
	{
		for  (i=0;i<one->len;i++)
		{
			a=one->data[i];
			b=one->imag[i];

			c=two->data[i];
			d=two->imag[i];

			one->data[i]=(a*c+b*d)/(c*c+d*d);
			one->imag[i]=(b*c-a*d)/(c*c+d*d);
		}
	}else
	{
		double *a=one->data;
		double *b=two->data;
		int len=one->len;
		div_1d_1d;
	}

	return 0;
}

/**Divide the data in an math_xy by a value
@param div value to divide the data by
*/
void inter_div_long_double(struct math_xy* in,double div)
{
	int len=in->len;
	double *a=in->data;
	double b=div;
	div_1d_double;
}

int math_xy_div_x(struct math_xy* in,double val)
{
	int i;
	for  (i=0;i<in->len;i++)
	{
		in->x[i]/=val;
	}

	return 0;

}
