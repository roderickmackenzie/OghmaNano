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

/** @file newton_interface.c
	@brief Load and run the newton solve .dll/.so file.  They are hot swappable hence the interface.
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
#include "lang.h"
#include "log.h"
#include "newton_interface.h"
#include <g_io.h>

void newton_load_dll(struct simulation *sim,char *solver_name)
{
	//printf_log(sim,_("Solver initialization\n"));
	char lib_path[PATH_MAX];

	find_dll(sim, lib_path,solver_name);

	if (sim->dll_solver_handle!=NULL)
	{
		return;
	}

	sim->dll_solver_handle = g_dlopen(lib_path);
	if (sim->dll_solver_handle==NULL)
	{
		ewe(sim,"%s %s\n",_("dll not loaded"),lib_path);
	}

	if (sim->dll_solve_cur!=NULL)
	{
		ewe(sim,_("dll_solve_cur not NULL\n"));
	}
	sim->dll_solve_cur = g_dlsym(sim->dll_solver_handle, "dll_solve_cur");
	if (sim->dll_solve_cur==NULL)
	{
		ewe(sim,_("dll function dll_solve_cur not found\n"));
	}

	if (sim->dll_solver_realloc!=NULL)
	{
		ewe(sim,_("dll_solver_realloc not NULL\n"));
	}
	sim->dll_solver_realloc = g_dlsym(sim->dll_solver_handle, "dll_solver_realloc");
	if (sim->dll_solver_realloc==NULL)
	{
		ewe(sim,_("dll function dll_solver_realloc not found\n"));
	}

	if (sim->dll_solver_free_memory!=NULL)
	{
		ewe(sim,_("dll_solver_free_memory not NULL\n"));
	}
	sim->dll_solver_free_memory = g_dlsym(sim->dll_solver_handle, "dll_solver_free_memory");
	if (sim->dll_solver_free_memory==NULL)
	{
		ewe(sim,_("dll function dll_solver_free_memory not found\n"));
	}

}


void newton_set_min_ittr(struct device *dev,int ittr)
{
	dev->newton_min_itt=ittr;
}

void solver_realloc(struct simulation *sim,struct device * dev)
{
	if (sim->dll_solver_realloc!=NULL)
	{
		(*sim->dll_solver_realloc)(sim,dev);
	}
}

void solver_free_memory(struct simulation *sim,struct device * dev)
{
	if (sim->dll_solver_free_memory!=NULL)
	{
		(*sim->dll_solver_free_memory)(sim,dev);
	}
}

void newton_interface_free(struct simulation *sim)
{
	if (sim->dll_solver_handle!=NULL)
	{
		g_dlclose(sim->dll_solver_handle);
	}
	sim->dll_solver_free_memory=NULL;
	sim->dll_solver_realloc=NULL;
	sim->dll_solve_cur=NULL;
}
