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

/** @file matrix.h
	@brief matrix file
*/

#ifndef matrix_h
#define matrix_h
#include <g_io.h>
#include <json_struct.h>

struct matrix_sort
{
	int Ti;
	int Tj;
	gdouble Tx;
};

struct matrix_index_sorter
{
	int index;
	int Ti;
	int Tj;
};

struct matrix
{
	//solver
	int nz;
	int nz_max;
	int M;
	int complex_matrix;
	int build_from_non_sparse;
	int msort_len;
	int ittr;

	int *Ti;		//row
	int *Tj;		//col
	double *Tx;		//data
	double *Txz;

	double *b;
	double *bz;

	int enable_row_mul;
	double *row_mul;
	int *row_item_count;

	char dump_name[100];
	//stats
	int tot_time;

	struct matrix_sort *msort;

	//cache
		int use_cache;
		char hash[256];
		char cache_file_path[OGHMA_PATH_MAX];
		char cache_index_file[OGHMA_PATH_MAX];

	//debug
		struct json_string debug_buffer;

	//threshold
		int threshold_enabled;
		double threshold_value;
		int threshold_removed;
};

#endif
