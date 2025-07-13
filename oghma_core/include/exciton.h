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

/** @file exciton.h
@brief a structure for the heat model
*/

#ifndef h_exciton
#define h_exciton
#include <g_io.h>
#include <complex.h>
#include "advmath.h"
#include <sim_struct.h>
#include <epitaxy_struct.h>
#include <ray.h>
#include <matrix.h>
#include <object.h>
#include <dat_file_struct.h>
#include <dim.h>
#include <mesh_struct.h>
#include <exciton_material.h>


struct exciton
{
	char dump_dir[OGHMA_PATH_MAX];
	struct dimensions dim;
	int dump_verbosity;

	//zxy
	double ***n;		//Exciton density
	double ***G;		//Generation
	double ***Gn;		//Generation
	double ***Gp;		//Generation
	double ***D;		//Diffusion constant
	double ***L;		//Diffusion length
	double ***tau;		//lifetime of exciton
	double ***k_pl;	//radiative decay rate in absence of quencher sites
	double ***k_fret;	//denotes the rate of Förster resonance energy transfer (FRET) in the presence of a neighboring material.
	double ***alpha;	//exciton–exciton annihilation rate constant
	double ***k_dis;	//Dissociation

	//Saved rates
	double ***Rk_pl;
	double ***Rk_fret;
	double ***Ralpha;
	double ***Rk_dis;

	//objects
	struct object ****obj;


	struct matrix mx;

	//boundry temperatures
	double n_y0;
	double n_y1;
	double n_x0;
	double n_x1;
	double n_z0;
	double n_z1;

	//Boundry type
	int y0_boundry;
	int y1_boundry;
	int x0_boundry;
	int x1_boundry;
	int z0_boundry;
	int z1_boundry;

	//heat sink
	double excitonsink_y0;
	double excitonsink_y1;
	double excitonsink_x0;
	double excitonsink_x1;
	double excitonsink_z0;
	double excitonsink_z1;

	double excitonsink_length_y0;
	double excitonsink_length_y1;
	double excitonsink_length_x0;
	double excitonsink_length_x1;
	double excitonsink_length_z0;
	double excitonsink_length_z1;

	//convergance
	int ex_conv;
	double min_error;
	int exciton_enabled;
	int exciton_max_ittr;
	int exciton_couple_to_electrical_solver;
	int solver_verbosity;

	//mesh
	struct mesh_obj mesh_data;

	//interfaces
	int exciton_split_at_interface;
	double exciton_interface_depth;
};

#endif
