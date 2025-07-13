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

#ifndef hash_list_h
#define hash_list_h
#include "list_struct.h"
	void hash_list_init(struct hash_list *in, int item_size);
	void* hash_list_add(struct hash_list *in,char *text, void *val);
	void* hash_list_get(struct hash_list *in,char *name);
	void* hash_list_get_end(struct hash_list *in,char *name);
	void hash_list_malloc(struct hash_list *in);
	void hash_list_free(struct hash_list *in);
	int hash_list_cmp(struct hash_list *in,char *name);
	int hash_list_get_pos(struct hash_list *in,char *name);
	int hash_list_istoken(struct hash_list *in,char *name);
	unsigned long hash_list_gen_key(char *text);
	int hash_list_sort_cmp(const void *a, const void *b);
	void hash_list_gen_keys(struct hash_list *in);
	int hash_list_quick_find(struct hash_list *in,char *name);
	void hash_list_qsort(struct hash_list *in); 
	//dump
	void hash_list_dump(struct hash_list *in);
	void hash_list_dump_int(struct hash_list *in);
	void hash_list_dump_double(struct hash_list *in);
#endif
