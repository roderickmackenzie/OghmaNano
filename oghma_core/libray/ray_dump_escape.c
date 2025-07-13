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


void dump_ang_escape(struct simulation *sim,struct ray_engine *in)
{
	struct dat_file buf;

	if (in->dump_verbosity==dump_nothing)
	{
		return;
	}

	dat_file_init(&buf);

	if (buffer_set_file_name(sim,NULL,&buf,"ang_escape.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.x_mul=1e9;
		strcpy(buf.title,"Photon escape probability");
		strcpy(buf.type,"heat");
		strcpy(buf.y_label,"Wavelength");
		strcpy(buf.x_label,"Angle");
		strcpy(buf.data_label,"Probability");

		strcpy(buf.y_units,"nm");
		strcpy(buf.x_units,"Degrees");
		strcpy(buf.data_units,"a.u.");

		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.x_len=in->ray_wavelength_points;
		buf.y_len=in->escape_bins;
		buf.z_len=1;
		dat_file_add_2d_double(sim,&buf, in->lam, in->angle, in->ang_escape, in->ray_wavelength_points, in->escape_bins);
		dat_file_dump_path(sim,"",NULL,&buf);
		dat_file_free(&buf);
	}
}

void dump_ang_escape_as_rgb(struct simulation *sim,struct ray_engine *in)
{
	double X;
	double Y;
	double Z;
	int R;
	int G;
	int B;

	int x;
	int y;
	char temp[200];
	struct dat_file buf_rgb;

	struct dat_file buf_X;
	struct dat_file buf_Y;
	struct dat_file buf_Z;

	struct dat_file buf_x;
	struct dat_file buf_y;
	struct dat_file buf_z;

	struct math_xy spec_out;

	if (in->dump_verbosity==dump_nothing)
	{
		return;
	}

	dat_file_init(&buf_rgb);

	dat_file_init(&buf_X);
	dat_file_init(&buf_Y);
	dat_file_init(&buf_Z);

	dat_file_init(&buf_x);
	dat_file_init(&buf_y);
	dat_file_init(&buf_z);

	dat_file_malloc(&buf_rgb);
	buf_rgb.y_mul=1.0;
	buf_rgb.x_mul=1e9;
	strcpy(buf_rgb.title,"viewing angle - RGB color");
	strcpy(buf_rgb.type,"yrgb");
	strcpy(buf_rgb.y_label,"Angle");
	strcpy(buf_rgb.data_label,"Color");
	strcpy(buf_rgb.y_units,"Degrees");
	strcpy(buf_rgb.data_units,"a.u.");
	strcpy(buf_rgb.icon,"color");
	strcpy(buf_rgb.cols,"yrgb");
	buf_rgb.x_len=1;
	buf_rgb.y_len=in->escape_bins;
	buf_rgb.z_len=1;
	buffer_add_json(&buf_rgb);


	dat_file_malloc(&buf_X);
	buf_X.y_mul=1.0;
	buf_X.data_mul=1.0;
	strcpy(buf_X.title,"CIE 1931 color space - X");
	strcpy(buf_X.type,"xy");
	strcpy(buf_X.y_label,"Angle");
	strcpy(buf_X.data_label,"Color");
	strcpy(buf_X.y_units,"Degrees");
	strcpy(buf_X.data_units,"a.u.");
	strcpy(buf_X.icon,"color");
	strcpy(buf_X.cols,"yd");
	buf_X.x_len=1;
	buf_X.y_len=in->escape_bins;
	buf_X.z_len=1;
	buffer_add_json(&buf_X);

	dat_file_malloc(&buf_Y);
	buf_Y.y_mul=1.0;
	buf_Y.data_mul=1.0;
	strcpy(buf_Y.title,"CIE 1931 color space - Y");
	strcpy(buf_Y.type,"xy");
	strcpy(buf_Y.y_label,"Angle");
	strcpy(buf_Y.data_label,"Color");
	strcpy(buf_Y.y_units,"Degrees");
	strcpy(buf_Y.data_units,"a.u.");
	strcpy(buf_Y.icon,"color");
	strcpy(buf_Y.cols,"yd");
	buf_Y.x_len=1;
	buf_Y.y_len=in->escape_bins;
	buf_Y.z_len=1;
	buffer_add_json(&buf_Y);

	dat_file_malloc(&buf_Z);
	buf_Z.y_mul=1.0;
	buf_Z.data_mul=1.0;
	strcpy(buf_Z.title,"CIE 1931 color space - Z");
	strcpy(buf_Z.type,"xy");
	strcpy(buf_Z.y_label,"Angle");
	strcpy(buf_Z.data_label,"Color");
	strcpy(buf_Z.y_units,"Degrees");
	strcpy(buf_Z.data_units,"a.u.");
	strcpy(buf_Z.icon,"color");
	strcpy(buf_Z.cols,"yd");
	buf_Z.x_len=1;
	buf_Z.y_len=in->escape_bins;
	buf_Z.z_len=1;
	buffer_add_json(&buf_Z);

	dat_file_malloc(&buf_x);
	buf_x.y_mul=1.0;
	buf_x.data_mul=1.0;
	strcpy(buf_x.title,"CIE 1931 color space - x");
	strcpy(buf_x.type,"xy");
	strcpy(buf_x.y_label,"Angle");
	strcpy(buf_x.data_label,"Color");
	strcpy(buf_x.y_units,"Degrees");
	strcpy(buf_x.data_units,"a.u.");
	strcpy(buf_x.icon,"color");
	strcpy(buf_x.cols,"yd");
	buf_x.x_len=1;
	buf_x.y_len=in->escape_bins;
	buf_x.z_len=1;
	buffer_add_json(&buf_x);

	dat_file_malloc(&buf_y);
	buf_y.y_mul=1.0;
	buf_y.data_mul=1.0;
	strcpy(buf_y.title,"CIE 1931 color space - y");
	strcpy(buf_y.type,"xy");
	strcpy(buf_y.y_label,"Angle");
	strcpy(buf_y.data_label,"Color");
	strcpy(buf_y.y_units,"Degrees");
	strcpy(buf_y.data_units,"a.u.");
	strcpy(buf_y.icon,"color");
	strcpy(buf_y.cols,"yd");
	buf_y.x_len=1;
	buf_y.y_len=in->escape_bins;
	buf_y.z_len=1;
	buffer_add_json(&buf_y);

	dat_file_malloc(&buf_z);
	buf_z.y_mul=1.0;
	buf_z.data_mul=1.0;
	strcpy(buf_z.title,"CIE 1931 color space - z");
	strcpy(buf_z.type,"xy");
	strcpy(buf_z.y_label,"Angle");
	strcpy(buf_z.data_label,"Color");
	strcpy(buf_z.y_units,"Degrees");
	strcpy(buf_z.data_units,"a.u.");
	strcpy(buf_z.icon,"color");
	strcpy(buf_z.cols,"yd");
	buf_z.x_len=1;
	buf_z.y_len=in->escape_bins;
	buf_z.z_len=1;
	buffer_add_json(&buf_z);


	for (y=0;y<in->escape_bins;y++)
	{
		math_xy_init(&spec_out);

		for (x=0;x<in->ray_wavelength_points;x++)
		{
			inter_append(&spec_out,in->lam[x],in->ang_escape[x][y]);
		}
		//printf("%d %d\n",in->ray_wavelength_points,spec_out.len);
		//getchar();
		if (color_cie_cal_XYZ(sim,&X,&Y,&Z,&spec_out,FALSE)==0)
		{
			color_XYZ_to_rgb(&R,&G,&B,X,Y,Z);

			sprintf(temp,"%le %.2x%.2x%.2x\n",in->angle[y],R,G,B);
			buffer_add_string(&buf_rgb,temp);

			sprintf(temp,"%le %le\n",in->angle[y],X);
			buffer_add_string(&buf_X,temp);

			sprintf(temp,"%le %le\n",in->angle[y],Y);
			buffer_add_string(&buf_Y,temp);

			sprintf(temp,"%le %le\n",in->angle[y],Z);
			buffer_add_string(&buf_Z,temp);
			double tot=X+Y+Z;
			if (tot==0)
			{
				tot=1.0;
				X=0.0;
				Y=0.0;
				X=0.0;

			}
			sprintf(temp,"%le %le\n",in->angle[y],X/(tot));
			buffer_add_string(&buf_x,temp);

			sprintf(temp,"%le %le\n",in->angle[y],Y/(tot));
			buffer_add_string(&buf_y,temp);

			sprintf(temp,"%le %le\n",in->angle[y],Z/(tot));
			buffer_add_string(&buf_z,temp);
		}

		math_xy_free(&spec_out);
	}

	dat_file_dump_path(sim,"","theta_RGB.csv",&buf_rgb);
	dat_file_free(&buf_rgb);

	dat_file_dump_path(sim,"","theta_X.csv",&buf_X);
	dat_file_free(&buf_X);

	dat_file_dump_path(sim,"","theta_Y.csv",&buf_Y);
	dat_file_free(&buf_Y);

	dat_file_dump_path(sim,"","theta_Z.csv",&buf_Z);
	dat_file_free(&buf_Z);

	dat_file_dump_path(sim,"","theta_small_x.csv",&buf_x);
	dat_file_free(&buf_x);

	dat_file_dump_path(sim,"","theta_small_y.csv",&buf_y);
	dat_file_free(&buf_y);

	dat_file_dump_path(sim,"","theta_small_z.csv",&buf_z);
	dat_file_free(&buf_z);

	detector_dump_bins(sim,in);
}

void ray_dump_abs_profile(struct simulation *sim,struct device *dev ,char *path,struct ray_engine *in)
{
	struct dat_file buf;
	struct dimensions *dim=&(dev->dim_optical);

	if (in->dump_verbosity==dump_nothing)
	{
		return;
	}

	dat_file_init(&buf);

	if (in->abs_profile!=NULL)
	{
		if (buffer_set_file_name(sim,NULL,&buf,"abs_profile.csv")==0)
		{
			dat_file_malloc(&buf);
			dim_info_to_buf(&buf,dim);
			strcpy(buf.title,"Optical absorption profile");
			strcpy(buf.data_label,"Optical absorption profile");
			strcpy(buf.data_units,"m^{-3}s^{-1}");
			strcpy(buf.type,"heat");

			dat_file_write_zxy_snapshot_as_slices(sim,path, &buf,dim,in->abs_profile);
			dat_file_free(&buf);


		}
	}


}
