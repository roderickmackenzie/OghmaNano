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

/** @file vec.h
	@brief Header file for vec.c
*/
#ifndef vec2d_inth
#define vec2d_inth
#include <g_io.h>
///Structure to hold vector

struct vec2d_int
{
	int x;
	int y;
};

void set_vec2d_int(struct vec2d_int *my_vec,int x, int y);
void cpy_vec2d_int(struct vec2d_int *out,struct vec2d_int *in);
void swp_vec2d_int(struct vec2d_int *in);
void add_vec2d_int(struct vec2d_int *a,struct vec2d_int *b);
void sub_vec2d_int(struct vec2d_int *a,struct vec2d_int *b);
void print_vec2d_int(struct vec2d_int *a);
#endif
