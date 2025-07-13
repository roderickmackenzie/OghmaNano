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

/** @file detector.h
@brief header file for the optical detectors
*/
#ifndef detector_h
#define detector_h
#include <g_io.h>
#include <enabled_libs.h>
#include <vec.h>
#include <sim_struct.h>
#include <triangle.h>
#include <dim.h>
#include <shape_struct.h>
#include <detector_struct.h>
#include <vectors.h>
#include <world_struct.h>
#include <device.h>
#include <ray.h>
#include <mesh_struct.h>

//detector
void detector_init(struct simulation *sim,struct detector *d);
void detector_free(struct simulation *sim,struct detector *d);
void detector_reset(struct simulation *sim,struct detector *det);
void detector_cpy(struct simulation *sim,struct detector *out,struct detector *in);
void detectors_dump_time_power(struct simulation *sim,struct device *dev);
void detector_malloc(struct simulation *sim,struct detector *det,struct dimensions *optical_dim);
void detector_add_point(struct simulation *sim,struct detector *det, struct ray *my_ray, int l);
void detector_dump(struct simulation *sim,struct detector *det,int detector_number);
void detector_dump_rendered_image(struct simulation *sim,char *out_dir, struct detector *det);
int detector_do_math(struct simulation *sim,struct detector *det);
int detector_add_above_device(struct simulation *sim, struct device *dev);
int dector_add_to_scene(struct simulation *sim,struct device *dev,struct detector *det);

//detectors
void detectors_init(struct detectors *dets);
void detectors_load(struct simulation *sim,struct detectors *dets, struct json_obj *json_detectors,struct dimensions *optical_dim);
void detectors_free(struct simulation *sim,struct detectors *dets);
void detectors_cpy(struct simulation *sim,struct detectors *out,struct detectors *in);
void dectors_add_to_scene(struct simulation *sim,struct device *dev, struct ray_engine *eng);
void detector_dump_bins(struct simulation *sim,struct ray_engine *in);
void detectors_reset(struct simulation *sim,struct ray_engine *eng, struct detectors *dets);
void detectors_add_input_power(struct simulation *sim,struct device *dev,int l,double mag);
void detectors_dump(struct simulation *sim,struct detectors *dets);
void detectors_dump_shapshots(struct simulation *sim,struct device *dev);
int detectors_set_verbosity(struct simulation *sim,struct detectors *dets, int verbosity);
int detectors_do_math(struct simulation *sim,struct detectors *dets);

#endif
