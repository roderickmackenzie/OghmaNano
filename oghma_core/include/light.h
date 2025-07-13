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

/** @file light.h
@brief light functions from liblight
*/

#ifndef h_light
#define h_light
#include <g_io.h>
#include <complex.h>
#include "advmath.h"
#include <math_xy.h>
#include <sim_struct.h>
#include <epitaxy_struct.h>
#include <ray.h>
#include <matrix.h>
#include <matrix_solver_memory.h>
#include <object.h>
#include <dat_file_struct.h>
#include <dim.h>

struct light_sources
{
	int nlight_sources;
	struct light_src *light_sources;

	//for EQE
	int use_flat_sepctrum;			
};

struct light_src
{
	int nspectra;
	struct math_xy spectra_tot;				//W*m-2
	struct math_xy spectra_tot_no_filter;	//W*m-2

	struct math_xy spectra_tot_photons;				//W*m-2
	struct math_xy spectra_tot_no_filter_photons;	//W*m-2

	struct math_xy *spectra;
	double light_multiplyer[20];
	//for EQE
	int use_flat_sepctrum;			


	//filter
	int filter_enabled;
	char filter_path[OGHMA_PATH_MAX];
	struct math_xy filter_read;
	double filter_dB;
	int filter_invert;
	double local_ground_view_factor;

	//external interface
	double n;
	int external_interface_enabled;
	char id[100];

	//config
	char illuminate_from[20];
	double x0;
	double y0;
	double z0;

	int theta_steps;
	double theta_start;
	double theta_stop;

	int phi_steps;
	double phi_start;
	double phi_stop;

	double dx_padding;
	double dy_padding;
	double dz_padding;

	double dx;
	double dy;
	double dz;

	int nx;
	int ny;
	int nz;

	double rotate_x;
	double rotate_y;

	char light_profile[STR_MAX];
	struct triangles light_profile_tri;
};

struct light
{
	//output files
	char dump_dir[OGHMA_PATH_MAX];

	//double zxyl
	float ****Ep;
	float ****Epz;
	float ****En;
	float ****Enz;
	double ****photons;
	double ****photons_asb;
	float ****H;

	//complex zxyl
	float complex ****t;
	float complex ****r;
	float complex ****nbar;

	//3D arrrays
	double ***Gn;
	double ***Gp;
	double ***Htot;
	double ***photons_tot;


	//1D arrays
	double *reflect;
	double *transmit;
	double reflect_power_den;
	double transmit_power_den;

	//for EQE
	int use_flat_sepctrum;			

	//Input spectra
	struct light_src light_src_y0;
	struct light_src light_src_y1;

	double *sun_y0;
	double *sun_y1;
	double *sun_photons_y0;
	double *sun_photons_y1;

	//with no filter
	double *sun_y0_no_filter;
	double *sun_y1_no_filter;
	double *sun_photons_y0_no_filter;
	double *sun_photons_y1_no_filter;

	//electricl field
	double *sun_E_y0;
	double *sun_E_y1;
	char suns_spectrum_file[200];
	char light_file_generation[300];

	//matrix
	int worker_max;
	struct matrix *mx;
	struct matrix_solver_memory *msm;

	//laser
	double laser_wavelength;
	int laser_pos;
	double ND;
	double spotx;
	double spoty;
	double pulseJ;
	double pulse_width;

	double Psun;
	int incoherent_wavelengths;
	double laser_eff;
	double Dphotoneff;

	//Dll section
	void (*fn_init)();
	void (*fn_solve_and_update)();
	int (*fn_solve_lam_slice)();
	double (*fn_cal_photon_density)();
	void (*light_ver)();
	void *lib_handle;

	//config
	char mode[20];
	int force_update;
	double *extract_eff;

	//Config values
	int disable_transfer_to_electrical_mesh;
	int disable_cal_photon_density;
	double light_file_generation_shift;
	int calculate_reflection;

	int print_wavlengths;

	int finished_solveing;

	double last_Psun;
	double last_laser_eff;
	double last_wavelength_laser;

	char snapshot_path[OGHMA_PATH_MAX];
	int dump_verbosity;
	int mesh_eq_device_layers;
};

#endif
