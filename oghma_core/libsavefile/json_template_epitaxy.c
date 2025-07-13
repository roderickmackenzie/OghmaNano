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

int json_template_epitaxy(struct json_obj *obj_main)
{
	struct json_obj *text;
	struct json_obj *obj_epitaxy;
	struct json_obj *obj_template;
	struct json_obj *obj_contacts;
	struct json_obj *obj_contact_template;
	struct json_obj *obj_layer_interface;
	struct json_obj *obj_contact_node;
	obj_epitaxy=json_obj_add(obj_main,"epitaxy","",JSON_NODE);
	json_obj_add(obj_epitaxy,"icon_","layers",JSON_STRING);

	obj_template=json_obj_add(obj_epitaxy,"template","",JSON_TEMPLATE);
	json_shape(obj_template);

	obj_layer_interface=json_obj_add(obj_template,"layer_interface","",JSON_NODE);
		//Direct tunneling
			text=json_obj_add(obj_layer_interface,"text_interface_tunneling_direct","",JSON_STRING);
			text->data_flags=JSON_PRIVATE;

			json_obj_add(obj_layer_interface,"dir_tunnel_e","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"dir_tunnel_e_A","1e-15",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"dir_tunnel_e_B","1e-15",JSON_DOUBLE);

			json_obj_add(obj_layer_interface,"dir_tunnel_h","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"dir_tunnel_h_A","1e-15",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"dir_tunnel_h_B","1e-15",JSON_DOUBLE);

		//Fowler–Nordheim tunneling
			json_obj_add(obj_layer_interface,"fn_tunnel_e","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"fn_tunnel_e_A","1e-15",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"fn_tunnel_e_B","1e-15",JSON_DOUBLE);

			json_obj_add(obj_layer_interface,"fn_tunnel_h","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"fn_tunnel_h_A","1e-15",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"fn_tunnel_h_B","1e-15",JSON_DOUBLE);

		//Thermiomic emission
			json_obj_add(obj_layer_interface,"te_tunnel_e","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"te_tunnel_e_A","1e-15",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"te_tunnel_e_B","1e-15",JSON_DOUBLE);

			json_obj_add(obj_layer_interface,"te_tunnel_h","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"te_tunnel_h_A","1e-15",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"te_tunnel_h_B","1e-15",JSON_DOUBLE);

		//Hopping conduction
			json_obj_add(obj_layer_interface,"hc_tunnel_e","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"hc_tunnel_e_A","1e-15",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"hc_tunnel_e_B","1e-15",JSON_DOUBLE);

			json_obj_add(obj_layer_interface,"hc_tunnel_h","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"hc_tunnel_h_A","1e-15",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"hc_tunnel_h_B","1e-15",JSON_DOUBLE);

		//Tunnelling through heterojunctions organic-organic
			text=json_obj_add(obj_layer_interface,"text_interface_tunneling_organic","",JSON_STRING);
			text->data_flags=JSON_PRIVATE;
			json_obj_add(obj_layer_interface,"interface_tunnel_e","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"interface_Ge","1e-15",JSON_DOUBLE);

			json_obj_add(obj_layer_interface,"interface_tunnel_h","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"interface_Gh","1e-15",JSON_DOUBLE);

		//doping
			text=json_obj_add(obj_layer_interface,"text_interface_doping","",JSON_STRING);
			text->data_flags=JSON_PRIVATE;

			json_obj_add(obj_layer_interface,"interface_left_doping_enabled","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"interface_left_doping","1e20",JSON_DOUBLE);
			json_obj_add(obj_layer_interface,"interface_right_doping_enabled","false",JSON_BOOL);
			json_obj_add(obj_layer_interface,"interface_right_doping","1e20",JSON_DOUBLE);

		//recombination interface models
			json_obj_add(obj_layer_interface,"interface_model","none",JSON_STRING);
			json_obj_add(obj_layer_interface,"interface_eh_tau","1e-15",JSON_DOUBLE);

	json_obj_add(obj_template,"solve_optical_problem","yes_nk",JSON_STRING);
	json_obj_add(obj_template,"solve_thermal_problem","true",JSON_BOOL);


	//obj_sub_shape_template=json_obj_add(obj_template,"template","",JSON_TEMPLATE);
	//json_shape(obj_sub_shape_template);

	obj_contacts=json_obj_add(obj_epitaxy,"contacts","",JSON_NODE);

	json_obj_add(obj_contacts,"show_minority","false",JSON_BOOL);

	obj_contact_template=json_obj_add(obj_contacts,"template","",JSON_TEMPLATE);
	json_shape(obj_contact_template);
	obj_contact_node=json_obj_add(obj_contact_template,"contact","",JSON_NODE);
	json_obj_add(obj_contact_node,"position","top",JSON_STRING);
	json_obj_add(obj_contact_node,"applied_voltage_type","constant",JSON_STRING);
	json_obj_add(obj_contact_node,"applied_voltage","-2.0",JSON_DOUBLE);
	json_obj_add(obj_contact_node,"contact_resistance_sq","0.0",JSON_DOUBLE);
	json_obj_add(obj_contact_node,"shunt_resistance_sq","0.0",JSON_DOUBLE);
	json_obj_add(obj_contact_node,"np","1e20",JSON_DOUBLE);
	json_obj_add(obj_contact_node,"majority","electron",JSON_STRING);
	json_obj_add(obj_contact_node,"minority","hole",JSON_STRING);
	json_obj_add(obj_contact_node,"majority_model","ohmic",JSON_STRING);
	json_obj_add(obj_contact_node,"minority_model","ohmic",JSON_STRING);
	json_obj_add(obj_contact_node,"majority_v0","1e5",JSON_DOUBLE);
	json_obj_add(obj_contact_node,"minority_v0","1e5",JSON_DOUBLE);
	json_obj_add(obj_contact_node,"majority_mu","1e-8",JSON_DOUBLE);
	json_obj_add(obj_contact_node,"minority_mu","1e-8",JSON_DOUBLE);

	//old not used any more
	//json_obj_add(obj_contact_template,"position","top",JSON_STRING);
	//json_obj_add(obj_contact_template,"applied_voltage_type","constant",JSON_STRING);
	//json_obj_add(obj_contact_template,"applied_voltage","-2.0",JSON_DOUBLE);
	//json_obj_add(obj_contact_template,"contact_resistance_sq","0.0",JSON_DOUBLE);
	//json_obj_add(obj_contact_template,"shunt_resistance_sq","0.0",JSON_DOUBLE);
	//json_obj_add(obj_contact_template,"np","1e20",JSON_DOUBLE);
	//json_obj_add(obj_contact_template,"charge_type","electron",JSON_STRING);
	//json_obj_add(obj_contact_template,"physical_model","ohmic",JSON_STRING);
	//json_obj_add(obj_contact_template,"ve0","1e5",JSON_DOUBLE);
	//json_obj_add(obj_contact_template,"vh0","1e5",JSON_DOUBLE);
	return 0;
}
