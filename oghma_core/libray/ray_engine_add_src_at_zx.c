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

int ray_engine_add_src_at_zx(struct simulation *sim,struct device *dev, int layer)
{
	int z;
	int x;
	int y;
	double Rmin;
	double Rmax;
	double Photons_gen;
	double Photons_points=0;
	double Photons_y=0.0;
	double Photons_tot=0.0;
	int threshold=FALSE;
	double Photons_y_last=0.0;
	double Photons_gen_last=0.0;
	double Photons_x_last=0.0;
	struct shape *s;
	struct ray_engine *eng=&(dev->eng);
	struct newton_state *ns=dev->ns;
	struct dimensions *dim=&ns->dim;
	struct ray_src *raysrc;
	struct epitaxy *epi=&(dev->my_epitaxy);
	struct epi_layer *epi_layer;
	int y_start=-1;
	struct simmode *sm=&(dev->simmode);

	if (sm->drift_diffision_simulations_enabled==FALSE)
	{
		return -1;
	}

	min_max_zxy_double(&Rmin, &Rmax, dim, ns->Rnet);
	//printf("%le %le\n",Rmin, Rmax);
	for (z=0;z<dim->zlen;z++)
	{
		Photons_y_last=-1.0;
		Photons_gen_last=-1.0;
		Photons_x_last=-1.0;

		for (x=0;x<dim->xlen;x++)
		{
			Photons_points=0;
			Photons_y=0.0;
			Photons_tot=0.0;
			threshold=FALSE;
			epi_layer=NULL;
			for (y=0;y<dim->ylen;y++)
			{
				s=dev->obj_zxy[z][x][y]->s;
				//printf("%d %le\n",y,ns->Rnet[z][x][y]);
				if (layer==s->epi_index)
				{
					if (y_start==-1)
					{
						y_start=y;
					}

					if (ns->Rnet[z][x][y]>1e10)
					{
						threshold=TRUE;
					}
					Photons_gen=ns->Rnet[z][x][y]/Rmax;
					Photons_tot+=Photons_gen;
					Photons_y+=Photons_gen*dim->y[y];
					Photons_points+=1.0;
					epi_layer=&(epi->layer[s->epi_index]);
				}
			}
			if (Photons_tot>0.0)
			{
				Photons_y=Photons_y/Photons_tot;
				Photons_gen=Photons_tot/Photons_points;
			}

			//printf("threshold %d %le %le\n",threshold,Photons_y,Photons_gen);

			if ((Photons_tot>0.01)&&(threshold==TRUE))
			{

				if (epi_layer!=NULL)
				{
					if (epi_layer->ray_super_sample_x==TRUE)
					{
						if (Photons_y_last!=-1.0)
						{
							double xpos=0.0;
							double dx=1.0/((double)epi_layer->ray_super_sample_x_points);
							while (xpos<1.0)
							{
								raysrc=ray_src_add_emitter(eng);
								raysrc->mesh_x=x;
								raysrc->mesh_y=y_start;
								raysrc->mesh_z=z;
								ray_src_layer_to_raysrc(raysrc, &(epi->layer[layer]));

								raysrc->mag=(Photons_gen*(1.0-xpos)+Photons_gen_last*xpos);
								raysrc->x=(dim->x[x]*(1.0-xpos)+Photons_x_last*xpos);
								raysrc->y=(Photons_y*(1.0-xpos)+Photons_y_last*xpos);
								raysrc->z=dim->z[z];
								xpos+=dx;
							}
						}
					}else
					{
						raysrc=ray_src_add_emitter(eng);
						ray_src_layer_to_raysrc(raysrc, &(epi->layer[layer]));
						raysrc->mesh_x=x;
						raysrc->mesh_y=y;
						raysrc->mesh_z=z;
						raysrc->mag=Photons_gen;
						raysrc->x=dim->x[x];
						raysrc->y=Photons_y;
						raysrc->z=dim->z[z];
					}
				}

				Photons_y_last=Photons_y;
				Photons_gen_last=Photons_gen;
				Photons_x_last=dim->x[x];

			}else
			{
				Photons_y_last=-1.0;
			}					
		}
	}

	return 0;

}


