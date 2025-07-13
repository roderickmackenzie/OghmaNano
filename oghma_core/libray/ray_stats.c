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

/** @file ray_stats.c
	@brief Perfrom stats on the ray tracing image
*/

void ray_escape_angle_reset(struct ray_engine *in,int l)
{
	int i;

	for (i=0;i<in->escape_bins;i++)
	{
		in->ang_escape[l][i]=0.0;
	}
}

void ray_escape_angle_norm(struct ray_engine *in)
{
	int i;
	int l;
	double max=0.0;
	for (l=0;l<in->ray_wavelength_points;l++)
	{
		for (i=0;i<in->escape_bins;i++)
		{
			if (in->ang_escape[l][i]>max)
			{
				max=in->ang_escape[l][i];
			}
		}
	}

	for (l=0;l<in->ray_wavelength_points;l++)
	{
		for (i=0;i<in->escape_bins;i++)
		{
			in->ang_escape[l][i]/=max;
		}
	}

}

double ray_cal_escape_angle(struct ray_engine *in, struct ray_worker *worker)
{
	int i;
	//double mag=0.0;
	double tot=0.0;
	int l=worker->l;
	for (i=0;i<worker->nrays;i++)
	{
		if (worker->rays[i].state==DONE)
		{
			if (worker->rays[i].xy_end.y<in->y_escape_level)
			{
				//mag=in->rays[i].mag;
				double raw_ang=(360.0/(2*3.14159))*atan(fabs(worker->rays[i].dir.y)/worker->rays[i].dir.x);
				if (raw_ang<0.0)
				{
					raw_ang=raw_ang+180.0;
				}
				double ang=raw_ang;
				int bin=(int)((ang/180.0)*(double)in->escape_bins);
				in->ang_escape[l][bin]+=worker->rays[i].mag1;
				tot=tot+worker->rays[i].mag1;
				//printf("%lf\n",worker->rays[i].mag1);
				//getchar();
			}
		}

	}

return tot;
}

