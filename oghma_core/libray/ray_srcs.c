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

int ray_src_free_emitters(struct simulation *sim,struct device *dev)
{
	struct ray_engine *eng=&(dev->eng);
	free_1d((void **)(&(eng->ray_srcs)));
	eng->n_ray_srcs=0;
	return 0;
}

int ray_src_clear_emitters(struct ray_engine *eng)
{
	int s;
	struct ray_src *src;
	for (s=0;s<eng->n_ray_srcs;s++)
	{
		src=&eng->ray_srcs[s];
		ray_src_free(src);
	}

	eng->n_ray_srcs=0;
	return 0;
}

struct ray_src *ray_src_add_emitter(struct ray_engine *eng)
{
	struct ray_src *ret;
	if (eng->n_ray_srcs_max==0)
	{
		eng->n_ray_srcs_max=8;
		malloc_1d((void **)(&(eng->ray_srcs)),eng->n_ray_srcs_max, sizeof(struct ray_src));
	}

	if (eng->n_ray_srcs_max<=eng->n_ray_srcs)
	{
		eng->n_ray_srcs_max*=2;
		eng->ray_srcs=realloc((void *)eng->ray_srcs,eng->n_ray_srcs_max*sizeof(struct ray_src));
	}

	ret=&eng->ray_srcs[eng->n_ray_srcs];
	ray_src_init(ret);
	ray_src_malloc(ret,eng);
	eng->n_ray_srcs++;
	return ret;
}
