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


int json_template_exciton(struct json_obj *obj_main)
{
	struct json_obj *obj_exciton;
	struct json_obj *obj_exciton_boundary;
	struct json_obj *text;
	obj_exciton=json_obj_add(obj_main,"exciton","",JSON_NODE);

	json_obj_add(obj_exciton,"exciton_enabled","false",JSON_BOOL);
	json_obj_add(obj_exciton,"exciton_max_ittr","20",JSON_INT);
	json_obj_add(obj_exciton,"exciton_min_error","1e-7",JSON_DOUBLE);
	json_obj_add(obj_exciton,"dump_verbosity","1",JSON_INT);
	json_obj_add(obj_exciton,"solver_verbosity","solver_verbosity_nothing",JSON_STRING);


	text=json_obj_add(obj_exciton,"text_exciton_interface","",JSON_INT);
	text->data_flags=JSON_PRIVATE;

	json_obj_add(obj_exciton,"exciton_split_at_interface","false",JSON_BOOL);
	json_obj_add(obj_exciton,"exciton_interface_depth","10e-9",JSON_DOUBLE);
	json_obj_add(obj_exciton,"exciton_interface_depth_u","nm",JSON_STRING);

	obj_exciton_boundary=json_obj_add(obj_exciton,"exciton_boundary","",JSON_NODE);

	json_obj_add(obj_exciton_boundary,"y0_boundry","neumann",JSON_STRING);
	json_obj_add(obj_exciton_boundary,"n_y0","1e24",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_y0","100.0",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_length_y0","1e-3",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"y1_boundry","heatsink",JSON_STRING);
	json_obj_add(obj_exciton_boundary,"n_y1","1e24",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_y1","0.1",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_length_y1","1e-2",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"x0_boundry","neumann",JSON_STRING);
	json_obj_add(obj_exciton_boundary,"n_x0","1e24",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_x0","0.1",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_length_x0","0.1",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"x1_boundry","neumann",JSON_STRING);
	json_obj_add(obj_exciton_boundary,"n_x1","1e24",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_x1","200.0",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_length_x1","0.1",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"z0_boundry","neumann",JSON_STRING);
	json_obj_add(obj_exciton_boundary,"n_z0","1e24",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_z0","200",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_length_z0","0.1",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"z1_boundry","neumann",JSON_STRING);
	json_obj_add(obj_exciton_boundary,"n_z1","1e24",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_z1","200.0",JSON_DOUBLE);
	json_obj_add(obj_exciton_boundary,"excitonsink_length_z1","0.1",JSON_DOUBLE);

	json_template_program(obj_exciton);
	return 0;
}
