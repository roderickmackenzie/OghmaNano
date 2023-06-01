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

/** @file heat_zxy_long_double.c
@brief memory functions for heat zxy arrays
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



//This shoudl be 3D interpolation but we are assuming the meshes are aligned.
gdouble interpolate_heat_zxy_long_double(struct dimensions *dim, gdouble ***data,int z, int x, gdouble y_in)
{
	int y=0;
	gdouble x0=0.0;
	gdouble x1=0.0;
	gdouble y0=0.0;
	gdouble y1=0.0;

	gdouble ret;

	if (y_in<dim->y[0])
	{
		return 0.0;
	}


	if (y_in>=dim->y[dim->ylen-1])
	{
		//printf("here %Le %Le\n",y_in,dim->y[dim->ylen-1]);
		y=dim->ylen-1;
		x0=dim->y[y-1];
		x1=dim->y[y];
		y0=data[z][x][y-1];
		y1=data[z][x][y];

	}else
	{
		y=search(dim->y,dim->ylen,y_in);
		//printf("%d\n",y);
		x0=dim->y[y];
		x1=dim->y[y+1];

		y0=data[z][x][y];
		y1=data[z][x][y+1];
	}
	ret=y0+((y1-y0)/(x1-x0))*(y_in-x0);

return ret;

}


gdouble avg_heat_zxy_long_double(struct dimensions *dim, gdouble ***data)
{
	int x=0;
	int y=0;
	int z=0;
	gdouble sum=0.0;

	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			for (y = 0; y < dim->ylen; y++)
			{
				sum+=data[z][x][y];
			}
		}
	}

return sum/((gdouble)(dim->zlen*dim->xlen*dim->ylen));
}
