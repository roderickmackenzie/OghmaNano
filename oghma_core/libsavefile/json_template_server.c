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

int json_template_server(struct json_obj *obj_main)
{
	struct json_obj *obj_server;
	struct json_obj *text;
	obj_server=json_obj_add(obj_main,"server","",JSON_NODE);
	text=json_obj_add(obj_server,"text_newton_first_itt_","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_server,"maxelectricalitt_first","1000",JSON_INT);
	json_obj_add(obj_server,"electricalclamp_first","0.1",JSON_DOUBLE);
	json_obj_add(obj_server,"math_electrical_error_first","1e-9",JSON_DOUBLE);
	json_obj_add(obj_server,"newton_first_temperature_ramp","True",JSON_BOOL);

	text=json_obj_add(obj_server,"text_cpu","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_server,"core_max_threads","0",JSON_STRING);
	json_obj_add(obj_server,"server_stall_time","2000",JSON_INT);
	json_obj_add(obj_server,"server_max_run_time","345600",JSON_INT);
	json_obj_add(obj_server,"server_min_cpus","1",JSON_INT);
	json_obj_add(obj_server,"server_steel","0",JSON_INT);
	json_obj_add(obj_server,"server_use_dos_disk_cache","true",JSON_BOOL);
	json_obj_add(obj_server,"max_core_instances","0",JSON_STRING);
	text=json_obj_add(obj_server,"text_gpu","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_server,"use_gpu","false",JSON_BOOL);
	json_obj_add(obj_server,"gpu_name","none",JSON_STRING);

	return 0;
}
