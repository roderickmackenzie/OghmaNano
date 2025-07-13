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

/** @file sweep_store.h
	@brief Store information as the simulation progresses such as voltage, current or carrier density, these are 1D arrays as a function of time of simulation step.
*/

#ifndef sweep_store_h
#define sweep_store_h
#include <g_io.h>
#include <math_xy.h>


struct sweep_store
{
	//recombination
	struct math_xy R_nfree_to_pfree;
	struct math_xy R_srh_nfree;
	struct math_xy R_srh_pfree;
	struct math_xy R_srh_nfree_to_ptrap;
	struct math_xy R_srh_pfree_to_ntrap;
	struct math_xy T_srh_pfree_to_ptrap;
	struct math_xy T_srh_nfree_to_ntrap;
	struct math_xy G_n;
	struct math_xy G_p;
	struct math_xy R_surface_y0;
	struct math_xy R_surface_y1;

	//Emission
	struct math_xy Rrad;
	struct math_xy Photon_flux;

	//charge
	struct math_xy Q_nfree;
	struct math_xy Q_pfree;
	struct math_xy Q_ntrap;
	struct math_xy Q_ptrap;
	struct math_xy Q_nfree_and_ntrap;
	struct math_xy Q_pfree_and_ptrap;
	struct math_xy Q_theta;

	//mobility
	struct math_xy mu_n;
	struct math_xy mu_p;
	struct math_xy mu_n_p_avg;
	struct math_xy mu_n_p_geom;

	//conductivity
	struct math_xy conductivity_n;
	struct math_xy conductivity_p;
	struct math_xy conductivity_n_p_avg;

	//Thermal
	struct math_xy H_joule;
	struct math_xy H_recombination;
	struct math_xy H_parasitic;

	//srh rates
	struct math_xy srh_n_r1;
	struct math_xy srh_n_r2;
	struct math_xy srh_n_r3;
	struct math_xy srh_n_r4;

	struct math_xy srh_p_r1;
	struct math_xy srh_p_r2;
	struct math_xy srh_p_r3;
	struct math_xy srh_p_r4;


	//J
	struct math_xy J_y0_n;
	struct math_xy J_y0_p;
	struct math_xy J_y1_n;
	struct math_xy J_y1_p;

	struct math_xy jout;
	struct math_xy jn_avg;
	struct math_xy jp_avg;
	struct math_xy dynamic_jn;
	struct math_xy dynamic_jp;
	struct math_xy jnout_mid;
	struct math_xy jpout_mid;
	struct math_xy iout;
	struct math_xy dynamic_jn_drift;
	struct math_xy dynamic_jn_diffusion;

	struct math_xy dynamic_jp_drift;
	struct math_xy dynamic_jp_diffusion;

	//pl
	struct math_xy dynamic_pl;
	struct math_xy dynamic_pl_tot;

	//field
	struct math_xy E_field;
	struct math_xy dynamic_Vapplied;
	struct math_xy band_bend;

	//other
	struct math_xy dynamic_qe;

	//singlet
	struct math_xy Ns;
	struct math_xy Nt;
	struct math_xy Nsd;
	struct math_xy Ntd;
	struct math_xy Nho;

	//singlet
	struct math_xy N1C;
	struct math_xy N3C;

	double ***band_snapshot;

	double time;
	double voltage;
	int dump_level;

};
#endif
