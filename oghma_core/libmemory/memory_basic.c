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

/** @file memory_basic.c
@brief memory functions for 3D arrays
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lang.h>
#include "sim.h"
#include "dump.h"
#include "mesh.h"
#include <math.h>
#include "log.h"
#include <solver_interface.h>
#include "memory.h"
#include <g_io.h>
#include <math_kern_1d.h>

void zx_copy_gdouble(struct dimensions *dim, gdouble **dst, gdouble **src)
{
int x=0;
int z=0;

	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			dst[z][x]=src[z][x];
		}
	}

}



void memory_flip_1d_long_double(gdouble *var,int len)
{
	int y=0;
	gdouble * data=malloc(sizeof(gdouble)*len);
	for (y=0;y<len;y++)
	{
		data[y]=var[len-1-y];
	}

	for (y=0;y<len;y++)
	{
		var[y]=data[y];
	}

	free(data);

}

void three_d_interpolate_srh(gdouble ****out, gdouble ****in, struct dimensions *dim_out, struct dimensions *dim_in,int band)
{
int x=0;
int y=0;
int z=0;

int yi;
int xi;

gdouble y_out;
gdouble x_out;

gdouble y00;
gdouble y01;
gdouble yr;
gdouble y0;

gdouble y10;
gdouble y11;
gdouble y1;

gdouble x0;
gdouble x1;
gdouble xr;

gdouble c;

	z=0;
	for (x = 0; x < dim_out->xlen; x++)
	{

		x_out=dim_out->x[x];
		xi=hashget(dim_in->x,dim_in->xlen,x_out);

		for (y = 0; y < dim_out->ylen; y++)
		{
			y_out=dim_out->y[y];
			yi=hashget(dim_in->y,dim_in->ylen,y_out);

			y00=dim_in->y[yi];
			y01=dim_in->y[yi+1];
			yr=(y_out-y00)/(y01-y00);
			y0=in[z][xi][yi][band]+yr*(in[z][xi][yi+1][band]-in[z][xi][yi][band]);

			y10=dim_in->y[yi];
			y11=dim_in->y[yi+1];
			yr=(y_out-y10)/(y11-y10);
			y1=in[z][xi+1][yi][band]+yr*(in[z][xi+1][yi+1][band]-in[z][xi+1][yi][band]);

			x0=dim_in->x[xi];
			x1=dim_in->x[xi+1];
			xr=(x_out-x0)/(x1-x0);

			c=y0+xr*(y1-y0);
			out[z][x][y][band]=c;
		}

	}

}

void three_d_interpolate_srh2(gdouble ****out, gdouble ****in, struct dimensions *dim_out, struct dimensions *dim_in,int band)
{
int x=0;
int y=0;
int z=0;

int yi;
int xi;

gdouble y_out;
gdouble x_out;

gdouble y00;
gdouble y01;
gdouble yr;
gdouble y0;

gdouble y10;
gdouble y11;
gdouble y1;

gdouble x0;
gdouble x1;
gdouble xr;

gdouble c;

	z=0;
	for (x = 0; x < dim_out->xlen; x++)
	{

		x_out=dim_out->x[x];
		xi=hashget(dim_in->x,dim_in->xlen,x_out);

		for (y = 0; y < dim_out->ylen; y++)
		{
			y_out=dim_out->y[y];
			yi=hashget(dim_in->y,dim_in->ylen,y_out);

			y00=dim_in->y[yi];
			y01=dim_in->y[yi+1];
			yr=(y_out-y00)/(y01-y00);
			y0=in[z][xi][yi][band]+yr*(in[z][xi][yi+1][band]-in[z][xi][yi][band]);

			y10=dim_in->y[yi];
			y11=dim_in->y[yi+1];
			yr=(y_out-y10)/(y11-y10);
			y1=in[z][xi+1][yi][band]+yr*(in[z][xi+1][yi+1][band]-in[z][xi+1][yi][band]);

			x0=dim_in->x[xi];
			x1=dim_in->x[xi+1];
			xr=(x_out-x0)/(x1-x0);

			c=y0+xr*(y1-y0);
			out[z][x][y][band]=c;
		}

	}

}


void srh_quick_dump(char *file_name, gdouble ****in, struct dimensions *dim,int band)
{
int x=0;
int y=0;
int z=0;
	FILE *out=g_fopen(file_name,"w");

	for (z = 0; z < dim->zlen; z++)
	{

		for (x = 0; x < dim->xlen; x++)
		{

			for (y = 0; y < dim->ylen; y++)
			{
				fprintf(out,"%le %le %le\n",(double)dim->x[x],(double)dim->y[y],(double)in[z][x][y][band]);
			}

			fprintf(out,"\n");
		}
	}

fclose(out);
}

/**Do a chop search for a value
@param x index array
@param N length
@param find Value to find
*/
int search(gdouble *x,int N,gdouble find)
{

	chop_search_1d

return pos;
}

/**Do a chop search for a value
@param x index array
@param N length
@param find Value to find
*/
int search_double(double *x,int N,double find)
{
	chop_search_1d

return pos;
}
