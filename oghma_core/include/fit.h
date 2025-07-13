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

/** @file fit.h
@brief functions for fitting.
*/

#ifndef fith
#define fith
#include <g_io.h>
#include <advmath.h>
#include <sim_struct.h>
#include <simplex.h>
#include <json.h>
#include <math_xy.h>
#include <fit_struct.h>


void fit_build_jobs(struct simulation *sim,struct fitconfig *config);
double get_all_error(struct simulation *sim,struct fitconfig *myfit);
double get_constraints_error(struct simulation *sim,struct fitconfig *config);
int fit_read_config(struct simulation *sim,struct fitconfig *config);
double fit_run_sims(struct simulation *fit,struct fitconfig *config);
int fit_now(struct simulation *sim,struct fitconfig *config);
void duplicate_global(struct simulation *sim,struct fitconfig *config,struct json *json_target);
void duplicate(struct simulation *sim,struct fitconfig *config,struct json *j,struct json_obj *json_fits_duplicate);
void fit_patch(struct simulation *sim,struct json *json_to_patch,struct json_obj *json_patch);
int get_fit_crashes(struct simulation *sim,struct fitconfig *config);

void fit_dump_log(struct simulation *sim,struct fitconfig *config,double error, double best_error);
void mass_copy_file(struct simulation *sim,struct fitconfig *config,char *input,int n);
void fit_build_jobs(struct simulation *sim,struct fitconfig *config);
void fit_load_vars(struct simulation *sim, struct json *in_json,struct fitconfig *config);
void fit_simplex_vars_to_multimin(struct simulation *sim,struct multimin *data,struct fitconfig *config);
void fit_save_vars(struct simulation *sim, struct json *j,struct fitconfig *config);
void fit_save_best_answer(struct simulation *sim,struct fitconfig *config, double error);
void fit_cmp_sim_and_exp(struct simulation *sim,struct json_obj *json_config, struct json_obj *json_import_config, struct math_xy *sim_data,struct math_xy *exp_data,char *sim_name);
double fit_get_sim_error(struct simulation *sim,struct fitconfig *config, int fit_number,int force_dump);
void fit_gen_plot(struct simulation *sim,struct fitconfig *config);
void fit_save_best_fit_files(struct simulation *sim,struct fitconfig *config);
int fit_randomize_json(struct simulation *sim, struct json *in_json, struct fitconfig *config);
void fit_vars_to_p(double *p,struct fitconfig *config);
int fit_vars_dump(struct simulation *sim, struct fitconfig *config);
void fit_p_to_vars(struct fitconfig *config, double *p);

//paths
int get_fit_dir_or_file_path(struct simulation *sim,char *out, struct fitconfig *config,int n,char *file_name);

//fit cpy
int fit_data_set_cpy(struct fit_data *out,struct fit_data *in);
int fit_fititem_cpy(struct fititem *out,struct fititem *in);
int fit_config_cpy(struct fitconfig *out,struct fitconfig *in);

//Fit config
int fit_config_init(struct fitconfig *config);
int fit_config_free(struct fitconfig *config);

//Fit item
int fititem_init(struct fititem *item);
int fititem_free(struct fititem *item);

//Fitting algos
int fit_newton(struct simulation *sim,struct fitconfig *config);
int fit_simplex(struct simulation *sim,struct fitconfig *config);

//fit_mcmc
int fit_mcmc(struct simulation *sim,struct fitconfig *config);
int fit_mcmc_dump_chains(struct simulation *sim,char *prefix,struct fitconfig *config);

//fit hmc
int fit_hmc(struct simulation *sim,struct fitconfig *config);
double U_hmc(struct simulation *sim,struct fitconfig *config, double *p, int i,char np );
double K_hmc(struct simulation *sim,struct fitconfig *config, double *p);
void grad_U_hmc(struct simulation *sim, struct fitconfig *config, double *grad, double *theta);
int fit_leapfrog_integration(struct simulation *sim, struct fitconfig *config, double *proposed_theta, double *proposed_momentum,
								double *theta, double *momentum, double *gradient);

//fit nuts
int fit_nuts(struct simulation *sim,struct fitconfig *config);

//fit_annealing
int fit_annealing(struct simulation *sim,struct fitconfig *config);

//Error functions
double my_f (struct simulation *sim,struct fitconfig *config);
double my_f_multimin (void *min,double *p);	//multimin wrappe for my_f
//void  my_df (const gsl_vector *v, void *params,  gsl_vector *df);
//void my_fdf (const gsl_vector *x, void *params, double *f, gsl_vector *df) ;
#endif
