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

/** @file ray_fun.h
@brief ray tracing header files.
*/
#ifndef ray_fun_h
#define ray_fun_h
#include <g_io.h>
#include <vec.h>
#include <sim_struct.h>
#include <device.h>
#include <ray.h>
#include <object.h>

#define WAIT 0
#define READY 1
#define DONE 2

#define TRUE 1
#define FALSE 0

#define RAY_MAX 5000

//ray_engine
THREAD_FUNCTION ray_thread_solve(void * in);
void light_update_ray_mat(struct simulation *sim,struct device *dev,struct ray_engine *eng);
void ray_engine_init(struct ray_engine *in);
int between(double v, double x0, double x1);
void add_triangle(struct world *w, double x0,double y0,double z0,double x1,double y1,double z1,double x2,double y2,double z2,int object_uid,int edge);
void ray_reset(struct ray_worker *worker);
int add_ray(struct simulation *sim,struct ray_worker *worker,struct vec *start,struct vec *dir,double mag,int obj_uid,int parent);
void ray_populate_with_shapes(struct simulation *sim,struct device *dev,struct epitaxy *in);
void obj_norm(struct vec *ret,struct triangle *my_obj);
int ray_intersect(struct vec *ret,struct triangle *my_obj,struct ray *my_ray);
int search_obj(struct simulation *sim,struct ray_engine *in,struct ray *my_ray);
struct triangle * search_triangle(struct simulation *sim,struct device *dev,struct ray *my_ray, int do_update);
int activate_rays(struct ray_worker *worker);
int pnpoly(struct ray_engine *in, struct vec *xy,int id);
void get_refractive(struct simulation *sim,struct ray_engine *in,double *alpha,double *n0,double *n1,struct ray *my_ray);
int propergate_next_ray(struct simulation *sim,struct device *dev,struct ray_engine *in,struct ray_worker *w);
void ray_configure_scene(struct simulation *sim,struct device *cell,struct ray_engine *eng,struct epitaxy *my_epitaxy);
void ray_engine_free(struct simulation *sim,struct device *in,struct ray_engine *eng);
void ray_read_config(struct simulation *sim,struct ray_engine *eng,struct world *w,struct json_obj *json_config);
void ray_solve(struct simulation *sim,struct device *dev, double mag,struct ray_worker *worker);
void ray_solve_all(struct simulation *sim,struct device *dev);
double ray_cal_escape_angle(struct ray_engine *in, struct ray_worker *worker);
void ray_escape_angle_reset(struct ray_engine *in,int l);
int search_object(struct simulation *sim,struct device *dev,struct ray *my_ray);
void ray_malloc(struct simulation *sim,struct device *in,struct ray_engine *eng);
void ray_escape_angle_norm(struct ray_engine *in);
double ray_tri_get_min_y(struct triangle* tri);
int ray_engine_add_src_at_zxy(struct simulation *sim,struct device *dev, int layer, int from_recombination);
int ray_engine_add_src_at_zx(struct simulation *sim,struct device *dev, int layer);


struct object *add_box(struct device *dev,double x0,double y0,double z0,double dx,double dy,double dz,int object_type);
struct object *add_pyramid(struct ray_engine *in,double x0,double y0,double z0,double dx,double dy,double dz);
struct object *add_dome(struct ray_engine *in,double x0,double y0,double z0,double dx0,double dy0,double dz0);

void ray_cpy(struct ray *a,struct ray *b);

struct object *add_plane(struct world *w,double x0,double y0,double z0,double dx,double dz,int object_type);

void ray_label_triangles(struct simulation *sim,struct device *dev);
//search
struct object *ray_obj_search_xyz(struct simulation *sim,struct device *dev,struct vec *xyz);
struct object *ray_obj_search(struct simulation *sim,struct device *dev,struct ray *in_ray);
struct object *ray_obj_search_by_name(struct simulation *sim,struct device *dev,char *serach_name);
//ray functions
void ray_init(struct ray *a);

//workers
void ray_worker_init(struct simulation *sim,struct ray_worker *worker);
void ray_worker_malloc(struct simulation *sim,struct ray_worker *worker);
void ray_worker_free(struct simulation *sim,struct ray_worker *worker);

//Viewpoint
void ray_viewpoint_reset(struct simulation *sim,struct ray_engine *eng,struct world *w);

//ray_src
void ray_src_dump(struct simulation *sim,struct device *dev);
int ray_engine_add_emitters(struct simulation *sim,struct device *dev);
int ray_check_if_needed(struct simulation *sim,struct device *dev);
int ray_apply_light_profile(struct simulation *sim,struct device *dev, struct ray_src *raysrc, double *mag, int nx, int ny, int nz);
int ray_src_layer_to_raysrc(struct ray_src *raysrc, struct epi_layer *layer);
int ray_src_free_emitters(struct simulation *sim,struct device *dev);
int ray_src_init(struct ray_src *raysrc);
int ray_src_clear_emitters(struct ray_engine *eng);
struct ray_src *ray_src_add_emitter(struct ray_engine *eng);
int ray_src_malloc(struct ray_src *src,struct ray_engine *eng);
int ray_src_free(struct ray_src *src);

//dump
int ray_dump(struct simulation *sim,struct device *dev);
void ray_dump_triangle(struct simulation *sim,struct device *dev,struct ray_engine *in,struct triangle *tri);
void dump_ray_to_file(struct simulation *sim,struct ray_engine *in,struct ray *my_ray,struct device *dev);
void dump_ang_escape(struct simulation *sim,struct ray_engine *in);
void ray_dump_all_rays(struct simulation *sim,char *dir_name,struct ray_engine *in,struct device *dev,struct ray_worker *worker,char *file_name);
void ray_dump_all_to_screen(struct simulation *sim,struct device *dev, struct ray_worker *worker);
void dump_ang_escape_as_rgb(struct simulation *sim,struct ray_engine *in);

//snapshots
void ray_setup_shapshots(struct simulation *sim,struct device *dev, struct ray_engine *eng);
void ray_dump_shapshot(struct simulation *sim,struct device *dev, struct ray_engine *eng,struct ray_worker *worker, char *postfix);

void ray_dump_abs_profile(struct simulation *sim,struct device *dev,char *path,struct ray_engine *in);
int ray_to_zxy(struct simulation *sim,struct device *dev,struct ray_engine *in,struct ray *my_ray, double alpha, struct ray_worker *w);

//ray_objects
int ray_delete_object(struct simulation *sim,struct device *dev,char *serach_name);
struct object *ray_add_object(struct device *dev,struct triangles *tri);
int ray_objects_remove_detectors(struct simulation *sim,struct device *dev);

#endif
