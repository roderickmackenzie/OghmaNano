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


#ifndef h_g_io_zip
#define h_g_io_zip
#include <enabled_libs.h>
#include <stdio.h>
#include <sim_struct.h>

int write_zip_buffer(struct simulation *sim,char *outfile,gdouble *buf,int buf_len);
int read_zip_buffer(struct simulation *sim,char *file_name,gdouble **buf);
int zip_file_add_new_file(char *zip_file_path, char *file_name,char *buffer, int len);
int zip_is_in_archive(char *full_file_name);
long zip_get_file_modification_date(char *full_file_name);
int zip_write_buffer(struct simulation *sim,char *full_file_name,char *buffer, int len);
int zip_extract_from_archive(char *path_to_archive, char *file_name, char *dest);
#endif
