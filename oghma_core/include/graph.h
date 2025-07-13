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

/** @file ui.h
@brief Code to read input files.
*/

#ifndef graph_h
#define graph_h
#include <g_io.h>
#include <vec.h>
#include <dat_file_struct.h>
#include <text_lib.h>
#include <json.h>
#include <dat_file_struct.h>

#define GRAPH_MOUSE_MODE_HOME 0
#define GRAPH_MOUSE_MODE_ROTATE 1
#define GRAPH_MOUSE_MODE_PAN 2
#define GRAPH_MOUSE_MODE_ZOOM 3

//list of plot_types
//xy - line graph of x/y
//heat
//trap_map
//2d - not used ambigous
//3d - a 3D plot such as https://upload.wikimedia.org/wikipedia/commons/2/27/Griewank_function_3D_plot.png

struct toolbar_info
{
	int visible;
	int checked;
};
struct toolbar_hints
{
	struct toolbar_info home;
	struct toolbar_info pointer;
	struct toolbar_info rotate;
	struct toolbar_info log_x;
	struct toolbar_info log_y;
	struct toolbar_info log_z;
};

struct graph_tick
{
	double pos;
	double value;
	char text[200];
	int major;
};

struct graph_obj
{
	struct vec xy0;
	struct vec xy1;
	struct rgb_char rgb;
	char obj_type[100];
	char text[100];
};

struct graph_axis
{
	char label[400];
	int enable;
	int hidden;
	double mul;
	int label_rot;
	int pixel_shift;
	struct vec scale_shift_zxy;
	struct vec label_shift_zxy;
	double *scale;
	int len;
	double start;
	double stop;

	struct vec p0;		//axis start
	struct vec p1;		//axis stop
	struct vec tic;		//axis stop
	int label_center_x;
	int log_scale;
	int log_scale_auto;
	int dry_run;
	int use_sci;
	int grid;
};

struct graph_data_set_info
{
	char y_axis;
	int color_map_within_line;
	struct color_map_item *cm;
	int hidden;
	char label[200];
};

struct ui_graph
{
	int width;
	int height;
	char *pixels;
	char *pixels_back;
	struct vec camera;		//Camera position
	struct vec look;		//Camera look-at target
	struct vec up;			//Camera up vector
	double fov;				//Field of view in degrees
	int ndata;
	struct dat_file *data;

	struct text_lib text_lib;
	char plot_type[10];
	char cols[10];
	struct graph_axis axis_x;
	struct graph_axis axis_y;
	struct graph_axis axis_yr;
	struct graph_axis axis_z;

	struct vec u;		//unit size
	int points;
	int lines;
	struct graph_data_set_info *info;
	struct json *j;
	struct graph_obj *objs;
	int nobjs;
	int max_objs;

	int camera_set;
	int shift_2d_x;
	struct vec2d_int xy_shift;
	//mouse
	int mouse_mode;
	struct vec2d_int mouse;
	struct vec2d_int mouse_last;
	int mouse_drag_started;
	int disable_rebuild;
	struct color_map_item *cm_default;
	struct toolbar_hints toolbar;

	//cut through fraction
	double cut_through_frac_z;
	double cut_through_frac_x;
	double cut_through_frac_y;

	//plot_options
	int show_key;
	int show_title;	
	int show_free_carriers;
	int show_trapped_carriers;
};

#endif
