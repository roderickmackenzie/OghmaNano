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

/** @file json.h
@brief Json decoder
*/

#ifndef json_h
#define json_h
#define json_enabled
#include <g_io.h>
#include <sim_struct.h>
#include <md5.h>
#include <json_struct.h>



//json obj
void json_obj_init(struct json_obj *obj);
void json_obj_realloc(struct json_obj *obj);
struct json_obj * json_obj_add(struct json_obj *obj,char *name,char *data, int data_type);
struct json_obj * json_obj_add_int(struct json_obj *obj,char *name, int data);
struct json_obj * json_obj_add_double(struct json_obj *obj,char *name, double data);
struct json_obj * json_obj_add_bool(struct json_obj *obj,char *name, int data);
struct json_obj * json_obj_add_string(struct json_obj *obj,char *name, char *data);
struct json_obj * json_obj_add_long_long(struct json_obj *obj,char *name, long long data);

void json_obj_free(struct json_obj *obj);
int json_obj_delete_node(struct json_obj *root_node, char *token);
int json_delete_segment(struct json_obj *root_node, char *segment_name);
void gobble(struct json *j);

//set_data
void json_set_data(struct json_obj *obj,char *data);
int json_set_data_double(struct json_obj *main_obj,char *token,double value);
int json_set_data_string(struct json_obj *main_obj,char *token,char *value);
int json_set_data_bool(struct json_obj *main_obj,char *token,int value);
int json_set_data_int(struct json_obj *main_obj,char *token,int value);
void json_set_data_dat_file(struct json_obj *obj);
int json_set_data_long_long(struct json_obj *main_obj,char *token,long long value);

//used by decode
void json_free(struct json *j);
void json_init(struct json *j);
void get_name(char *out,struct json *j);
void get_value(char *out,struct json *j, int debug,int *value_type);
void json_obj_all_free(struct json_obj *obj);
struct json_obj *json_obj_find(struct json_obj *obj, char *name);
int json_decode(struct json *j,struct json_obj *obj);
int json_load(struct simulation *sim,struct json *j,char *full_file_name);


struct json_obj *json_obj_find_by_path(struct json_obj *obj, char *path);
int json_save(struct json *j);
void json_cpy(struct simulation *sim,struct json *out,struct json *in);
void json_obj_cpy_data(struct json_obj *out,struct json_obj *in);
void json_obj_cpy(struct json_obj *out,struct json_obj *in);
int json_load_from_path(struct simulation *sim,struct json *j,char *path,char *file_name);
void json_chk_sum(struct simulation *sim,struct md5 *sum,struct json_obj *json_in);
int json_checksum_check(struct simulation *sim,char *out_check_sum,char *chk_file,struct md5 *in_sum);

struct json_obj *json_find_sim_struct(struct simulation *sim, struct json *j,char *sim_command);
void remove_comma(struct json_string  *buf);
void json_dump_to_string(struct json_string  *buf,struct json_obj *obj,int level,struct json_dump_settings *settings);
int json_save_as(struct simulation *sim,char *file_name,struct json *j);
int json_obj_save_as(struct simulation *sim,char *file_name,struct json_obj *j);

int json_is_token(struct json_obj *obj,char *name);

//get_data
int json_get_string(struct simulation *sim,struct json_obj *obj, char *out,char *name,int stop_on_error);
int json_get_hex_string(struct simulation *sim,struct json_obj *obj, char *out,char *name,int stop_on_error);
int json_get_int(struct simulation *sim,struct json_obj *obj, int *out,char *name,int stop_on_error);
int json_get_english(struct simulation *sim,struct json_obj *obj, int *out,char *name,int stop_on_error);
int json_get_double(struct simulation *sim,struct json_obj *obj, double *out,char *name,int stop_on_error);
int json_get_double_fabs(struct simulation *sim,struct json_obj *obj, double *out,char *name,int stop_on_error);
int json_get_long_double(struct simulation *sim, struct json_obj *obj, gdouble *out,char *name,int stop_on_error);
int json_get_float(struct simulation *sim,struct json_obj *obj, float *out,char *name,int stop_on_error);
int json_get_long_long(struct simulation *sim,struct json_obj *obj, long long *out,char *name,int stop_on_error);
int json_get_long(struct simulation *sim,struct json_obj *obj, long *out,char *name,int stop_on_error);
int json_get_equation(struct simulation *sim,struct json_obj *obj, struct rpn_equation *equ,char *name,int stop_on_error);
int json_get_cpus(struct simulation *sim,struct json_obj *obj, int *out,char *name,int stop_on_error);
int json_get_time_iso8601(struct simulation *sim,struct json_obj *obj, long long *out,char *name,int stop_on_error);

//search
struct json_obj *json_search_for_obj_by_uid(struct json_obj *obj, char *value);
struct json_obj *json_search_for_token_value(char *path, struct json_obj *obj,char *token, char *value);
int json_update_random_ids(struct json_obj *obj);

//diagnostics
int json_calculate_memory(struct json_obj *obj,int *tot);

//dump
void tabs(struct json_string *buf,int number);
void json_dump_obj(struct json_obj *obj);
void json_dump(struct json_obj *obj,struct json_string *buf, int level,struct json_dump_settings *settings);
void json_dump_buffer(struct json *j);
void json_dump_all(struct json *j);
int json_dump_obj_string_from_path(struct json_string *buf,struct json *j, char *json_path);
int json_to_latex(struct json_string *buf,struct json_obj *obj,struct hash_list *token_lib);

//python interface
int json_dump_tokens_from_path(struct json_string *buf,struct json *j, char *json_path);
int json_dump_settings_init(struct json_dump_settings *settings);
int json_get_token_value_from_path(struct json_string *buf,int *data_type, struct json *j, char *json_path, char *token);
int json_set_token_value_using_path(struct json *j, char *json_path, char *token, char *value);
int json_get_all_sim_modes(struct json_string *buf,struct json *j);
int json_is_token_from_path(struct json *j, char *json_path, char *token);
struct json_obj *json_add_bib_item_at_path(struct json *j, char *json_path, char *token);
int json_delete_token_using_path(struct json *j, char *json_path, char *token);
int json_search_for_token_value_in_path(char *path, struct json *j, char *token, char *value);
int json_py_add_segment(char *new_segment_path, char *path,struct json *j,char *human_name,int pos);
int json_update_random_ids_at_path(struct json *j, char *path);
int json_delete_segment_by_path(struct json *j, char *path, char *segment_name);
int json_clone_segment(char *new_segment_path, char *root_path,char *src_segment, struct json *j,char *new_human_name);
int json_py_segments_swap(struct json *j,char *root_path,int i0, int i1);
int json_py_import_json_to_obj(struct json *j,char *path,char *import_json_as_text);
int json_py_init_rand();
int json_py_to_latex(struct json_string *buf,struct json *j, char *json_path,struct hash_list *token_lib);
int json_py_isnode(struct json *j, char *json_path);
int json_py_clear_segments(struct json *j, char *json_path);
int json_py_dump_bib_cite(struct json_string *buf,struct json *j, char *json_path);
int json_py_bib_get_oghma_citations(struct json_string *single_quote,struct json_string *text,struct json *j,char *user_id);
int json_py_add_obj_double(struct json *j,char *root_path,char *token, double value);
int json_py_add_obj_int(struct json *j,char *root_path,char *token, int value);
int json_py_add_obj_bool(struct json *j,char *root_path,char *token, int value);
int json_py_add_obj_string(struct json *j,char *root_path,char *token, char *value);

//segmnents
int json_segments_renumber(struct json_obj *root_node);
int json_segments_swap(struct json_obj *root_node, int i0, int i1);
int json_segments_move_last_to_pos(struct json_obj *root_node, int i0);
int json_segments_copy_to_clipboard(struct json *j, struct json_string *buf, char *path, int *rows, int n_rows);
int json_segments_paste_from_clipboard(struct json *j, char *root_path, char *buf, int buf_len, int row);
int json_clear_segments(struct json_obj *root_node);
struct json_obj *json_segments_add(struct json_obj *obj,char *human_name, int pos);
struct json_obj *json_segments_add_by_path(struct json_obj *root_obj,char *path,char *human_name, int pos);
struct json_obj *json_segments_find_by_name(struct json_obj *root_obj,char *name_in);

//json fast
int json_fast_load(char *file_name, void (*callback)(), void *data);

//import
int json_import_from_buffer(struct json *j,char *buf,int len);
int json_import_ojb_from_buffer(struct json *j,struct json_obj *obj,char *buf,int len);

//json string
void json_string_init(struct json_string *in);
void json_string_free(struct json_string *in);
int json_string_cat_char(struct json_string *buf,char in_data);
int json_string_del_last_chars(struct json_string *buf,int n);
int json_string_clear(struct json_string *buf);
void json_string_cat(struct json_string *buf,char *data);

int json_compat(struct json *j,char *token, char *value);
int json_compat_fixup(struct json *j);
int json_import_old_oghma_file(struct json *j, char *file_name);
int json_guess_if_oghma_json_file(char *file_name);

//segment counter
int json_segment_counter_init(struct json_segment_counter *data);
int json_segment_counter_load(struct json_segment_counter *data,struct json *j,char *path);
int json_segment_counter_load_from_obj(struct json_segment_counter *data,struct json_obj *obj);
struct json_obj *json_segment_counter_get_next(struct json_segment_counter *data);

//bibtex
struct json_obj *json_add_bib_item(struct json *j, struct json_obj *root_obj, char *token);
int json_bib_decode(struct json *j,struct json_obj *obj);
int json_dump_bib_to_string(struct json_string *buf,struct json_obj *obj, struct json_dump_settings *settings);
int json_bib_cite(struct json_string *buf,struct json_obj *bib_obj);
int json_py_bib_enforce_citation(struct json *j, char *token);

//yml
int json_yml_decode(struct json *j,struct json_obj *obj, int indent_in);
int json_yml_to_math_xy(struct json *j);

//copy paste
int json_copy_to_clipboard(struct json *j, struct json_string *buf, char *path,char *paste_object_type, int *segments, int n_segments);
struct json_obj * json_clip_start(struct json *j,char *paste_object_type);
struct json_obj * json_clip_add_data(struct json *j,struct json_obj *data);
int json_clip_check_paste_object(struct json *json_clip, char *paste_object_type);

int json_clip_segments_append(struct json *j, struct json_obj *obj_target_root, char *paste_object_type, int row, char *buf, int buf_len);
int json_clip_segments_append_at_path(struct json *j, char *root_path, char *paste_object_type, int row, char *buf, int buf_len);
int json_clip_segment_replace_at_path(struct json *j, char *root_path, char *paste_object_type, char *buf, int buf_len, char *segment_name);
int json_clip_segment_replace(struct json *j, struct json_obj *obj_target_root, char *paste_object_type, char *buf, int buf_len, char *segment_name);

#endif
