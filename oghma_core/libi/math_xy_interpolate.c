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
#include <unistd.h>
#include <sim_struct.h>
#include <math_xy.h>
#include "util.h"
#include <log.h>
#include <memory.h>

gdouble math_interpolate_raw_long_double(gdouble *x,gdouble *data,int len,gdouble pos)
{
gdouble x0;
gdouble x1;
gdouble y0;
gdouble y1;

gdouble ret;
int i=0;

if (pos<x[0])
{

return 0.0;
}


if (pos>=x[len-1])
{
	i=len-1;
	x0=x[i-1];
	x1=x[i];

	y0=data[i-1];
	y1=data[i];

}else
{
	i=search(x,len,pos);
	x0=x[i];
	x1=x[i+1];

	y0=data[i];
	y1=data[i+1];
}
ret=y0+((y1-y0)/(x1-x0))*(pos-x0);
return ret;
}

float math_interpolate_raw_float(double *x,float *data,int len,double pos)
{
double x0;
double x1;
float y0;
float y1;

float ret;
int i=0;

if (pos<x[0])
{

	return 0.0;
}


if (pos>=x[len-1])
{
	i=len-1;
	x0=x[i-1];
	x1=x[i];

	y0=data[i-1];
	y1=data[i];

}else
{
	i=search_double(x,len,pos);
	x0=x[i];
	x1=x[i+1];

	y0=data[i];
	y1=data[i+1];
}
ret=y0+((y1-y0)/(x1-x0))*(pos-x0);
return ret;
}

double math_interpolate_raw_double(double *x,double *data,int len,double pos)
{
double x0;
double x1;
double y0;
double y1;

double ret;
int i=0;

if (pos<x[0])
{

	return 0.0;
}


if (pos>=x[len-1])
{
	i=len-1;
	x0=x[i-1];
	x1=x[i];

	y0=data[i-1];
	y1=data[i];

}else
{
	i=search(x,len,pos);
	x0=x[i];
	x1=x[i+1];

	y0=data[i];
	y1=data[i+1];
}
ret=y0+((y1-y0)/(x1-x0))*(pos-x0);
return ret;
}

double inter_get_noend(struct math_xy* in,double x)
{
	double x0;
	double x1;
	double y0;
	double y1;

	double ret;
	int i=0;

	if (x<in->x[0])
	{
		return in->data[0];
	}

	if (x>=in->x[in->len-1])
	{
		return in->data[in->len-1];
	}


		i=search_double(in->x,in->len,x);
		x0=in->x[i];
		x1=in->x[i+1];

		y0=in->data[i];
		y1=in->data[i+1];

	double eval=0.0;

	if ((y1-y0)==0.0)
	{
		eval=0.0;
	}else
	if ((x-x0)==0.0)
	{
		eval=0.0;
	}else
	{
		eval=((y1-y0)/(x1-x0))*(x-x0);
	}

	ret=y0+eval;
	return ret;
}
