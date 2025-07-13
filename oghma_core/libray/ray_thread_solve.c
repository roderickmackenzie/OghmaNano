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
#include <gui_hooks.h>
#include <util.h>
#include <memory.h>
#include <epitaxy_struct.h>
#include <epitaxy.h>
#include <dump.h>
#include <device_fun.h>
#include <clock.h>
#include <g_io.h>
#include <detector.h>
#include <server.h>

/** @file ray_thread_solve.c
	@brief This will call the ray tracer for the standard case.
*/

THREAD_FUNCTION ray_thread_solve(void * in)
{
	char one[200];
	char send_data[OGHMA_PATH_MAX+10];
	double input_mag=0.0;
	struct ray_worker worker;
	struct job *j=(struct job *)in;
	struct simulation *sim=(struct simulation *)j->sim;
	struct device *dev=(struct device *)j->data0;
	struct ray_engine *eng=&(dev->eng);
	int l=j->data_int0;
	struct ray_src *raysrc=NULL;

	ray_worker_init(sim,&worker);
	ray_worker_malloc(sim,&worker);

	worker.l=l;
	worker.raysrc=(struct ray_src *)j->data1;
	worker.ray_min_intensity=eng->ray_min_intensity;

	raysrc=worker.raysrc;

	if (raysrc->light!=-1)				//It's a free object
	{
			ray_solve(sim,dev,1.0, &worker);
	}else
	if (raysrc->epi_layer!=-1)			//it's an epitaxy layer
	{
		input_mag=dev->my_epitaxy.layer[raysrc->epi_layer].pl_spectrum.data[l];
		ray_solve(sim,dev,raysrc->mag*input_mag, &worker);
		//printf("%le\n",100.0*worker.total_detected_magnitude/worker.total_input_magnitude);
		raysrc->emitted[l]=worker.total_input_magnitude;
		raysrc->detected[l]=worker.total_detected_magnitude;


		ray_cal_escape_angle(eng,&worker);
	}

	ray_dump_shapshot(sim,dev, eng ,&worker, raysrc->name);
	ray_reset(&worker);
	j->data0=NULL;
	j->data1=NULL;
	j->data2=NULL;

	ray_worker_free(sim,&worker);
	sprintf(send_data,"text:%s",j->name);
	gui_send_data(sim,gui_sub,send_data);
	sprintf(one,"*");
	waveprint(sim,one,eng->lam[l]);
	//printf("%d %d\n",j->w->pipefd[0],j->w->pipefd[1]);
	server2_job_finished(sim,j);
	return 0;
}



