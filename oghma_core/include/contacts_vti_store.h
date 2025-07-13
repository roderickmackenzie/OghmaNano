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

/** @file contacts_vti_store.h
	@brief No idea what this does.
*/
#ifndef contacts_vti_store_h
#define contacts_vti_store_h
#include <device.h>
#include <sim_struct.h>
#include <contacts_vti_store_struct.h>
#include <fom.h>

void dump_contacts_init(struct simulation *sim,struct device *in,struct contacts_vti_store *store);
void dump_contacts_malloc(struct simulation *sim,struct device *in,struct contacts_vti_store *store);
void contacts_dump(struct simulation *sim,struct device *in,struct contacts_vti_store *store,int force);
void dump_contacts_add_data(struct simulation *sim,struct device *in,struct contacts_vti_store *store);
void dump_contacts_free(struct simulation *sim,struct device *in,struct contacts_vti_store *store);
void contacts_cal_external_jv(struct simulation *sim,struct device *dev,struct contacts_vti_store *store);
void contacts_dump_stats(struct device *dev,struct fom *fom,struct contacts_vti_store *store);
void contacts_dump_calculated_curves(struct simulation *sim,struct device *dev,struct contacts_vti_store *store);
#endif
