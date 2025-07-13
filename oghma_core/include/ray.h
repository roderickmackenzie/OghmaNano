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

/** @file ray.h
@brief ray tracing header files.
*/
#ifndef ray_h
#define ray_h
#include <g_io.h>
#include <enabled_libs.h>
#include <vec.h>
#include <math_xy.h>
#include <sim_struct.h>
#include <triangle.h>
#include <dim.h>
#include <shape_struct.h>
#include <object.h>
#include <oghma_const.h>
#include <dim.h>

struct ray
{
	struct vec xy;
	struct vec xy_end;
	struct vec dir;
	int state;
	int bounce;
	int obj_uid_start;		//The ray started in
	int parent;
	int uid;
	double mag0;			//Start mag
	double mag1;			//Stop mag
};


struct ray_src
{
	double x;
	double y;
	double z;

	int theta_steps;
	double theta_start;
	double theta_stop;

	int phi_steps;
	double phi_start;
	double phi_stop;

	double dx_padding;
	double dy_padding;
	double dz_padding;

	double dx;
	double dy;
	double dz;

	int nx;
	int ny;
	int nz;

	double single_ray_area;

	double rotate_x;
	double rotate_y;

	int epi_layer;		//epi layer
	int light;			//light source
	int emission_source;	//single point or mesh

	double mag;			//The magnitude of the soruce
	int mesh_x;			//Mesh point where the source came from
	int mesh_y;			//
	int mesh_z;

	double *emitted;
	double *detected;

	char name[20];

};

//The worker solves only one wavelength from one light source at a time. 
struct ray_worker
{
	struct ray *rays;
	int nrays;
	int nray_max;
	int top_of_done_rays;
	int l;
	int worker_n;
	int rays_shot;
	struct ray_src *raysrc;

	double ray_min_intensity;

	double total_input_magnitude;
	double total_detected_magnitude;
};

struct ray_engine
{
	int enabled;

	struct ray_src *ray_srcs;
	int n_ray_srcs;
	int n_ray_srcs_max;

	double y_escape_level;
	double *angle;
	double **ang_escape;
	int ray_wavelength_points;
	double *lam;

	//benchmarking
	int tot_rays;
	double start_time;

	//run control
	int ray_auto_run;
	int run_each_n_steps;
	int dump_verbosity;
	char ray_snapshot_dir[OGHMA_PATH_MAX];
	int disable_error_on_no_light_srcs;

	//Abs profile tracker
	int ray_dump_abs_profile;
	double ***abs_profile;
	struct math_xy abs_objects;
	struct math_xy tot_ray_power;

	//from json config
	int escape_bins;
	double ray_min_intensity;
	int ray_max_bounce;
	int ray_sim_reflected;
	int ray_sim_transmitted;
	
	int call_count;

	double Psun;
};

#endif
