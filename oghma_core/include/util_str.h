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

/** @file util_str.h
@brief util functions for strings
*/


#ifndef h_util_str
#define h_util
#include <g_io.h>

#define is_number(a) (( a >= '0' && a <= '9' )||(a=='e')||(a=='E')||(a=='+')||(a=='-')||(a=='.'))

//number
int get_number_in_string(double *out, char* in, int n, int *comment_pos);
int get_numbers_in_string(double *out, int *index, int nindex, char* in, int *comment_pos);
int cmpstr_min(char * in1,char *in2);
int strextract_name(char *out,char * in);
int format_float(char *out,double in);

//cmp
int strcmp_end(char * str,char *end);
int strcmp_begin(char * str,char *begin);
int strcmp_begin_safe(char * str,int str_len,char *begin,int begin_len);
int compare_numbers(const char *a, const char *b);
int strnatcmp(const char *a, const char *b);

//count
int str_count(char *in,char *find);
int str_count_char(char *in, char val);
int count_csv_items(char *in);
int str_ckecksum(char *in_string, int mod);

char* strextract_domain(char * in);
int is_domain(char * in);
int extract_str_number(char * in,char *cut);
int strextract_int(char * in);
int str_isnumber(char *input);
void split_dot(char *out, char *in);
int split_reverse(char *in,char token);
int get_line(char *out,char *data,long len,long *pos, int out_buffer_max);

int str_is_ascii(char *in_string);
void str_to_lower(char *out, char *in);
int str_get_file_ext(char *ext,char *in, int max);

//copy
int strcpy_malloc(char **out,char *in);
int strcat_malloc(char **ret,int *max_len, char *txt_to_append);

//replace
int str_replace(char *in,char *find,char *replace, int max_len);
int str_replace_char(char *in,char search, char replace);
int replace_number_in_string(char *buf, char* in, double replace, int n);

//split
int str_remove_before(char *in, char val);
void str_remove_after(char *in, char search_char);
int str_split_end(char *in, char val);
int str_split(char *out, char *in, int *pos, char val);
int str_remove_before_pos(char *in, int start_val);

//dump
void string_to_hex(char* out,char* in);
int hex_to_string(char* in);

//latex
int str_escape_latex(char *in, int max);

//extract
int str_get_tail(char *out, char *in, int extract_len);

//clean
void remove_space_after(char *in);
int remove_space_before(char *in);
int remove_quotes(char *out);
int str_remove_tail_numbers(char *in);

//search
int str_get_char_last_pos(char *in,char val);
int str_get_char_first_pos(char *in,char val);

//sprintf
void sprintf_xlsx(char *output, int row_counter, int xlsx_format, const char *format, ...);

//checksums
int str_ckecksum(char *in_string, int mod);
int str_md5(char *out, char *in);
#endif
