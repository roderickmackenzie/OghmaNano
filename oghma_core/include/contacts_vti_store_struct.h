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

/** @file contacts_vti_store.h
	@brief No idea what this does.
*/
#ifndef contacts_vti_store_struct_h
#define contacts_vti_store_struct_h
#include <math_xy.h>

struct contacts_vti_store
{
	struct math_xy *time_J;
	struct math_xy *time_v;
	struct math_xy *J;
	struct math_xy *J_external;

	struct math_xy jv;
	struct math_xy jv_internal;
	struct math_xy iv;
	struct math_xy vi;
	struct math_xy power;		//V*I
	struct math_xy power_den;
	struct math_xy sigma;		//conductivity

	//Calculated quantities
	int found_voc;
	double Pmax;
	double Pmax_den;
	double V_pmax;
	double J_pmax;
	double Isc;
	double Jsc;
	double Voc;
	double FF;
	double pce;
	double sigma_out;
};

#endif
