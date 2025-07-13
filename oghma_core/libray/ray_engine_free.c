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
#include <util.h>
#include <unistd.h>
#include <device_fun.h>
#include <g_io.h>
#include <math_xy.h>
#include <memory.h>
#include <object_fun.h>

/** @file ray_engine_free.c
	@brief Ray tracing for the optical model, this should really be split out into it's own library.
*/

void ray_engine_free(struct simulation *sim,struct device *dev,struct ray_engine *eng)
{
	int i=0;
	struct world *w=&(dev->w);

	free_1d((void **)(&(eng->lam)));


	if (eng->ang_escape!=NULL)
	{
		for (i=0;i<eng->ray_wavelength_points;i++)
		{
			free(eng->ang_escape[i]);
		}

	}

	free_1d((void **)(&(eng->ang_escape)));
	free_1d((void **)(&(eng->angle)));

	for (i=0;i<w->objects;i++)
	{
		object_nalpha_free(&(w->obj[i]));
	}

	free_zxy_double(&(dev->dim_optical), &(eng->abs_profile));

	math_xy_free(&eng->abs_objects);
	math_xy_free(&eng->tot_ray_power);

	ray_engine_init(eng);
}
