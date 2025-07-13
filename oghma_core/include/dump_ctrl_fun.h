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

/** @file dump_ctrl.h
	@brief Set/Get dump flags to decided what to dump.
*/


#ifndef dump_ctrl_fun_h
#define dump_ctrl_fun_h
#include <g_io.h>
#include <sim_struct.h>
#include <dump_ctrl.h>
#include <device.h>
#include <dat_file_struct.h>

//dump ctrl
int dump_ctrl_init(struct dump_ctrl *in);
int dump_ctrl_free(struct dump_ctrl *in);
int dump_ctrl_cpy(struct dump_ctrl *out, struct dump_ctrl *in);
struct dump_item * dump_ctrl_find_item(struct dump_ctrl *in,char *name);
struct dump_item * dump_ctrl_add_item(struct dump_ctrl *in,char *name);
int dump_ctrl_dump(struct dump_ctrl *in);
int dump_ctrl_add_banned_files(struct simulation *sim,struct device *dev);
int dump_ctrl_enable_id(struct dump_ctrl *in, char *id, int val);
int dump_ctrl_zxy_to_dat_file(struct simulation *sim,struct dat_file *buf,struct dump_ctrl *in,struct dimensions *dim);

//dump item
int dump_item_add_array(struct dump_item *in, void *array, char *id);
int dump_item_init(struct dump_item *in);
int dump_item_free(struct dump_item *in);
int dump_item_cpy(struct dump_item *out, struct dump_item *in);
int dump_ctrl_add_to_dat_file(struct dat_file *out, struct dump_ctrl *in,char *name);
int dump_item_dump(struct dump_item *in);

//old needs to be removed
int get_dump_status(struct simulation *sim,int a);
void set_dump_status(struct simulation *sim,int name, int a);
#endif
