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

/** @file fit_struct.h
@brief functions for fitting.
*/

#ifndef fit_struct_h
#define fit_struct_h
#include <g_io.h>
#include <advmath.h>
#include <simplex_struct.h>
#include <json_struct.h>
#include <math_xy_struct.h>

struct fit_data
{
	int enabled;
	int run_this_simulation;
	char fit_name[200];
	char fit_agaist[200];
	char sim_data[200];
	struct json_obj *json_fit_patch;
	struct json_obj *json_fit_duplicate_local;
	struct json_obj *json_fit_config;
	struct json_obj *json_fit_import_config;
	double error;
};

struct fititem
{
	double min;
	double max;
	double add_error;
	int log_fit;
	char json_token[200];
	double value;		//Can be on a log
	double true_value;	//Can never be log
	//Monte carlo
	struct math_xy chain_accepted;	//Markov chain
	struct math_xy chain_all;	//Markov chain
};

struct fitconfig
{
	char dir_prefix[100];

	int data_sets;
	struct fit_data *data_set;

	double simplexmul;
	int simplexreset;
	int fitvars;
	struct fititem *fititem;
	int randomize;
	double disable_reset_at;
	double converge_error;
	int enable_simple_reset;
	double constraints_error[100];
	int n_constraints;
	int iterations;
	int sub_iterations;
	int sub_iterations_two;
	int stall_steps;
	int fit_method;
	double best_ever_error;
	double sigma;
	int store_log_values_as_logged;


	//Monte carlo
	struct math_xy loglikelihood;	//Markov chain
	int fit_mcmc_dump;
	int accept;
	int reject;

	//Thermal annealing
	double fit_cooling_const;
	int fit_annealing_steps;
	int fit_annealing_random_reset;

	//mcmc
	int fit_mcmc_steps;
	int fit_mcmc_random_reset;

	//HMC
	int fit_hmc_random_reset;
	int leapfrog_steps;
	double *step_size;

	//Newton
	double fit_newton_clamp;
	int fit_newton_steps;
	int fit_newton_random_reset;

	//Fit control
	int fit_run_forever;
	int automatically_save_best_answers;
};

#endif
