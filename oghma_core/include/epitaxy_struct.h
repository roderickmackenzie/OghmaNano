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

/** @file epitaxy.h
	@brief Read the epitaxy from the epitaxy.inp file.
*/


#ifndef epitaxy_struct_h
#define epitaxy_struct_h
#include <g_io.h>
#include "advmath.h"
#include <sim_struct.h>
#include <shape_struct.h>
#include <component.h>
#include <dos_struct.h>

struct epi_layer
{
	int layer_number;
	gdouble y_start;
	gdouble y_stop;
	struct shape s;		//this shape
	gdouble width;
	int pl_use_experimental_emission_spectra;
	int pl_f2f;
	int pl_f2t;
	double pl_experimental_emission_efficiency;

	int pl_enabled;
	gdouble pl_fe_fh;
	gdouble pl_fe_te;
	gdouble pl_te_fh;
	gdouble pl_th_fe;
	gdouble pl_fh_th;

	//ray tracing
	int theta_steps;
	double theta_start;
	double theta_stop;
	int phi_steps;
	double phi_start;
	double phi_stop;

	double dx_padding;
	double dy_padding;
	double dz_padding;

	int nx;
	int ny;
	int nz;
	
	int emission_source;
	int ray_super_sample_x;
	int ray_super_sample_x_points;
	//end raytracing

	char pl_spectrum_file[OGHMA_PATH_MAX];
	struct math_xy pl_spectrum;			//Normed to 1.0 at max
	struct math_xy pl_spectrum_norm;	//Area normed to 1.0
	double peak_wavelength;

	//Generation
	gdouble G_percent;		//Percentage of light absorbed in each layer

	int solve_optical_problem;
	int solve_thermal_problem;

	//double optical_J;
	//int optical_count;
};

struct epitaxy
{
	int layers;
	struct epi_layer *layer;
};

#endif
