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

/** @file shape_struct.h
	@brief A structure to hold shapes
*/


#ifndef shape_struct_h
#define shape_struct_h
#include <g_io.h>
#include "advmath.h"
#include <sim_struct.h>
#include <triangle.h>
#include <component.h>
#include <enabled_libs.h>
#include <dos_struct.h>
#include <heat_material.h>
#include <exciton_material.h>
#include <singlet_material.h>
#include <color_struct.h>
#include <dat_file_struct.h>

struct shape_interface
{
	int interface_type;
	gdouble interface_R;

	//tunneling
		//Direct tunneling
			int dir_tunnel_e;
			double dir_tunnel_e_A;
			double dir_tunnel_e_B;

			int dir_tunnel_h;
			double dir_tunnel_h_A;
			double dir_tunnel_h_B;

		//Fowler–Nordheim tunneling
			int fn_tunnel_e;
			double fn_tunnel_e_A;
			double fn_tunnel_e_B;

			int fn_tunnel_h;
			double fn_tunnel_h_A;
			double fn_tunnel_h_B;

		//Thermiomic emission
			int te_tunnel_e;
			double te_tunnel_e_A;
			double te_tunnel_e_B;

			int te_tunnel_h;
			double te_tunnel_h_A;
			double te_tunnel_h_B;

		//Hopping conduction
			int hc_tunnel_e;
			double hc_tunnel_e_A;
			double hc_tunnel_e_B;

			int hc_tunnel_h;
			double hc_tunnel_h_A;
			double hc_tunnel_h_B;

		//Organic-organic
			int interface_tunnel_e;
			double interface_Ge;

			int interface_tunnel_h;
			double interface_Gh;

	//doping
	int interface_left_doping_enabled;
	gdouble interface_left_doping;

	int interface_right_doping_enabled;
	gdouble interface_right_doping;
};

struct shape
{
	int enabled;

	double dx;
	double dy;
	double dz;

	double dx_padding;
	double dy_padding;
	double dz_padding;

	int nx;
	int ny;
	int nz;

	char name[100];
	char shape_type[20];
	char optical_material[200];
	char dos_file[100];
	char bhj_file[100];

	double x0;
	double y0;
	double z0;

	int epi_index;

	struct math_xy alpha;
	struct math_xy n;
	struct triangles tri;
	double rotate_x;
	double rotate_y;
	#ifdef libcircuit_enabled
		struct component com;
	#endif

	char id[100];
	struct dos dosn;
	struct dos dosp;
	struct heat_material heat;
	struct exciton_material ex;
	struct singlet_material sing;
	struct singlet_opv_material sing_opv;

	double Gnp;
	int optical_thickness_enabled;
	double optical_thickness;
	double Dphotoneff;

	struct obj_color color;
	struct dat_file bhj;

	double sum[10];			//A general counter for doing math

	//These are just pointers to memory defined elsewhere
	struct math_xy *abs_object;		//pointer to math tree for abs

	//Open GL min/max of object
		double g_x0;
		double g_y0;
		double g_x1;
		double g_y1;

	//nested objects
	struct shape *shapes;
	int nshape;

	int obj_type;	//ACTIVE,CONTACT, or OTHER
	struct shape_interface iface;
};

#endif
