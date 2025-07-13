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
#include <device_fun.h>
#include <object_fun.h>
#include <mesh.h>

/** @file build.c
	@brief Set up the simulation window for the ray tracer
*/


void ray_worker_init(struct simulation *sim,struct ray_worker *worker)
{
	worker->rays=NULL;
	worker->nrays=0;
	worker->nray_max=-1;
	worker->top_of_done_rays=-1;
	worker->l=-1;
	worker->worker_n=-1;
	worker->rays_shot=0;
	worker->raysrc=NULL;

	worker->ray_min_intensity=1e-6;

	worker->total_input_magnitude=0.0;
	worker->total_detected_magnitude=0.0;
}

void ray_worker_malloc(struct simulation *sim,struct ray_worker *worker)
{
	worker->nray_max=1000;
	worker->top_of_done_rays=0;
	worker->nrays=0;
	malloc_1d((void **)(&(worker->rays)),worker->nray_max, sizeof(struct ray));
}

void ray_worker_free(struct simulation *sim,struct ray_worker *worker)
{
	free_1d((void **)(&(worker->rays)));
	ray_worker_init(sim,worker);
}



