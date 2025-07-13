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

/** @file dump.h
	@brief Fucntions to write data to disk.
*/


#ifndef h_dump
#define h_dump
#include <g_io.h>
#include "device.h"
#include "dump_ctrl.h"
#include "dat_file.h"
#include <sim_struct.h>

struct snapshots
{
	char icon[100];
	char type[100];
	char plot_type[100];
	char name[100];
	char path[OGHMA_PATH_MAX];
};

void dump_init(struct simulation *sim,struct device* in);
void dump_load_config(struct simulation* sim,struct device *in);
void dump_remove_snapshots(struct simulation* sim, char *output_path);
void dump_slice(struct device *in,char *prefix);
void dump_1d_slice(struct simulation *sim,struct device *dev,char *out_dir);
void dump_zx(struct simulation *sim,struct device *in,char *out_dir);
void dump_zxy_charge(struct simulation *sim,struct device *dev,char *out_dir);
void dump_zxy_conductivity(struct simulation *sim,struct device *dev,char *out_dir);
void dump_zxy_boundarys(struct simulation *sim,struct device *dev,char *out_dir);
void dump_zxy_J(struct simulation *sim,struct device *dev,char *out_dir);
void dump_zxy_Jx(struct simulation *sim,struct device *dev,char *out_dir);
void dump_zxy_Jy(struct simulation *sim,struct device *dev,char *out_dir);
void dump_zxy_Jz(struct simulation *sim,struct device *dev,char *out_dir);
void dump_zxy_interfaces(struct simulation *sim,struct device *dev,char *out_dir);
void dump_write_to_disk(struct simulation *sim,struct device* in);
void dat_file_write_zxy_snapshot_as_slices(struct simulation *sim,char * path, struct dat_file *buf,struct dimensions *dim,double ***data);

//Singlet
void dump_zxy_singlet(struct simulation *sim,struct device *dev,char *out_dir);

//Singlet_opv
void dump_zxy_singlet_opv(struct simulation *sim,struct device *dev,char *out_dir);

//energy cut through
void dump_energy_slice(struct simulation *sim,struct device *in,int x, int y, int z);
void dump_device_map(struct simulation *sim,char* out_dir,struct device *in);

void dump_clean_cache_files(struct simulation* sim);


//snapshots
void snapshots_init(struct snapshots *snap);
void dump_make_snapshot_dir(struct simulation *sim,char *ret_path, int number,struct snapshots *snap);

//light
int dump_can_i_dump(struct simulation *sim,struct device *dev, char *file_name);
int dump_is_file_in_banned(struct simulation *sim,struct device *dev, char *file_name);
int dump_do_i_add_random_noise(struct simulation *sim, double *sigma,char *file_name);

//math_xy
void dump_math_xy_tree(struct simulation *sim,char *out_dir,struct dat_file *buf,struct math_xy *in);
#endif
