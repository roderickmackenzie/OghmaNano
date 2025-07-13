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

/** @file color.h
	@brief Header file for lib which handles cie_colors
*/

#ifndef cie_color_h
#define cie_color_h

	#include <g_io.h>
	#include <sim_struct.h>
	#include <device.h>
	#include <color_struct.h>
	#include <json_struct.h>

	void color_cie_init(struct simulation *sim);
	void color_cie_load(struct simulation *sim);
	void color_cie_free(struct simulation *sim);
	void wavelength_to_rgb(int *r,int *g,int *b,double wavelength);
	int color_cie_cal_XYZ(struct simulation *sim,double *X,double *Y,double *Z,struct math_xy *L_input, int input_in_ev);
	void color_XYZ_to_rgb(int *R,int *G, int *B,double X,double Y, double Z);
	int decode_rgb_double(double *r,double *g,double *b,char *rgb);
	int color_map_get_colors(char *text);
	int color_map_test(struct simulation *sim);
	int color_map_get_color2(struct rgb_char *rgb,double pos, struct color_map_item* map, int interpolate);
	struct color_map_item* color_map_find_by_name(char *name);
	struct color_map_item* color_map_find_random();
	void color_map_build_index();

	//obj color
	int obj_color_init(struct obj_color *obj);
	int obj_color_free(struct obj_color *obj);
	int obj_color_cpy(struct obj_color *out, struct obj_color *in);
	int obj_color_load_from_json(struct obj_color *obj, struct json_obj *j);
	int obj_color_save_to_json(struct json_obj *j,struct obj_color *obj);
	int obj_color_set_rgba(struct obj_color *obj, double r, double g, double b, double alpha);

	//rgb_char
	void set_rgb_char(struct rgb_char *in, char r, char g, char b, char alpha);
	void set_rgb_char_from_obj_color(struct rgb_char *out, struct obj_color *in);
	void rgb_char_cpy(struct rgb_char *out, struct rgb_char *in);
	int decode_rgb(struct rgb_char *in,char *rgb);
#endif
