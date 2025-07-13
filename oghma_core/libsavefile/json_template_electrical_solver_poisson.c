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

/** @file json_template_electrical_solver_poisson.c
@brief json_template_electrical_solver_poisson
*/


#include <enabled_libs.h>
#include <json.h>
#include <savefile.h>

int json_template_electrical_solver_poisson(struct json_obj *obj_electrical_solver)
{
	struct json_obj *obj_poisson;

	obj_poisson=json_obj_add(obj_electrical_solver,"poisson","",JSON_NODE);

	json_obj_add(obj_poisson,"posclamp","1.0",JSON_DOUBLE);
	json_obj_add(obj_poisson,"pos_max_ittr","100",JSON_DOUBLE);
	json_obj_add(obj_poisson,"pos_min_error","1e-4",JSON_DOUBLE);
	json_obj_add(obj_poisson,"math_enable_pos_solver","true",JSON_BOOL);
	json_obj_add(obj_poisson,"dump_print_pos_error","false",JSON_BOOL);
	json_obj_add(obj_poisson,"pos_dump_verbosity","0",JSON_INT);
	json_obj_add(obj_poisson,"solver_verbosity","solver_verbosity_nothing",JSON_STRING);

	return 0;
}
