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

/** @file solver_interface.c
	@brief Load the sparse matrix solver .so/.dll.  If this is UMFPACK the plugin will call UMFPACK, for other custom solvers the work will be done in the plugin.
*/

#include <enabled_libs.h>
#include <stdio.h>
#include <stdlib.h>
#include "util.h"
#include "oghma_const.h"
#include "device.h"
#include "dump_ctrl.h"
#include "config.h"
#include "cal_path.h"
#include <lang.h>
#include <log.h>
#include <code_ctrl.h>
#include <g_io.h>

static int unused __attribute__((unused));

void solver_init(struct simulation *sim,char *solver_name)
{
char lib_path[PATH_MAX];




	if (sim->dll_matrix_handle==NULL)
	{
		find_dll(sim, lib_path,solver_name);
		sim->dll_matrix_handle = g_dlopen(lib_path);

		if (sim->dll_matrix_handle==NULL)
		{
			ewe(sim,"%s %s\n",_("dll not loaded"),lib_path);
		}

		sim->dll_matrix_solve = g_dlsym(sim->dll_matrix_handle, "dll_matrix_solve");
		if (sim->dll_matrix_solve==NULL)
		{
			ewe(sim,_("dll function dll_matrix_solve not found\n"));
		}

		sim->dll_matrix_solver_free = g_dlsym(sim->dll_matrix_handle, "dll_matrix_solver_free");
		if (sim->dll_matrix_solver_free==NULL)
		{
			ewe(sim,_("dll function dll_matrix_solver_free not found\n"));
		}

		sim->dll_matrix_init = g_dlsym(sim->dll_matrix_handle, "dll_matrix_init");
		if (sim->dll_matrix_init==NULL)
		{
			ewe(sim,_("dll function dll_matrix_init not found\n"));
		}

	}


}

void solver_get_mem(struct simulation *sim,struct matrix_solver_memory *msm)
{

	(*sim->dll_matrix_init)(msm);
}

void solver_free(struct simulation *sim,struct matrix_solver_memory *msm)
{
	if (sim->dll_matrix_handle!=NULL)
	{
		(*sim->dll_matrix_solver_free)(msm);
		matrix_solver_memory_free(sim,msm);
	}

}

void solver_unload_dll(struct simulation *sim)
{
	if (sim->fitting==FIT_NOT_FITTING)
	{
		printf_log(sim,"unload DLLs\n");
	}
	if (sim->dll_matrix_handle!=NULL)
	{

		if (g_dlclose(sim->dll_matrix_handle)!=0)
		{
			ewe(sim,"%s\n",_("Error closing dll"));
		}

		sim->dll_matrix_handle=NULL;
		sim->dll_matrix_solve=NULL;
		sim->dll_matrix_solver_free=NULL;
		sim->dll_matrix_init=NULL;

	}
}
