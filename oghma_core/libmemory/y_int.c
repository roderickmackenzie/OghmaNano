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

/** @file y_int.c
@brief memory functions for 3D arrays
*/

#include "sim.h"
#include <math.h>
#include "log.h"
#include <solver_interface.h>
#include "memory.h"
#include <g_io.h>
#include <math_kern_1d.h>

void malloc_y_int(struct dimensions *dim,int * (*var))
{

	malloc_1d((void **)var,dim->ylen, sizeof(int));
}


void free_y_int( int * (*in_var))
{

	free_1d((void **)in_var);

}

void cpy_y_int(struct dimensions *dim,int * (*out), int * (*in), int alloc)
{
	cpy_1d((void **)out, (void **)in, dim->ylen, sizeof(int), alloc);

}
