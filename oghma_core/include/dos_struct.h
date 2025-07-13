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

/** @file dos_struct.h
	@brief Hold information about the DoS.
*/


#ifndef dos_struct_h
#define dos_struct_h
#include <g_io.h>
#include <rpn_struct.h>
#include <dos_an.h>

struct dos_cache_obj
{
	int len;
	char id[100];
	char md5[100];
	char *dosn;
	char *dosp;
};

struct dos_cache
{
	int enabled;
	int setup;
	int len;
	int len_max;
	struct dos_cache_obj *objs;
};

struct dosconfig
{
	char dos_name[20];
	int dos_number;
	int dostype;
	int dos_free_carrier_stats;
	gdouble Nt;
	gdouble Et;
	gdouble nstart;
	gdouble nstop;
	int npoints;

	int traps;
	gdouble dband;
	gdouble detrap;
	int srh_bands;
	gdouble srh_start;
	gdouble srh_stop;


	gdouble srh_sigman;
	gdouble srh_sigmap; 
	gdouble srh_vth;
	gdouble Nc;
	gdouble Nv;
	gdouble me;
	gdouble mh;

	struct rpn_equation Eg;
	struct rpn_equation Xi;
	double epsilonr;

	int Esteps;
	struct dos_an_data my_dos_an;

};

struct dos
{
	int enabled;
	gdouble *x;
	int xlen;
	int tlen;
	int srh_bands;
	gdouble *t;
	gdouble *srh_E;
	gdouble *srh_den;
	gdouble **c;
	gdouble **w;
	gdouble ***srh_r1;
	gdouble ***srh_r2;
	gdouble ***srh_r3;
	gdouble ***srh_r4;
	gdouble ***srh_c;
	struct dosconfig config;

	int dd_enabled;
	struct rpn_equation muz;
	struct rpn_equation mux;
	struct rpn_equation muy;
	int mobility_symmetric;

	//Thermal dependent mobility
	int mu_tdep_enable;
	double mu_delta;

	//Auger
	int auger_enabled;
	gdouble Cn;
	gdouble Cp;

	//SS SRH
	int ss_srh_enabled;
	gdouble n1;
	gdouble p1;
	gdouble tau_n;
	gdouble tau_p;

	//recombination
	double B;
	int f2f_lambda_enable;
	double f2f_lambda;

	//Doping
	double Na0;
	double Na1;
	double Nd0;
	double Nd1;

	//Peorvskite
	double ion_density;
	double ion_mobility;
};


#endif
