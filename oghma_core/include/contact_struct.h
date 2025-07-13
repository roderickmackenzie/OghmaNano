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

/** @file contact_struct.h
	@brief Definition of the contacts.
*/


#ifndef contact_struct_h
#define contact_struct_h

#include <g_io.h>
#include <shape_struct.h>

struct contact
{
	char name[100];
	int position;

	int active;
	int ground;

	char applied_voltage_type[100];
	gdouble voltage;
	gdouble voltage_want;
	gdouble voltage_last;
	gdouble store;
	gdouble np;
	int charge_type;
	double area;

	char shape_file_name[100];
	struct shape shape;

	gdouble contact_resistance_sq;
	gdouble shunt_resistance_sq;

	int majority_model;
	int minority_model;
	double majority_v0;
	double minority_v0;
	double majority_mu;
	double minority_mu;
	gdouble J;
	gdouble i;

	int level_y;

};

#endif
