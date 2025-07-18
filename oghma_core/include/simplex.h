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

/** @file simplex.c
@brief Downhill simplex code
*/
#ifndef simplex_h
#define simplex_h

#define TINY 1.0e-10		//A small number.
#define SIMPLEX_CONVERGED 1
#define  SIMPLEX_MAX 2

#include <g_io.h>
#include <sim_struct.h>
#include <simplex_struct.h>

void multimin_dump(struct simulation *sim,struct multimin *data);
void multimin_init(struct multimin *data);
void multimin_malloc(struct multimin *data);
void multimin_init_simplex(struct multimin *data);
void multimin_free(struct multimin *data);
void multimin_cal_center(struct multimin *data);
void multimin_find_best(struct multimin *data);
void multimin_sync(struct multimin *data,int s);
void multimin_shrink(struct multimin *data);
double contract(struct multimin *data,double mul);
double expand(struct multimin *data,double mul);
double reflect(struct multimin *data,double mul);
int simplex_iterate(struct simulation *sim,struct multimin *data);
void simplex_copy_ans(struct multimin *data);
void newton_start(struct simulation *sim,struct multimin *data);

#endif
