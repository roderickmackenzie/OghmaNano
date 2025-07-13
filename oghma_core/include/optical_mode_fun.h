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

/** @file optical_mode_fun.h
	@brief Mode solver functions
*/


#ifndef h_optical_mode_fun
#define h_optical_mode_fun
#include <g_io.h>
#include <enabled_libs.h>
#include "advmath.h"
#include <sim_struct.h>
#include <device.h>
#include <dim.h>
#include <optical_mode.h>

int mode_free(struct simulation *sim,struct optical_mode *in);
void mode_init(struct simulation *sim,struct optical_mode *in);
int mode_dump(struct simulation *sim,struct device *dev,struct optical_mode *in,char *path);
int mode_cpy(struct simulation *sim,struct optical_mode *out,struct optical_mode *in);
int mode_cal_photon_density(struct simulation *sim,struct optical_mode *in, double ***E);
void mode_cal_gamma(struct simulation *sim,struct device *dev, struct optical_mode *mode);
void mode_to_device(struct simulation *sim,struct device *dev, struct optical_mode *mode);
int mode_load_config(struct simulation *sim,struct optical_mode *mode,struct device *dev);
int mode_malloc(struct simulation *sim,struct optical_mode *mode);
int optical_mode_build_mesh(struct simulation *sim,struct optical_mode *mode,struct device *dev);
int mode_set_materal_params(struct simulation *sim,struct optical_mode *mode,struct device *dev);
int mode_solve(struct simulation *sim,struct optical_mode *mode,struct device *dev, int x0, int y0);
double mode_build_matrix(struct simulation *sim,struct optical_mode *mode,struct matrix *mx, struct device *dev, int build_matrix,double *beta_out);
int mode_search(struct simulation *sim,struct optical_mode *mode,struct device *dev);
int is_eigenvalue(struct optical_mode *mode,double val);
void mode_guess(struct simulation *sim,struct device *dev,struct optical_mode *mode, int x0, int y0);
void mode_dump_snapshot(struct simulation *sim,char *output_path, struct optical_mode *mode,int step);
void mode_norm(struct simulation *sim, struct optical_mode *mode,double Nph);
int mode_solve_for_00(struct simulation *sim,struct optical_mode *mode,struct device *dev);
double mode_build_matrix_TM(struct simulation *sim,struct optical_mode *mode,struct matrix *mx, struct device *dev, int build_matrix, double *beta_out);
#endif
