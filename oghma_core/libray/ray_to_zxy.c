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
#include <oghma_const.h>
#include <math.h>
#include <stdlib.h>
#include <cal_path.h>
#include <log.h>
#include <ray_fun.h>
#include <util.h>
#include <detector.h>

/** @file ray_to_zxy.c
	@brief Ray tracing for the optical model, this should really be split out into it's own library.
*/


int ray_to_zxy(struct simulation *sim,struct device *dev,struct ray_engine *in,struct ray *my_ray,double alpha,struct ray_worker *worker)
{
	if (in->abs_profile==NULL)
	{
		return -1;
	}

	int x=-1;
	int y=-1;
	int z=-1;

	int x1=-1;
	int y1=-1;
	int z1=-1;

	int i;
	double dx;
	double dy;
	double dz;
	double min_step;
	int steps;
	double len;
	struct vec dxyz;
	struct vec pos;
	double tot_len=0.0;
	//double volume_beam=0.0;
	//double volume_box=0.0;
	//double volume_ratio=0.0;
	double Photons_m3_lost_in_beam=0.0;
	double beam_start_power=0.0;
	struct dimensions *dim=&(dev->dim_optical);
	struct ray_src *raysrc=worker->raysrc;
	struct light_src *lightsrc=NULL;
	int l=worker->l;
	vec_cpy(&dxyz,&(my_ray->xy_end));
	vec_sub(&dxyz,&(my_ray->xy));

	len=vec_fabs(&dxyz);
	dx=(dev->optical_mesh_data.meshdata_x.stop-dev->optical_mesh_data.meshdata_x.start)/(double)dim->xlen;
	dy=(dev->optical_mesh_data.meshdata_y.stop-dev->optical_mesh_data.meshdata_y.start)/(double)dim->ylen;
	dz=(dev->optical_mesh_data.meshdata_z.stop-dev->optical_mesh_data.meshdata_z.start)/(double)dim->zlen;

	min_step=dx;

	//vec_print(&w->min);
	//vec_print(&w->max);
	//getchar();
	//dim_dump(dim);
	//getchar();

	if (dy<min_step)
	{
		min_step=dy;
	}
	if (dz<min_step)
	{
		min_step=dz;
	}

	steps=len/min_step;

	vec_div(&dxyz,(double)steps);
	vec_cpy(&pos,&(my_ray->xy));

	double mag=my_ray->mag0;

	if (raysrc->light!=-1)
	{
		lightsrc=&(dev->lights.light_sources[raysrc->light]);
		beam_start_power=lightsrc->spectra_tot_photons.data[l]*in->Psun*dim->dl;	//Wm-2
		mag*=beam_start_power;
	}

	//printf("%le %le\n",beam_start_power,mag);
	//getchar();

	for (i=0;i<steps;i++)
	{
		vec_add(&pos,&dxyz);
		tot_len+=min_step;
		x=(pos.x-dev->optical_mesh_data.meshdata_x.start)/dx;
		y=(pos.y-dev->optical_mesh_data.meshdata_y.start)/dy;
		z=(pos.z-dev->optical_mesh_data.meshdata_z.start)/dz;

		if ((x!=x1)||(y!=y1)||(z!=z1))
		{
			if ((x<dim->xlen)&&(y<dim->ylen)&&(z<dim->zlen))
			{
				if ((x>=0)&&(y>=0)&&(z>=0))
				{
					//volume_box=dx*dz*dy;
					//volume_beam=raysrc->single_ray_area*tot_len;
					//volume_ratio=(volume_box)/volume_beam;
					Photons_m3_lost_in_beam=mag*(exp(-alpha*0.0)-exp(-alpha*tot_len))/tot_len;
					in->abs_profile[z][x][y]+=Photons_m3_lost_in_beam;
					
					
					mag=mag*exp(-alpha*tot_len);				
					//printf("%le ",mag);
					//vec_print(&pos);
					x1=x;
					y1=y;
					z1=z;
					tot_len=0.0;
				}
			}
		}


	}

	return 0;
}




