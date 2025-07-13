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

/** @file ray.c
	@brief Ray tracing for the optical model, this should really be split out into it's own library.
*/


void dump_ray_to_file(struct simulation *sim,struct ray_engine *in,struct ray *my_ray,struct device *dev)
{

	int r;
	int g;
	int b;

	char temp[200];
	struct world *w=&(dev->w);

	struct dat_file buf;
	dat_file_init(&buf);

	dat_file_malloc(&buf);
	buf.y_mul=1.0;
	buf.x_mul=1e9;
	strcpy(buf.title,"Ray trace file");
	strcpy(buf.type,"poly");
	strcpy(buf.y_label,"Position");
	strcpy(buf.x_label,"Position");
	strcpy(buf.data_label,"Position");

	strcpy(buf.y_units,"m");
	strcpy(buf.x_units,"m");
	strcpy(buf.data_units,"m");

	wavelength_to_rgb(&r,&g,&b,600e-9);
	buf.rgb.r=r;
	buf.rgb.g=g;
	buf.rgb.b=b;

	buf.logscale_x=0;
	buf.logscale_y=0;
	buf.x_len=1;
	buf.y_len=w->triangles;
	buf.z_len=1;
	buffer_add_json(&buf);


	struct vec v;

	vec_cpy(&v,&(my_ray->xy_end));
	vec_sub(&v,&(my_ray->xy));
	vec_mul(&v,0.25);
	vec_add(&v,&(my_ray->xy));

	sprintf(temp,"%le %le %le\n",
								my_ray->xy.z,		my_ray->xy.x,		my_ray->xy.y);
	buffer_add_string(&buf,temp);

	sprintf(temp,"%le %le %le\n",
								my_ray->xy_end.z,	my_ray->xy_end.x,	my_ray->xy_end.y);
	buffer_add_string(&buf,temp);

	sprintf(temp,"%le %le %le\n",
								v.z,	v.x,	v.y);
	buffer_add_string(&buf,temp);


	buffer_add_string(&buf,"\n");


	sprintf(temp,"ray_%d.dat",my_ray->uid);
	printf("dumped %s \n",temp);
	dat_file_dump_path(sim,"",temp,&buf);
	dat_file_free(&buf);

}

void ray_dump_triangle(struct simulation *sim,struct device *dev,struct ray_engine *in,struct triangle *tri)
{

	char temp[200];
	struct world *my_world=&(dev->w);
	//printf("file dump\n");
	struct dat_file buf;
	dat_file_init(&buf);

	dat_file_malloc(&buf);
	buf.y_mul=1.0;
	buf.x_mul=1e9;
	strcpy(buf.title,"Ray trace triange file");
	strcpy(buf.type,"poly");
	strcpy(buf.y_label,"Position");
	strcpy(buf.x_label,"Position");
	strcpy(buf.data_label,"Position");

	strcpy(buf.y_units,"m");
	strcpy(buf.x_units,"m");
	strcpy(buf.data_units,"m");
	buf.logscale_x=0;
	buf.logscale_y=0;
	buf.x_len=1;
	buf.y_len=1;
	buf.z_len=1;
	buffer_add_json(&buf);

	sprintf(temp,"#name %s\n",my_world->obj[tri->object_uid].name);
	buffer_add_string(&buf,temp);


	sprintf(temp,"%le %le %le\n",tri->xy0.z,tri->xy0.x,tri->xy0.y);
	buffer_add_string(&buf,temp);

	sprintf(temp,"%le %le %le\n",tri->xy1.z,tri->xy1.x,tri->xy1.y);
	buffer_add_string(&buf,temp);

	sprintf(temp,"%le %le %le\n",tri->xy2.z,tri->xy2.x,tri->xy2.y);
	buffer_add_string(&buf,temp);

	sprintf(temp,"%le %le %le\n",tri->xy0.z,tri->xy0.x,tri->xy0.y);
	buffer_add_string(&buf,temp);

	sprintf(temp,"\n");
	buffer_add_string(&buf,temp);

	sprintf(temp,"\n");
	buffer_add_string(&buf,temp);


	//sprintf(temp,"triangle_%d.dat",tri->tri_uid);
	sprintf(temp,"triangle0.dat");
	dat_file_dump_path(sim,"",temp,&buf);
	dat_file_free(&buf);
}
