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

/** @file dat_file.h
	@brief Strcutr to hold .dat files before they are written to disk.
*/

#ifndef dat_file_h
#define dat_file_h
#include <g_io.h>
#include <advmath.h>
#include <dat_file_struct.h>
#include <device.h>
#include <triangle.h>
#include <ray.h>
#include <circuit_struct.h>

void buffer_zip_set_name(struct dat_file *in,char * name);
void dat_file_init(struct dat_file *in);
void dat_file_malloc(struct dat_file *in);
int dat_file_malloc_py_data(struct dat_file *dat);

void buffer_dump(struct simulation *sim,char * file,struct dat_file *in);
void dat_file_dump_path(struct simulation *sim,char *path,char * file,struct dat_file *in);
void dat_file_free(struct dat_file *in);
void dat_file_free_only(struct dat_file *in);
void buffer_dump_aes(char *path,char * file,struct dat_file *in,char *key_text);
int dat_file_dump_gnuplot_file(char * path,struct dat_file *in, int png, FILE* makefile);

void dat_file_increase_buffer(struct dat_file *in,int size);
void dat_file_reset(struct dat_file *in);
int buffer_set_file_name(struct simulation *sim,struct device *dev,struct dat_file *in,char * file_name);
int dat_file_cpy(struct dat_file *out,struct dat_file *in);
int dat_file_remove_last_char(struct dat_file *in);

//buffer add
void buffer_add_csv_header(struct dat_file *in);
int buffer_add_json(struct dat_file *in);
void buffer_add_3d_device_data_including_boundaries(struct simulation *sim,struct dat_file *buf,struct device *dev,gdouble ***data,gdouble **left,gdouble **right);
void buffer_add_xy_data_z_label(struct dat_file *in,gdouble *x, gdouble *y, gdouble *z, int len);
void buffer_add_zxy_object_uid(struct simulation *sim,struct dat_file *in,struct object ****data, struct dimensions *dim);
void dat_file_add_math_xy(struct simulation *sim,struct dat_file *out,struct math_xy *in);
void dat_file_add_math_xy_with_probe(struct simulation *sim,struct device *dev, struct dat_file *out, struct math_xy *in);
void dat_file_add_xy_double(struct simulation *sim,struct dat_file *in,double *x, double *y, int len);
void buffer_add_string(struct dat_file *in,char * string);
void dat_file_add_zxyt_long_double(struct simulation *sim,struct dat_file *buf,struct device *dev);
void dat_file_add_zxy_double_l(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,double ****data, int l);
void dat_file_add_zxy(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,void ***data,void **y0,void **y1,int var_type);
void dat_file_add_zxy_double(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,double ***data);
void dat_file_add_rays(struct simulation *sim,struct dat_file *buf,struct ray_worker *worker);
void dat_file_add_2d_double(struct simulation *sim,struct dat_file *in, double *x, double *y, double **data, int x_len, int y_len);

//zxy
void dat_file_add_zxy_data(struct simulation *sim,struct dat_file *buf,struct dimensions *dim, gdouble ***data);
void dat_file_add_zxy_data_with_probe(struct simulation *sim,struct device *dev,struct dat_file *buf,struct dimensions *dim,gdouble ***data);

void dat_file_add_zxy_float(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,float ***data);
void dat_file_add_zxy_float_l(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,float ****data, int l);
void dat_file_add_zxy_float_abs(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,float ***data);

void dat_file_add_zxy_int(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,int ***data);

void buffer_add_zxy_double_y_slice(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,double ***data,int y);
void buffer_add_3d_device_data_int(struct simulation *sim,struct dat_file *buf,struct device *in,int ***data);
void buffer_add_3d_to_2d_projection(struct simulation *sim,struct dat_file *buf,struct device *in,gdouble ***data);
void dat_file_add_zxrgb_double(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,double ***data);
void buffer_add_yl_light_data_float(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,float ****data,gdouble shift, int z, int x);
void buffer_add_xzy_data_float(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,float ***data);
void dat_file_zxyl_add_yl_double(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,double ****data,double shift, int z, int x);
void dat_file_dump_info(struct dat_file* in);
void dat_file_add_circuit_links(struct simulation *sim,struct dat_file *buf,struct device *dev,struct circuit *cir);
void dat_file_add_circuit_nodes(struct simulation *sim,struct dat_file *buf,struct device *dev,struct circuit *cir);
void dat_file_add_circuit_links_as_colored_components(struct simulation *sim,struct dat_file *buf,struct device *dev,struct circuit *cir);

int dat_file_json_header_end(char *data, int data_len, int *start, int *stop);
void dat_file_info_old_format(struct simulation *sim,struct dat_file *in,char *data, int data_len);
int dat_file_guess_dim(struct dat_file *in,char *data, long data_len);
int dat_file_have_i_loaded_this(struct dat_file *in);

//zx
void dat_file_add_zx_int(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,int **data);
int dat_file_add_zx_double(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,double **data);

//zy
void dat_file_add_zy_int(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,int **data);

//xy
void dat_file_add_xy_int(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,int **data);

//load
int dat_file_load(struct dat_file *in,char *file_name);
int dat_file_load_yrgb(struct dat_file *in,char *data, long data_len);
int dat_file_load_info(struct simulation *sim,struct dat_file *in,char *data, int data_len);
int dat_file_load_info_peek(struct dat_file *in,char **buf, long *len, char *file_name);
void dat_file_load_json_info(struct simulation *sim,struct dat_file *in,char *data, int data_len);
int dat_file_load_xd(struct dat_file *in,char *data, long data_len);
int dat_file_load_xyd(struct dat_file *in,char *data, long data_len);
int dat_file_load_xzd(struct dat_file *in,char *data, long data_len);
int dat_file_load_yzd(struct dat_file *in,char *data, long data_len);
int dat_file_load_bin_zxyd(struct dat_file *in,char *data, long data_len);
int dat_file_load_rays(struct dat_file *in,char *data, long data_len);
int dat_file_load_trap_map(struct dat_file *in,char *data, long data_len);
int dat_file_load_zxyzxyrgb(struct dat_file *in,char *data, long data_len);
int dat_file_load_zxyrgb(struct dat_file *in,char *data, long data_len);
int dat_file_load_zxrgb(struct dat_file *in,char *data, long data_len);
int dat_file_load_bin_zxyrgb_grid(struct dat_file *in,char *data, long data_len);
int dat_file_load_search_for_other_parts(struct dat_file *in,char *file_name);
int dat_file_load_zxyd(struct dat_file *in,char *data, long data_len);

//yd
int dat_file_load_yd(struct dat_file *in,char *data, long data_len);
int dat_file_sort_yd(struct dat_file *dat);
int dat_file_load_yd_from_csv(struct dat_file *in,char *file_name, int x_col, int y_col, int skip_lines);
int dat_file_load_ydd_from_csv(struct dat_file *in,char *file_name, int x_col, int y_col0, int y_col1, int skip_lines);

//export
double rgb_clamp(double val);
int dat_file_to_rgba(unsigned char **buf, int *w, int *h,struct dat_file *in);
int dat_files_save_as_csv(char *dir_path,struct dat_file *data, int ndata);
int dat_files_save_as_gnuplot(char *dir_path,struct dat_file *data, int ndata);
int dat_files_save_as_xlsx(char *dir_path,struct dat_file *data, int ndata);

//math
int dat_file_min_max(double *min_out, double *max_out, struct dat_file *in);
int dat_file_min_max_fabs(double *min_out, double *max_out, struct dat_file *in);
int dat_file_quartile(double *min_out, double *max_out, struct dat_file *in,double lower_quartile,double upper_quartile );
int dat_file_swap_xy_axies(struct dat_file *dat);
int dat_file_flip_z(struct dat_file *dat);
int dat_file_flip_x(struct dat_file *dat);
int dat_file_flip_y(struct dat_file *dat);
int dat_file_triangles_norm(struct dat_file *dat);

//save
void dat_file_save(char * file_name,struct dat_file *in);

//object to 3D array
void dat_file_add_zxy_float_l_from_objects(struct simulation *sim,struct dat_file *buf,struct dimensions *dim,struct object ****data , int l, char t);

//trap_map
int dat_file_trap_map_init(struct dat_file_trap_map *in);
int dat_file_trap_map_decode(struct dat_file_trap_map *out,struct dat_file *in,float *f_data);
int dat_file_trap_map_free(struct dat_file_trap_map *out,struct dat_file *in);
int dat_file_trap_map_get_min_max(struct dat_file *in);

//display
int dat_file_how_can_i_display_the_data(struct dat_file_display_options *options, struct dat_file *in);

//stars
int dat_file_load_stars_from_file(struct dat_file *in,char *file_name);
int dat_file_load_stars(struct dat_file *in,char *data, long data_len);
void dat_file_add_stars(struct simulation *sim,struct dat_file *buf, double *data, int len);
#endif
