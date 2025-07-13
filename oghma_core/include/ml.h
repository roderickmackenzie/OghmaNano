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

/** @file ml.h
	@brief Header file for ml.c
*/
#ifndef ml_h
#define ml_h
#include <json_struct.h>
#include <dat_file.h>
#include "json.h"
#include <hash_list.h>
#include <math_xy.h>
#include <token_lib.h>

struct ml_vectors_obj
{
	struct math_xy *hist;
	struct hash_list min;
	struct hash_list max;
	int *log;
	struct token_lib_item** tokens;
};

struct ml_stats
{
	struct json j;

	struct ml_vectors_obj vec;
	struct ml_vectors_obj vec_norm;
	struct ml_vectors_obj vec_combined;
	struct ml_vectors_obj vec_combined_norm;

	char json_vectors_file[OGHMA_PATH_MAX];
	char base_sim_path[OGHMA_PATH_MAX];
	char build_path[OGHMA_PATH_MAX];
	char main_hist_dir[OGHMA_PATH_MAX];

	int ml_random_n;

	struct json_obj *json_obj_ml_random;
	struct hash_list token_lib;

	char last_device_id[OGHMA_PATH_MAX];
	FILE *csv_file;
	char csv_file_name[OGHMA_PATH_MAX];
	long csv_line;

	int csv_col;
	int done;
	int total;
	int finished_building;
	struct hash_list log;
};

struct vd_sub_sim
{
	struct json j;
	double Psun;
	char sub_sim_name[STR_MAX];
	char sim_mode[STR_MAX];
	char virtual_device_dir[OGHMA_PATH_MAX];
	char virtual_device_dir_sub_sim[OGHMA_PATH_MAX];
	struct json_obj *json_sub_sim;
};

struct ml_build
{
	struct json j;
	char base_sim_path[OGHMA_PATH_MAX];
	char build_path[OGHMA_PATH_MAX];
	char ml_tab_name[STR_MAX];
	int ml_number_of_archives;
	int ml_sims_per_archive;
	int done;
	int total;
	int finished_building;
	struct rand_state rand;
};

struct ml_vectors
{
	struct json j;
	char base_sim_path[OGHMA_PATH_MAX];
	char search_path[OGHMA_PATH_MAX];
	char ml_tab_name[STR_MAX];
	char output_file[STR_MAX];
	char errors_file[STR_MAX];
	char stats_file[STR_MAX];
	struct json_obj *json_obj_ml_sims;
	struct json_obj *json_obj_ml_random;
	struct json_obj *json_obj_config;
	int ml_sims_n;
	int ml_random_n;
	int done;
	int total;
	int finished_building;
	int errors;
};

//build
int ml_build_init(struct ml_build *in);
int ml_build_load(struct ml_build *in,char *base_sim_path,char *build_path, char *ml_tab_name);
int ml_build_gen(struct ml_build *in);
int ml_build_free(struct ml_build *in);

//ml_vectors
int ml_vectors_init(struct ml_vectors *in);
int ml_vectors_load(struct ml_vectors *in,char *base_sim_path,char *search_path, char *output_dir, char *ml_tab_name);
int ml_vectors_gen(struct ml_vectors *in);
int ml_vectors_clean(struct ml_vectors *in);
int ml_vectors_free(struct ml_vectors *in);
int ml_vectors_write_header_to_output_file(struct ml_vectors *in);
int ml_get_vectors_from_file(struct dat_file *buf, struct vd_sub_sim *vd_sub_sim, char *vectors, char *vector_file_name);
int ml_vectors_write_tail_to_output_file(struct ml_vectors *in);

//vd_sub_sim
int ml_vectors_vd_sub_sim_init(struct vd_sub_sim *in);
int ml_vectors_vd_sub_sim_free(struct vd_sub_sim *in);
int ml_vectors_vd_sub_sim_load(struct ml_vectors *in, struct vd_sub_sim *vd_sub_sim);
int ml_vectors_vd_sub_sim_get_jv(struct dat_file *buf, struct ml_vectors *in, struct vd_sub_sim *vd_sub_sim);
int ml_vectors_vd_sub_sim_get_sim_info(struct dat_file *buf, struct ml_vectors *in, struct vd_sub_sim *vd_sub_sim);
int ml_vectors_vd_params(struct dat_file *buf,struct ml_vectors *in, struct vd_sub_sim *vd_sub_sim);

//ml_stats
int ml_stats_init(struct ml_stats *in);
int ml_stats_run(struct ml_stats *in);
void callback_ml_min_max(char *full_path,char *val, void *data, int *ret);
void callback_log_list(char *full_path,char *val, void *data, int *ret);
void callback_ml_build_hist(char *full_path,char *val, void *data, int *ret);
int ml_stats_free(struct ml_stats *in);
int ml_stats_load(struct ml_stats *in, char *base_sim_path,char *tab_name);
int ml_stats_setup_lookup_tables(struct ml_stats *in, int *log, struct hash_list *list,struct token_lib_item** tokens);
int ml_stats_dump_latex_head(FILE *out);
int ml_stats_dump_latex_add_2x1_figures(FILE *out,char *file_name0, char *file_name1);
int ml_stats_dump_latex_tail(FILE *out);
void callback_ml_extract_vectors_list(char *full_path,char *val, void *data);

int ml_vectors_obj_init(struct ml_vectors_obj *vec);
int ml_vectors_obj_malloc(struct ml_stats *in,struct ml_vectors_obj *vec, int norm);
int ml_vectors_obj_free(struct ml_vectors_obj *vec);
int ml_vectors_obj_update_min_value(struct ml_vectors_obj *vec, char *token, double value);
int ml_vectors_obj_update_max_value(struct ml_vectors_obj *vec, char *token, double value);
int ml_vectors_obj_dump(struct ml_vectors_obj *vec, char *output_path, char *name);
int ml_vectors_obj_dump_hist(struct ml_stats *in,struct ml_vectors_obj *vec, char *output_path, char *name);
int ml_vectors_obj_add_to_hist(struct ml_vectors_obj *vec, int hist_index, double value);

int ml_make_nets_json(char *new_json_file_path,char *sim_path, struct json *j, char *uid);
#endif
