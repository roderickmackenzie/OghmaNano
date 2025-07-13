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

/** @file light.h
@brief light functions from liblight
*/

#ifndef h_light_fun
#define h_light_fun
#include <g_io.h>
#include <complex.h>
#include "advmath.h"
#include <math_xy.h>
#include <sim_struct.h>
#include <epitaxy_struct.h>
#include <light.h>
#include <device.h>

void light_init(struct simulation *sim, struct light *in);
void light_norm_photon_density(struct simulation *sim, struct device *dev, struct light *li);
void light_malloc(struct simulation *sim, struct device *dev, struct light *li);
double light_cal_photon_density(struct simulation *sim,struct light *li, struct device *dev);
void light_load_config(struct simulation *sim,struct light *li, struct device *dev);
void light_load_json(struct simulation *sim,struct device *dev, struct json_obj *json_config);
void light_build_materials_arrays(struct simulation *sim,struct light *li, struct device *dev);
void light_set_sun_power(struct device* dev,struct light *li,double power, double laser_eff);
void light_cpy_memory(struct simulation *sim,struct dimensions *dim,struct light *out,struct light *in);
void light_set_unity_power(struct device* dev,struct light *li);
void light_solve_optical_problem(struct simulation *sim,struct device *dev,struct light *li);
void light_solve_all(struct simulation *sim,struct device *dev,struct light *li);
void light_set_dump(struct light *li,int dump);
void light_free(struct simulation *sim,struct dimensions *dim,struct light *li);
void light_dump(struct simulation *sim,struct device *dev,struct light *li);
int light_solve_lam_slice(struct simulation *sim,struct device *dev, struct light *li,double *sun_E,int z, int x,int lam, int w, int flip_material);
void light_dump_1d(struct simulation *sim,struct device *dev,struct light *li, int i);
void light_dump_verbose_1d(struct simulation *sim,struct device *dev,struct light *li, int i,char *ext);
void light_dump_verbose_2d(struct simulation *sim,struct device *dev,struct light *li);
void light_get_mode(struct device *dev,struct math_xy *mode,int lam,struct light *li);
void light_free_epitaxy(struct light *li);
void light_import_epitaxy(struct simulation *sim,struct light *li,struct epitaxy *my_epitaxy);
int light_load_laser(struct simulation *sim, struct device *dev, struct light *li,char *name, struct json_obj *json_config);
double light_get_sun(struct light *li);
void light_set_sun(struct light *li,double Psun);
void light_set_model(struct light *li,char *model);
int light_get_pos_from_wavelength(struct simulation *sim,struct device *dev, struct light *li,double lam);
void light_setup_dump_dir(struct simulation *sim,char *path,struct light *li);

void light_dump_sim_info(struct simulation *sim,char *path,struct light *li,struct device *dev);
int device_import_photon_gen_rate(struct simulation *sim,struct device *dev);
void light_load_filter(struct simulation *sim,struct light *li, struct json_obj *json_config);
double light_get_optical_power(struct simulation *sim, struct device *dev,struct light *li);
double light_get_optical_power_no_filter(struct simulation *sim, struct device *dev, struct light *li);

void light_dump_snapshots(struct simulation *sim,struct dimensions *dim,char *output_path, struct device *dev, struct light *li);
void light_flip_y_float(struct dimensions *dim,float ****in,int z,int x,int l);
void light_flip_y_float_complex(struct dimensions *dim,float complex ****in,int z,int x,int l);
void light_build_obj_pointer_array(struct simulation *sim,struct light *li, struct device *dev);

//light_stats
double light_cal_photons_abs_l(struct device *dev, struct simulation *sim,struct light *li,int l);
void light_dump_stats(struct simulation *sim,char *path,struct device *dev , struct light *li);
double light_J_photo(struct device *dev ,struct light *li);
double light_i_photo(struct device *dev ,struct light *li);
void light_cal_photon_density_y(struct simulation *sim,struct light *li,struct device *dev, int z, int x, int l);
void light_cal_power_tx_rx(struct device *dev, struct simulation *sim,struct light *li);

//light_src
void light_src_cal_min_max(struct simulation *sim,double  *min,double  *max,struct light_src *in);
void light_src_init(struct simulation *sim,struct light_src *in);
void light_src_free(struct simulation *sim, struct light_src *in);
void light_src_load(struct simulation *sim,struct light_src *in, struct json_obj *json_light_src);
void light_src_cpy(struct simulation *sim,struct light_src *out, struct light_src *in);
void light_src_build_spectra_tot(struct simulation *sim,struct light_src *in, struct mesh *mesh_l);
void light_src_dump(struct simulation *sim,char *path,struct light_src *in);
void light_src_cal_min_max(struct simulation *sim,double  *min,double  *max,struct light_src *in);
void light_calculate_complex_n_zxl(struct device *dev, struct light *li, int z, int x, int l, int flip);
void light_calculate_complex_n(struct device *dev,struct light *li);

#endif
