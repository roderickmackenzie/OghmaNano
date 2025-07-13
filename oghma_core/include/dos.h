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

/** @file dos.h
	@brief Headers for reading and getting values from the DoS.
*/


#ifndef dos_h
#define dos_h
#include <g_io.h>
#include <device.h>
#include <dos_struct.h>
#include <shape.h>
#include <json.h>

void dos_config_load(struct simulation *sim,struct dosconfig *confige,struct dosconfig *configh,char * dos_file, struct json_obj *json_dos);
gdouble get_dn_trap_den(gdouble top,gdouble T,int type,int band, struct shape *s);
gdouble get_dp_trap_den(gdouble top,gdouble T,int type, struct shape *s);

double get_n_muz(struct simulation *sim,struct shape *s, struct rpn_calculator *rpn_cal, double x, double y, double T);
double get_p_muz(struct simulation *sim,struct shape *s, struct rpn_calculator *rpn_cal, double x, double y, double T);

double get_n_mux(struct simulation *sim,struct shape *s, struct rpn_calculator *rpn_cal, double x, double y, double T);
double get_p_mux(struct simulation *sim,struct shape *s, struct rpn_calculator *rpn_cal, double x, double y, double T);

double get_n_muy(struct simulation *sim,struct shape *s, struct rpn_calculator *rpn_cal, double x, double y, double T);
double get_p_muy(struct simulation *sim,struct shape *s, struct rpn_calculator *rpn_cal, double x, double y, double T);

//Auger
gdouble get_Cn(struct shape *s);
gdouble get_Cp(struct shape *s);
//SS SRH
//Steady state SRH
gdouble get_ss_srh_n1(struct shape *s);
gdouble get_ss_srh_p1(struct shape *s);
gdouble get_ss_srh_tau_n(struct shape *s);
gdouble get_ss_srh_tau_p(struct shape *s);

gdouble get_top_from_n(struct shape *s,gdouble n,gdouble T);
gdouble get_top_from_p(struct shape *s,gdouble p,gdouble T);
void get_n_den(struct shape *s,gdouble top,gdouble T,gdouble *n, gdouble *dn, gdouble *w);
void get_p_den(struct shape *s,gdouble top,gdouble T, gdouble *p, gdouble *dp, gdouble *w);
gdouble get_n_mu(struct shape *s);
gdouble get_p_mu(struct shape *s);
gdouble get_dpdT_den(struct shape *s,gdouble top,gdouble T);
gdouble get_dndT_den(struct shape *s,gdouble top,gdouble T);
void gen_dos_fd_gaus_n(struct simulation *sim,char * dos_file, struct json_obj *json_dos);
void gen_dos_fd_gaus_p(struct simulation *sim,char * dos_file, struct json_obj *json_dos);
//int hashget(gdouble *x,int N,gdouble find);


void dos_init(struct dos *mydos);
void dos_free(struct dos *mydos);
void dos_cpy(struct dos *out,struct dos *in);

//DoS dos.c
gdouble get_dos_filled_n(struct device *in);
gdouble get_dos_filled_p(struct device *in);
gdouble dos_srh_get_fermi_n(struct shape *s,gdouble n, gdouble p,int band,gdouble T);
gdouble dos_srh_get_fermi_p(struct shape *s,gdouble n, gdouble p,int band,gdouble T);
gdouble get_Nc_free(struct shape *s);
gdouble get_Nv_free(struct shape *s);
void load_binary_dos_file(struct simulation *sim,struct dos *mydos,char *file);
double get_dos_ion_density(struct shape *s);
double get_dos_ion_mobility(struct shape *s);
gdouble get_dos_epsilonr(struct shape *s);
gdouble dos_get_band_energy_n(struct shape *s,int band);
gdouble dos_get_band_energy_p(struct shape *s,int band);
double get_dos_Eg(struct simulation *sim,struct shape *s,struct rpn_calculator *rpn_cal,double x, double y, double T);
double get_dos_Xi(struct simulation *sim,struct shape *s,struct rpn_calculator *rpn_cal,double x, double y, double T);
void load_dos(struct simulation *sim,struct device *in,struct shape *s,struct json_obj *json_dos);
gdouble get_dos_E_n(struct shape *s,int band);
gdouble get_dos_E_p(struct shape *s,int band);

void get_n_srh(struct simulation *sim,struct shape *s,gdouble top,gdouble T,int trap,gdouble *nt,gdouble *srh1,gdouble *srh2,gdouble *srh3,gdouble *srh4);
void get_p_srh(struct simulation *sim,struct shape *s,gdouble top,gdouble T,int trap,gdouble *pt,gdouble *srh1,gdouble *srh2,gdouble *srh3,gdouble *srh4);
void get_dn_srh(struct simulation *sim,struct shape *s,gdouble top,gdouble T,int trap,gdouble *dnt,gdouble *srh1,gdouble *srh2,gdouble *srh3,gdouble *srh4);
void get_dp_srh(struct simulation *sim,struct shape *s,gdouble top,gdouble T,int trap,gdouble *dpt,gdouble *srh1,gdouble *srh2,gdouble *srh3,gdouble *srh4);
gdouble get_n_pop_srh(struct simulation *sim,struct shape *s,gdouble top,gdouble T,int trap);
gdouble get_p_pop_srh(struct simulation *sim,struct shape *s,gdouble top,gdouble T,int trap);
gdouble get_dn_pop_srh(struct simulation *sim,struct shape *s,gdouble top,gdouble T,int trap);
gdouble get_dp_pop_srh(struct simulation *sim,struct shape *s,gdouble top,gdouble T,int trap);
void gen_dos_fd_gaus_fd(struct simulation *sim,struct epitaxy *in_epitaxy,struct json_obj *json_epi);
void gen_dos_fd_gaus_fd_stand_alone(struct simulation *sim,char *input_path);
void gen_do(struct simulation *sim,struct dosconfig *in,struct dosconfig *in2,char * outfile,struct json_obj *json_dos,int electrons);

//dos cache
void dos_cache_setup(struct simulation *sim,struct dos_cache *obj,struct json_obj *all_json);
void dos_cache_dump(struct dos_cache *obj);
void dos_cache_init(struct dos_cache *cache);
void dos_cache_obj_free(struct dos_cache_obj *obj);
void dos_cache_free(struct dos_cache *cache);

gdouble get_top_from_ion(gdouble n);
void get_ion_den(gdouble top,gdouble *n, gdouble *dn);

gdouble get_top_from_singlet(gdouble n);
void get_singlet_den(gdouble top,gdouble *n, gdouble *dn);

void check_fermi_inversion_n(struct simulation *sim,struct shape *s,gdouble n,int do_check);
void check_fermi_inversion_p(struct simulation *sim,struct shape *s,gdouble p,int do_check);

//DoS config
void dosconfig_init(struct dosconfig *config);
void dosconfig_free(struct dosconfig *config);
void dos_load_equations(struct simulation *sim,struct dosconfig *config, struct json_obj *json_dos);

//Dos rho
int dos_gen_rho(struct dosconfig *in,double *rho, double *E_mesh, int electrons);

#endif
