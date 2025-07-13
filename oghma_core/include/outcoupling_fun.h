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

/** @file outcoupling_fun.h
@brief outcoupling functions from liboutcoupling
*/

#ifndef h_outcoupling_fun
#define h_outcoupling_fun
#include <g_io.h>
#include <complex.h>
#include "advmath.h"
#include <math_xy.h>
#include <sim_struct.h>
#include <epitaxy_struct.h>
#include <outcoupling.h>
#include <device.h>

int outcoupling_load_config(struct simulation *sim,struct outcoupling *li, struct device *dev);
void outcoupling_cpy(struct simulation *sim,struct dimensions *dim, struct outcoupling *out,struct outcoupling *in);
void outcoupling_setup_dump_dir(struct simulation *sim,char *path,struct outcoupling *li);
void outcoupling_dump(struct simulation *sim,struct device *dev,struct outcoupling *li);
void outcoupling_dump_snapshots(struct simulation *sim,struct device *dev, char *output_path,struct outcoupling *li);
void outcoupling_free(struct simulation *sim,struct dimensions *dim,struct outcoupling *li);
void outcoupling_init(struct simulation *sim,struct outcoupling *li);
void outcoupling_load_dlls(struct simulation *sim,struct outcoupling *li);
void outcoupling_malloc(struct simulation *sim,struct device *dev, struct outcoupling *li);
int outcoupling_solve_lam_slice(struct simulation *sim, struct device *dev, struct outcoupling *li,int z, int x,int l, int w);
int outcoupling_zx_lambda_solver(struct simulation *sim, struct outcoupling *li, struct device *dev, int l, int nw);
THREAD_FUNCTION thread_outcoupling_solve(void * in);
void outcoupling_solve_and_update(struct simulation *sim,struct device *dev,struct outcoupling *li);
void outcoupling_cal_photons_escape_prob_lam_avg(struct simulation *sim,struct device *dev ,struct outcoupling *li,int target_device);
void outcoupling_cal_photons_escape_prob_y_avg(struct simulation *sim,struct device *dev ,struct outcoupling *li);
int outcoupling_solve_with_transfer_matrix(struct simulation *sim,struct device *dev,struct outcoupling *li);
int outcoupling_solve_ray_on_optical_mesh(struct simulation *sim,struct device *dev,struct outcoupling *li);
int outcoupling_solve_ray_on_electrical_mesh(struct simulation *sim,struct device *dev,struct outcoupling *li);
int outcoupling_add_ray_srcs(struct simulation *sim,struct device *dev, int from_recombination, int allow_over_sampling);
int outcoupling_transfer_single_point_to_electrical_mesh(struct simulation *sim,struct device *dev,struct outcoupling *li, struct ray_src *src);
int outcoupling_transfer_zxy_point_to_electrical_mesh(struct simulation *sim,struct device *dev,struct outcoupling *li, struct ray_src *src);

//dump
void outcoupling_dump_sim_info(struct simulation *sim,char *path,struct outcoupling *li,struct device *dev);
int outcoupling_dump_from_own_mesh(struct simulation *sim,struct device *dev,struct outcoupling *li);
int outcoupling_dump_from_electrical_mesh(struct simulation *sim,struct device *dev,struct outcoupling *li);
#endif
