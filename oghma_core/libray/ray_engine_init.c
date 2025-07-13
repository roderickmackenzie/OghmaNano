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
/** @file ray_engine_init.c
	@brief Ray tracing for the optical model, this should really be split out into it's own library.
*/

void ray_engine_init(struct ray_engine *in)
{
	in->enabled=FALSE;
	in->n_ray_srcs=0;
	in->n_ray_srcs_max=0;
	in->ray_srcs=NULL;
	in->ray_wavelength_points=-1;

	in->y_escape_level=-1.0;
	in->angle=NULL;
	in->ang_escape=NULL;
	in->lam=NULL;
	in->tot_rays=0;
	in->start_time=0.0;

	//run control
	in->ray_auto_run=FALSE;
	in->run_each_n_steps=1;
	in->dump_verbosity=-1;
	strcpy(in->ray_snapshot_dir,"");
	in->disable_error_on_no_light_srcs=FALSE;


	//Abs profile tracker
	in->ray_dump_abs_profile=FALSE;
	in->abs_profile=NULL;
	math_xy_init(&in->abs_objects);
	math_xy_init(&in->tot_ray_power);

	//From json config
	in->escape_bins=0;
	in->ray_min_intensity=1e-6;
	in->ray_max_bounce=7;
	in->ray_sim_reflected=TRUE;
	in->ray_sim_transmitted=TRUE;

	in->call_count=-1;
	in->Psun=-1.0;
}

