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

/** @file math_xy.h
	@brief Header file for i.c
*/
#ifndef math_xy_h
#define math_xy_h
#include <g_io.h>
#include "advmath.h"
#include <sim_struct.h>
#include <math_xy_struct.h>
#include <rand_state.h>

int inter_get_col_n(struct simulation *sim,char *name);
void math_xy_smooth_range(struct math_xy* out,struct math_xy* in,int points,double x);
double inter_avg_range(struct math_xy* in,double start,double stop);
double inter_array_get_max(double *data,int len);

//div
int math_xy_div(struct math_xy* one,struct math_xy* two);
void inter_div_long_double(struct math_xy* in,double div);
int math_xy_div_x(struct math_xy* in,double val);

void inter_make_cumulative(struct math_xy* in);
void inter_y_mul_dx(struct math_xy* in);
void inter_add_x(struct math_xy* in,double value);
double inter_get_quartile(struct math_xy* in,double value);
void inter_save_seg(struct math_xy* in,char *path,char *name,int seg);
double inter_intergrate(struct math_xy* in);
void inter_to_log_mesh(struct math_xy* out,struct math_xy* in);
int math_xy_smooth(struct math_xy* out,struct math_xy* in,int points);
double inter_sum_mod(struct math_xy* in);
void math_xy_set_value(struct math_xy* in,double value);
double inter_get_neg(struct math_xy* in,double x);

void inter_to_new_mesh(struct math_xy* in,struct math_xy* out);
void inter_swap(struct math_xy* in);


double inter_get_fabs_max(struct math_xy* in);
double inter_norm_to_one_range(struct math_xy* in,double min,double max);
void math_xy_chop(struct math_xy* in,double min, double max);
void inter_save_a(struct math_xy* in,char *path,char *name);
void math_xy_dump(struct math_xy* in);
void inter_purge_zero(struct math_xy* in);

int math_xy_duplicate_last(struct math_xy* in, double x);
void math_xy_init(struct math_xy* in);
void inter_sub_long_double(struct math_xy* in,double value);
void inter_sub(struct simulation *sim,struct math_xy* one,struct math_xy* two);
double inter_sum(struct math_xy* in);
int inter_get_col(char *file);
int math_xy_load_by_col(struct math_xy* in,char *name,int col);
double math_xy_get_diff(struct math_xy* delta,struct math_xy* one,struct math_xy* two, struct math_xy_get_diff_config *config);
int math_xy_get_diff_config_init(struct math_xy_get_diff_config *config);
void inter_pow(struct math_xy* in,double p);
gdouble math_interpolate_raw_long_double(gdouble *x,gdouble *data,int len,gdouble pos);
float math_interpolate_raw_float(double *x,float *data,int len,double pos);
double inter_norm(struct math_xy* in,double mul);


void inter_rescale(struct math_xy* in,double xmul, double ymul);
void inter_mod(struct math_xy* in);
void inter_add(struct math_xy* out,struct math_xy* in);
void math_xy_norm_area(struct math_xy* in,double mul);

void inter_add_long_double(struct math_xy* in,double value);
double inter_intergrate_lim(struct math_xy* in,double from, double to);
void math_xy_deriv(struct math_xy* out,struct math_xy* in);

void inter_convolve(struct math_xy* one,struct math_xy* two);

int inter_join_bins(struct math_xy* in,double delta);
void inter_reset(struct math_xy* in);

void math_xy_sin(struct math_xy *in,double mag,double fx,double delta);
void math_xy_cos(struct math_xy *in,double mag,double fx,double phi);
void inter_purge_x_zero(struct math_xy* in);

void math_xy_get_left_right_start(struct math_xy* in,int *left,int *right, double fraction);

int math_xy_dft_full(struct math_xy *fx_data,struct math_xy* data, int start_fx, int stop_fx);
double math_interpolate_raw_double(gdouble *x, double *data,int len,double pos);

//search
void inter_find_peaks(struct math_xy* out,struct math_xy* in,int find_max);
int inter_search_pos(struct math_xy* in,double x);
int math_xy_get_closest_y_value(struct math_xy* in,double *out_x, double *out_y ,double y);

//sort
int inter_sort(struct math_xy* in);
int math_xy_is_sorted(struct math_xy* in);
int math_xy_sort_just_x(struct math_xy* in);
int inter_sort_compare(const void *a, const void *b);

//scales
void math_xy_log_x(struct math_xy* in);
void math_xy_log_y(struct math_xy* in);
void math_xy_log_y_m(struct math_xy* in);
void math_xy_log_x_m(struct math_xy* in);

//memory
void math_xy_free(struct math_xy* in);
void math_xy_malloc(struct math_xy* in,int len);
void math_xy_malloc_branch(struct math_xy* in,int len);
void inter_realloc(struct math_xy* in,int len);
void math_xy_import_array(struct math_xy* in,double *x,double *y,int len,int alloc);
int math_xy_init_mesh(struct math_xy* in,int len,double min,double max);
int math_xy_init_mesh_log10(struct math_xy* in,int len,double min,double max);
void math_xy_cpy(struct math_xy* in,struct math_xy* orig,int alloc);
void inter_append(struct math_xy* in,double x,double y);

//dft
void math_xy_dft(double *real,double *imag,struct math_xy* in,double fx);
void math_xy_dft_extract(double * dc,double *real,double *imag,struct math_xy* in,double fx);

//data checks
int math_xy_check_all_real_numbers(struct math_xy* in);

//interpolation
double inter_get_hard(struct math_xy* in,double x);
int inter_get(struct math_xy* in,double x,double *ret);
double inter_get_noend(struct math_xy* in,double x);

//histogram
void math_xy_add_to_hist(struct math_xy* in,double pos,double value);
void math_xy_add_to_hist_log10(struct math_xy* in,double pos,double value);
int math_xy_make_hist(struct math_xy* out,struct math_xy* in, int bins);
//delta errors
double math_xy_get_delta(struct math_xy* one,struct math_xy* two);

//stats
double math_xy_avg(struct math_xy* in);

//save/load
int math_xy_save(struct math_xy* in,char *name);
int math_xy_load(struct math_xy* in,char *name);
void inter_print(struct math_xy* in);

//min/max
int math_xy_get_min(struct math_xy* in,double *ret);
int inter_get_max_pos(struct math_xy* in);
int math_xy_get_min_max(struct math_xy* in,double *min, double *max);
double inter_get_min_range(struct math_xy* in,double min, double max);
int inter_get_min_pos(struct math_xy* in);
double math_xy_get_max(struct math_xy* in);
void math_xy_get_max_and_pos(struct math_xy* in,double *max, double *x);
double inter_get_max_range(struct math_xy* in,int start, int stop);

//random
int math_xy_add_gaussian_noise(struct math_xy *in, struct rand_state *rand,double sigma);

//fitting
int math_xy_polyfit(struct math_xy *in, int degree, double *coeffs);

//mul
int math_xy_mul_double(struct math_xy* in,double mul);
int math_xy_mul(struct math_xy* a,struct math_xy* b);
#endif
