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


#ifndef h_sweep
#define h_sweep
#include <g_io.h>
#include "device.h"
#include <sweep_store.h>
#include "dat_file.h"
#include <sim_struct.h>


int sweep_init(struct simulation *sim,struct sweep_store *store);
int sweep_add_data(struct simulation *sim,struct sweep_store *store,struct device *in);
void sweep_free(struct simulation *sim,struct device *in,struct sweep_store *store);

//dumps
void sweep_save(struct simulation *sim,struct device *in,char *outputpath,struct sweep_store *store);
void sweep_save_j(struct simulation *sim,struct device *in,char *outputpath,struct sweep_store *store);
void sweep_dump_recombination(struct simulation *sim,struct device *dev,char *out_dir,struct sweep_store *store);
void sweep_dump_singlet(struct simulation *sim,struct device *dev,char *out_dir,struct sweep_store *store);
void sweep_dump_singlet_opv(struct simulation *sim,struct device *dev,char *out_dir,struct sweep_store *store);
void dynamic_info_to_buf(struct simulation *sim,struct dat_file *buf, struct device *dev,struct math_xy* data);
void sweep_save_thermal(struct simulation *sim,struct device *dev,char *outputpath,struct sweep_store *store);
int sweep_dump_emission(struct simulation *sim,struct device *dev,char *out_dir,struct sweep_store *store);
#endif
