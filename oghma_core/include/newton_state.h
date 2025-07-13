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

/** @file newton_state.h
	@brief The main structure which holds information about the device.
*/

#ifndef newton_state_h
#define newton_state_h
#include <stdio.h>
#include <dim.h>

struct newton_state
{
	char name[10];
	int active;
	struct dimensions dim;
	int problem_type;
	int last_ittr;
	double last_error;
	double last_max_error;
	double last_time;
	//Fermi vars
		//Phi
			gdouble ***phi;

		//Fermi vars for electrons
			gdouble ***x;
			gdouble ****xt;

		//Fermi vars for holes
			gdouble ***xp;
			gdouble ****xpt;

		//NIon
			gdouble ***x_Nion;

		//Singlet
			double ***x_Ns;
			double ***x_Nt;
			double ***x_Nsd;
			double ***x_Ntd;
			double *x_Nho;

		//Singlet_opv
			double ***x_N1C;
			double ***x_N3C;

		//Fermi levels for schottky contact
			gdouble **x_y0;
			gdouble **xp_y0;
			gdouble **x_y1;
			gdouble **xp_y1;

	//Things calculated as a result of Fermi levels
		//Ions
			double ***Nion;
			double ***dNion;
			double ***dNiondphi;
			double ***Nion_last;

		//Singlet
			double ***Ns;
			double ***Nt;
			double ***Nsd;
			double ***Ntd;
			double *Nho;

			double ***dNs;
			double ***dNt;
			double ***dNsd;
			double ***dNtd;
			double *dNho;

			double ***Ns_last;
			double ***Nt_last;
			double ***Nsd_last;
			double ***Ntd_last;
			double *Nho_last;

		//Singlet_opv
			double ***N1C;
			double ***N3C;

			double ***dN1C;
			double ***dN3C;

			double ***N1C_last;
			double ***N3C_last;
			double ***dN1C_last;
			double ***dN3C_last;

		//Bands
			double ***Ev;
			double ***Ec;

		//Recombination
			double ***Rfree;
			double ***Rauger;
			double ***Rss_srh;

			double ***Rn;
			double ***Rp;
			double ***Rnet;

			double ***Rn_srh;
			double ***Rp_srh;

		//Free charges
			double ***n;
			double ***p;
			double ***dn;
			double ***dndphi;
			double ***dp;
			double ***dpdphi;
			double ***Dn;		//Maybe remove?
			double ***Dp;		//Maybe remove?

			double ***Fn;
			double ***Fp;

			double ***nf_save;
			double ***pf_save;

			double ***nfequlib;
			double ***pfequlib;

			double ***nlast;
			double ***plast;

			double ***wn;
			double ***wp;

			double ***n_orig;
			double ***p_orig;

			double ***n_orig_f;
			double ***p_orig_f;

			double ***n_orig_t;	
			double ***p_orig_t;

			double ***t;			//in->Xi[z][x][y];
			double ***tp;			//in->Xi[z][x][y]+in->Eg[z][x][y]
			double ***t_ion;

		//Traps 3d n
			double ***nt_all;
			double ***tt;			//in->Xi[z][x][y];

			double ***nt_save;
			double ***ntequlib;

		//Traps 3d p
			double ***pt_all;
			double ***tpt;			//in->Xi[z][x][y]+in->Eg[z][x][y]

			double ***pt_save;
			double ***ptequlib;

		//Traps 4d n
			double  ****nt;
			double  ****ntlast;
			double  ****dnt;
			double  ****srh_n_r1;
			double  ****srh_n_r2;
			double  ****srh_n_r3;
			double  ****srh_n_r4;
			double  ****dsrh_n_r1;
			double  ****dsrh_n_r2;
			double  ****dsrh_n_r3;
			double  ****dsrh_n_r4;
			double  ****Fnt;

			double  ****nt_r1;
			double  ****nt_r2;
			double  ****nt_r3;
			double  ****nt_r4;

			double ****ntb_save;

		//Traps 4d p
			double  ****pt;
			double  ****ptlast;
			double  ****dpt;
			double  ****srh_p_r1;
			double  ****srh_p_r2;
			double  ****srh_p_r3;
			double  ****srh_p_r4;
			double  ****dsrh_p_r1;
			double  ****dsrh_p_r2;
			double  ****dsrh_p_r3;
			double  ****dsrh_p_r4;
			double  ****Fpt;

			double  ****pt_r1;
			double  ****pt_r2;
			double  ****pt_r3;
			double  ****pt_r4;

			double ****ptb_save;

		//Rates
			double ***nrelax;
			double ***ntrap_to_p;
			double ***prelax;
			double ***ptrap_to_n;

		//Current
			double ***Jn;
			double ***Jp;
			double ***Jn_x;
			double ***Jp_x;
			double ***Jn_z;
			double ***Jp_z;

			double ***Jn_diffusion;
			double ***Jn_drift;

			double ***Jn_x_diffusion;
			double ***Jn_x_drift;

			double ***Jn_z_diffusion;
			double ***Jn_z_drift;

			double ***Jp_diffusion;
			double ***Jp_drift;

			double ***Jp_x_diffusion;
			double ***Jp_x_drift;

			double ***Jp_z_diffusion;
			double ***Jp_z_drift;

			double ***Jion;

		//Current at contacts
			double **Jn_y0;
			double **Jn_y1;
			double **Jp_y0;
			double **Jp_y1;

			double **Jn_x0;
			double **Jn_x1;
			double **Jp_x0;
			double **Jp_x1;

			double **Jn_z0;
			double **Jn_z1;
			double **Jp_z0;
			double **Jp_z1;

		//delete??
			double ***phi_save;

	//for clever exiting of solver
		gdouble last_errors[10];
		int last_error_pos;

	//What to solver for
		int allowed_equations;
		int singlet_enabled;
		int singlet_enabled_Ns;
		int singlet_enabled_Nt;
		int singlet_enabled_Nsd;
		int singlet_enabled_Ntd;
		int singlet_enabled_Nho;
		int singlet_opv_enabled;

	//for accelerating the Bernoulli fucntion
		double ***By_xi_plus;
		double ***By_xi_neg;
		double ***By_xip_plus;
		double ***By_xip_neg;

		double ***Bx_xi_plus;
		double ***Bx_xi_neg;
		double ***Bx_xip_plus;
		double ***Bx_xip_neg;

		double ***Bz_xi_plus;
		double ***Bz_xi_neg;
		double ***Bz_xip_plus;
		double ***Bz_xip_neg;

		double ***dBy_xi_plus;
		double ***dBy_xi_neg;
		double ***dBy_xip_plus;
		double ***dBy_xip_neg;

		double ***dBx_xi_plus;
		double ***dBx_xi_neg;
		double ***dBx_xip_plus;
		double ***dBx_xip_neg;

		double ***dBz_xi_plus;
		double ***dBz_xi_neg;
		double ***dBz_xip_plus;
		double ***dBz_xip_neg;

	//Arrays used by newton solver
		double *newton_dntrap;
		double *newton_dntrapdntrap;
		double *newton_dntrapdn;
		double *newton_dntrapdp;
		double *newton_dJdtrapn;
		double *newton_dJpdtrapn;

		double *newton_dptrapdp;
		double *newton_dptrapdptrap;
		double *newton_dptrap;
		double *newton_dptrapdn;
		double *newton_dJpdtrapp;
		double *newton_dJpdtrapp_interface_right;
		double *newton_dJdtrapp;
		double *newton_dphidntrap;
		double *newton_dphidptrap;
		double *newton_ntlast;
		double *newton_ptlast;

		//Singlet
		double *newton_dNsG_dntrap;
 		double *newton_dNsG_dptrap;

		double *newton_dNtG_dntrap;
 		double *newton_dNtG_dptrap;

		//Singlet_opv
		double *newton_dN1C_dntrap;
 		double *newton_dN1C_dptrap;

		double *newton_dN3C_dntrap;
 		double *newton_dN3C_dptrap;

	//Offsets
		//Standard electrical solver
			double ddh;

	//Solve equations
		int ***equs;			//**move
		int ***equs_all;		//**move
		int ***equs_matrix_pos;	//**move
		int start_of_aux_equations;

	//Matrix building vars
		double Je_build;
		double Jh_build;

		double Nho_build;
		double dNho_build;



};


struct newton_state_complex
{
	struct dimensions dim;

	gdouble complex ***phi;
	gdouble complex ***x;
	gdouble complex ***xp;

	gdouble complex ****xt;
	gdouble complex ****xpt;

};

struct newton_states
{
	int len;
	int max;
	struct newton_state *lib;
};


#endif
