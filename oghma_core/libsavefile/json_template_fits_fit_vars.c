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

int json_template_fits_fit_vars(struct json_obj *obj_fits)
{
	struct json_obj *obj_fit_fit_vars;
	struct json_obj *obj_template;

	obj_fit_fit_vars=json_obj_add(obj_fits,"vars","",JSON_NODE);
	json_obj_add(obj_fit_fit_vars,"icon_","vars",JSON_STRING);

	obj_template=json_obj_add(obj_fit_fit_vars,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"fit_var_enabled","true",JSON_BOOL);
	json_obj_add(obj_template,"human_var","one/two/three",JSON_STRING);
	json_obj_add(obj_template,"json_var","one/two/three",JSON_STRING);
	json_obj_add(obj_template,"min","0.0",JSON_DOUBLE);
	json_obj_add(obj_template,"max","100.0",JSON_DOUBLE);
	json_obj_add(obj_template,"log_fit","false",JSON_BOOL);
	json_obj_add(obj_template,"error","100.0",JSON_DOUBLE);

	return 0;
}
