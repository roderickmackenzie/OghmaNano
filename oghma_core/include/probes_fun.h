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

/** @file probes_fun.h
	@brief Store information as the simulation progresses such as voltage, current or carrier density, these are 1D arrays as a function of time of simulation step.
*/

#ifndef probes_fun_h
#define probes_fun_h
#include <g_io.h>
#include <probes.h>

void probes_init(struct simulation* sim,struct device *dev);
void probes_load(struct simulation* sim,struct device *dev);
void probes_cpy(struct simulation* sim,struct device *out,struct device *in);
void probes_free(struct simulation* sim,struct device *dev);
void probes_dump(struct simulation* sim,struct device *dev);
int probes_set_full_name(struct simulation* sim,struct device *dev);
int probes_dump_to_json(struct simulation* sim,struct device *dev, struct fom *fom);
void probes_add_data(struct simulation* sim,struct device *dev,void *data_in, struct dat_file *in_buf, int data_type);
void probes_make_dir(struct simulation *sim,struct device *dev);
#endif
