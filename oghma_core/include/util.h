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

/** @file util.h
@brief util functions
*/


#ifndef h_util
#define h_util
#include <g_io.h>
#include <enabled_libs.h>
#include <stdio.h>
#include <sim_struct.h>
#include <util_str.h>
#include <color.h>

void set_ewe_lock_file(char *lockname,char *data);
void print_hex(struct simulation *sim,unsigned char *data);
void remove_dir(struct simulation *sim,char* dir_name);
int ewe(struct simulation *sim, const char *format, ...);
int ewe_on_neg_value(double val, struct simulation *sim, const char *format, ... );
void write_lock_file( struct simulation *sim);

void randomprint(struct simulation *sim,char *in);
int scanarg( char* in[],int count,char * find);
int get_arg_plusone_pos( char* in[],int count,char * find);
char * get_arg_plusone( char* in[],int count,char * find);

int english_to_bin(struct simulation *sim,char * in);
void fx_with_units(char *unit,double *mul,double max_val);
void time_with_units(char *out,double number);
int ohms_with_units(char *out,double val);
int file_size_with_units(char *out, int size_bytes);
int path_up_level(char *out, char *in);
FILE *fopena(char *path,char *name,const char *mode);
long get_dir_size(char *path);
int get_dir_min_max_file_age(char *path,long *min, long *max);

void poll_gui(struct simulation *sim);

void get_meter_dim(char *unit,double *mul,double max_val);
void get_time_dim(char *unit,double *mul,double max_val);
void get_wavelength_dim(char *unit,double *mul,double max_val);

int hashget(gdouble *x,int N,gdouble find);
int oghma_fgets(char *buf,int len,FILE *file);
int copy_file(struct simulation *sim,char *output,char *input);
#endif
