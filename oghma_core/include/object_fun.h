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

/** @file object.h
@brief ray tracing header files.
*/
#ifndef object_fun_h
#define object_fun_h
#include <g_io.h>
#include <vec.h>
#include <sim_struct.h>
#include <triangle.h>
#include <detector.h>
#include <object.h>

//Object
void object_flip_y_axis(struct object *obj);
void object_sub_y(struct object *obj,double y);
void object_add_y(struct object *obj,double y);
double object_get_min_y(struct object *obj);
void object_init(struct object *obj);
void object_free(struct object *obj);
void object_cal_min_max(struct object *obj);
void object_nalpha_malloc(struct object *obj,int l_max);
void object_nalpha_free(struct object *obj);
void object_malloc(struct object *obj);
#endif
