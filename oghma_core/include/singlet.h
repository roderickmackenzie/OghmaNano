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

/** @file singlet.h
@brief a structure for the heat model
*/

#ifndef h_singlet
#define h_singlet
#include <g_io.h>
#include <complex.h>
#include "advmath.h"
#include <sim_struct.h>
#include <epitaxy_struct.h>
#include <ray.h>
#include <matrix.h>
#include <object.h>
#include <dat_file_struct.h>
#include <dim.h>
#include <mesh_struct.h>
#include <singlet_material.h>


struct singlet
{
	int singlet_enabled;
	int ystart;
	int ystop;
	int ylen;

	struct matrix mx;

	gdouble error;

	gdouble Nion_mul;
	int singlet_conv;
	int full_newton;

};

struct singlet_opv
{
	int singlet_enabled;
};

#endif
