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
#include <epitaxy_struct.h>
#include <epitaxy.h>
#include <device_fun.h>


/** @file ray_build_scene.c
	@brief Set up the simulation window for the ray tracer
*/

int ray_engine_add_emitters(struct simulation *sim,struct device *dev)
{
	int i;
	struct light_src *lightsrc;
	struct ray_src *raysrc;
	struct ray_engine *eng=&(dev->eng);

	ray_src_clear_emitters(eng);


	for (i=0;i<dev->lights.nlight_sources;i++)
	{
		lightsrc=&(dev->lights.light_sources[i]);
		if (strcmp(lightsrc->illuminate_from,"xyz")==0)
		{
			raysrc=ray_src_add_emitter(eng);

			raysrc->x=lightsrc->x0;
			raysrc->y=lightsrc->y0;
			raysrc->z=lightsrc->z0;

			raysrc->theta_steps=lightsrc->theta_steps;
			raysrc->theta_start=lightsrc->theta_start;
			raysrc->theta_stop=lightsrc->theta_stop;

			raysrc->phi_steps=lightsrc->phi_steps;
			raysrc->phi_start=lightsrc->phi_start;
			raysrc->phi_stop=lightsrc->phi_stop;

			raysrc->dx_padding=lightsrc->dx_padding;
			raysrc->dy_padding=lightsrc->dy_padding;
			raysrc->dz_padding=lightsrc->dz_padding;

			raysrc->dx=lightsrc->dx;
			raysrc->dy=lightsrc->dy;
			raysrc->dz=lightsrc->dz;

			raysrc->nx=lightsrc->nx;
			raysrc->ny=lightsrc->ny;
			raysrc->nz=lightsrc->nz;

			//calculate beam area
			if ((raysrc->nx>1)&&(raysrc->nz>1))
			{
				raysrc->single_ray_area=(raysrc->dx_padding+raysrc->dx)*(raysrc->dz_padding+raysrc->dz);
			}else
			if ((raysrc->nx>1)&&(raysrc->ny>1))
			{
				raysrc->single_ray_area=(raysrc->dx_padding+raysrc->dx)*(raysrc->dy_padding+raysrc->dy);
			}else
			if ((raysrc->nz>1)&&(raysrc->ny>1))
			{
				raysrc->single_ray_area=(raysrc->dz_padding+raysrc->dz)*(raysrc->dy_padding+raysrc->dy);
			}else
			if ((raysrc->nz==1)&&(raysrc->nx==1)&&(raysrc->ny==1))
			{
				raysrc->single_ray_area=1.0;
			}

			raysrc->rotate_x=lightsrc->rotate_x;
			raysrc->rotate_y=lightsrc->rotate_y;

			raysrc->epi_layer=-1;
			raysrc->emission_source=-1;
			raysrc->light=i;


		}
	}

	return 0;

}


