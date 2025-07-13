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

int json_template_math(struct json_obj *obj_main)
{
	struct json_obj *obj_math;
	struct json_obj *obj_random;
	struct json_obj *obj_matrix;
	struct json_obj *text;
	obj_math=json_obj_add(obj_main,"math","",JSON_NODE);

	text=json_obj_add(obj_math,"text_newton_first_itt","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;

	json_obj_add(obj_math,"maxelectricalitt_first","1000",JSON_INT);
	json_obj_add(obj_math,"electricalclamp_first","0.1",JSON_DOUBLE);
	json_obj_add(obj_math,"math_electrical_error_first","1e-9",JSON_DOUBLE);
	json_obj_add(obj_math,"newton_first_temperature_ramp","True",JSON_BOOL);

	text=json_obj_add(obj_math,"text_newton_later_itt","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_math,"maxelectricalitt","100",JSON_INT);
	json_obj_add(obj_math,"electricalclamp","1.0",JSON_DOUBLE);
	json_obj_add(obj_math,"electricalerror","1e-8",JSON_DOUBLE);

	text=json_obj_add(obj_math,"text_newton_exit_strategy","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_math,"newton_clever_exit","True",JSON_BOOL);
	json_obj_add(obj_math,"newton_min_itt","5",JSON_INT);
	json_obj_add(obj_math,"remesh","False",JSON_BOOL);
	json_obj_add(obj_math,"newmeshsize","8",JSON_INT);
	json_obj_add(obj_math,"kl_in_newton","True",JSON_BOOL);

	text=json_obj_add(obj_math,"text_newton_solver_type","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;

	json_obj_add(obj_math,"newton_name","newton",JSON_STRING);

	//Electrical solver block normalization
		text=json_obj_add(obj_math,"text_solver_normalization","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_math,"matrix_block_normalization","False",JSON_BOOL);
		json_obj_add(obj_math,"block_auto","True",JSON_BOOL);
		json_obj_add(obj_math,"block_phi_norm","1e3",JSON_DOUBLE);
		json_obj_add(obj_math,"block_Je_norm","1e20",JSON_DOUBLE);
		json_obj_add(obj_math,"block_Jh_norm","1e20",JSON_DOUBLE);
		json_obj_add(obj_math,"block_srh_e_norm","1e20",JSON_DOUBLE);
		json_obj_add(obj_math,"block_srh_h_norm","1e20",JSON_DOUBLE);

	//Matrix threshold
		text=json_obj_add(obj_math,"text_solver_threshold","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_math,"matrix_threshold_enabled","False",JSON_BOOL);
		json_obj_add(obj_math,"matrix_threshold","1e-20",JSON_DOUBLE);

	//Current
		text=json_obj_add(obj_math,"text_newton_current","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_math,"math_current_calc_at","contacts",JSON_STRING);
		json_obj_add(obj_math,"use_sg_currents","True",JSON_BOOL);

	//Output
		text=json_obj_add(obj_math,"text_newton_output","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_math,"math_dynamic_mesh","False",JSON_BOOL);
		json_obj_add(obj_math,"math_stop_on_convergence_problem","False",JSON_BOOL);
		json_obj_add(obj_math,"math_stop_on_inverted_fermi_level","False",JSON_BOOL);
		json_obj_add(obj_math,"solver_verbosity","solver_verbosity_at_end",JSON_STRING);

	obj_random=json_obj_add(obj_math,"random","",JSON_NODE);
	json_obj_add(obj_random,"random_function","random_twister",JSON_STRING);
	json_obj_add(obj_random,"random_init","random_time",JSON_STRING);
	json_obj_add(obj_random,"random_seed","42",JSON_INT);

	obj_matrix=json_obj_add(obj_math,"matrix","",JSON_NODE);
	text=json_obj_add(obj_matrix,"text_real_solver_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_matrix,"solver_name","umfpack",JSON_STRING);
	json_obj_add(obj_matrix,"core_max_threads","all",JSON_STRING);
	json_obj_add(obj_matrix,"matrix_dump_error","False",JSON_BOOL);
	json_obj_add(obj_matrix,"matrix_dump_every_matrix","False",JSON_BOOL);

	text=json_obj_add(obj_matrix,"text_complex_solver_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_matrix,"complex_solver_name","complex_umfpack",JSON_STRING);
	return 0;
}
