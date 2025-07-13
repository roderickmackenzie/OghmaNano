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

/** @file dim.h
	@brief Dimention file
*/

#ifndef dim_h
#define dim_h
#include <g_io.h>
#include <dat_file_struct.h>

struct dimensions
{
	int zlen;
	int xlen;
	int ylen;
	int llen;

	gdouble *y;
	gdouble *x;
	gdouble *z;
	double *l;

	gdouble *dY;
	gdouble *dX;
	gdouble *dZ;

	gdouble dy;	//Mesh spacing for uniform mesh
	gdouble dx;	//Mesh spacing for uniform mesh
	gdouble dz;	//Mesh spacing for uniform mesh
	double dl;	//Mesh spacing for uniform mesh

	int srh_bands;

	double y_start;
	double x_start;
	double z_start;
	double l_start;

	double y_stop;
	double x_stop;
	double z_stop;
	double l_stop;

	double y_tot_len;
	double x_tot_len;
	double z_tot_len;
	double l_tot_len;
};

struct dim_zx_epitaxy
{
	int zlen;
	int xlen;
	int ylen;
};



void dim_set_simple_mesh_x(struct dimensions *dim, double start, double stop);
void dim_set_simple_mesh_y(struct dimensions *dim, double start, double stop);
void dim_set_simple_mesh_z(struct dimensions *dim, double start, double stop);

//dimension
void dim_init(struct dimensions *dim);
void dim_free(struct dimensions *dim);
void dim_malloc(struct dimensions *dim);
void dim_cpy(struct dimensions *out,struct dimensions *in);
void dim_cpy_l(struct dimensions *out,struct dimensions *in);
void dim_malloc_xyz(struct dimensions *dim,char xyz);
void dim_free_xyz(struct dimensions *dim,char xyz);
void dim_swap(struct dimensions *out,struct dimensions *in);
void dim_info_to_buf(struct dat_file *buf,struct dimensions *dim);
gdouble dim_dl_xyz(struct dimensions *dim, int x0, int y0, int z0,int x1,int y1, int z1);
void dim_init_xyz(struct dimensions *dim,char xyz);
void dim_rescale_if_needed_xyz(struct dimensions *dim,char xyz,double L);
void dim_to_plot_type(char *plot_type, int zlen, int xlen, int ylen);

//dim_epitaxy
void dim_init_zx_epitaxy(struct dim_zx_epitaxy *dim);
void dim_free_zx_epitaxy(struct dim_zx_epitaxy *dim);

#endif
