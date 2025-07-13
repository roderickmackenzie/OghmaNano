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

/** @file fdtd.h
	@brief Header for FDTD functions.
*/


#ifndef h_fdtd
#define h_fdtd
#include <g_io.h>
#include <enabled_libs.h>
#include <complex.h>
#include "advmath.h"
#include <sim_struct.h>
#include <device.h>

#ifdef use_open_cl
	//#define CL_USE_DEPRECATED_OPENCL_1_2_APIS
	#define CL_TARGET_OPENCL_VERSION 200
#include <CL/cl.h>
#endif
#include <dim.h>
#include <light.h>

#ifdef use_open_cl
	typedef struct //__attribute__((__packed__)) 
	{
		cl_int xlen;
		cl_int ylen;
		cl_int zlen;
		cl_float dx;
		cl_float dy;
		cl_float dz;
		cl_float dt2;
		cl_int sim_step;

		//boundary conditions
		cl_int y0;
		cl_int y1;
		cl_int x0;
		cl_int x1;
		cl_int z0;
		cl_int z1;
	} opencl_data ;

	typedef struct
	{
		cl_int x;
		cl_int y;
		cl_int z;
		cl_int excite_Ex;
		cl_int excite_Ey;
		cl_int excite_Ez;
		float omega;
		cl_int excitation_type;
	} opencl_light_src ;

#endif

struct fdtd_data
{

	struct dimensions dim;
	struct vec world_min;
	float ***Ex;
	float ***Ey;
	float ***Ez;
	float ***Hx;
	float ***Hy;
	float ***Hz;
	float ***Ex_last;
	float ***Ey_last;
	float ***Ez_last;
	float ***Ex_last_last;
	float ***Ey_last_last;
	float ***Ez_last_last;
	float ***Hx_last;
	float ***Hy_last;
	float ***Hz_last;
	float ***epsilon_r;
	float ***sigma;
	int ***detectors;

	float ***alpha;


	float ***tot_power_den;
	float dt;
	float dt2;

	float f;
	float omega;



	int excitation_mesh_point_x;
	int excitation_mesh_point_y;

	char *src_code;
	struct object ****obj;

	#ifdef use_open_cl
		cl_context context;
		cl_device_id device;

		//local memory
		float *gEx;
		float *gEy;
		float *gEz;
		float *gHx;
		float *gHy;
		float *gHz;
		float *gEx_last;
		float *gEy_last;
		float *gEz_last;
		float *gHx_last;
		float *gHy_last;
		float *gHz_last;
		float *gepsilon_r;
		float *gsigma;
		int *gdetectors;

		//opengl memory
		cl_mem ggEx;
		cl_mem ggEy;
		cl_mem ggEz;

		cl_mem ggHx;
		cl_mem ggHy;
		cl_mem ggHz;

		cl_mem ggEx_last;
		cl_mem ggEy_last;
		cl_mem ggEz_last;

		cl_mem ggHx_last;
		cl_mem ggHy_last;
		cl_mem ggHz_last;

		cl_mem ggepsilon_r;
		cl_mem ggsigma;
		cl_mem ggdetectors;

		cl_mem ggopencl_data;
		cl_mem gglight_srcs;

		cl_program prog;
		cl_command_queue cq;

		cl_kernel cal_E;
		cl_kernel cal_H;
		cl_kernel update_abc;
		cl_kernel update_excitation;

		//tx data
		opencl_data my_opencl_data;
		opencl_light_src light_srcs;		//This should be an array but no time now.
	#endif

	//config
	int lam_jmax;
	float gap;
	int max_ittr;
	float max_time;
	float src_start;
	float src_stop;
	float lambda;

	float stop;
	float time;
	int step;
	float escape;
	int excitation_type;
	int pulse_length;
	int excite_Ex;
	int excite_Ey;
	int excite_Ez;

	//boundary conditions
	int y0;
	int y1;
	int x0;
	int x1;
	int z0;
	int z1;
	double last_power;
};


void fdtd_init(struct fdtd_data *data);
int do_fdtd(struct simulation *sim,struct device *dev);
void fdtd_get_mem(struct simulation *sim, struct fdtd_data *data);
void fdtd_free_all(struct simulation *sim, struct fdtd_data *data);

void fdtd_zero_arrays(struct simulation *sim,struct fdtd_data *data);

void fdtd_solve_step(struct simulation *sim,struct fdtd_data *data,struct device *dev);

void fdtd_dump(struct simulation *sim,char *output_path,struct device *dev, struct fdtd_data *data);

void fdtd_mesh(struct simulation *sim,struct fdtd_data *data,struct device *dev);
void fdtd_3d_malloc_float(struct fdtd_data *in, float * (***var));

float fdtd_test_conv(struct simulation *sim,struct fdtd_data *data);
void fdtd_set_lambda(struct simulation *sim,struct fdtd_data *data,struct device *dev,float lambda);
void fdtd_solve_all_lambda(struct simulation *sim,struct device *dev,struct fdtd_data *data);
void fdtd_solve_lambda(struct simulation *sim,struct fdtd_data *data,struct device *dev,float lambda);
void fdtd_load_config(struct simulation *sim,struct device *dev, struct fdtd_data *data,struct json_obj *json_obj);
void fdtd_excitation(struct simulation *sim,struct fdtd_data *data,struct device *dev);
int fdtd_world_x_to_mesh(struct fdtd_data *data,float x);
int fdtd_world_y_to_mesh(struct fdtd_data *data,float y);
int fdtd_world_z_to_mesh(struct fdtd_data *data,float z);
void fdtd_time_step(struct simulation *sim,struct fdtd_data *data);
void fdtd_load_boundary_conditions(struct simulation *sim, struct fdtd_data *data,struct json_obj *json_obj);
void fdtd_detectors(struct simulation *sim,struct device *dev,struct fdtd_data *data);
void fdtd_detectors_add_powers(struct simulation *sim,struct device *dev,struct fdtd_data *data);
//stats
double fdtd_cal_power_y(struct simulation *sim,struct fdtd_data *data, int y);
float fdtd_power_zxy(struct simulation *sim,struct fdtd_data *data,int z, int x, int y);
float fdtd_power_y(struct simulation *sim,struct fdtd_data *data, int y);
double fdtd_cal_abs_power(struct simulation *sim,struct fdtd_data *data);
double fdtd_cal_tot_power_den(struct simulation *sim,struct fdtd_data *data);
void fdtd_add(struct fdtd_data *data,double dEz,double dEx,double dEy,int z, int x, int y, double *sum);

//opencl
void fdtd_opencl_load_config(struct simulation *sim, struct fdtd_data *data);
void opencl_init(struct simulation *sim, struct fdtd_data *data);
size_t fdtd_opencl_load_code(struct simulation *sim,struct fdtd_data *data,char *source_code_file);
void fdtd_opencl_kernel_init(struct simulation *sim, struct fdtd_data *data);
const char *opencl_error_decode(int error);
void fdtd_opencl_get_mem(struct simulation *sim, struct fdtd_data *data);
void fdtd_opencl_freemem(struct simulation *sim, struct fdtd_data *data);
int fdtd_opencl_solve_step(struct simulation *sim,struct fdtd_data *data);
void fdtd_opencl_pull_data(struct simulation *sim,struct fdtd_data *data);
void fdtd_opencl_push_to_gpu(struct simulation *sim,struct fdtd_data *data);
void fdtd_opencl_write_ctrl_data(struct simulation *sim,struct fdtd_data *data);
void opencl_cards_to_json(struct simulation *sim);

//OpenCL
void opencl_write_excitation_data(struct simulation *sim,struct device *dev,struct fdtd_data *data);

#ifdef use_open_cl
	cl_int g_clSetKernelArg (struct simulation *sim, cl_kernel kernel, cl_uint arg_index, size_t arg_size, const void *arg_value);
	cl_int g_clEnqueueWriteBuffer (struct simulation *sim, cl_command_queue command_queue, cl_mem buffer, cl_bool blocking_write, size_t offset,	size_t cb, const void *ptr, cl_uint num_events_in_wait_list, const cl_event *event_wait_list, cl_event *event);

#endif
#endif
