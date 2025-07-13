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

/** @file sim.c
@brief init sim structure
*/


#include <enabled_libs.h>
#include <json.h>
#include <savefile.h>

int json_template_fits_fit_config(struct json_obj *obj_fits)
{
	struct json_obj *obj_fit_config;
	struct json_obj *text;

	obj_fit_config=json_obj_add(obj_fits,"fit_config","", JSON_NODE);
	text=json_obj_add(obj_fit_config,"text_fit_method_","", JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_fit_config,"fit_method","simplex", JSON_STRING);

	//simplex
	text=json_obj_add(obj_fit_config,"text_fit_simplex_","", JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_fit_config,"fit_simplexmul","0.1", JSON_DOUBLE);
	json_obj_add(obj_fit_config,"fit_enable_simple_reset","false", JSON_BOOL);
	json_obj_add(obj_fit_config,"fit_simplex_reset","1000", JSON_INT);
	json_obj_add(obj_fit_config,"fit_disable_reset_at","0.095", JSON_DOUBLE);
	json_obj_add(obj_fit_config,"fit_randomize","false", JSON_BOOL);
	json_obj_add(obj_fit_config,"fit_stall_steps","400", JSON_INT);

	//newton
	json_obj_add(obj_fit_config,"fit_newton_clamp", "1.0", JSON_DOUBLE);
	json_obj_add(obj_fit_config,"fit_newton_steps", "1000", JSON_INT);
	json_obj_add(obj_fit_config,"fit_newton_random_reset","true", JSON_BOOL);

	//Thermal Annealing
	json_obj_add(obj_fit_config,"fit_cooling_const","10.0", JSON_DOUBLE);
	json_obj_add(obj_fit_config,"fit_annealing_steps", "1000", JSON_INT);
	json_obj_add(obj_fit_config,"fit_annealing_random_reset","true", JSON_BOOL);

	//MCMC
	json_obj_add(obj_fit_config,"fit_mcmc_steps","1000", JSON_INT);
	json_obj_add(obj_fit_config,"fit_sigma","200.0", JSON_DOUBLE);
	json_obj_add(obj_fit_config,"fit_mcmc_dump","100", JSON_INT);
	json_obj_add(obj_fit_config,"fit_leapfrog_steps","10", JSON_INT);
	json_obj_add(obj_fit_config,"fit_mcmc_random_reset","false", JSON_BOOL);

	//HMC
	json_obj_add(obj_fit_config,"fit_hmc_random_reset","false", JSON_BOOL);

	//Fit Control
	text=json_obj_add(obj_fit_config,"text_fit_control_","", JSON_STRING);
	text->data_flags=JSON_PRIVATE;


	json_obj_add(obj_fit_config,"fit_converge_error","1e-3", JSON_DOUBLE);

	json_obj_add(obj_fit_config,"fit_dump_snapshots","false", JSON_BOOL);
	json_obj_add(obj_fit_config,"fit_run_forever","true", JSON_BOOL);


	return 0;
}
