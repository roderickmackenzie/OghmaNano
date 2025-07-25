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

/** @file probe.h
@brief Stark probe code
*/


#ifndef _probe
#define _probe
#include <g_io.h>
#include <sim.h>
#include <device.h>

struct optical_probe_config
{
struct math_xy *time_stark;
gdouble *probe_wavelength;
int n_probe_wavelength;
gdouble stark_mul;
int use_ss_spectra;
};

double optical_probe_cal(struct simulation *sim,struct device *dev,	gdouble wavelength);
void dump_optical_probe_spectrum(struct simulation *sim,struct device *dev,char *out_dir, int dump_number);
void optical_probe_init(struct simulation *sim,struct device *dev);
void optical_probe_free(struct simulation *sim,struct device *dev);
void optical_probe_record_step(struct simulation *sim,struct device *dev);
void optical_probe_dump(struct simulation *sim,struct device *dev);
#endif
