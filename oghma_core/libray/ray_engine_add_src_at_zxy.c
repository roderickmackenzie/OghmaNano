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

int ray_engine_add_src_at_zxy(struct simulation *sim,struct device *dev, int layer, int from_recombination)
{
	int z;
	int x;
	int y;
	int add_src;
	double Rmin;
	double Rmax;
	double Photons;
	struct shape *s;
	struct ray_engine *eng=&(dev->eng);
	struct newton_state *ns=dev->ns;
	struct dimensions *dim=&ns->dim;
	struct ray_src *raysrc;
	struct epitaxy *epi=&(dev->my_epitaxy);
	struct simmode *sm=&(dev->simmode);

	if (sm->drift_diffision_simulations_enabled==FALSE)
	{
		return -1;
	}

	if (from_recombination==TRUE)
	{
		min_max_zxy_double(&Rmin, &Rmax, dim, ns->Rnet);
	}
	//printf("ROD\n");
	//getchar();
	for (z=0;z<dim->zlen;z++)
	{
		for (x=0;x<dim->xlen;x++)
		{
			for (y=0;y<dim->ylen;y++)
			{
				s=dev->obj_zxy[z][x][y]->s;

				if (s->epi_index==layer)
				{
					add_src=TRUE;
					if (from_recombination==TRUE)
					{
						Photons=ns->Rnet[z][x][y]/Rmax;
						if ((Photons<0.01)&&(ns->Rnet[z][x][y]<1e10))
						{
							add_src=FALSE;
						}
					}else
					{
						Photons=1.0;
					}

					if (add_src==TRUE)
					{
						raysrc=ray_src_add_emitter(eng);
						ray_src_layer_to_raysrc(raysrc, &(epi->layer[layer]));
						raysrc->mesh_x=x;
						raysrc->mesh_y=y;
						raysrc->mesh_z=z;
						raysrc->mag=Photons;
						raysrc->x=dim->x[x];
						raysrc->y=dev->device_start.y+dim->y[y];
						raysrc->z=dim->z[z];
						sprintf(raysrc->name,"%d_%d_%d",z,x,y);
					}

				}
			}
		}
	}

	return 0;

}


