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


/** @file detector_dump_bins.c
	@brief Ray tracing for the optical model, this should really be split out into it's own library.
*/


void detector_dump_bins(struct simulation *sim,struct ray_engine *in)
{
	struct dat_file buf;

	dat_file_init(&buf);

	if (buffer_set_file_name(sim,NULL,&buf,"escape_bins_raw.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.x_mul=1.0;
		buf.y_mul=1e9;
		strcpy(buf.title,"Angle vs. Wavelength");
		strcpy(buf.type,"heat");
		strcpy(buf.x_label,"Wavelength");
		strcpy(buf.y_label,"Angle");
		strcpy(buf.data_label,"Intensity");
		strcpy(buf.x_units,"nm");
		strcpy(buf.y_units,"Degrees");
		strcpy(buf.data_units,"Counts");
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.x_len=in->ray_wavelength_points;
		buf.y_len=in->escape_bins;
		buf.z_len=1;

		dat_file_add_2d_double(sim,&buf, in->angle, in->lam, in->ang_escape, in->ray_wavelength_points, in->escape_bins);

		dat_file_dump_path(sim,"",NULL,&buf);
		dat_file_free(&buf);
	}

}

