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

/** @file singlet_fun.h
@brief singlet functions from libsinglet
*/

#ifndef h_singlet_fun
#define h_singlet_fun
#include <g_io.h>
#include <complex.h>
#include <sim_struct.h>
#include <epitaxy_struct.h>
#include <singlet.h>
#include <device.h>
#include <json.h>
#include <shape_struct.h>
#include <device.h>

void singlet_load(struct simulation *sim,struct device *dev);
void singlet_opv_load(struct simulation *sim,struct device *dev);

//singlet material
void singlet_material_init(struct singlet_material *mat);
void singlet_material_cpy(struct singlet_material *out,struct singlet_material *in);
void singlet_material_free(struct singlet_material *mat);
void singlet_material_load_from_json(struct simulation *sim,struct singlet_material *mat, struct json_obj *json_singlet_material);
void singlet_material_gen_kfq(struct simulation *sim,struct device *dev,struct shape *s);

//singlet_opv material
void singlet_opv_material_init(struct singlet_opv_material *mat);
void singlet_opv_material_cpy(struct singlet_opv_material *out,struct singlet_opv_material *in);
void singlet_opv_material_free(struct singlet_opv_material *mat);
void singlet_opv_material_load_from_json(struct simulation *sim,struct singlet_opv_material *mat, struct json_obj *json_data);
#endif
