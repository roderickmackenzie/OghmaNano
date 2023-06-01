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
@brief input file reader header file
*/

#ifndef inp_h
#define inp_h
#include "inp_struct.h"

void inp_replace_double(struct inp_file *in,char *token, double value);
int inp_get_array_len(struct inp_file *in,char *token);
int inp_get_array(char ** out,struct inp_file *in,char *token);
int inp_save(struct inp_file *in);
void inp_init(struct inp_file *in);
int inp_aes_load(struct inp_file *in,char *path,char *file,char *key);
int inp_load(struct inp_file *in,char *file);
void inp_free(struct inp_file *in);
int inp_search_double(struct inp_file *in,double* out,char* token);
int inp_search_int(struct inp_file *in,int* out,char* token);
int inp_search_longint(struct inp_file *in,long int* out,char* token);
int inp_search_string(struct inp_file *in,char* out,char* token);
int inp_search(char* out,struct inp_file *in,char *token);
void inp_check(struct inp_file *in,double ver);
int inp_read_buffer(char **buf, long *len,char *full_file_name);
void inp_reset_read(struct inp_file *in);
char* inp_get_string(struct inp_file *in);
char* inp_search_part(struct inp_file *in,char *token);
int inp_load_from_path(struct inp_file *in,char *path,char *file);
void inp_replace(struct inp_file *in,char *token, char *text);
int inp_search_pos(struct inp_file *in,char *token);
int inp_search_english(struct inp_file *in,char *token);
int inp_isfile(char *full_file_name);
int zip_is_in_archive(char *full_file_name);
int isfile(char *in);
int zip_write_buffer(char *full_file_name,char *buffer, int len);

void inp_listdir( char *dir_name,struct inp_list *out);
void inp_list_free(struct inp_list *in);
int inp_listcmp(struct inp_list *in,char *name);
int guess_whole_sim_name(char *ret,char *dir_name,char* search_name);
int search_for_token(char *ret,char *dir_name,char* token,char *search_value);

#endif
