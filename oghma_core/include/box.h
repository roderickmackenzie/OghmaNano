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

/** @file box.h
@brief ray tracing header files.
*/
#ifndef box_h
#define box_h
#include <g_io.h>

struct box
{
	char name[100];
	struct vec xyz;
	struct vec dxyz;
	int len;
	struct box *b;
};

void box_init(struct box *b);
void box_set(struct box *b,struct vec *xyz,struct vec *dxyz);
struct box* box_add(struct box *b,struct vec *xyz,struct vec *dxyz);
void box_free(struct box *b);
void box_count(struct box *b,int *tot);
void box_save(struct simulation *sim,char *file_name,struct box *in);
void box_to_dat_file(struct simulation *sim,struct dat_file *buf,struct box *in);
void box_dump(struct simulation *sim,struct box *in);

#endif
