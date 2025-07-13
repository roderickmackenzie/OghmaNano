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

/** @file mesh_struct.h
@brief meshing structure
*/

#ifndef mesh_struct_h
#define mesh_struct_h
#include <g_io.h>

struct mesh_layer
{
	double dx;
	double len;
	double mul;
	gdouble *dmesh;
	int n_points;
	int left_right;
	int start_at_edge_left;
	int start_at_edge_right;

	double start;
	double end;
};

struct mesh
{
	int enabled;
	int nlayers;
	int remesh;

	struct mesh_layer *layers;

	double start;
	double stop;

	int tot_points;
	int automatic;

	int start_at_zero;
	int stop_at_end;

	//These are used if we want to store the mesh in this object
	double *mesh;
	double *dmesh;
};

struct mesh_obj
{
	struct mesh meshdata_x;
	struct mesh meshdata_y;
	struct mesh meshdata_z;
	struct mesh meshdata_l;
	struct mesh meshdata_t;
};

#endif
