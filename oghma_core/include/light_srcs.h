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

/** @file light_srcs.h
	@brief The main structure which holds information about the device.
*/

#ifndef device_light_srcs_h
#define device_light_srcs_h
#include <g_io.h>
#include <light.h>
#include <mesh.h>

void light_srcs_init(struct simulation *sim,struct light_sources *srcs);
void light_srcs_free(struct simulation *sim,struct light_sources *srcs);
void light_srcs_cpy(struct simulation *sim,struct light_sources *out,struct light_sources *in);
void light_srcs_load(struct simulation *sim,struct light_sources *srcs,struct json_obj *json_light_sources,struct mesh *mesh_l);
void light_srcs_dump(struct simulation *sim,char *path,struct light_sources *srcs);
#endif
