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
#include <dat_file.h>
#include <dump.h>

/** @file ray_snapshots.c
	@brief Set up the simulation window for the ray tracer
*/

void ray_setup_shapshots(struct simulation *sim,struct device *dev, struct ray_engine *eng)
{
	struct snapshots snap;

	if (eng->dump_verbosity==dump_nothing)
	{
		strcpy(eng->ray_snapshot_dir,"none");
		return;
	}

	snapshots_init(&snap);
	strcpy(snap.type,"snapshots");
	strcpy(snap.plot_type,"3d");
	strcpy(snap.name,"ray_trace");
	strcpy(snap.path,get_output_path(dev));

	dump_make_snapshot_dir(sim,eng->ray_snapshot_dir, -1 ,&snap);

}

void ray_dump_shapshot(struct simulation *sim,struct device *dev, struct ray_engine *eng,struct ray_worker *worker,char *postfix)
{
	struct dat_file buf;
	char out_dir[PATH_MAX];
	char temp[200];
	char file_name[200];

	//printf("%d\n",eng->dump_verbosity);
	if (eng->dump_verbosity>0)
	{
		if (eng->call_count==-1)
		{

			sprintf(temp,"%d",worker->l);
			join_path(2,out_dir,eng->ray_snapshot_dir,temp);
			g_mkdir(out_dir);
			//printf("%s %s\n",eng->ray_snapshot_dir,out_dir);
			sprintf(file_name,"ray_%s.csv", postfix);		//,worker->layer
			dat_file_init(&buf);
			dat_file_malloc(&buf);

			sprintf(temp,"{\n");
			buffer_add_string(&buf,temp);

			sprintf(temp,"\t\"wavelength\":%le\n",(double )eng->lam[worker->l]);
			buffer_add_string(&buf,temp);

			sprintf(temp,"}");
			buffer_add_string(&buf,temp);
			//printf("%s\n",out_dir);
			dat_file_dump_path(sim,out_dir,"data.json",&buf);
			dat_file_free(&buf);

			ray_dump_all_rays(sim,out_dir,eng,dev,worker,file_name);
		}else
		{
			//This is used if we are call the ray tracer multiple times for each simulation step
			sprintf(temp,"%d",eng->call_count);
			join_path(2,out_dir,eng->ray_snapshot_dir,temp);
			g_mkdir(out_dir);
			//printf("%s %s\n",eng->ray_snapshot_dir,out_dir);
			sprintf(file_name,"%.1lfnm.csv",eng->lam[worker->l]*1e9);		//,worker->layer

			dat_file_init(&buf);
			dat_file_malloc(&buf);

			sprintf(temp,"{\n");
			buffer_add_string(&buf,temp);

			sprintf(temp,"\t\"step\":%d\n",eng->call_count);
			buffer_add_string(&buf,temp);

			sprintf(temp,"}");
			buffer_add_string(&buf,temp);

			dat_file_dump_path(sim,out_dir,"data.json",&buf);
			dat_file_free(&buf);

			ray_dump_all_rays(sim,out_dir,eng,dev,worker,file_name);
		}
	}

}


