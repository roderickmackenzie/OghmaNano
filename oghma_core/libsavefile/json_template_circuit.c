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


int json_template_circuit(struct json_obj *obj_main)
{
	struct json_obj *obj_circuit;
	struct json_obj *obj_circuit_diagram;
	struct json_obj *obj_circuit_config;
	struct json_obj *obj_component_template;

	obj_circuit=json_obj_add(obj_main,"circuit","",JSON_NODE);
	json_obj_add(obj_circuit,"enabled","false",JSON_BOOL);
	json_obj_add(obj_circuit,"icon_","kirchhoff",JSON_STRING);

	obj_circuit_diagram=json_obj_add(obj_circuit,"circuit_diagram","",JSON_NODE);
	obj_component_template=json_obj_add(obj_circuit_diagram,"template","",JSON_TEMPLATE);
	json_obj_add(obj_component_template,"name","component",JSON_STRING);
	json_obj_add(obj_component_template,"comp","resistor",JSON_STRING);
	json_obj_add(obj_component_template,"x0","2",JSON_INT);
	json_obj_add(obj_component_template,"y0","2",JSON_INT);
	json_obj_add(obj_component_template,"x1","3",JSON_INT);
	json_obj_add(obj_component_template,"y1","3",JSON_INT);
	json_obj_add(obj_component_template,"R","10.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"R_sigma","0.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"C","0.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"L","0.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"a","1e-3",JSON_DOUBLE);
	json_obj_add(obj_component_template,"a_sigma","0.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"b","1e-3",JSON_DOUBLE);
	json_obj_add(obj_component_template,"b_sigma","0.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"c","1e-3",JSON_DOUBLE);
	json_obj_add(obj_component_template,"c_sigma","0.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"nid","1.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"nid_sigma","0.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"I0","1e-12",JSON_DOUBLE);
	json_obj_add(obj_component_template,"I0_sigma","0.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"b0","0.1",JSON_DOUBLE);
	json_obj_add(obj_component_template,"b0_sigma","0.1",JSON_DOUBLE);
	json_obj_add(obj_component_template,"phi0","0.1",JSON_DOUBLE);
	json_obj_add(obj_component_template,"phi0_sigma","0.1",JSON_DOUBLE);
	json_obj_add(obj_component_template,"layer","none",JSON_STRING);
	json_obj_add(obj_component_template,"Dphotoneff","1.0",JSON_DOUBLE);
	json_obj_add(obj_component_template,"com_enable_sigma","false",JSON_BOOL);
	json_obj_add(obj_component_template,"count","1",JSON_INT);

	obj_circuit_config=json_obj_add(obj_circuit,"config","",JSON_NODE);
	json_obj_add(obj_circuit_config,"solver_verbosity","solver_verbosity_at_end",JSON_STRING);
	json_obj_add(obj_circuit_config,"circuit_mesh_src","hand_drawn",JSON_STRING);

	return 0;
}
