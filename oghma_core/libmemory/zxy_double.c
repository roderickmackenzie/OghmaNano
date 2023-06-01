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
#include "zxy_math_kern.h"

void malloc_zxy_double(struct dimensions *dim, double * (***var))
{
	malloc_3d((void ****)var,dim->zlen, dim->xlen, dim->ylen, sizeof(double));
}

void free_zxy_double(struct dimensions *dim, double * (***var))
{
	free_3d((void****)var,dim->zlen, dim->xlen, dim->ylen,sizeof(double));
}

void cpy_zxy_double(struct dimensions *dim, double * (***out), double * (***in),int aloc)
{
	if (aloc==TRUE)
	{
		free_3d((void****)out,dim->zlen, dim->xlen, dim->ylen,sizeof(double));
		malloc_3d((void****)out,dim->zlen, dim->xlen, dim->ylen,sizeof(double));
		if (*in==NULL)
		{
			return;
		}
	}else
	{
		if (in==NULL)
		{
			printf("Warning copying null pointer\n");
		}

		if (out==NULL)
		{
			printf("Warning copying onto null pointer!\n");
			getchar();
		}
	}

	cpy_3d((void****)out, (void****)in, dim->zlen, dim->xlen, dim->ylen, sizeof(double));
}


double zx_y_max_double(struct dimensions *dim, double ***var,int y)
{
	int x=0;
	int z=0;

	double max=var[0][0][0];

	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			if (var[z][x][y]>max)
			{
				max=var[z][x][y];
			}
		}
	}

return max;
}

void set_zxy_double(struct dimensions *dim, double ***data, double val)
{
	int var_size=sizeof(double);
	int z_len=dim->zlen;
	int x_len=dim->xlen;
	int y_len=dim->ylen;
	memset_zxy;
}

void quick_dump_zx_y_double(char *file_name, double ***in, struct dimensions *dim)
{
int x=0;
int y=0;
int z=0;
FILE *out;
char full_name[200];

	for (y = 0; y < dim->ylen; y++)
	{
		sprintf(full_name,"%s.%d.dat",file_name,y);
		out=g_fopen(full_name,"w");

		for (z = 0; z < dim->zlen; z++)
		{

			for (x = 0; x < dim->xlen; x++)
			{
					fprintf(out,"%le %le %le\n",(double)dim->z[z],(double)dim->x[x],in[z][x][y]);
			}
			fprintf(out,"\n");
		}

		fclose(out);

	}

}

void div_zxy_double(struct dimensions *dim, double ***src, double val)
{
	int z_len=dim->zlen;
	int x_len=dim->xlen;
	int y_len=dim->ylen;
	div_zxy;
}

void mul_zxy_double_double(struct dimensions *dim, double ***a, double b)
{
	mul_zxy_double;
}

void mul_zxy_double_zxy_double(struct dimensions *dim, double ***a, double ***b)
{
	mul_zxy_zxy;
}

void div_zxy_double_zxy_double(struct dimensions *dim, double ***a, double ***b)
{
	div_zxy_zxy;
}

void pow_zxy_double(struct dimensions *dim, double ***a, double val)
{
	pow_zxy;
}

void abs_zxy_double(struct dimensions *dim, double ***a)
{
	abs_zxy;
}

void add_zxy_double_zxy_double(struct dimensions *dim, double ***a, double ***b)
{
	add_zxy_zxy;
}	

double avg_vol_zxy_double(struct device *in, double ***src)
{
	double sum=0.0;
	double ret=0.0;

	avg_vol_xzy;

	return ret;
}

int min_max_zxy_double(double *min_out, double *max_out, struct dimensions *dim, double ***var)
{
	int z_len=dim->zlen;
	int x_len=dim->xlen;
	int y_len=dim->ylen;
	min_max_zxy
	if (min_out!=NULL)
	{
		*min_out=min;
	}

	if (max_out!=NULL)
	{
		*max_out=max;
	}
	return 0;
}

int max_abs_zxy_double(double *peak_out, struct dimensions *dim, double ***var)
{
	int z_len=dim->zlen;
	int x_len=dim->xlen;
	int y_len=dim->ylen;
	min_max_zxy

	double ret=fabs(min);

	if (fabs(max)>fabs(min))
	{
		ret=fabs(max);
	}

	if (peak_out!=NULL)
	{
		*peak_out=ret;
	}
	return 0;
}

double inter_zxy_double(struct dimensions *dim, double ***src)
{
double sum=0.0;

inter_zxy;

return sum;
}

