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

int json_data_view_gui_3d_fixup(struct json *j)
{
	struct json_obj *obj_seg;
	struct json_obj *obj_config_3d;
	struct json_obj *obj_config_3d_view;
	struct json_obj *obj_user_input;
	struct json_obj *json_plots;

	json_plots=json_obj_find_by_path(&(j->obj), "plots");

	//3d
		obj_seg=json_segments_find_by_name(json_plots,"3d");
		if (obj_seg==NULL)
		{
	
			obj_seg=json_segments_add(json_plots,"3d", -1);
		}

		//user input
			obj_user_input=json_obj_find(obj_seg,"user_input");
			json_set_data_bool(obj_user_input,"enable_view_move", TRUE);

		obj_config_3d=json_obj_find(obj_seg,"config_3d");
		//view
			obj_config_3d_view=json_obj_find(obj_config_3d,"view");
			json_set_data_double(obj_config_3d_view,"window_x", 0.0);
			json_set_data_double(obj_config_3d_view,"window_y", 0.0);
			json_set_data_double(obj_config_3d_view,"window_w", 1.0);
			json_set_data_double(obj_config_3d_view,"window_h", 1.0);



	//3d_small_0_0
		obj_seg=json_segments_find_by_name(json_plots,"3d_small_0_0");
		if (obj_seg==NULL)
		{
			obj_seg=json_segments_add(json_plots,"3d_small_0_0", -1);
		}
		//user input
			obj_user_input=json_obj_find(obj_seg,"user_input");
			json_set_data_bool(obj_user_input,"enable_view_move", TRUE);

		obj_config_3d=json_obj_find(obj_seg,"config_3d");

		//view
			obj_config_3d_view=json_obj_find(obj_config_3d,"view");
			json_set_data_double(obj_config_3d_view,"window_x", 0.0);
			json_set_data_double(obj_config_3d_view,"window_y", 0.0);
			json_set_data_double(obj_config_3d_view,"window_w", 0.5);
			json_set_data_double(obj_config_3d_view,"window_h", 0.5);



	//3d_small_0_1
		obj_seg=json_segments_find_by_name(json_plots,"3d_small_0_1");
		if (obj_seg==NULL)
		{
			obj_seg=json_segments_add(json_plots,"3d_small_0_1", -1);
		}
		//user input
			obj_user_input=json_obj_find(obj_seg,"user_input");
			json_set_data_bool(obj_user_input,"enable_view_move", FALSE);

		obj_config_3d=json_obj_find(obj_seg,"config_3d");
		//view
			obj_config_3d_view=json_obj_find(obj_config_3d,"view");
			json_set_data_double(obj_config_3d_view,"window_x", 0.0);
			json_set_data_double(obj_config_3d_view,"window_y", 0.5);
			json_set_data_double(obj_config_3d_view,"window_w", 0.5);
			json_set_data_double(obj_config_3d_view,"window_h", 0.5);

			json_set_data_double(obj_config_3d_view,"xRot", 3.0);
			json_set_data_double(obj_config_3d_view,"yRot", 1.0);
			json_set_data_double(obj_config_3d_view,"zRot", 1.0);

	//3d_small_1_0
		obj_seg=json_segments_find_by_name(json_plots,"3d_small_1_0");
		if (obj_seg==NULL)
		{
			obj_seg=json_segments_add(json_plots,"3d_small_1_0", -1);
		}
		//user input
			obj_user_input=json_obj_find(obj_seg,"user_input");
			json_set_data_bool(obj_user_input,"enable_view_move", FALSE);

		obj_config_3d=json_obj_find(obj_seg,"config_3d");
		//view
			obj_config_3d_view=json_obj_find(obj_config_3d,"view");
			json_set_data_double(obj_config_3d_view,"window_x", 0.5);
			json_set_data_double(obj_config_3d_view,"window_y", 0.0);
			json_set_data_double(obj_config_3d_view,"window_w", 0.5);
			json_set_data_double(obj_config_3d_view,"window_h", 0.5);

			json_set_data_double(obj_config_3d_view,"xRot", 90.0);
			json_set_data_double(obj_config_3d_view,"yRot", 0.0);
			json_set_data_double(obj_config_3d_view,"zRot", 0.0);
	//3d_small_1_1
		obj_seg=json_segments_find_by_name(json_plots,"3d_small_1_1");
		if (obj_seg==NULL)
		{
			obj_seg=json_segments_add(json_plots,"3d_small_1_1", -1);
		}
		//user input
			obj_user_input=json_obj_find(obj_seg,"user_input");
			json_set_data_bool(obj_user_input,"enable_view_move", FALSE);

		obj_config_3d=json_obj_find(obj_seg,"config_3d");
		//view
			obj_config_3d_view=json_obj_find(obj_config_3d,"view");
			json_set_data_double(obj_config_3d_view,"window_x", 0.5);
			json_set_data_double(obj_config_3d_view,"window_y", 0.5);
			json_set_data_double(obj_config_3d_view,"window_w", 0.5);
			json_set_data_double(obj_config_3d_view,"window_h", 0.5);

			json_set_data_double(obj_config_3d_view,"xRot", 3.0);
			json_set_data_double(obj_config_3d_view,"yRot", 90.0);
			json_set_data_double(obj_config_3d_view,"zRot", 0.0);
	return 0;
}

