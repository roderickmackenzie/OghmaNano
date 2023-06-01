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

/** @file zx_long_double.c
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




void malloc_2d_long_double(int zlen, int xlen, gdouble * (**var))
{
	int z=0;

	if (*var!=NULL)
	{
		printf("Warning malloc_2d_long_double allocating onto non NULL pointer\n");
		getchar();
	}

	*var = (gdouble **) malloc(zlen * sizeof(gdouble *));

	for (z = 0; z < zlen; z++)
	{
		(*var)[z] = (gdouble *) malloc(xlen * sizeof(gdouble));
		memset((*var)[z], 0, xlen * sizeof(gdouble));
	}

}

void free_2d_long_double(int zlen, int xlen, gdouble * (**in_var))
{
	int z=0;
	gdouble **var=*in_var;

	if (var==NULL)
	{
		return;
	}

	//printf("%d %d %d\n",dim->zlen,dim->xlen,dim->ylen);
	for (z = 0; z < zlen; z++)
	{
		free(var[z]);
	}

	//printf("free\n");
	free(var);

	*in_var=NULL;
}

void cpy_2d_long_double(int zlen, int xlen, gdouble * (**out), gdouble * (**in))
{
	int z=0;

	for (z = 0; z < zlen; z++)
	{
		memcpy((*out)[z], (*in)[z], xlen * sizeof(gdouble));
	}

}
