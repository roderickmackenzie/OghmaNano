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

/** @file heat.h
@brief a structure for the heat model
*/

#ifndef h_heat
#define h_heat
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
#include <heat_material.h>


struct heat
{
	char dump_dir[OGHMA_PATH_MAX];
	struct dimensions dim;
	int thermal_model_type;
	int dump_verbosity;

	//zxy
	gdouble ***Tl;
	gdouble ***Te;
	gdouble ***Th;

	gdouble ***Hl;

	gdouble ***H_optical;
	gdouble ***H_joule;
	gdouble ***H_parasitic;
	gdouble ***H_recombination;

	gdouble ***He;
	gdouble ***Hh;

	gdouble ***kl;
	gdouble ***ke;
	gdouble ***kh;

	//objects
	struct object ****obj;


	struct matrix mx;

	//boundry temperatures
	gdouble Ty0;
	gdouble Ty1;
	gdouble Tx0;
	gdouble Tx1;
	gdouble Tz0;
	gdouble Tz1;

	//Boundry type
	int Ty0_boundry;
	int Ty1_boundry;
	int Tx0_boundry;
	int Tx1_boundry;
	int Tz0_boundry;
	int Tz1_boundry;

	//heat sink
	gdouble heatsink_y0;
	gdouble heatsink_y1;
	gdouble heatsink_x0;
	gdouble heatsink_x1;
	gdouble heatsink_z0;
	gdouble heatsink_z1;

	gdouble heatsink_length_y0;
	gdouble heatsink_length_y1;
	gdouble heatsink_length_x0;
	gdouble heatsink_length_x1;
	gdouble heatsink_length_z0;
	gdouble heatsink_length_z1;

	int Tliso;
	int Triso;
	int nofluxl;

	//convergance
	int thermal_conv;
	gdouble min_error;
	int newton_enable_external_thermal;
	int thermal_l;
	int thermal_e;
	int thermal_h;
	int thermal_max_ittr;
	int thermal_couple_to_electrical_solver;
	struct mesh_obj mesh_data;

	//Options
	int joule_heating;
	int parasitic_heating;
	int recombination_heating;
	int optical_heating;

	int solver_verbosity;

};

#endif
