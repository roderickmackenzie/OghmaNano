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

int ray_check_if_needed(struct simulation *sim,struct device *dev)
{
	int l;
	int i;
	struct light_src *lightsrc;
	struct epi_layer *layer;
	struct ray_engine *eng=&(dev->eng);
	struct epitaxy* epitaxy = &(dev->my_epitaxy);
	struct json_obj *json_outcoupling;
	char outcoupling_mode[100];
	struct simmode *sm=&(dev->simmode);


	eng->enabled=FALSE;

	//If we are running an fdtd simulation then we are not ray tracing.
	if (strcmp_end(sm->optical_solver,"ray_trace")==0)
	{
		eng->enabled=TRUE;
		return 0;
	}

	if (strcmp_end(sm->optical_solver,"fdtd")==0)
	{
		eng->enabled=FALSE;
		return -1;
	}

	json_outcoupling=json_obj_find_by_path(&(dev->config.obj), "optical.outcoupling");
	json_get_string(sim, json_outcoupling, outcoupling_mode,"outcoupling_model",TRUE);

	if (strcmp(outcoupling_mode,"ray_trace")==0)
	{
		for (l=0;l<epitaxy->layers;l++)
		{
			layer=&(epitaxy->layer[l]);

			if (layer->pl_enabled==TRUE)
			{
				eng->enabled=TRUE;
				return 0;
			}
		}
	}

	for (i=0;i<dev->lights.nlight_sources;i++)
	{
		lightsrc=&(dev->lights.light_sources[i]);
		if (strcmp(lightsrc->illuminate_from,"xyz")==0)
		{
			eng->enabled=TRUE;
			return 0;
		}
	}

	return 0;
}

int ray_src_init(struct ray_src *raysrc)
{
	raysrc->x=0.0;
	raysrc->y=0.0;
	raysrc->z=0.0;

	raysrc->theta_steps=0;
	raysrc->theta_start=0.0;
	raysrc->theta_stop=0.0;

	raysrc->phi_steps=0;
	raysrc->phi_start=0.0;
	raysrc->phi_stop=0.0;

	raysrc->dx_padding=0.0;
	raysrc->dy_padding=0.0;
	raysrc->dz_padding=0.0;

	raysrc->dx=0.0;
	raysrc->dy=0.0;
	raysrc->dz=0.0;

	raysrc->nx=0;
	raysrc->ny=0;
	raysrc->nz=0;

	raysrc->single_ray_area=0.0;

	raysrc->rotate_x=0.0;
	raysrc->rotate_y=0.0;

	raysrc->epi_layer=0;
	raysrc->light=0;
	raysrc->emission_source=0;
	raysrc->mag=0.0;
	raysrc->mesh_x=-1;
	raysrc->mesh_y=-1;
	raysrc->mesh_z=-1;

	raysrc->emitted=NULL;
	raysrc->detected=NULL;

	strcpy(raysrc->name,"");
	return 0;
}

int ray_src_malloc(struct ray_src *src,struct ray_engine *eng)
{
	malloc_1d((void **)(&(src->emitted)),eng->ray_wavelength_points, sizeof(double));
	malloc_1d((void **)(&(src->detected)),eng->ray_wavelength_points, sizeof(double));
	return 0;
}

int ray_src_free(struct ray_src *src)
{
	free_1d((void **)(&src->emitted));
	free_1d((void **)(&src->detected));
	return 0;
}

int ray_src_layer_to_raysrc(struct ray_src *raysrc, struct epi_layer *layer)
{
	raysrc->theta_steps=layer->theta_steps;
	raysrc->theta_start=layer->theta_start;
	raysrc->theta_stop=layer->theta_stop;

	raysrc->phi_steps=layer->phi_steps;
	raysrc->phi_start=layer->phi_start;
	raysrc->phi_stop=layer->phi_stop;

	raysrc->dx_padding=layer->dx_padding;
	raysrc->dy_padding=layer->dy_padding;
	raysrc->dz_padding=layer->dz_padding;

	raysrc->nx=layer->nx;
	raysrc->ny=layer->ny;
	raysrc->nz=layer->nz;

	raysrc->rotate_x=0.0;
	raysrc->rotate_y=0.0;

	raysrc->emission_source=layer->emission_source;
	raysrc->epi_layer=layer->layer_number;
	raysrc->light=-1;
	return 0;
}





