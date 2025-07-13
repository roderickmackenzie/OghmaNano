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

/** @file fom.h
	@brief Figure of merit
*/

#ifndef fom_h
#define fom_h
#include <g_io.h>
#include <oghma_const.h>
#include <device.h>
#include <sim.h>
#include <fom_struct.h>
#include <device.h>

int fom_item_init(struct fom_item *in);
int fom_item_free(struct fom_item *in);
int fom_init(struct fom *in);
int fom_free(struct fom *in);
struct fom_item * fom_add_val(struct device *dev, struct fom *in,char *token,double value);
int fom_dump_as_json(struct device *dev, char *path,char *file_name,struct fom *in);
int fom_dump_as_csv(char *path,char *file_name,struct fom *data,int append);
int fom_dump_as_csv_to_file(FILE* out,struct fom *data,int append);

#endif
