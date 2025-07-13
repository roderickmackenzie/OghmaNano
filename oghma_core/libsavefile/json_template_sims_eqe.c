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

int json_template_sims_eqe(struct json_obj *obj_sims)
{
	struct json_obj *obj_eqe;
	struct json_obj *obj_template;
	struct json_obj *text;

	//eqe
	obj_eqe=json_obj_add(obj_sims,"eqe","",JSON_NODE);
	json_obj_add(obj_eqe,"icon_","qe",JSON_STRING);

	obj_template=json_obj_add(obj_eqe,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","EQE",JSON_STRING);
	json_obj_add(obj_template,"icon","qe",JSON_STRING);

	//config
		json_obj_add(obj_template,"eqe_voltage","-20.0",JSON_DOUBLE);
		json_obj_add(obj_template,"eqe_light_power2","1.0",JSON_DOUBLE);
		json_obj_add(obj_template,"eqe_single_light_point","True",JSON_BOOL);
		json_obj_add(obj_template,"eqe_suns_start","1e-3",JSON_DOUBLE);
		json_obj_add(obj_template,"eqe_suns_stop","1.0",JSON_DOUBLE);
		json_obj_add(obj_template,"eqe_wavelength","532e-9",JSON_DOUBLE);
		json_obj_add(obj_template,"eqe_use_electrical_dos","False",JSON_BOOL);
		//Generation model
		text=json_obj_add(obj_template,"text_generation_","",JSON_STRING);
		text->data_flags=JSON_PRIVATE;
		json_obj_add(obj_template,"charge_carrier_generation_model","transfer_matrix",JSON_STRING);

	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	return 0;
}
