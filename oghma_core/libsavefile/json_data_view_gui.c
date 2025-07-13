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

int data_view_gui_config(struct json_obj *obj_gui_config)
{
	struct json_obj *obj_jv;
	struct json_obj *obj_template;
	struct json_obj *obj_template_user_input;
	struct json_obj *obj_template_plot_2d;
	struct json_obj *obj_template_plot_2d_trap_map;
	struct json_obj *obj_template_plot_3d;
	struct json_obj *obj_template_plot_3d_view;
	struct json_obj *obj_template_plot_3d_background;
	struct json_obj *obj_template_plot_3d_objects;

	obj_jv=json_obj_add(obj_gui_config,"plots","",JSON_NODE);
	json_obj_add(obj_jv,"icon_","plot",JSON_STRING);

	obj_template=json_obj_add(obj_jv,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","name",JSON_STRING);
	json_obj_add(obj_template,"icon","plot",JSON_STRING);
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	//user input
		obj_template_user_input=json_obj_add(obj_template,"user_input","",JSON_NODE);
		json_obj_add(obj_template_user_input,"enable_view_move","true",JSON_BOOL);

	///2d config
		obj_template_plot_2d=json_obj_add(obj_template,"config_2d","",JSON_NODE);
		obj_template_plot_2d_trap_map=json_obj_add(obj_template_plot_2d,"trap_map","",JSON_NODE);
		json_obj_add(obj_template_plot_2d_trap_map,"trap_map_show_free_carriers","true",JSON_BOOL);

	///3d config
		obj_template_plot_3d=json_obj_add(obj_template,"config_3d","",JSON_NODE);


		//view
			obj_template_plot_3d_view=json_obj_add(obj_template_plot_3d,"view","",JSON_NODE);
			json_obj_add(obj_template_plot_3d_view,"xRot","25.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_view,"yRot","1.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_view,"zRot","0.0",JSON_DOUBLE);

			json_obj_add(obj_template_plot_3d_view,"x_pos","0.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_view,"y_pos","0.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_view,"zoom","25.0",JSON_DOUBLE);

			json_obj_add(obj_template_plot_3d_view,"window_x","0.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_view,"window_y","0.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_view,"window_w","1.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_view,"window_h","1.0",JSON_DOUBLE);




		//background
			obj_template_plot_3d_background=json_obj_add(obj_template_plot_3d,"background","",JSON_NODE);
			json_obj_add(obj_template_plot_3d_background,"color_r","0.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_background,"color_g","0.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_background,"color_b","0.0",JSON_DOUBLE);
			json_obj_add(obj_template_plot_3d_background,"color_alpha","0.5",JSON_DOUBLE);

		//objects
			obj_template_plot_3d_objects=json_obj_add(obj_template_plot_3d,"objects","",JSON_NODE);
			json_obj_add(obj_template_plot_3d_objects,"render_grid","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"render_fdtd_grid","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"render_cords","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"render_photons","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"render_plot","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"draw_device","true",JSON_BOOL);

			json_obj_add(obj_template_plot_3d_objects,"optical_mode","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"plot_graph","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"show_world_box","false",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"show_electrical_box","false",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"show_thermal_box","false",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"show_detectors","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"text","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"dimensions","false",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"stars_distance","0",JSON_INT);
			json_obj_add(obj_template_plot_3d_objects,"transparent_objects","false",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"draw_rays","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"ray_solid_lines","false",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"render_light_sources","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"show_gl_lights","false",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"show_buttons","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"stars","true",JSON_BOOL);
			json_obj_add(obj_template_plot_3d_objects,"color_map","Matlab jet",JSON_STRING);
	return 0;
}

int json_data_view_gui_configs(struct json *j)
{
	json_free(j);
	struct json_obj *obj_gui_config;
	j->is_template=TRUE;

	obj_gui_config=&(j->obj);

	data_view_gui_config(obj_gui_config);


	//json_dump_obj(&(j->obj));

	return 0;
}
