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

/** @file singlet_material.h
@brief a structure for the singlet model
*/

#ifndef h_singlet_material
#define h_singlet_material
#include <g_io.h>

struct singlet_material
{
	int singlet_enabled;
	double singlet_k_fret;
	double singlet_k_s;
	double singlet_k_isc;
	double singlet_k_ss;
	double singlet_k_sp;
	double singlet_k_st;
	double singlet_k_dext;
	double singlet_k_t;
	double singlet_k_tp;
	double singlet_k_tt;
	double singlet_k_sd;
	double singlet_k_iscd;
	double singlet_k_spd;
	double singlet_k_std;
	double singlet_k_ssd;
	double singlet_k_td;
	double singlet_k_ttd;
	double singlet_k_tpd;
	//double singlet_zeta;		//remove as now calculated from singlet_zeta
	double singlet_k_cav;
	double singlet_beta_sp;
	double singlet_C;
	double singlet_N_dop;
	double singlet_W;
	//singlet solver+
	double singlet_k_risc;
	double singlet_sigma_em;
	double singlet_sigma_t1tn;
	double singlet_sigma_np;

	//Calculating kfq
	double singlet_a;
	int kfq_n;
	double E_max;
	double *kfq;
	double *dkfq;
};

struct singlet_opv_material
{
	int singlet_enabled;
	double k_d_s;
	double k_isc;
	double k_risc;
	double k_tta;
	double k_sta;
	double k_ssa;
	double alpha;
	double k_fs;
	double k_dt;
	double k_ft;
	double k_dct;
	double k_isc_ct;
	double k_risc_ct;
	double k_f;
};
#endif
