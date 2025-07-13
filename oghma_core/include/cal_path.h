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

/** @file cal_path.h
	@brief Header file for the functions which calculate in which file location to find stuff.
*/


#ifndef cal_path_h
#define cal_path_h
#include <g_io.h>
#include <sim_struct.h>
#include <path_ops.h>

void cal_path(struct simulation *sim);
char *get_cache_path(struct simulation *sim);
char *get_materials_path(struct simulation *sim);
char *get_filter_path(struct simulation *sim);
char *get_cie_color_path(struct simulation *sim);
char *get_shape_path(struct simulation *sim);
char *get_spectra_path(struct simulation *sim);
int find_dll(struct simulation *sim, char *lib_path,char *lib_name);
char *get_oghma_local_path(struct simulation *sim);
char *get_tmp_path(struct simulation *sim);
char *get_tmp_path_fast(struct simulation *sim);
void mkdirs(char *dir);

//<strip>
void set_key_path(struct simulation *sim);
//</strip>

#endif
