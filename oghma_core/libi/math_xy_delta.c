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

/** @file math_xy_delta.c
	@brief Simple functions to read in scientific data from text files and perform simple maths on the data.
*/
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <math_xy.h>
#include "util.h"
#include "oghma_const.h"
#include <memory.h>

int math_xy_get_diff_config_init(struct math_xy_get_diff_config *config)
{
	config->mull=NULL;
	config->mul_val=-1.0;
	config->sigma=-1.0;
	config->window_left=-1.0;
	config->delta_type=-1.0;
	return 0;
}

double math_xy_get_diff(struct math_xy* delta,struct math_xy* one,struct math_xy* two, struct math_xy_get_diff_config *config)
{
	int i;
	int points_max=400;
	double error=0.0;
	double start;
	double stop;
	double etemp=0.0;
	double exp;
	double sim;
	double mul;
	double dx=0.0;
	double pos=0.0;
	double div=1.0;
	//printf("%s\n", two->file_name);

	math_xy_malloc(delta,points_max);
	delta->len=points_max;

	if ((two->len<=0)||(one->len<=0))
	{
		return -1.0;
	}

	start=one->x[0];
	if (two->x[0]>start)
	{
		start=two->x[0];
	}

	stop=one->x[one->len-1];
	if (two->x[two->len-1]<stop)
	{
		stop=two->x[two->len-1];
	}

	dx=(stop-start)/(double)points_max;
	pos=start;

	for (i=0;i<points_max;i++)
	{
		exp=inter_get_noend(one,pos);
		sim=inter_get_noend(two,pos);
		if (config->mull!=NULL)
		{
			mul=inter_get_noend(config->mull,pos);
		}else
		{
			mul=config->mul_val;
		}

		if (config->delta_type==DIFF_DELTA)
		{
			etemp=fabs(exp-sim)*mul;
		}else
		if (config->delta_type==DIFF_PDF)
		{
			etemp=log(normal_pdf(sim,exp,config->sigma))*mul;
			//printf("%le %le %le %le %le\n",etemp,sim,exp,normal_pdf(sim,exp,config->sigma),config->sigma);
		}else
		if (config->delta_type==DIFF_CHI)
		{
			etemp=pow(((exp-sim)*mul)/config->sigma,2.0);
		}else
		{
			printf("math_xy_get_diff: Delta type unknown\n");			
		}

		delta->x[i]=pos;

		if (delta->x[i]<config->window_left)
		{
			etemp=0.0;
		}

		delta->data[i]=etemp;
		error+=etemp;
		pos+=dx;
	}

	if (config->delta_type==DIFF_DELTA)
	{
		div=((double)points_max);
	}
	//printf("error=%le\n",error);
	return error/div;
}

double math_xy_get_delta(struct math_xy* one,struct math_xy* two)
{
	int x;
	double sum=0.0;
	for (x=0;x<one->len;x++)
	{
		sum+=fabs(one->data[x]-two->data[x]);
	}

	sum/=(double)one->len;

	return sum;
}



