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

/** @file ray_dump_all_rays.c
	@brief Ray tracing for the optical model, this should really be split out into it's own library.
*/


void ray_dump_all_rays(struct simulation *sim,char *dir_name,struct ray_engine *in,struct device *dev,struct ray_worker *worker,char *file_name)
{
	int r;
	int g;
	int b;

	struct dat_file buf;
	dat_file_init(&buf);
	if (buffer_set_file_name(sim,dev,&buf,file_name)==0)
	{

		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.x_mul=1e9;
		strcpy(buf.title,"Ray trace file");
		strcpy(buf.type,"rays");
		strcpy(buf.y_label,"Position");
		strcpy(buf.x_label,"Position");
		strcpy(buf.data_label,"Position");

		strcpy(buf.y_units,"m");
		strcpy(buf.x_units,"m");
		strcpy(buf.data_units,"m");
		strcpy(buf.cols,"rays");
		wavelength_to_rgb(&r,&g,&b,in->lam[worker->l]);
		buf.rgb.r=r;
		buf.rgb.g=g;
		buf.rgb.b=b;
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.x_len=1;
		buf.y_len=worker->nrays;
		buf.z_len=1;
		buf.bin=dev->dump_binary;
		buf.part=TRUE;
		buffer_add_json(&buf);

		dat_file_add_rays(sim,&buf,worker);

		dat_file_dump_path(sim,dir_name,NULL,&buf);
		dat_file_free(&buf);
	}

}
