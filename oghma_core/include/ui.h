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

#ifndef ui_h
#define ui_h
#include <g_io.h>
#include <vec.h>
#include <dat_file_struct.h>
#include <text_lib.h>
#include <json.h>
#include <dat_file_struct.h>
#include <graph.h>



int ui_graph_init(struct ui_graph *data);
int ui_graph_draw(struct ui_graph *data,int w, int h);
int ui_graph_free(struct ui_graph *data);
int ui_graph_draw_line(struct ui_graph *data, struct vec2d_int *xy0, struct vec2d_int *xy1, struct rgb_char *rgb, int thickness);
int ui_graph_set_pixel(struct ui_graph *data,struct vec2d_int *xy, struct rgb_char *rgb);
int graph_rotate_around_y(struct ui_graph *data, double ang);
int graph_rotate_around_x(struct ui_graph *data, double ang);
int graph_load_set_up_axies(struct ui_graph *data);
int project_3d_to_2d(struct ui_graph *data, struct vec2d_int *point_2d , struct vec *point_3d);
int unproject_2d_to_3d_zspace(struct ui_graph *data, struct vec2d_int *point_2d, double z_space, struct vec *point_3d);
int ui_graph_draw_3d_line(struct ui_graph *data, struct vec *p0, struct vec *p1, struct rgb_char *rgb, int thick);
int ui_graph_draw_3d_point(struct ui_graph *data, struct vec *p0, struct rgb_char *rgb, int dx, int dy);
void ui_graph_anti_alias(struct ui_graph *data);
int graph_setup_window(struct ui_graph *data,char *font_path);
int ui_graph_plot_1d_line(struct ui_graph *data);
int ui_graph_plot_2d_mesh(struct ui_graph *data);
int graph_load_file(struct ui_graph *data, char *file_name,struct dat_file *dat_in, int axis);
int graph_load_multiplot(struct ui_graph *data, char *base_path, char *file_name);
int ui_graph_scale_point(struct ui_graph *data, char axis ,struct vec *in,double d_in,int direct);
int ui_graph_draw_3d_filled_rectangle(struct ui_graph *data, struct vec *p0, struct vec *p1, struct rgb_char *rgb);
int graph_ui_axies(struct ui_graph *data);
int graph_draw_objs(struct ui_graph *data);
void graph_set_json(struct ui_graph *data,struct json *j);
struct graph_obj *graph_objs_check_memory(struct ui_graph *data);
int graph_load_bands(struct ui_graph *data,char *materials_path, struct json *j);
int ui_graph_plot_2d_heat(struct ui_graph *data);
int graph_mouse(struct ui_graph *data, int x, int y);
int ui_graph_draw_2d_filled_rectangle(struct ui_graph *data, struct vec2d_int *xy0, struct vec2d_int *xy1, struct rgb_char *rgb);
int graph_mouse_release(struct ui_graph *data);
int ui_graph_unscale_point(struct ui_graph *data, char axis ,struct vec *in,double *d_in);
int ui_graph_plot_trap_map(struct ui_graph *data);
int graph_ui_format_axis_number(char *out, struct graph_axis *axis,double val);
int ui_graph_draw_3d_circle(struct ui_graph *data, struct vec *p0, struct rgb_char *rgb, int r);
int graph_ui_axis_get_start_stop(struct graph_axis *axis,double *array,int len,int log);
int ui_graph_hide_data(struct ui_graph *data,int hide);
int ui_graph_plot_yrgb(struct ui_graph *data);
int ui_graph_plot_zxrgb(struct ui_graph *data);
int graph_update_color_maps(struct ui_graph *data,struct color_map_item* cm);
int graph_data_set_info_init(struct graph_data_set_info *in,struct ui_graph *data);
int graph_set_white_space(struct ui_graph *data);
int ui_graph_get_paths(struct json_string *buf,struct ui_graph *data);
int graph_draw_color_bar(struct ui_graph *data, char *title, double min, double max, char *units);
int graph_draw_key(struct ui_graph *data);
int graph_transpose_data(struct ui_graph *data,int transpose);
int graph_set_key_text(struct ui_graph *data, int i, char *text);
double graph_project_var(struct ui_graph *data,struct dat_file *dat, int z_in, int x_in, int y_in);
int graph_free_files(struct ui_graph *data);
int graph_add_empty_plot_with_colorbar(struct ui_graph *data);
int ui_graph_plot_colorbar(struct ui_graph *data);

int ui_project_val_to_mesh(struct dat_file *out,char *sub_path, char *token0, char *token1,struct json *j);
//inode
int inode_is_hidden(char *file_name);
#endif
