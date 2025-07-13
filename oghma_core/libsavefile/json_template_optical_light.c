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

int json_template_optical_light(struct json_obj *obj_optical)
{
	struct json_obj *obj_light;
	obj_light=json_obj_add(obj_optical,"light","",JSON_NODE);
	json_obj_add(obj_light,"light_model","full",JSON_STRING);
	json_obj_add(obj_light,"sun","AM1.5G",JSON_STRING);
	json_obj_add(obj_light,"Dphotoneff","1.0",JSON_DOUBLE);
	json_obj_add(obj_light,"incoherent_wavelengths","5",JSON_INT);
	json_obj_add(obj_light,"NDfilter","0.000000e+00",JSON_DOUBLE);
	json_obj_add(obj_light,"light_flat_generation_rate","2e28",JSON_DOUBLE);
	json_obj_add(obj_light,"light_file_generation","Gn.inp",JSON_STRING);
	json_obj_add(obj_light,"light_file_qe_spectra","",JSON_STRING);
	json_obj_add(obj_light,"light_file_generation_shift","200e-9",JSON_DOUBLE);
	json_obj_add(obj_light,"dump_verbosity","10",JSON_INT);
	json_obj_add(obj_light,"mesh_eq_device_layers","false",JSON_BOOL);

	return 0;
}
