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

/** @file optical_mode.h
	@brief Mode solver functions
*/


#ifndef h_optical_mode
#define h_optical_mode
#include <g_io.h>
#include <enabled_libs.h>
#include <math_xy.h>

struct optical_mode
{
	int enabled;
	double gamma;
	double L;

	struct dimensions dim;
	double ***Ey;			//Mode Ey
	double ***Ph_Ey;		//Normalized photon density
	double ***Photons;		//mode containing the photon desntiy
	double ***n;
	struct object ****obj;
	double lambda;
	double omega;
	double beta2;
	double k0;
	double n_eff;
	double eigenvalues[100];
	int n_eigenvalues;
	int mode_max_ittr;
	double mode_stop_error;
	int mode_max_eigenmode_x;
	int mode_max_eigenmode_y;
	char mode_te_tm[100];
	int force_fundermental;
};

#endif
