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

/** @file exp.h
	@brief Functions to meaure physical things from the device, such as current.
*/


#ifndef exp_h
#define exp_h
#include <g_io.h>
#include <device.h>

double get_jn_avg(struct device *dev);
double get_jp_avg(struct device *dev);
gdouble get_charge_change(struct device *dev);
void cal_J_drift_diffusion(struct device *dev);
double get_Jn_diffusion(struct device *dev);
double get_Jn_drift(struct device *dev);
double get_Jp_diffusion(struct device *dev);
double get_Jp_drift(struct device *dev);
gdouble get_avg_field(struct device *dev);
gdouble get_np_tot(struct device *dev);
void reset_npequlib(struct device *dev);
void get_avg_np_pos(struct device *dev,gdouble *nx,gdouble *px);
double get_background_charge(struct device *dev);
void reset_np_save(struct device *dev);
double get_avg_recom(struct device *dev);
double get_avg_recom_n(struct device *dev);
double get_avg_recom_p(struct device *dev);
double get_avg_Rn(struct device *dev);
double get_avg_Rp(struct device *dev);
double get_avg_k(struct device *dev);
void get_avg_mu(struct device *dev,double *ret_mue,double *ret_muh);
void get_avg_geom_micro_mu(struct device *dev,double *ret_mu);
void get_avg_conductance(struct device *dev,double *ret_sigma_e,double *ret_sigma_h);
double get_free_n_charge_delta(struct device *dev);
double get_free_p_charge_delta(struct device *dev);
double get_total_n_trapped_charge(struct device *dev);
double get_total_p_trapped_charge(struct device *dev);
double get_n_trapped_charge_delta(struct device *dev);
double get_p_trapped_charge_delta(struct device *dev);
double get_avg_relax_n(struct device *dev);
double get_avg_relax_p(struct device *dev);
double get_avg_J(struct device *dev);
double get_free_np_avg(struct device *dev);
double get_extracted_np(struct device *dev);
double get_extracted_k(struct device *dev);
double get_charge_delta(struct device *dev);
double get_I_recomb(struct device *dev);
double get_J_left(struct device *dev);
double get_J_right(struct device *dev);
double get_J_recom(struct device *dev);
double get_I_ce(struct simulation *sim,struct device *dev);
double get_equiv_I(struct simulation *sim,struct device *dev);

double get_extracted_n(struct device *dev);
double get_extracted_p(struct device *dev);
double get_equiv_V(struct simulation *sim,struct device *dev);
double get_equiv_J(struct simulation *sim,struct device *dev);
double get_I(struct device *dev);
double get_J(struct device *dev);
double get_charge(struct device *dev);
double get_avg_gen(struct device *dev);
void set_orig_charge_den(struct device *dev);
double get_charge_tot(struct device *dev);
double get_tot_photons_abs(struct device *dev);
double get_i_intergration(struct device *dev);
double get_avg_J_std(struct device *dev);
double get_max_Jsc(struct device *dev);
void get_tau(struct device *dev, double *ret_tau, double *ret_tau_all);
int get_free_nf_pf_nt_pt_charge(struct device *dev,double *nf,double *pf,double *nt,double *pt);

//thermal 

gdouble get_avg_Tl(struct device *dev);
gdouble get_avg_Te(struct device *dev);
gdouble get_avg_Th(struct device *dev);
gdouble cal_contact_charge(struct device *dev);
#endif
