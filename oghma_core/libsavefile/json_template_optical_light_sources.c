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

int json_virtual_sepctra(struct json_obj *obj)
{

	struct json_obj *obj_virtual_spectra;
	struct json_obj *obj_light_spectra;
	struct json_obj *obj_light_filters;
	struct json_obj *obj_external_interface;
	struct json_obj *obj_light_spectra_template;
	struct json_obj *obj_light_filters_template;
	//virtual spectra
	obj_virtual_spectra=json_obj_add(obj,"virtual_spectra","",JSON_NODE);

	obj_light_spectra=json_obj_add(obj_virtual_spectra,"light_spectra","",JSON_NODE);
	obj_light_spectra_template=json_obj_add(obj_light_spectra,"template","",JSON_TEMPLATE);
	json_obj_add(obj_light_spectra_template,"light_spectrum","AM1.5G",JSON_STRING);
	json_obj_add(obj_light_spectra_template,"light_multiplyer","1.0",JSON_DOUBLE);
	json_obj_add(obj_light_spectra_template,"id","",JSON_RANDOM_ID);


	obj_light_filters=json_obj_add(obj_virtual_spectra,"light_filters","",JSON_NODE);
	obj_light_filters_template=json_obj_add(obj_light_filters,"template","",JSON_TEMPLATE);
	json_obj_add(obj_light_filters_template,"filter_enabled","false",JSON_BOOL);
	json_obj_add(obj_light_filters_template,"filter_material","glasses/glass",JSON_STRING);
	json_obj_add(obj_light_filters_template,"filter_invert","true",JSON_BOOL);
	json_obj_add(obj_light_filters_template,"filter_db","1000.0",JSON_DOUBLE);
	json_obj_add(obj_light_filters_template,"id","",JSON_RANDOM_ID);

	obj_external_interface=json_obj_add(obj_virtual_spectra,"external_interface","",JSON_NODE);
	json_obj_add(obj_external_interface,"enabled","false",JSON_BOOL);
	json_obj_add(obj_external_interface,"light_external_n","1.0",JSON_DOUBLE);

	json_obj_add(obj_virtual_spectra,"id","",JSON_RANDOM_ID);

	return 0;
}

int json_template_optical_light_sources(struct json_obj *obj_optical)
{
	struct json_obj *obj_light_sources;
	struct json_obj *obj_lights;
	struct json_obj *obj_light_template;
	obj_light_sources=json_obj_add(obj_optical,"light_sources","",JSON_NODE);
	json_obj_add(obj_light_sources,"Psun","1.0",JSON_DOUBLE);

	obj_lights=json_obj_add(obj_light_sources,"lights","",JSON_NODE);

	obj_light_template=json_obj_add(obj_lights,"template","",JSON_TEMPLATE);
	json_world_object(obj_light_template);

	//json_obj_add(obj_light_template,"name","Light\\nsource",JSON_STRING);
	json_obj_add(obj_light_template,"icon","lighthouse",JSON_STRING);

	json_obj_add(obj_light_template,"light_illuminate_from","y0",JSON_STRING);

	json_virtual_sepctra(obj_light_template);

	json_obj_add(obj_light_template,"ray_theta_steps","200",JSON_INT);
	json_obj_add(obj_light_template,"ray_theta_start","0",JSON_INT);
	json_obj_add(obj_light_template,"ray_theta_stop","360",JSON_INT);
	json_obj_add(obj_light_template,"ray_phi_steps","5",JSON_INT);
	json_obj_add(obj_light_template,"ray_phi_start","0",JSON_INT);
	json_obj_add(obj_light_template,"ray_phi_stop","360",JSON_INT);
	json_obj_add(obj_light_template,"filter_local_ground_view_factor","180.0",JSON_DOUBLE);

	return 0;
}
