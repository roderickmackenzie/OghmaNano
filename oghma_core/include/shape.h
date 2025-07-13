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

/** @file shape.h
	@brief Read the epitaxy from the epitaxy.inp file.
*/


#ifndef shape_h
#define shape_h
#include <g_io.h>
#include "advmath.h"
#include <sim_struct.h>
#include <shape_struct.h>
#include <epitaxy_struct.h>
#include <dat_file_struct.h>
#include <device.h>

int shape_load_file(struct simulation *sim,struct epitaxy *in,struct shape *s, char *file_name, gdouble y_pos);
int shape_get_index(struct simulation *sim,struct epitaxy *in,gdouble x,gdouble y,gdouble z);
void shape_free(struct simulation *sim,struct shape *s);
int shape_in_shape(struct simulation *sim,struct shape *s,gdouble z,gdouble x,gdouble y);
void shape_init(struct shape *s);
//load the materials
	void shape_load_materials(struct simulation *sim,struct device *dev, struct shape *s);
	int shape_load_nk(struct simulation *sim,struct device *dev,struct shape *s);

void shape_cpy(struct simulation *sim,struct shape *out,struct shape *in);
int shape_load_from_json(struct simulation *sim,struct device *dev, struct shape *s, struct json_obj *obj ,gdouble y_pos);
void shape_cal_min_max(struct simulation *sim,struct vec *min,struct vec *max,struct shape *s);
void shape_dump(struct simulation *sim,struct shape *s);
void shape_gen_plane(struct simulation *sim,struct shape *s);
void shape_project_point_to_world(struct simulation *sim,struct shape *s,struct vec *out,struct vec *in);
void shape_project_world_point_to_shape(struct simulation *sim,struct shape *s,struct vec *out,struct vec *in);

int json_populate_shape_from_json_world_object(struct shape *s, struct json_obj *obj);
int json_save_shape_to_world_object(struct json_obj *obj, struct shape *s);

int shape_interface_init(struct shape_interface *iface);
int shape_interface_cpy(struct shape_interface *out, struct shape_interface *in);
int shape_load_interface_json(struct simulation *sim, struct shape_interface *iface,struct json_obj *interface_json);
int shape_load_dos(struct simulation *sim,struct dos *dos_n,struct dos *dos_p, struct json_obj *json_dos);;
#endif
