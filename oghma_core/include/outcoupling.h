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

/** @file outcoupling.h
@brief outcoupling functions from liboutcoupling
*/

#ifndef h_outcoupling
#define h_outcoupling
#include <g_io.h>
#include <complex.h>
#include <math_xy.h>
#include <sim_struct.h>
#include <ray.h>
#include <object.h>
#include <dim.h>

struct outcoupling
{
	//output files
	char dump_dir[OGHMA_PATH_MAX];
	char snapshot_path[OGHMA_PATH_MAX];
	int dump_verbosity;

	//double zxyl
	double ****photons;
	double ****photons_escape_prob;

	//3D arrrays
	double ***photons_escape_prob_lam_avg;

	//double zxl
	double ***photons_escape_prob_y_avg;

	//1D arrays
	double *reflect;
	double *transmit;

	int incoherent_wavelengths;

	//Dll section
	void (*fn_init)();
	void (*fn_solve_and_update)();
	int (*fn_solve_lam_slice)();
	double (*fn_cal_photon_density)();
	void (*outcoupling_ver)();
	void *lib_handle;

	//config
	char mode[20];
	int print_wavlengths;
	double Dphotoneff;

	int solved_on_electircal_mesh;
};

#endif
