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
#include <sim.h>
#include <string.h>
#include <savefile.h>
#include <lock.h>
#include <mesh.h>
#include <memory.h>
#include <log.h>
#include <gui_hooks.h>
#include <json.h>

int json_local(struct json *j)
{
	json_free(j);
	struct json_obj *obj_main;
	struct json_obj *obj_international;
	struct json_obj *obj_opencl;
	struct json_obj *obj_gui_config;
	struct json_obj *obj_icon_lib;
	struct json_obj *obj_cluster;
	struct json_obj *obj_cluster_config;
	struct json_obj *obj_cluster_template;
	struct json_obj *obj_windows;
	struct json_obj *obj_os;
	struct json_obj *obj_window_template;


	j->is_template=TRUE;

	obj_main=&(j->obj);
	//international
		obj_international=json_obj_add(obj_main,"international","",JSON_NODE);
		json_obj_add(obj_international,"lang","auto",JSON_STRING);

	//opencl
		obj_opencl=json_obj_add(obj_main,"opencl","",JSON_NODE);
		json_obj_add(obj_opencl,"device","none",JSON_STRING);

	//gui_config
		obj_gui_config=json_obj_add(obj_main,"gui_config","",JSON_NODE);
		json_obj_add(obj_gui_config,"enable_opengl","true",JSON_BOOL);
		json_obj_add(obj_gui_config,"gui_use_icon_theme","false",JSON_BOOL);
		json_obj_add(obj_gui_config,"matlab_interpreter","octave",JSON_STRING);
		json_obj_add(obj_gui_config,"enable_webbrowser","false",JSON_BOOL);
		json_obj_add(obj_gui_config,"enable_betafeatures","false",JSON_BOOL);
		json_obj_add(obj_gui_config,"toolbar_icon_size","48",JSON_INT);

	//icon_lib
		obj_icon_lib=json_obj_add(obj_main,"icon_lib","",JSON_NODE);
		json_obj_add(obj_icon_lib,"text-x-generic","text-x-generic",JSON_STRING);
		json_obj_add(obj_icon_lib,"wps-office-xls","wps-office-xls",JSON_STRING);
		json_obj_add(obj_icon_lib,"info","info_file",JSON_STRING);
		json_obj_add(obj_icon_lib,"text-x-generic","text-x-generic",JSON_STRING);
		json_obj_add(obj_icon_lib,"wps-office-xls","wps-office-xls",JSON_STRING);
		json_obj_add(obj_icon_lib,"spectra","spectra_file",JSON_STRING);
		json_obj_add(obj_icon_lib,"organic_material","organic_material",JSON_STRING);
		json_obj_add(obj_icon_lib,".png","image-png",JSON_STRING);
		json_obj_add(obj_icon_lib,".oghma","si",JSON_STRING);
		json_obj_add(obj_icon_lib,".xlsx","wps-office-xls",JSON_STRING);
		json_obj_add(obj_icon_lib,".pdf","pdf",JSON_STRING);
		json_obj_add(obj_icon_lib,"desktop","folder",JSON_STRING);
		json_obj_add(obj_icon_lib,"constraints","dat_file",JSON_STRING);

	//cluster
		obj_cluster=json_obj_add(obj_main,"cluster","",JSON_NODE);
		obj_cluster_template=json_obj_add(obj_cluster,"template","",JSON_TEMPLATE);
		json_obj_add(obj_cluster_template,"name","Cluster",JSON_STRING);
		json_obj_add(obj_cluster_template,"icon","server",JSON_STRING);
		json_obj_add(obj_cluster_template,"enabled","true",JSON_BOOL);
		//cluster_config
			obj_cluster_config=json_obj_add(obj_cluster_template,"config","",JSON_NODE);
			json_obj_add(obj_cluster_config,"cluster_iv","none",JSON_STRING);
			json_obj_add(obj_cluster_config,"cluster_key","none",JSON_STRING);
			json_obj_add(obj_cluster_config,"cluster_user_name","none",JSON_STRING);
			json_obj_add(obj_cluster_config,"cluster_ip","127.0.0.1",JSON_STRING);
			json_obj_add(obj_cluster_config,"cluster_cluster_dir","none",JSON_STRING);
			json_obj_add(obj_cluster_config,"cluster_master_ip","127.0.0.1",JSON_STRING);
			json_obj_add(obj_cluster_config,"cluster_node_list","",JSON_STRING);

		json_obj_add(obj_cluster_template,"id","",JSON_RANDOM_ID);

	//windows
		obj_windows=json_obj_add(obj_main,"windows","",JSON_NODE);
		obj_window_template=json_obj_add(obj_windows,"template","",JSON_TEMPLATE);
		json_obj_add(obj_window_template,"name","none",JSON_STRING);
		json_obj_add(obj_window_template,"x","-1",JSON_INT);
		json_obj_add(obj_window_template,"y","-1",JSON_INT);


	//os
		obj_os=json_obj_add(obj_main,"os","",JSON_NODE);
		json_obj_add(obj_os,"use_wine","false",JSON_BOOL);

	//json_dump_all(j);
	
	return 0;
}
