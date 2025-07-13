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
#include <oghma_const.h>
#include <math.h>
#include <stdlib.h>
#include <cal_path.h>
#include <log.h>
#include <ray_fun.h>
#include <unistd.h>
#include <dump_ctrl.h>
#include <gui_hooks.h>
#include <util.h>
#include <memory.h>
#include <epitaxy_struct.h>
#include <epitaxy.h>
#include <dump.h>
#include <device_fun.h>
#include <g_io.h>
#include <detector.h>
#include <triangles.h>

/** @file solve.c
	@brief This will call the ray tracer for the standard case.
*/

int ray_apply_light_profile(struct simulation *sim, struct device *dev, struct ray_src *raysrc, double *mag, int nx, int ny, int nz)
{
	int light_src_n;
	struct light_src *src;
	double x_pos=0.0;
	double z_pos=0.0;
	double mul=1.0;
	struct light_sources *srcs=&(dev->lights);
	struct vec my_vec;

	if ((raysrc->nx)>1&&(raysrc->nz>1))
	{
		x_pos=(double)nx/(double)raysrc->nx;
		z_pos=(double)nz/(double)raysrc->nz;
	}else
	if ((raysrc->ny)>1&&(raysrc->nx>1))
	{
		x_pos=(double)ny/(double)raysrc->ny;
		z_pos=(double)nx/(double)raysrc->nx;
	}else
	if ((raysrc->ny)>1&&(raysrc->nz>1))
	{
		x_pos=(double)ny/(double)raysrc->ny;
		z_pos=(double)nz/(double)raysrc->nz;
	}else
	{
		return 0;
	}

	light_src_n=raysrc->light;
	src=&(srcs->light_sources[light_src_n]);

	if (strcmp(src->light_profile,"box")!=0)
	{
		my_vec.x=x_pos;
		my_vec.z=z_pos;
		mul=triangles_interpolate(&src->light_profile_tri,&my_vec);
		if (mul<0.01)
		{
			mul=0.0;
		}
		printf("%lf %lf %le\n",x_pos,z_pos,mul);
		//mul=sqrt(mul);
		(*mag)*=mul;
	}

	return 0;

}
void ray_solve(struct simulation *sim,struct device *dev, double mag,struct ray_worker *worker)
{


}

