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

/** @file rand.h
@brief generate random numbers for randomizing input files
*/



#ifndef rand_h
	#include <g_io.h>
	#include <sim_struct.h>
	#include <rand_state.h>

	int rand_init(struct rand_state *r);
	int rand_load(struct rand_state *r,struct json_obj *json_obj);
	int rand_test(struct rand_state *r);
	int rand_seed(struct rand_state* rand);
	int rand_hex(struct rand_state* rand, char *out,int n);
	int rand_int(struct rand_state* r);
	int rand_int_range(struct rand_state* r,int start_in,int stop_in);
	double rand_double(struct rand_state* r);

	double rand_gaussian(struct rand_state* r, double mean, double stddev);
	double rand_lin_range_double(struct rand_state *r,double min, double max);
	double rand_log_range_double(struct rand_state *r,double min, double max);

#endif
