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

/** @file inp.h
@brief Code to read input files.
*/

#ifndef inp_h
#define inp_h
#include <g_io.h>
#include "advmath.h"
#include "inp_struct.h"
#include <sim_struct.h>
#include <g_io_zip.h>
#include "list_struct.h"

//#pragma message("Don't use me")

void inp_replace_double(struct simulation *sim,struct inp_file *in,char *token, double value);
int inp_save(struct simulation *sim,struct inp_file *in);
void inp_init(struct simulation *sim,struct inp_file *in);
int inp_load(struct simulation *sim,struct inp_file *in,char *file);
void inp_free(struct simulation *sim,struct inp_file *in);
int inp_search_gdouble(struct simulation *sim,struct inp_file *in,gdouble* out,char* token);
void inp_search_string(struct simulation *sim,struct inp_file *in,char* out,char* token);
int inp_search(struct simulation *sim,char* out,struct inp_file *in,char *token);
int inp_read_buffer(struct simulation *sim,char **buf, long *len,char *full_file_name);
void inp_reset_read(struct simulation *sim,struct inp_file *in);
int inp_load_from_path(struct simulation *sim,struct inp_file *in,char *path,char *file);
void inp_replace(struct simulation *sim,struct inp_file *in,char *token, char *text);
int inp_isfile(struct simulation *sim,char *full_file_name);

void inp_listdir(struct simulation *sim, char *dir_name,struct list *out);

void inp_replace_offset(struct simulation *sim,struct inp_file *in,char *token, char *text,int offset);
void inp_load_from_buffer(struct simulation *sim,struct inp_file *in,char *file,char *buffer,int len);

#endif
