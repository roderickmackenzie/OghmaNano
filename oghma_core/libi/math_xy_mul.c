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

/**Rescale the scale and the data
@param in The structure holding the data
@param xmul multiply x axis by this
@param ymul multiply y axis by this
*/
void inter_rescale(struct math_xy* in,double xmul, double ymul)
{
int i;
for  (i=0;i<in->len;i++)
{
	in->x[i]*=xmul;
	in->data[i]*=ymul;
}

}

/**Multiply the data in a 1D math_xy by a number
@param in input math_xy
*/
int math_xy_mul_double(struct math_xy* in,double mul)
{
	int i;
	if (in->data==NULL)
	{
		return -1;
	}

	for (i=0;i<in->len;i++)
	{
		in->data[i]*=mul;

		if (in->complex_enabled==TRUE)
		{
			in->imag[i]*=mul;
		}
	}

	return 0;
}

int math_xy_mul(struct math_xy* a,struct math_xy* b)
{
	int i;
	for  (i=0;i<a->len;i++)
	{
		a->data[i]*=b->data[i];
	}

	return 0;
}
