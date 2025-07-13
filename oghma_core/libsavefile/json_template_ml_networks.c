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

int json_template_ml_networks(struct json_obj *obj_root)
{
	struct json_obj *obj_ml_networks;
	struct json_obj *obj_ml_networks_template;
	struct json_obj *obj_ml_networks_config;
	struct json_obj *obj_ml_network_inputs;
	struct json_obj *obj_ml_network_inputs_template;
	struct json_obj *obj_ml_network_outputs;
	struct json_obj *obj_ml_network_outputs_template;

	obj_ml_networks=json_obj_add(obj_root,"ml_networks","",JSON_NODE);
	json_obj_add(obj_ml_networks,"id","",JSON_RANDOM_ID);
	obj_ml_networks_config=json_obj_add(obj_ml_networks,"config","",JSON_NODE);
	json_obj_add(obj_ml_networks_config,"none","none",JSON_STRING);

	obj_ml_networks_template=json_obj_add(obj_ml_networks,"template","",JSON_TEMPLATE);
	json_obj_add(obj_ml_networks_template,"icon","neural_network",JSON_STRING);
	json_obj_add(obj_ml_networks_template,"name","name",JSON_STRING);
	json_obj_add(obj_ml_networks_template,"enabled","true",JSON_BOOL);

		//ml_network_inputs
		obj_ml_network_inputs=json_obj_add(obj_ml_networks_template,"ml_network_inputs","",JSON_NODE);
		json_obj_add(obj_ml_network_inputs,"none","none",JSON_STRING);
		obj_ml_network_inputs_template=json_obj_add(obj_ml_network_inputs,"template","",JSON_TEMPLATE);
		json_obj_add(obj_ml_network_inputs_template,"ml_input_vector","Input vector",JSON_STRING);

		//ml_network_outputs
		obj_ml_network_outputs=json_obj_add(obj_ml_networks_template,"ml_network_outputs","",JSON_NODE);
		json_obj_add(obj_ml_network_outputs,"none","none",JSON_STRING);
		obj_ml_network_outputs_template=json_obj_add(obj_ml_network_outputs,"template","",JSON_TEMPLATE);
		json_obj_add(obj_ml_network_outputs_template,"ml_output_vector","Output vector",JSON_STRING);

	json_obj_add(obj_ml_networks_template,"id","",JSON_RANDOM_ID);


	return 0;
}
