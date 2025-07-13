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
#include <json.h>
#include <util.h>
#include <triangles.h>

/** @file ray_config.c
	@brief Read the config file for the ray tracer
*/

void ray_read_config(struct simulation *sim,struct ray_engine *eng,struct world *w,struct json_obj *json_config)
{
	struct json_obj *json_ray;
	struct json_obj *json_light_sources;

	if (json_config==NULL)
	{
		ewe(sim,"json_config null\n");
	}

	json_ray=json_obj_find_by_path(json_config, "sims.ray.segment0.config");

	if (json_ray==NULL)
	{
		ewe(sim,"Object config not found\n");
	}

	json_get_english(sim, json_ray,&(eng->ray_dump_abs_profile),"ray_dump_abs_profile",TRUE);
	json_get_int(sim, json_ray, &(eng->escape_bins),"ray_escape_bins",TRUE);

	json_get_english(sim, json_ray, &(eng->ray_auto_run),"ray_auto_run",TRUE);
	json_get_int(sim, json_ray, &(eng->run_each_n_steps),"ray_auto_run_n",TRUE);

	json_get_int(sim, json_ray, &(eng->dump_verbosity),"dump_verbosity",TRUE);
	json_get_double(sim, json_ray, &(eng->ray_min_intensity),"ray_min_intensity",TRUE);
	json_get_int(sim, json_ray, &(eng->ray_max_bounce),"ray_max_bounce",TRUE);
	json_get_english(sim, json_ray, &(eng->ray_sim_reflected),"ray_sim_reflected",TRUE);
	json_get_english(sim, json_ray, &(eng->ray_sim_transmitted),"ray_sim_transmitted",TRUE);

	json_light_sources=json_obj_find_by_path(json_config, "optical.light_sources");
	json_get_double(sim, json_light_sources, &(eng->Psun),"Psun",TRUE);

}


