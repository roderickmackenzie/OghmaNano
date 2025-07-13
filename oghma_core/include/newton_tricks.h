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

/** @file newton_tricks.h
@brief functions to solver for an external voltage
*/

#ifndef newton_tricks_h
#define newton_tricks_h
#include <g_io.h>

struct newton_math_state
{
	int max_electrical_itt;
	gdouble min_cur_error;
	int newton_min_itt;
	gdouble electrical_clamp;
	int newton_clever_exit;
};

void newton_push_state(struct device *in);
void newton_pop_state(struct device *in);
gdouble sim_externalv(struct simulation *sim,struct device *in,gdouble wantedv);
gdouble sim_i(struct simulation *sim,struct device *in,gdouble wantedi);
void auto_ramp_contacts(struct simulation *sim,struct device *in);
void ramp_externalv(struct simulation *sim,struct device *in,gdouble from,gdouble to);
void set_ntricks_fast(int val);
gdouble sim_voc(struct device *in);
void newton_sim_simple(struct simulation  *sim,struct device *in);
void ntricks_auto_ramp_contacts(struct simulation *sim,struct device *in);


void newton_externv_aux(struct simulation *sim,struct device *in,gdouble V,gdouble* i,gdouble* didv,gdouble* didphi,gdouble* didxil,gdouble* didxipl,gdouble* didphir,gdouble* didxir,gdouble* didxipr);
gdouble newton_externv(struct simulation *sim,struct device *in,gdouble Vtot);
gdouble newton_externalv_simple(struct simulation *sim,struct device *in,gdouble V);
gdouble sim_externalv_ittr(struct simulation *sim,struct device *in,gdouble wantedv);

void state_cache_init(struct simulation *sim,struct device *in);
void hash_dir(struct simulation *sim,char *out);
//void state_gen_vector(struct simulation *sim,struct device *in);
//int state_find_vector(struct simulation *sim,struct device *in,char *out);

//memory
void solver_cal_memory_1D_2D(struct simulation *sim,struct device *in,int *ret_N,int *ret_M);

//offsets
int get_offset(struct device *dev, int z, int x, int y, int band, int *phi, int *n, int *p, int *srh_n, int *srh_p, int *nion);
int get_offset2(struct device *dev, int offset, int z, int x, int y, int *Ns, int *Nt, int *Nsd, int *Ntd, int *N1C, int *N3C);
int get_offset_aux(struct device *dev,int *kcl, int *Nho);

//newton
double newton_get_error(struct simulation *sim,struct device *in);
int newton_dump_bandwidth(struct simulation *sim,struct device *dev);
void update_solver_vars_1D_2D(struct simulation *sim,struct device *dev,int z,int x_in,int clamp);

//equations
void newton_setup_equs(struct simulation *sim,struct device *in);
void newton_set_equs(struct simulation *sim,struct device *dev,int val);

//thermal
int thermal_ramp_needed(struct simulation *sim,struct device *dev);
void thermal_ramp(struct simulation *sim,struct device *dev);
void device_set_temperature_val(struct simulation *sim,struct device *in,double val);
#endif

