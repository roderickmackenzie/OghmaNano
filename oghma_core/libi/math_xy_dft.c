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

/**Do a DFT
@param real real array
@param imag imag array
@param in input data
@param fx frequency
*/

int math_xy_dft_full(struct math_xy *fx_data,struct math_xy* data, int start_fx, int stop_fx)
{

	double r=0.0;
	double i=0.0;
	int x=0;
	int fx_i=0;
	double fx=0.0;
	double dc=0.0;
	dc=inter_sum(data)/((double)data->len);

	double dt=0.0;
	double tot_len=0.0;
	double r0;
	double r1;
	double i0;
	double i1;
	for (fx_i=start_fx;fx_i<stop_fx;fx_i++)
	{
		fx=fx_data->x[fx_i];
		printf("ftw %le\n",fx);
		r=0.0;
		i=0.0;
		tot_len=0.0;

		for (x=0;x<data->len-1;x++)
		{
			//if (x<data->len-1)
			//{
				dt=(data->x[x+1]-data->x[x]);
			//}
			r0=(data->data[x]-dc)*cos(2.0*M_PI*fx*data->x[x]);
			r1=(data->data[x+1]-dc)*cos(2.0*M_PI*fx*data->x[x+1]);
			i0=-(data->data[x]-dc)*sin(2.0*M_PI*fx*data->x[x]);
			i1=-(data->data[x+1]-dc)*sin(2.0*M_PI*fx*data->x[x+1]);
			r+=(r1+r0)*dt/2.0;
			i+=(i1+i0)*dt/2.0;
			tot_len+=dt;
		}

		fx_data->data[fx_i]=r*2.0/tot_len;
		fx_data->imag[fx_i]=i*2.0/tot_len;
		//printf("DFT2 r= %le im=%le\n",fx_data->data[fx_i],fx_data->imag[fx_i]);
	}

	return 0;
}

void math_xy_dft(double *real,double *imag,struct math_xy* in,double fx)
{
double r=0.0;
double i=0.0;
int x=0;
double len=(double)in->len;

for (x=0;x<in->len;x++)
{
	r+=in->data[x]*cos(2.0*M_PI*fx*in->x[x]);
	i+=-in->data[x]*sin(2.0*M_PI*fx*in->x[x]);
}
*real=r*2.0/len;
*imag=i*2.0/len;
}


void math_xy_dft_extract(double * dc,double *real,double *imag,struct math_xy* in,double fx)
{
double r=0.0;
double i=0.0;
int x=0;
double len=(double)in->len;
*dc=inter_sum(in)/len;

for (x=0;x<in->len;x++)
{
	r+=(in->data[x]-*dc)*cos(2.0*M_PI*fx*in->x[x]);
	i+=-(in->data[x]-*dc)*sin(2.0*M_PI*fx*in->x[x]);
}
*real=r*2.0/len;
*imag=i*2.0/len;
//printf("DFT r= %le im=%le\n",*real,*imag);
}



