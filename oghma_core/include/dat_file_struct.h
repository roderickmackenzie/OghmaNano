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

/** @file dat_file_struct.h
	@brief Strcutr to hold .dat files before they are written to disk.
*/

#ifndef dat_file_struct_h
#define dat_file_struct_h
#include <g_io.h>
#include "advmath.h"
#include "list_struct.h"
#include <triangle.h>
#include <color_struct.h>

//valid plot types
//xy :xy graph with lines
//2d :2D graph openmesh
//heat :heatmap

struct dat_file_display_options
{
	int normal_graph;
	int threeD_world;
};

struct dat_file_trap_map
{
	double ***Ec_f;
	double ***nf;
	double ****Ec;
	double ****nt;

	double ***Ev_f;
	double ***pf;
	double ****Ev;
	double ****pt;

	double Ec_max;
	double Ev_min;
};

struct dat_file
{
	char title[100];
	char type[100];
	double x_mul;
	double y_mul;
	double z_mul;
	double x_offset;
	double y_offset;
	double z_offset;
	double data_mul;
	char x_label[100];
	char y_label[100];
	char z_label[100];
	char data_label[100];
	char x_units[100];
	char y_units[100];
	char z_units[100];
	struct rgb_char rgb;
	char icon[100];
	char data_units[100];
	int logscale_x;
	int logscale_y;
	int logscale_z;
	int logscale_data;
	int write_to_zip;
	int norm_x_axis;
	int norm_y_axis;
	double data_min;
	double data_max;
	double data_min1;
	double data_max1;
	int x_len;
	int y_len;
	int z_len;
	int srh_bands;
	double time;
	double Vexternal;
	char *buf;
	struct triangle *data;
	int len;
	int max_len;
	char zip_file_name[400];
	char file_name[4096];
	char cols[20];		//These can be zxyd
	int bin;
	int valid_data;
	long modify_time;
	int new_read;
	double *x_scale;
	double *y_scale;
	double *z_scale;
	double ***py_data;
	int encrypted;
	struct list list;
	int col_count;
	int append;
	int part;
	int search_started;
	int include_json_header;
	int xlsx_format;
	int plotted;
	int transpose;
	int flip_z;
	int flip_x;
	int flip_y;
	struct dat_file_trap_map trap_map;
};


#endif
