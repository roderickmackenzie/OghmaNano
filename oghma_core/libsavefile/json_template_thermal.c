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

int json_template_thermal(struct json_obj *obj_main)
{
	struct json_obj *obj_thermal;
	struct json_obj *obj_thermal_boundary;
	obj_thermal=json_obj_add(obj_main,"thermal","",JSON_NODE);

	json_obj_add(obj_thermal,"icon_","thermal",JSON_STRING);
	json_obj_add(obj_thermal,"set_point","300.0",JSON_DOUBLE);
	json_template_mesh(obj_thermal, TRUE,TRUE, TRUE, TRUE, FALSE);

	obj_thermal_boundary=json_obj_add(obj_thermal,"thermal_boundary","",JSON_NODE);
	json_obj_add(obj_thermal_boundary,"y0_boundry","neumann",JSON_STRING);
	json_obj_add(obj_thermal_boundary,"Ty0","300.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_y0","100.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_length_y0","1e-3",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"y1_boundry","heatsink",JSON_STRING);
	json_obj_add(obj_thermal_boundary,"Ty1","300.0", JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_y1","0.1",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_length_y1","1e-2",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"x0_boundry","neumann",JSON_STRING);
	json_obj_add(obj_thermal_boundary,"Tx0","300.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_x0","0.1",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_length_x0","0.1",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"x1_boundry","neumann",JSON_STRING);
	json_obj_add(obj_thermal_boundary,"Tx1","300.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_x1","200.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_length_x1","0.1",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"z0_boundry","neumann",JSON_STRING);
	json_obj_add(obj_thermal_boundary,"Tz0","300.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_z0","200.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_length_z0","0.1",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"z1_boundry","neumann",JSON_STRING);
	json_obj_add(obj_thermal_boundary,"Tz1","300.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_z1","200.0",JSON_DOUBLE);
	json_obj_add(obj_thermal_boundary,"heatsink_length_z1","0.1",JSON_DOUBLE);

	json_obj_add(obj_thermal,"thermal","false",JSON_BOOL);
	json_obj_add(obj_thermal,"thermal_model_type","thermal_lattice",JSON_STRING);
	json_obj_add(obj_thermal,"thermal_l","true",JSON_BOOL);
	json_obj_add(obj_thermal,"thermal_e","false",JSON_BOOL);
	json_obj_add(obj_thermal,"thermal_h","false",JSON_BOOL);
	json_obj_add(obj_thermal,"nofluxl","1",JSON_INT);
	json_obj_add(obj_thermal,"thermal_max_ittr","20",JSON_INT);
	json_obj_add(obj_thermal,"thermal_min_error","1e-7",JSON_DOUBLE);
	json_obj_add(obj_thermal,"joule_heating","true",JSON_BOOL);
	json_obj_add(obj_thermal,"parasitic_heating","true",JSON_BOOL);
	json_obj_add(obj_thermal,"thermal_couple_to_electrical_solver","true",JSON_BOOL);
	json_obj_add(obj_thermal,"recombination_heating","false",JSON_BOOL);
	json_obj_add(obj_thermal,"optical_heating","false",JSON_BOOL);
	json_obj_add(obj_thermal,"dump_verbosity","1",JSON_INT);
	json_obj_add(obj_thermal,"solver_verbosity","solver_verbosity_nothing",JSON_STRING);

	return 0;
}
