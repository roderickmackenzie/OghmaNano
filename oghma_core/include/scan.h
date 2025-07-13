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

/** @file scan.h
	@brief Header file for vec.c
*/
#ifndef scan_h
#define scan_h
#include <vec.h>
#include <dat_file.h>
#include "list_struct.h"
#include "json.h"

struct scan_item
{
	struct list list;
	char opp[STR_MAX];
	char raw_values[STR_MAX];
	char token_json[STR_MAX];
	char token_json1[STR_MAX];
	int pos;
};

struct scan
{
	struct scan_item *items;
	int nitems;
	int optimizer_enabled;
	int scan_optimizer_dump_at_end;
	int scan_optimizer_dump_n_steps;
	char name[STR_MAX];
	char last_error[STR_MAX];
	int early_stop;
};

int scan_load_config(struct simulation *sim,struct scan *in, struct json_obj *json_scan);
int scan_init(struct scan *in);
int scan_free(struct scan *in);
int scan_cpy(struct scan *out,struct scan *in);
void scan_dump(struct simulation *sim,struct scan *in);
int scan_step(struct scan *in);
int scan_fast_forward(struct scan *in,int steps);

//scan item
int scan_item_init(struct scan_item *item);
int scan_item_free(struct scan_item *item);
int scan_item_cpy(struct scan_item *out,struct scan_item *in);

int scan_make_dirs(struct simulation *sim,struct scan *in,char *base_path);
int scan_get_path(char *out,struct scan *in);
int scan_apply_to_json(struct simulation *sim,struct json *j,struct scan *in);
int scan_load_config_from_file(struct simulation *sim,struct scan *in, char *path, char *scan_name);
int scan_reset(struct scan *in);
int scan_test_end(struct scan *in);
int scan_optimizer(struct simulation *sim,struct scan *in,char *base_path);
int scan_count(struct simulation *sim,struct scan *in);
#endif
