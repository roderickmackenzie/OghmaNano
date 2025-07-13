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

/** @file sim_struct.h
@brief define the sim structure, the sim structure is used to keep all simulation parameters which are physicaly part of the device. Such as dll locations.
*/


#ifndef sim_struct_h
#define sim_struct_h
#include <g_io.h>
#include <enabled_libs.h>
#include <stdio.h>
#include <server_struct.h>
#include "cache_struct.h"
#include <hard_limit_struct.h>
#include <g_io.h>

	#include <sys/mman.h>
	#include <sys/stat.h>
	#include <fcntl.h>
	#include <unistd.h>

#include <dirent.h>
#include <math_xy_struct.h>
#include <dos_struct.h>

//<strip>


#include <oghma_const.h>
#include <mesh_struct.h>
#include <paths.h>
#include <rand_mtwister.h>
#include <fit_struct.h>

struct logging
{
	int log_level;
	char path[OGHMA_PATH_MAX];
	int html;
};

struct matrix_solver_dll
{
	char name[20];
	void (*dll_matrix_init)();
	void (*dll_matrix_solve)();
	void (*dll_matrix_solver_free)();
	void *dll_matrix_handle;
};

struct simulation
{
	//plotting
	FILE *gnuplot;
	FILE *gnuplot_time;
	//dump
	int dump_array[100];
	int dumpfiles;
	//struct dumpfiles_struct *dumpfile;

	//paths
	char root_simulation_path[OGHMA_PATH_MAX];

	//struct logging log;
	int log_level;
	int html;

	struct paths paths;
	char share_path[OGHMA_PATH_MAX];
	char exe_path[OGHMA_PATH_MAX];
	char exe_path_dot_dot[OGHMA_PATH_MAX];
	char cache_path[OGHMA_PATH_MAX];
	char cache_path_for_fit[OGHMA_PATH_MAX];
	char oghma_local_path[OGHMA_PATH_MAX];
	char command_line_path[OGHMA_PATH_MAX];

	//solver name
	char complex_solver_name[20];
	char enable_optimizer[20];

	//Matrix solver dll	- external
		struct matrix_solver_dll matrix;

	//Complex matrix solver dll	- thses should use the matrix_solver_dll structure
		void (*dll_complex_matrix_init)();
		void (*dll_complex_matrix_solve)();
		void (*dll_complex_matrix_solver_free)();
		void *dll_complex_matrix_handle;

	//Newton solver dll
		int (*dll_solve_cur)();
		int (*dll_solver_realloc)();
		int (*dll_solver_free_memory)();
		void *dll_solver_handle;

	//Solve dlls
	char force_sim_mode[100];

	//Fitting vars
	double last_total_error;
	int fitting;
	int fit_dump_snapshots;
	struct server_struct server;

	int gui;
	long int bytes_written;
	long int bytes_read;
	long int files_read;
	long int files_written;

	int math_stop_on_convergence_problem;

	int cache_len;
	int cache_max;
	struct cache_item *cache;

	//gui
	int mindbustx;

	struct math_xy cie_x;
	struct math_xy cie_y;
	struct math_xy cie_z;

	char *error_log;
	int error_log_size;
	int error_log_size_max;
	int errors_logged;


	struct hard_limit hl;
	struct dos_cache doscache;
	int running_on_real_windows;

	struct mesh_obj meshdata_t;
	double *T_dos;
	int T_dos_len;

	//random numbers
	struct rand_state rand;

	//configure	- used to derive non device paramters
	struct json config;

	//cache of math_xy data
	struct hash_list math_xy_cache;
	struct hash_list triangles_cache;

	//Fit config
	struct fitconfig fitconfig;
};

#endif

