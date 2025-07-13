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

/** @file jv.h
@brief JV curve header file.
*/


#ifndef jv_h
#define jv_h
#include <sim.h>
#include <device.h>
#include <json.h>
#include <sweep_store.h>

struct jv
{
	double Vstart;
	double Vstop;
	double Vstep;
	double jv_step_mul;
	double jv_light_efficiency;
	double jv_max_j;
	int jv_single_point;
	int dump_verbosity;
	int dump_energy_space;
	int dump_x;
	int dump_y;
	int dump_z;
	int jv_use_external_voltage_as_stop;
	char charge_carrier_generation_model[200];
	int dump_sclc;
	int eqe_smooth;
};

void sim_jv(struct simulation *sim,struct device *dev);
void jv_load_config(struct simulation *sim, struct jv* dev, struct sweep_store *sweep, struct json_obj *json_jv);
#endif
