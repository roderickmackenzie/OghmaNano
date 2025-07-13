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

/** @file memory.h
@brief allocate 3D memory
*/
#ifndef memory_h
#define memory_h
#include <g_io.h>
#include <device.h>
//zxy gdouble
void zxy_mul_gdouble(struct dimensions *dim, gdouble ***a, gdouble b);
void zxy_long_double_mul_by_zxy_long_double(struct dimensions *dim, gdouble ***a, gdouble ***b);
void zxy_long_double_div_by_zxy_long_double(struct dimensions *dim, gdouble ***a, gdouble ***b);
void cpy_zxy_long_double(struct dimensions *dim, gdouble * (***out), gdouble * (***in), int aloc);
void zxy_mod_gdouble(struct dimensions *dim, gdouble ***src);
void zxy_norm_gdouble(struct dimensions *dim, gdouble ***var);

//zxy double
void malloc_zxy_double(struct dimensions *dim, double * (***var));
void free_zxy_double(struct dimensions *dim, double * (***var));
void cpy_zxy_double(struct dimensions *dim, double * (***out), double * (***in), int aloc);
double zx_y_max_double(struct dimensions *dim, double ***var,int y);
void set_zxy_double(struct dimensions *dim, double ***data, double val);
void quick_dump_zx_y_double(char *file_name, double ***in, struct dimensions *dim);
void div_zxy_double(struct dimensions *dim, double ***src, double val);
double avg_vol_zxy_double(struct device *in, double ***src);
double inter_zxy_double(struct dimensions *dim, double ***src);
void mul_zxy_double_zxy_double(struct dimensions *dim, double ***a, double ***b);
void div_zxy_double_zxy_double(struct dimensions *dim, double ***a, double ***b);
void add_zxy_double_zxy_double(struct dimensions *dim, double ***a, double ***b);
void sub_zxy_double_zxy_double(struct dimensions *dim, double ***a, double ***b);
int min_max_zxy_double(double *min_out, double *max_out, struct dimensions *dim, double ***var);
void abs_zxy_double(struct dimensions *dim, double ***a);
void pow_zxy_double(struct dimensions *dim, double ***a, double val);
int max_abs_zxy_double(double *peak_out, struct dimensions *dim, double ***var);
double interpolate_zxy_3d_double(struct dimensions *dim, double ***data, double z_in, double x_in, double y_in);
double interpolate_zxy_2d_double(struct dimensions *dim, double ***data, int z_slice, double x_in, double y_in);
double interpolate_zxy_1d_double(struct dimensions *dim, double ***data, int z, int x, double y_in);

//srh bands
void free_srh_double(struct dimensions *dim, gdouble * (**** in_var));
void malloc_srh_double(struct dimensions *dim, gdouble * (****var));
void cpy_srh_double(struct dimensions *dim, double *(****dst), double *(****src));
int min_max_srh_double(struct dimensions *dim, double *ret_min, double *ret_max, double ****data);

//zxy_int
void set_zxy_int(struct dimensions *dim, int ***data, int val);
void malloc_zxy_int(struct dimensions *dim, int * (***var));
void free_zxy_int(struct dimensions *dim, int * (***var));
void dump_zxy_int(struct dimensions *dim, int ***var);
void cpy_zxy_int(struct dimensions *dim, int * (***out),int * (***in), int alloc);

//zxy_p_object
void malloc_zxy_p_object(struct dimensions *dim, struct object * (****var));
void free_zxy_p_object(struct dimensions *dim, struct object * (****var));
void cpy_zxy_p_object(struct dimensions *dim, struct object * (****out), struct object * (****in));

//zx_layer_p_object
void malloc_zx_layer_p_object(struct dim_zx_epitaxy *dim, struct object * (****var));
void free_zx_layer_p_object(struct dim_zx_epitaxy *dim, struct object * (****var));
void cpy_zx_layer_p_object(struct dim_zx_epitaxy *dim, struct object * (****out), struct object * (****in));
//zx_int
void malloc_zx_int(struct dimensions *dim, int * (**var));
void free_zx_int(struct dimensions *dim, int *(**in_var));
void cpy_zx_int(struct dimensions *dim, int * (**out), int * (**in));


//zxy_long_double
void malloc_zxy_long_double(struct dimensions *dim, gdouble * (***var));
void free_zxy_long_double(struct dimensions *dim, gdouble * (***in_var));
void zxy_load_long_double(struct simulation *sim, struct dimensions *dim,gdouble * *** data,char *file_name);
void set_zxy_long_double(struct dimensions *dim, gdouble ***var, gdouble val);
void flip_zxy_long_double_y(struct simulation *sim, struct dimensions *dim,gdouble *** data);
gdouble interpolate_zxy_long_double(struct dimensions *dim, gdouble ***data,int z, int x, gdouble y_in);
void mul_zxy_double_double(struct dimensions *dim, double ***a, double b);
void add_zxy_long_double_double(struct dimensions *dim, gdouble ***a, double ***b);
long double avg_vol_zxy_long_double(struct device *in, gdouble ***src);
gdouble three_d_avg_raw(struct device *in, gdouble ***src);
gdouble three_d_integrate(struct dimensions *dim, gdouble ***src);
gdouble three_d_avg_gfabs(struct device *in, gdouble ***src);
void three_d_printf(struct dimensions *dim, gdouble ***src);
void three_d_sub_gdouble(struct dimensions *dim, gdouble ***var, gdouble ***sub);
void three_d_add_gdouble(struct dimensions *dim, gdouble ***var, gdouble ***add);
void three_d_interpolate_gdouble(gdouble ***out, gdouble ***in, struct dimensions *dim_out, struct dimensions *dim_in);
void three_d_quick_dump(char *file_name, gdouble ***in, struct dimensions *dim);
void three_d_interpolate_srh(gdouble ****out, gdouble ****in, struct dimensions *dim_out, struct dimensions *dim_in,int band);
void srh_quick_dump(char *file_name, gdouble ****in, struct dimensions *dim,int band);
void three_d_interpolate_srh2(gdouble ****out, gdouble ****in, struct dimensions *dim_out, struct dimensions *dim_in,int band);
gdouble zxy_min_gdouble(struct dimensions *dim, gdouble ***var);
double zxy_max_double(struct dimensions *dim, double ***var);
gdouble zxy_sum_gdouble(struct dimensions *dim, gdouble ***src);
void zxy_max_y_pos_slice_long_double(struct dimensions *dim, gdouble ***var,int z, int x,double *max_y_mid, double *max_yn, double *max_yp,double *val);

//y_double
void div_y_double_y_double(double * a,double * b, int len);
void div_y_double_double(double * a,double b, int len);

//y_int
void malloc_y_int(struct dimensions *dim, int * (*var));
void free_y_int( int * (*in_var));
void cpy_y_int(struct dimensions *dim, int * (*out), int * (*in),  int alloc);

//zxy_long_double_complex
void malloc_zxy_long_double_complex(struct dimensions *dim, gdouble complex * (***var));
void free_zxy_long_double_complex(struct dimensions *dim, gdouble complex * (***in_var));
void cpy_light_zxyl_long_double_complex(struct dimensions *dim, gdouble complex * (****out),gdouble complex * (****in));

//light_zxyl_long_double
void malloc_light_zxyl_long_double(struct dimensions *dim, gdouble * (****var));
void free_light_zxyl_long_double(struct dimensions *dim, gdouble * (****in_var));
void flip_light_zxyl_long_double_y(struct simulation *sim, struct dimensions *dim,gdouble **** data);
void div_light_zxyl_long_double(struct dimensions *dim, gdouble ****data,gdouble val);
void memset_light_zxyl_long_double(struct dimensions *dim, gdouble ****data,int val);
void memset_light_zxyl_long_double_y(struct dimensions *dim, gdouble ****data,int z, int x, int l,gdouble val);
void cpy_light_zxyl_long_double(struct dimensions *dim, gdouble * (****out), gdouble * (****in));

//light_zxyl_float
void malloc_light_zxyl_float(struct dimensions *dim, float * (****var));
void free_light_zxyl_float(struct dimensions *dim, float * (****in_var));
void cpy_light_zxyl_float(struct dimensions *dim, float * (****out), float * (****in));
void flip_light_zxyl_float_y(struct simulation *sim, struct dimensions *dim,float **** data);
void div_light_zxyl_float(struct dimensions *dim, float ****data,float val);
void memset_light_zxyl_float(struct dimensions *dim, float ****data,int val);
void memset_light_zxyl_float_y(struct dimensions *dim, float ****data,int z, int x, int l,float val);

//light_zxy_double
void flip_light_zxy_double_y(struct simulation *sim, struct dimensions *dim,double *** data);
double interpolate_light_zxy_double_intergral(struct dimensions *dim, double ***data,int z, int x, double y_start,double y_stop);

//light_zxyl_long_double_complex
void malloc_light_zxyl_long_double_complex(struct dimensions *dim, gdouble complex * (****var));
void free_light_zxyl_long_double_complex(struct dimensions *dim, gdouble complex * (****in_var));

//light_zxyl_float_complex
void malloc_light_zxyl_float_complex(struct dimensions *dim, float complex * (****var));
void free_light_zxyl_float_complex(struct dimensions *dim, float complex * (****in_var));
void cpy_light_zxyl_float_complex(struct dimensions *dim, float complex * (****out),float complex * (****in));

//light_zxy_p_object
void malloc_light_zxy_p_object(struct dimensions *dim, struct object * (****var));
void cpy_light_zxy_p_object(struct dimensions *dim, struct object * (****out),struct object * (****in));

// heat_zxy_long_double
gdouble interpolate_heat_zxy_long_double(struct dimensions *dim, gdouble ***data,int z, int x, gdouble y_in);
gdouble avg_heat_zxy_long_double(struct dimensions *dim, gdouble ***data);

void memory_flip_1d_long_double(gdouble *var,int len);
void memory_flip_1d_int(int *var,int len);


//matrix
void matrix_init(struct matrix *mx);
int solver_mul(struct matrix *mx);
int matrix_setup_mul(struct matrix *mx, struct device *dev);
void matrix_dump(struct simulation *sim,struct matrix *mx);
int matrix_dump_to_file(struct matrix *mx,char *file_name);
void matrix_malloc(struct simulation *sim,struct matrix *mx);
void matrix_free(struct simulation *sim,struct matrix *mx);
void matrix_cpy(struct simulation *sim,struct matrix *out,struct matrix *in);
void matrix_realloc(struct simulation *sim,struct matrix *mx);
int matrix_solve(struct simulation *sim,struct matrix_solver_memory *msm,struct matrix *mx);
void matrix_cache_reset(struct simulation *sim,struct matrix *mx);
void matrix_save(struct simulation *sim,struct matrix *mx);
int matrix_load(struct simulation *sim,struct matrix *mx);
gdouble matrix_cal_error(struct simulation *sim,struct matrix *mx);
void matrix_zero_b(struct simulation *sim,struct matrix *mx);
void matrix_dump_b(struct simulation *sim,struct matrix *mx);
void matrix_dump_J(struct simulation *sim,struct matrix *mx);
void matrix_add_nz_item(struct simulation *sim,struct matrix *mx,int x,int y,gdouble val);
void matrix_convert_J_to_sparse(struct simulation *sim,struct matrix *mx);
void matrix_stats(struct simulation *sim,struct matrix *mx);
int matrix_cmp_to_file(struct simulation *sim,struct matrix *mx,char *file_name);
void matrix_load_from_file(struct simulation *sim,struct matrix *mx,char *file_name);
int matrix_write_hash_to_index(struct matrix *mx);
int matrix_to_hist(struct math_xy *A, struct math_xy *b, struct matrix *mx);
int matrix_min_max(double *min_A,double *max_A, double *min_b, double *max_b, struct matrix *mx);
int matrix_dump_hist_parts(char *path,int dump_number, struct matrix *mx, struct device *dev);
int matrix_dump_debug_info_to_file(struct matrix *mx, char *file_name);
int matrix_threshold(struct matrix *mx);

//raw memory opps
int search(gdouble *x,int N,gdouble find);
int search_double(double *x,int N,double find);

//Basic memory opps

//2d gdouble
void malloc_2d_long_double(int zlen, int xlen, gdouble * (**var));
void free_2d_long_double(int zlen, int xlen, gdouble * (**in_var));
void cpy_2d_long_double(int zlen, int xlen, gdouble * (**out), gdouble * (**in));

//3d int
void malloc_3d_int(int zlen, int xlen, int ylen, int * (***var));
void free_3d_int(int zlen, int xlen, int ylen, int * (***in_var));
void cpy_3d_int(int zlen, int xlen, int ylen, int * (***out), int * (***in));

//matrix solver memory
void matrix_solver_memory_init(struct matrix_solver_memory *msm);
int matrix_solver_memory_cpy(struct matrix_solver_memory *out,struct matrix_solver_memory *in);

//generic
//3d
void malloc_3d( void * (***var),int zlen, int xlen, int ylen,int item_size);
void free_3d(void * (***in_var),int zlen, int xlen, int ylen,int item_size);
void cpy_3d(void * (***out), void * (***in),int zlen, int xlen, int ylen,int item_size);
void cpy_3d_alloc(void * (***out), void * (***in),int zlen, int xlen, int ylen,int item_size);

//4d
void free_4d( void *(**** in_var), int zlen, int xlen, int ylen,int bands,int item_size);
void cpy_4d( void *(****dst), void *(****src),int zlen, int xlen, int ylen,int bands,int item_size);
void malloc_4d( void * (****var), int zlen, int xlen, int ylen,int bands,int item_size);

//2d
void malloc_2d(void * (**var), int zlen, int xlen, int item_size);
void free_2d(void *(**in_var), int zlen, int xlen, int item_size);
void cpy_2d(void * (**out), void * (**in),int zlen, int xlen,  int item_size);
void cpy_2d_alloc(void * (**out), void * (**in),int zlen, int xlen, int item_size);
void mem_set_2d(void *data, void *val,int zlen, int xlen, int item_size);

//1d
void malloc_1d(void * (*var),int zlen, int item_size);
void free_1d( void * (*in_var));
void cpy_1d(void * (*out), void * (*in), int zlen, int item_size,int alloc);


// light_zxyl_double
void malloc_zxyl_double(struct dimensions *dim, double * (****var));
void free_zxyl_double(struct dimensions *dim, double * (****in_var));
void cpy_zxyl_double(struct dimensions *dim, double * (****out), double * (****in),int aloc);
double interpolate_zxyl_double(struct dimensions *dim, double ****data,double z_in, double x_in, double y_in, int l);
int memset_zxyl_double(struct dimensions *dim, double ****data,int val);

//Old light_zxyl_double that needs renaming
void cpy_light_zxyl_wavelength_double(struct dimensions *dim, double ****out, double ****in,int l);
void mul_light_zxyl_wavelength_double(struct dimensions *dim, double ****out, int l,double mul);
void flip_light_zxyl_double_y(struct simulation *sim, struct dimensions *dim,double **** data);
void div_light_zxyl_double(struct dimensions *dim, double ****data,double val);
void memset_light_zxyl_double_y(struct dimensions *dim, double ****data,int z, int x, int l,double val);

//zxy_float
void malloc_zxy_float(struct dimensions *dim, float * (***var));
void free_zxy_float(struct dimensions *dim, float * (***var));
void cpy_light_zxy_float(struct dimensions *dim, float * (***out), float * (***in));
void cpy_light_zxy_float_no_alloc(struct dimensions *dim, float * (***out), float * (***in));
void mul_zxy_float_float(struct simulation *sim, struct dimensions *dim,float *** src,float val);
void memset_zxy_float(struct dimensions *dim, float ***data,int val);
void div_light_zxy_float(struct dimensions *dim, float ***src,float val);

/// light_l_double
void malloc_light_l_double(struct dimensions *dim, double * (*var));
void free_light_l_double(struct dimensions *dim, double * (*in_var));
void cpy_light_l_double(struct dimensions *dim, double * (*out), double * (*in));
double intergrate_light_l_double(struct dimensions *dim, double *var);

//1d_double
void sort_ascending_1d_double(double *in, int len);
int add_1d_double(double *in,int len, double val);

//zxl_double
void malloc_zxl_double(struct dimensions *dim, double * (***var));
void free_zxl_double(struct dimensions *dim, double * (***var));
void cpy_zxl_double(struct dimensions *dim, double * (***out), double * (***in),int aloc);
void zxl_to_zxrgb_double(struct simulation *sim, struct dimensions *dim, double * (***rgb_out), double ***in);
void set_zxl_double(struct dimensions *dim, double ***data, double val);
int min_max_zxl_double(double *min_out, double *max_out, struct dimensions *dim, double ***var);
void div_zxl_double(struct dimensions *dim, double ***src, double val);




////////////////////xy
//xy_double
void malloc_xy_double(struct dimensions *dim, double * (**var));
void free_xy_double(struct dimensions *dim, double * (**var));
void cpy_xy_double(struct dimensions *dim, double * (**out), double * (**in), int alloc);
void mem_set_xy_double(struct dimensions *dim, gdouble **data, double val);
void add_xy_double_xy_double(struct dimensions *dim, double **data_out, double **data_in);
void div_xy_double_double(struct dimensions *dim, double **data, double val);

//xy_long_double
void malloc_xy_long_double(struct dimensions *dim, gdouble * (**var));
void free_xy_long_double(struct dimensions *dim, gdouble * (**var));
void cpy_xy_long_double(struct dimensions *dim, gdouble * (**out), gdouble * (**in), int alloc);

//xy_int
void malloc_xy_int(struct dimensions *dim, int * (**var));
void free_xy_int(struct dimensions *dim, int *(**var));
void cpy_xy_int(struct dimensions *dim, int *(**out), int *(**in));

////////////////////zx
//zx_double
void malloc_zx_double(struct dimensions *dim, double * (**var));
void mem_set_zx_double(struct dimensions *dim, double **data, double val);
void free_zx_double(struct dimensions *dim, double * (**in_var));
void mem_set_zx_double(struct dimensions *dim, gdouble **data, double val);
void cpy_zx_double(struct dimensions *dim, double * (**out),double * (**in), int alloc);
void add_zx_double_zx_double(struct dimensions *dim, double **data_out, double **data_in);;
void div_zx_double_double(struct dimensions *dim, double **data, double val);
void dump_zx_double_double(struct dimensions *dim, double **data);

//zx long double
void malloc_zx_gdouble(struct dimensions *dim, gdouble * (**var));
void free_zx_gdouble(struct dimensions *dim, gdouble * (**var));
void cpy_zx_long_double(struct dimensions *dim, gdouble * (**out),gdouble * (**in), int alloc);
void mem_set_zx_long_double(struct dimensions *dim, gdouble **data, gdouble val);
void mem_mul_zx_area(struct dimensions *dim, gdouble **data);
void mem_mul_zx_long_double(struct dimensions *dim, gdouble **data,gdouble val);
void mem_div_zx_long_double(struct dimensions *dim, gdouble **data,gdouble val);
void mem_zx_invert_long_double(struct dimensions *dim, gdouble **data);
void mem_set_zx_gdouble_from_zx_gdouble(struct dimensions *dim, gdouble **data_out, gdouble **data_in);
void mem_add_zx_gdouble_from_zx_gdouble(struct dimensions *dim, gdouble **data_out, gdouble **data_in);
void zx_copy_gdouble(struct dimensions *dim, gdouble **dst, gdouble **src);

//zx_epitaxy_int
void malloc_zx_epitaxy_int(struct dim_zx_epitaxy *dim, int * (***var));
void free_zx_epitaxy_int(struct dim_zx_epitaxy *dim, int *(***var));
void cpy_zx_epitaxy_int(struct dim_zx_epitaxy *dim, int * (***out),int * (***in));
void dump_zx_epitaxy_int(struct dim_zx_epitaxy *dim, int ***var);


////////////////////zy
//zy gdouble
void malloc_zy_long_double(struct dimensions *dim, gdouble * (**var));
void free_zy_long_double(struct dimensions *dim, gdouble * (**var));
void cpy_zy_long_double(struct dimensions *dim, gdouble * (**out), gdouble * (**in), int alloc);

//zy double
void malloc_zy_double(struct dimensions *dim, double * (**var));
void free_zy_double(struct dimensions *dim, double * (**var));
void cpy_zy_double(struct dimensions *dim, double * (**out), double * (**in), int alloc);
void mem_set_zy_double(struct dimensions *dim, gdouble **data, double val);
void add_zy_double_zy_double(struct dimensions *dim, double **data_out, double **data_in);
void div_zy_double_double(struct dimensions *dim, double **data, double val);
void dump_zy_double_double(struct dimensions *dim, double **data);

//zy int
void malloc_zy_int(struct dimensions *dim, int * (**var));
void free_zy_int(struct dimensions *dim, int *(**in_var));
void cpy_zy_int(struct dimensions *dim, int *(**out), int *(**in));

//z double
void malloc_z_double(struct dimensions *dim,double * (*var));
void free_z_double( double * (*in_var));
void cpy_z_double(struct dimensions *dim,double * (*out), double * (*in), int alloc);

#endif
