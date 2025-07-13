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

/** @file pl.h
@brief PL code.
*/

#ifndef pl_h
#define pl_h
#include <g_io.h>
#include <math_xy.h>
#include <sim_struct.h>

struct pl
{
	int pl_data_added;
	struct math_xy fe_to_fh;
	struct math_xy fe_to_te;
	struct math_xy te_to_fh;
	struct math_xy fh_to_th;
	struct math_xy th_to_fe;

	struct math_xy luminescence_ev;
	struct math_xy luminescence_lam;
};

int pl_init(struct pl *pl);
int pl_free(struct pl *pl);
int pl_dump_spectra(struct simulation *sim,char *out_dir,struct device *dev, struct pl *pl);
int pl_cal_simulated_spectra(struct simulation *sim,struct device *dev, struct pl *pl);
int pl_cal_experimental_spectra(struct simulation *sim,struct device *dev, struct pl *pl);
int calculate_photon_power_m2(struct simulation *sim,struct device *dev);
void exp_cal_absorption(struct simulation *sim,struct device *dev);
void exp_cal_emission(struct simulation *sim,char *out_dir,struct device *dev);
int calculate_eqe(struct simulation *sim,struct device *dev, double *eqe, struct math_xy *eqe_lam, double *Rtot);
int v_eqe_poly_smooth(struct simulation *sim,struct device *dev, struct math_xy *v_eqe, struct math_xy *v_eqe_R);
int eqe_dump(struct simulation *sim,struct device *dev, char *path);
#endif
