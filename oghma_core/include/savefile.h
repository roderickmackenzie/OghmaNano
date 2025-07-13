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

/** @file savefile.h
@brief Json decoder
*/

#ifndef c_h
#define savefile_h
#define savefile_enabled
#include <g_io.h>
#include <json_struct.h>
#include <json.h>
#include <shape.h>
#include <vec.h>

//json obj
int json_template_sim(struct json_obj *obj_main);

//template functions
void json_build_template_from_file(	struct json *j);
int json_template_sims_poly(struct json_obj *obj_sims);
int json_template_sims_eqe(struct json_obj *obj_sims);
int json_template_sims_jv(struct json_obj *obj_sims);
int json_template_sims_sunsvoc(struct json_obj *obj_sims);
int json_template_sims_sunsjsc(struct json_obj *obj_sims);
int json_template_sims_ce(struct json_obj *obj_sims);
int json_template_sims_pl_ss(struct json_obj *obj_sims);
int json_template_sims_spm(struct json_obj *obj_sims);
int json_template_sims_fdtd(struct json_obj *obj_sims);
int json_template_sims_cv(struct json_obj *obj_sims);
int json_template_sims_transfer_matrix(struct json_obj *obj_sims);
int json_template_sims_equilibrium(struct json_obj *obj_sims);
int json_template_sims_mode(struct json_obj *obj_sims);
int json_template_sims_ray(struct json_obj *obj_sims);
int json_template_sims_exciton(struct json_obj *obj_sims);
int json_template_sims_time_domain(struct json_obj *obj_sims);
int json_template_sims_fx_domain(struct json_obj *obj_sims);

int json_template_exciton(struct json_obj *obj_main);
int json_template_parasitic(struct json_obj *obj_main);
int json_template_math(struct json_obj *obj_main);
int json_template_server(struct json_obj *obj_main);
int json_template_epitaxy(struct json_obj *obj_main);

//fits
int json_template_fits(struct json_obj *obj_main);
int json_template_fits_fit_config(struct json_obj *obj_fits);
int json_template_fits_duplicate(struct json_obj *obj_fits);
int json_template_fits_fit_vars(struct json_obj *obj_fits);
int json_template_fits_rules(struct json_obj *obj_fits);
int json_template_fits_fits(struct json_obj *obj_fits);

int json_template_optical_lasers(struct json_obj *obj_optical);
int json_template_optical_boundary(struct json_obj *obj_optical);
int json_template_optical_light(struct json_obj *obj_optical);
int json_template_optical_outcoupling(struct json_obj *obj_optical);
int json_template_optical_spctral2(struct json_obj *obj_optical);
int json_template_optical_ray(struct json_obj *obj_optical);

//electrical
int json_template_electrical_boundary(struct json_obj *obj_electrical_solver);
int json_template_electrical_solver_cache(struct json_obj *obj_electrical_solver);
int json_template_electrical_solver_poisson(struct json_obj *obj_electrical_solver);
int json_template_dump(struct json_obj *obj_main);
int json_template_circuit(struct json_obj *obj_main);
int json_shape_dos(struct json_obj *obj, int material_db);
int json_template_solver_program(struct json_obj *obj_in);

//singlet
int json_template_singlet(struct json_obj *obj_main);

//automation
int json_template_scans(struct json_obj *obj_main);
int json_template_ml(struct json_obj *obj_main);
int json_template_ml_networks(struct json_obj *obj_root);

//import config
int json_template_import_config(struct json_obj *obj_root,char *name);

int json_template_optical(struct json_obj *obj_main);
int json_template_electrical_solver(struct json_obj *obj_main);
int json_template_thermal(struct json_obj *obj_main);

//mesh
int json_template_mesh(struct json_obj *obj_root,int x,int y, int z, int t, int l);
int json_mesh_get_points(struct json_obj *mesh_xyz);
double json_mesh_get_len(struct json_obj *mesh_xyz);

int json_template_hard_limit(struct json_obj *obj_main);
int json_template_perovskite(struct json_obj *obj_main);
int json_template_gl(struct json_obj *obj_main);
int json_gl_flyby(struct json_obj *obj);
int json_template_gui_config(struct json_obj *obj_main);
int json_template_world(struct json_obj *obj_main);
int json_shape(struct json_obj *obj);
int json_template_optical_light_sources(struct json_obj *obj_optical);
int json_template_optical_detectors(struct json_obj *obj_optical);
int json_gl_light_object(struct json_obj *obj);

int json_gl_lights_fix_up(struct json_obj *obj_lights);
int json_data_view_gui_3d_fixup(struct json *j);

//world object
int json_world_object(struct json_obj *obj);
int json_world_object_expand_xyz0(struct vec **xyz,int *count,struct json_obj *obj);
int json_world_size(struct json *j, struct vec *my_min, struct vec *my_max);
int json_world_electrical_size(struct json *j, struct vec *my_min, struct vec *my_max);
int json_world_thermal_size(struct json *j, struct vec *my_min, struct vec *my_max);
int json_world_object_get_min_max(struct vec *my_min, struct vec *my_max, struct json_obj *obj);
int json_get_shape_from_segment_path(struct shape *s, struct json *j, char *path, int n);
int json_world_rescale(struct json *j, double rx, double ry, double rz);

int json_load_triangles_ittr(struct json_obj *in,struct paths *paths);
int json_load_triangles(struct json *j,struct paths *paths);

//contacts
int get_top_contact_layer(struct json *j);
int get_btm_contact_layer(struct json *j);
int json_fixup_new_contact_size(struct json *j,char *contact_path);
int json_fixup_contacts(struct json *j);

//epitaxy
int json_epitaxy_enforce_rules(struct json *j);
int json_epitaxy_get_n_segments(struct json *j);
double json_epitaxy_get_layer_start(struct json *j,int layer);
double json_epitaxy_get_layer_stop(struct json *j,int layer);
int json_epitaxy_symc_to_mesh(struct json *j);
double json_epitaxy_get_len(struct json *j);
double json_epitaxy_get_device_start(struct json *j);
int json_epitaxy_find_first_active_layer(struct json *j);
int json_epitaxy_project_values_to_mesh(double *x, double *y,int len, char *token0, char *token1, char *sub_path,struct json *j);

//groups
int json_groups_get_all_linked_uids(struct json_string *buf,struct json *j,char *search_uid);


//material db
int json_db_electrical_constants(struct json_obj *obj_main);
int json_db_materials(struct json *j);
int json_db_spectra(struct json *j);
int json_db_filter(struct json *j);

//shape db
int json_shape_db_threshold(struct json_obj *obj_main);
int json_shape_db_threshold(struct json_obj *obj_main);
int json_shape_saw_wave(struct json_obj *obj_main);
int json_shape_db_blur(struct json_obj *obj_main);
int json_shape_db_mesh(struct json_obj *obj_main);
int json_shape_boundary(struct json_obj *obj_main);
int json_shape_db_item_import(struct json_obj *obj_main);
int json_shape_db_item_lens(struct json_obj *obj_main);
int json_shape_db_item_xtal(struct json_obj *obj_main);
int json_shape_db_item_honeycomb(struct json_obj *obj_main);
int json_shape_db_item_gaus(struct json_obj *obj_main);
int json_db_shape(struct json *j);
int json_db_morphology(struct json *j);

//json folders
int json_folder_material(struct json *j);
int json_folder_backup(struct json *j);
int json_folder_backup_main(struct json *j);
int json_folder_multi_plot_dir(struct json *j);
int json_folder_morphology(struct json *j);
int json_folder(struct json *j);

//bib
int json_template_bib(struct json_obj *obj);

//snapshots
int json_folder_snapshots(struct json *j);

//program
int json_template_program(struct json_obj *obj_in);

//update item
int json_template_update_item(struct json *j);

//gui_config
int json_data_view_gui_configs(struct json *j);

#endif
