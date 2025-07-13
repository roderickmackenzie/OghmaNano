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

/** @file circuit.h
@brief Header files for nodal analysis
*/

#ifndef circuit_h
#define circuit_h
#include <g_io.h>
#include <sim_struct.h>
#include <circuit_struct.h>

void circuit_init(struct circuit *cir);
void circuit_malloc(struct simulation * sim,struct circuit *cir);
void circuit_free(struct simulation * sim,struct circuit *cir);

void circuit_cpy(struct simulation * sim,struct circuit *out,struct circuit *in);
void circuit_alloc_nodes_and_links(struct simulation * sim,struct circuit *cir);
void circuit_build_device(struct simulation * sim,struct circuit *cir,struct device *dev);
void circuit_solve(struct simulation * sim,struct circuit *cir,struct device *dev);
void circuit_apply_voltages(struct simulation * sim,struct circuit *cir,struct device *dev);
void circuit_transfer_to_electrical_mesh(struct simulation * sim,struct circuit *cir,struct device *dev);
double circuit_node_get_I(struct simulation * sim,struct circuit *cir,int n);
struct circuit_node *circuit_add_node(struct simulation * sim,struct circuit *cir,int x,int y,int z,int type);
int circuit_find_node_by_xyz(struct simulation * sim,struct circuit *cir,int x,int y,int z);
void circuit_node_set_type(struct simulation * sim, struct circuit_node *node, int type);
void circuit_print_nodes(struct simulation * sim,struct circuit *cir);
void circuit_print_links(struct simulation * sim,struct circuit *cir);
struct circuit_link *circuit_add_link(struct simulation * sim,struct circuit *cir,struct circuit_link *in_link);
int circuit_load_config(struct simulation * sim,struct circuit *cir,struct json_obj *json_circuit,struct epitaxy *epi);
void circuit_time_step(struct simulation * sim,struct circuit *cir);

void circuit_cal_resistance(struct simulation * sim,struct circuit *cir,struct device *dev);
void circuit_plot_resistance(struct simulation * sim,struct circuit *cir,struct device *dev);
int circuit_find_link(struct simulation * sim,struct circuit *cir,int z0,int x0,int y0, int z1,int x1,int y1);
double circuit_get_max_I(struct simulation * sim,struct circuit *cir);
void circuit_calculate_matrix_pos(struct simulation * sim,struct circuit *cir);
void circuit_cal_device_resistance(struct simulation * sim,struct device *dev);

int link_get_other_end(struct circuit *cir,struct circuit_link *link,int node);
void link_init(struct circuit_link *link);
void circuit_build_and_solve_matrix(struct simulation * sim,struct circuit *cir,struct device *dev, int dump_number);
void circuit_spm(struct simulation * sim,struct device *dev,gdouble x0,gdouble x1,gdouble z0,gdouble z1);
void circuit_malloc_matrix(struct simulation * sim,struct circuit *cir);
int circuit_load_base_config(struct simulation * sim,struct circuit *cir,struct json_obj *json_circuit);
void circuit_build_nodes_using_mesh(struct simulation * sim,struct circuit *cir,struct device *dev);
void circuit_build_links_from_mesh(struct simulation * sim,struct circuit *cir,struct device *dev);

//load
void circuit_load(struct simulation * sim,struct circuit *cir);
int circuit_load_expand(struct simulation * sim,struct circuit *cir, int max_components);

//dump
void circuit_dump_to_obj_file(struct simulation * sim,char *file_name,struct device *dev,struct circuit *cir);
void circuit_dump_I(struct simulation * sim,struct device *dev,char *out_dir);
void circuit_printf_links(struct simulation * sim,struct circuit *cir);
void circuit_dump_iv_labels(struct simulation * sim,struct circuit *cir,char *out_dir);
void circuit_dump_circuit_diagram_snapshot(struct simulation * sim,struct device *dev,char *output_path);
int circuit_dump_links_bin(struct simulation * sim,struct device *dev,struct circuit *cir);
int circuit_dump_nodes_bin(struct simulation * sim,struct device *dev,struct circuit *cir);

//nodes
void circuit_nodes_select(struct simulation * sim,struct circuit *cir,int value);
struct circuit_node * circuit_nodes_find_min_xyz(struct simulation * sim,struct circuit *cir);
void circuit_nodes_flood_fill(struct simulation * sim,struct circuit *cir,int node_index);
struct circuit_node * circuit_nodes_selected_find_maxx_maxy_maxz(struct simulation * sim,struct circuit *cir);
struct circuit_node * circuit_nodes_find_node_x_plus_one(struct simulation * sim,struct circuit *cir,struct circuit_node *base_node);
struct circuit_node * circuit_nodes_selected_find_miny(struct simulation * sim,struct circuit *cir,struct circuit_node *base_node);
void circuit_dump_snapshot(struct simulation * sim,struct device *dev,char *out_dir);
void circuit_dump_I_layers(struct simulation * sim,struct device *dev,char *out_dir);
void circuit_dump_gnuplot(struct simulation * sim,struct device *dev,struct circuit *cir);
int circuit_remove_dead_ends(struct simulation * sim,struct circuit *cir);
int circuit_remove_all_dead_ends(struct simulation * sim,struct circuit *cir);
void circuit_build_nodes_from_layers(struct simulation * sim,struct circuit *cir,struct device *dev);
void circuit_build_links_from_layers(struct simulation * sim,struct circuit *cir,struct device *dev);
int circuit_cal_max_y_node_level(struct simulation * sim,int *max_y,int *node_pos,struct circuit *cir,struct device *dev, int x, int z);
int circuit_cal_min_y_node_level(struct simulation * sim,int *min_y,int *node_pos,struct circuit *cir,struct device *dev, int x, int z);

//node
void circuit_node_init(struct circuit_node *node);
void circuit_node_free(struct circuit_node *node);
void circuit_node_add_link(struct circuit_node *node,int link_index);
void circuit_node_cpy(struct circuit_node *out,struct circuit_node *in);

//Photon gen
int circuit_calculate_number_of_diodes(struct simulation * sim,struct circuit *cir);
void circuit_apply_photo_generation(struct simulation * sim,struct circuit *cir,struct device *dev);

#endif
