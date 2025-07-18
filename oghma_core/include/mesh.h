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

/** @file mesh.h
@brief meshing functions
*/

#ifndef mesh_h
#define mesh_h
#include <g_io.h>
#include <json.h>
//mesh layer
void mesh_layer_init(struct simulation * sim, struct mesh_layer *layer );

void mesh_check_y(struct simulation *sim,struct mesh *in,struct device *dev);
int mesh_check_x(struct simulation *sim,struct device *dev);
int mesh_remesh_y(struct simulation *sim,struct device *dev);
void mesh_save(struct simulation *sim,char *file_name,struct mesh *in);
void mesh_free(struct mesh *in);
void mesh_build(struct simulation *sim,struct device *in);
void mesh_cal_layer_widths(struct device *dev);
void mesh_init(struct mesh *in);
void mesh_dump(struct mesh *in);
int mesh_dump_to_file(char * file_name, struct mesh *in);
int mesh_to_dat_file(struct dat_file *buf, struct mesh *in, int to_memory);
void mesh_load_from_json(struct simulation * sim, struct mesh *in,struct json_obj *mesh_xyz);
void mesh_cpy(struct simulation *sim,struct mesh *out,struct mesh *in);
void mesh_malloc_sub_mesh(struct simulation * sim, struct mesh *in);
void mesh_gen_simple(struct simulation * sim, struct mesh *in,gdouble len,int points,double start);
int mesh_to_dim(struct simulation *sim,struct dimensions *dim, struct mesh *in,char xyz);
int mesh_file_to_dim(struct simulation *sim,struct dimensions *dim, struct mesh *in,char *file_name);
gdouble mesh_to_dim_heat(struct simulation *sim,struct dimensions *dim, struct mesh *in,char xyz);
int mesh_to_lin_array(int *tot_points, double *tot_len, double **mesh_in, double **dmesh_in, struct mesh *in);
int mesh_to_lin_array_lambda(double *mesh_in, struct mesh *in);
int mesh_to_lin_array_one_point_per_layer(struct mesh *in, struct json *j);
int mesh_y_rescale_if_needed_to_epi_layers(struct simulation *sim,struct mesh *in,struct device *dev);
int mesh_rescale_optical_x_to_electrical_x(struct simulation *sim,struct device *dev);

//mesh obj
void mesh_obj_cpy(struct simulation *sim,struct mesh_obj *out,struct mesh_obj *in);
void mesh_obj_load(struct simulation *sim,struct mesh_obj *mesh,struct json_obj *json_mesh);
void mesh_obj_free(struct simulation *sim,struct mesh_obj *in);
void mesh_obj_init(struct mesh_obj *in);
void dim_dump(struct dimensions *dim);
void dim_dump_y(struct dimensions *dim);
void dim_dump_l(struct dimensions *dim);
void mesh_obj_apply_srh_contacts(struct simulation *sim,struct mesh_obj *mesh,struct device *dev);
void mesh_obj_dump(struct mesh_obj *in);

//mesh basic math
int mesh_scale_to_mesh(struct mesh *in0,struct mesh *in1);
int mesh_scale(struct simulation *sim,struct mesh *in,double len);
int mesh_get_len(double *len,struct mesh *in);
#endif
