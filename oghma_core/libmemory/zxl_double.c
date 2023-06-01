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
#include "sim.h"
#include "dump.h"
#include "mesh.h"
#include <math.h>
#include "log.h"
#include "memory.h"
#include <g_io.h>
#include <zxy_math_kern.h>
#include <color.h>

void malloc_zxl_double(struct dimensions *dim, double * (***var))
{
	malloc_3d((void ****)var,dim->zlen, dim->xlen, dim->llen, sizeof(double));
}

void free_zxl_double(struct dimensions *dim, double * (***var))
{
	free_3d((void****)var,dim->zlen, dim->xlen, dim->llen,sizeof(double));
}

void cpy_zxl_double(struct dimensions *dim, double * (***out), double * (***in),int aloc)
{
	if (aloc==TRUE)
	{
		free_3d((void****)out,dim->zlen, dim->xlen, dim->llen,sizeof(double));
		malloc_3d((void****)out,dim->zlen, dim->xlen, dim->llen,sizeof(double));
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

	cpy_3d((void****)out, (void****)in, dim->zlen, dim->xlen, dim->llen, sizeof(double));
}

void set_zxl_double(struct dimensions *dim, double ***data, double val)
{
	int var_size=sizeof(double);
	int z_len=dim->zlen;
	int x_len=dim->xlen;
	int y_len=dim->llen;
	memset_zxy;
}

void zxl_to_zxrgb_double(struct simulation *sim, struct dimensions *dim, double * (***rgb_out), double ***in)
{
	int x, z, l;
	double X, Y, Z;
	int R, G, B;

	struct math_xy luminescence_tot;

	struct dimensions XYZ_dim;
	double ***XYZ=NULL;
	double max;
	dim_init(&XYZ_dim);
	dim_cpy(&XYZ_dim,dim);
	dim_free_xyz(&XYZ_dim,'l');
	XYZ_dim.llen=3;
	dim_malloc_xyz(&XYZ_dim,'l');
	XYZ_dim.l[0]=0.0;
	XYZ_dim.l[1]=1.0;
	XYZ_dim.l[2]=2.0;

	malloc_zxl_double(&(XYZ_dim), &XYZ);

	malloc_zxl_double(&(XYZ_dim), rgb_out);

	for (z=0;z<dim->zlen;z++)
	{
		for (x=0;x<dim->xlen;x++)
		{

			math_xy_init(&luminescence_tot);

			for (l=0;l<dim->llen;l++)
			{
				inter_append(&luminescence_tot,dim->l[l],in[z][x][l]);
			}

			color_cie_cal_XYZ(sim,&X,&Y,&Z,&luminescence_tot,FALSE);
			XYZ[z][x][0]=X;
			XYZ[z][x][1]=Y;
			XYZ[z][x][2]=Z;

			math_xy_free(&luminescence_tot);
		}
	}

	min_max_zxl_double(NULL, &max, &XYZ_dim, XYZ);
	div_zxl_double(&XYZ_dim, XYZ, max);

	for (z=0;z<dim->zlen;z++)
	{
		for (x=0;x<dim->xlen;x++)
		{

			X=XYZ[z][x][0];
			Y=XYZ[z][x][1];
			Z=XYZ[z][x][2];

			color_XYZ_to_rgb(&R,&G,&B,X,Y,Z);

			(*rgb_out)[z][x][0]=R*Y;
			(*rgb_out)[z][x][1]=G*Y;
			(*rgb_out)[z][x][2]=B*Y;
		}

	}

	free_zxl_double(&XYZ_dim,&XYZ);
	dim_free(&XYZ_dim);
}

void div_zxl_double(struct dimensions *dim, double ***src, double val)
{
	int z_len=dim->zlen;
	int x_len=dim->xlen;
	int y_len=dim->llen;
	div_zxy;
}

int min_max_zxl_double(double *min_out, double *max_out, struct dimensions *dim, double ***var)
{
	int z_len=dim->zlen;
	int x_len=dim->xlen;
	int y_len=dim->llen;
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
