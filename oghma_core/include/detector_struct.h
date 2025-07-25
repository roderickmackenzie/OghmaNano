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

/** @file detector.h
@brief header file for the optical detectors
*/
#ifndef detector_struct_h
#define detector_struct_h
#include <g_io.h>
#include <enabled_libs.h>
#include <sim_struct.h>
#include <shape_struct.h>
#include <object.h>
#include <math_xy.h>
#include <dim.h>

struct detector
{
	struct shape shape;
	int viewpoint_nx;
	int viewpoint_nz;
	double tot;
	struct math_xy detected_time;

	struct dimensions dim;
	double ***image;
	double *emission;	//what is emitted
	double *abs;		//what is absorbed
	double *eff;		//efficency of the process

	int dump_verbosity;
};

struct detectors
{
	struct detector *det;
	int detectors;
};

#endif
