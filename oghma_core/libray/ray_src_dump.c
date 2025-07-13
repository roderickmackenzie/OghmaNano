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

void ray_src_dump(struct simulation *sim,struct device *dev)
{
	int i;
	struct ray_src *src;
	struct ray_engine *eng=&(dev->eng);
	printf_log(sim,"%-14s%-14s%-14s","x","y","z");
	printf_log(sim,"%-14s%-14s%-14s","theta_steps","theta_start","theta_stop");
	printf_log(sim,"%-14s%-14s%-14s","phi_steps","phi_start","phi_stop");
	printf_log(sim,"\n");

	for (i=0;i<eng->n_ray_srcs;i++)
	{
		src=&(eng->ray_srcs[i]);
	
		printf_log(sim,"%-14le%-14le%-14le",src->x,src->y,src->z);
		printf_log(sim,"%-14d%-14le%-14le",src->theta_steps, src->theta_start,src->theta_stop);
		printf_log(sim,"%-14d%-14le%-14le",src->phi_steps, src->phi_start,src->phi_stop);
		printf_log(sim,"\n");
	}
}
