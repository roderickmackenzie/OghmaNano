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

#include <enabled_libs.h>
#include <stdio.h>
#include <ray.h>
#include <ray_fun.h>
#include <oghma_const.h>
#include <math.h>
#include <stdlib.h>
#include <cal_path.h>
#include <log.h>
#include <device.h>
#include <util.h>
#include <triangles.h>
#include <memory.h>
#include <device_fun.h>
#include <object_fun.h>
#include <mesh.h>

/** @file ray_engine_malloc.c
	@brief Set up the simulation window for the ray tracer
*/


void ray_malloc(struct simulation *sim,struct device *dev,struct ray_engine *eng)
{
	int i=0;
	eng->ray_wavelength_points=dev->optical_mesh_data.meshdata_l.tot_points;

	struct dimensions *dim=&(dev->dim_optical);


	if (eng->enabled==FALSE)
	{
		ewe(sim,"Ray not enabled");
	}


	//eng->tri=malloc(sizeof(struct triangle)*eng->triangles_max);


	eng->lam=malloc(sizeof(double)*eng->ray_wavelength_points);


	eng->ang_escape=(double **)malloc(sizeof(double*)*eng->ray_wavelength_points);
	eng->angle=(double *)malloc(sizeof(double)*eng->escape_bins);

	double da=180.0/(double)eng->escape_bins;
	double apos=0.0;
	for (i=0;i<eng->escape_bins;i++)
	{
		apos+=da;
		eng->angle[i]=apos;
	}


	if (mesh_to_lin_array_lambda(eng->lam,  &(dev->optical_mesh_data.meshdata_l))==-1)
	{
		ewe(sim,"mesh does not match\n");
	}

	for (i=0;i<eng->ray_wavelength_points;i++)
	{
		eng->ang_escape[i]=(double*)malloc(sizeof(double)*eng->escape_bins);
	}
	
	if (eng->ray_dump_abs_profile==TRUE)
	{
		if ((dim->zlen==0)||(dim->xlen==0)||(dim->ylen==0))
		{
			ewe(sim,"the optical mesh is zero in one axis\n");
		}

		malloc_zxy_double(dim, &(eng->abs_profile));
	}


	math_xy_alloc_device_tree(sim, &(eng->abs_objects), dev, eng->lam,  eng->ray_wavelength_points);
	math_xy_malloc(&(eng->tot_ray_power),eng->ray_wavelength_points);
	eng->tot_ray_power.len=eng->ray_wavelength_points;
	strcpy(eng->tot_ray_power.file_name,"tot_ray_power");
}
