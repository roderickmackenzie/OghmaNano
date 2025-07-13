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

/** @file device.h
	@brief The main structure which holds information about the device.
*/

#ifndef device_fun_h
#define device_fun_h
#include <g_io.h>
#include <stdio.h>
#include "code_ctrl.h"
#include "light.h"
#include <epitaxy_struct.h>
#include "advmath.h"
#include <dos_struct.h>
#include <contact_struct.h>
#include <perovskite_struct.h>
#include <circuit_struct.h>
#include <dim.h>
#include <matrix.h>
#include <device.h>
#include <shape.h>
#include <object.h>
#include <box.h>
#include <mesh.h>
#include <math_xy.h>
#include <oghma_script.h>

void device_init(struct simulation *sim,struct device *in);
void device_malloc(struct simulation *sim,struct device *in);
void device_cpy(struct simulation *sim,struct device *out,struct device *in);
void device_free(struct simulation *sim,struct device *in);
void device_load_math_config(struct simulation *sim,struct device *in);
void device_dump_world_to_file(struct simulation *sim,struct device *dev,char *file_name);
void device_build_scene(struct simulation *sim,struct device *dev);
struct object*  device_add_shape_to_world(struct simulation *sim,struct box* b,struct device *dev,struct shape *s, int object_type);
void device_calculate_joule_heat(struct simulation *sim,struct device *dev);
void device_calculate_recombination_heat(struct simulation *sim,struct device *dev);
int device_build_obj_zxy(struct simulation *sim,struct device *dev,struct object ****obj_zx_layer,struct object ****obj_zxy, struct vec* mesh_offset,struct dimensions *dim);
int device_build_obj_zxy_optical(struct simulation *sim,struct device *dev);
int device_obj_build_zy(struct simulation *sim,struct device *dev,struct object ****obj_zx_layer,struct object ****obj_zxy, struct vec* mesh_offset,struct dimensions *dim, int z);
void device_set_temperature(struct simulation *sim,struct device *in);
int dim_alloc_zx_epitaxy(struct dim_zx_epitaxy *dim,struct device *dev);

void device_world_stats(struct simulation *sim,struct device *dev);
int device_cal_start_stop(struct simulation *sim,struct device *dev);

//cahce
void device_cache_init(struct solver_cache *cache);
void device_cache_cpy(struct solver_cache *out,struct solver_cache *in);
int epitaxy_load_electrical_data(struct simulation *sim,struct device *dev, struct epitaxy *epi,struct json_obj *json_epi);
void device_interface_doping(struct simulation *sim,struct device *dev);
char *get_input_path(struct device *dev);
char *get_output_path(struct device *dev);
void set_input_path(struct device *dev,char *in);
void set_output_path(struct device *dev,char *in);
void device_to_dim(struct simulation *sim,struct dimensions *dim,struct device *dev);

int math_xy_alloc_device_tree(struct simulation *sim, struct math_xy *tree, struct device *dev, double *x, int len);
int device_load_json(struct simulation *sim, struct device *dev);
int device_run_simulation(struct simulation *sim, struct device *dev);

//Move this
int math_xy_from_mesh(struct simulation *sim, struct math_xy *in, struct mesh *mesh);
int device_build_optical_mesh(struct simulation *sim,struct device *dev);
int device_load_objects_and_meshes(struct simulation *sim, struct device *dev);
int device_set_electrical_boundary(struct simulation *sim,struct device *dev);
int device_dump_electrical_boundary(struct simulation *sim,struct device *dev);

//simmode
void simmode_init(struct simmode *sm);
void simmode_cpy(struct simmode *out,struct simmode *sm);
int simmode_calculate(struct simulation *sim, struct simmode *sm,struct json_obj *json_in);
int simmode_is_optical(struct simmode *sm);
int simmode_guess_optical_solver(struct simulation *sim, struct simmode *sm, struct json *j);
int simmode_dump( struct simmode *sm);

//electrical solver
int solve_all(struct simulation *sim,struct device *dev);
int solve_all_do_work(struct simulation *sim,struct device *dev);

//clock
int device_clock_start(struct simulation *sim,struct device *dev);
int device_clock_poll(struct simulation *sim,struct device *dev);
int device_clock_stop(struct simulation *sim,struct device *dev);

int device_matrix_cal_norm(struct simulation *sim, struct device *dev);

#endif
