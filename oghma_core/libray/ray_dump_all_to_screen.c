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
#include <dat_file.h>
#include <string.h>
#include <color.h>
#include <dump.h>
#include <util.h>
#include <detector.h>

/** @file ray_dump_all_to_screen.c
	@brief Ray tracing for the optical model, this should really be split out into it's own library.
*/



void ray_dump_all_to_screen(struct simulation *sim,struct device *dev,struct ray_worker *worker)
{
	int i=0;

	printf_log(sim,"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
	struct object *obj;
	struct world *my_world=&(dev->w);

	printf_log(sim,"start:\n");
	ray_src_dump(sim,dev);

	printf_log(sim,"triangles:\n");
	int o=0;

	//int n=0;
	for (o=0;o<my_world->objects;o++)
	{
		obj=&(my_world->obj[o]);
		printf_log(sim,"object: %s\n",obj->name);
		for (i=0;i<obj->tri.len;i++)
		{
			printf_log(sim," (%.4le,%.4le,%.4le) %d",obj->tri.data[i].xy0.x,obj->tri.data[i].xy0.y,obj->tri.data[i].xy0.z,obj->tri.data[i].object_type);
			printf_log(sim," (%.4le,%.4le,%.4le) %d",obj->tri.data[i].xy1.x,obj->tri.data[i].xy1.y,obj->tri.data[i].xy1.z,obj->tri.data[i].object_type);
			printf_log(sim," (%.4le,%.4le,%.4le) %d\n",obj->tri.data[i].xy2.x,obj->tri.data[i].xy2.y,obj->tri.data[i].xy2.z,obj->tri.data[i].object_type);


	//in->tri[i].xy1.x,in->tri[i].xy1.y,in->tri[i].edge);
		}
	}

	printf_log(sim,"rays x,y,x_vec,y_vec:\n");

	for (i=0;i<worker->nrays;i++)
	{
		printf_log(sim,"%d (%le,%le,%le) (%le,%le,%le) (%lf,%lf,%lf) mag0=%le mag1=%le state=%d\n",
				worker->rays[i].state,
				worker->rays[i].xy.x		,	worker->rays[i].xy.y	,	worker->rays[i].xy.z,
				worker->rays[i].xy_end.x	,	worker->rays[i].xy_end.y,	worker->rays[i].xy_end.z,
				worker->rays[i].dir.x		,	worker->rays[i].dir.y	,	worker->rays[i].dir.z,
				worker->rays[i].mag0, worker->rays[i].mag1,
				worker->rays[i].state);

	}

	printf_log(sim,"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");

}

