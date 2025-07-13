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

/** @file circuit.h
@brief Header files for nodal analysis
*/

#ifndef circuit_struct_h
#define circuit_struct_h
#include <g_io.h>
#include <shape_struct.h>
#include <sim_struct.h>
#include <matrix_solver_memory.h>
#include <contact_struct.h>

#define CIR_KNOWN 0
#define CIR_UNKNOWN 1
#define CIR_CHANGE_X 2

struct circuit_config_line
{
	char component[100];
	int x0;
	int y0;
	int z0;
	int x1;
	int y1;
	int z1;
	double L;
	double C;
	double R;
	double R_sigma;
	double a;
	double a_sigma;
	double b;
	double b_sigma;
	double c;
	double c_sigma;
	double nid;
	double nid_sigma;
	double I0;
	double I0_sigma;
	double phi0;
	double phi0_sigma;
	double b0;
	double b0_sigma;
	int com_enable_sigma;
	double Dphotoneff;
	char layer_name[100];
	int uid;
	int count;
};

struct circuit_link
{
	int start;
	int stop;
	char type;
	double L;
	double C;
	double R;
	double a;
	double b;
	double c;
	double I0;
	double phi0;
	double b0;
	double Isc;
	int enable_Isc;
	double n0;
	double i;
	double Dphotoneff;
	double dl;		//Length between nodes
	int uid;

	//only used for diodes and to figure out where they are.
	struct shape *s;
	int x;
	int z;
	int id;

	int enabled;

};

struct circuit_node
{
	double V;
	double V_last;
	char type;
	int matrix_pos;
	int z;
	int x;
	int y;

	double z_pos;
	double x_pos;
	double y_pos;

	int *links;
	int nlinks;
	int nlinks_max;
	char selected;
	int node_index;
	int contact_number;		//contact
};

struct circuit
{
	int nodes_len;
	int links_len;
	int nodes_max;
	int links_max;
	int unknowns;
	struct matrix mx;
	struct circuit_node *nodes;
	struct circuit_link *links;
	int config_nlines;
	struct circuit_config_line * config_lines;
	int abstract_circuit;		//The circuit does not follow a device structure
	int enabled;
	struct matrix_solver_memory msm;
	int quite;
	int prime;
	int step;
	int solver_verbosity;
	int circuit_mesh_src;
};

#endif
