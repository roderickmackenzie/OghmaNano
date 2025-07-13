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

/** @file vec.h
	@brief Header file for vec.c
*/
#ifndef oghma_glh
#define oghma_glh

#define GL_GLEXT_PROTOTYPES
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glext.h>

#include <vec.h>
#include <dat_file.h>
#include <ft2build.h>
#include <text_lib.h>
#include <vec2d_int.h>
#include <graph.h>
#include <color.h>

//We may have to remove these later
#define GL_POINTS 0x0000
#define GL_LINES 0x0001
#define GL_LINE_LOOP 0x0002
#define GL_LINE_STRIP 0x0003
#define GL_TRIANGLES 0x0004
#define GL_TRIANGLE_STRIP 0x0005
#define GL_TRIANGLE_FAN 0x0006
#define GL_QUADS 0x0007
#define GL_QUAD_STRIP 0x0008
#define GL_POLYGON 0x0009


struct gl_code_block
{
	int gl_array_type;
	int solid_lines;
	int gl_array_points;		//This is how many xzy points there are in the array.
	int gl_line_width;
	float *gl_array_float32C;
	float *gl_array_colors_float32C;
	float slice_plane_x;
	float slice_plane_y;
	int gl_point_size;
};

struct gl_base_object
{
	float r;
	float g;
	float b;
	float alpha;
	float r_false;
	float g_false;
	float b_false;
	float rotate_y;
	float rotate_x;
	int xyz_max;
	int xyz_n;
	struct vec* xyz;
	float dx;
	float dy;
	float dz;
	char render_as[100];
	int selected;
	int moveable;
	int resizable;
	int selectable;
	int allow_cut_view;
	char text[STR_MAX];
	float text_size;
	char html[STR_MAX];
	char id[STR_MAX];
	char id1[STR_MAX];
	char image_path[STR_MAX];
	int blocks_n;
	int blocks_max;
	struct gl_code_block *blocks;
	int deleted;
	unsigned char *image_buf;
	int image_w;
	int image_h;
	unsigned int texture;
	int texture_used;
	int object_type;
	int inside;
};

struct gl_mouse_event
{
	double time;
	struct vec dxyz;
	double rotate_x;
	double rotate_y;

	int working;	//this is what we are going to objects
	int drag;
	int rotate;
	int scale;

	int mouse_mode;
	int button;
	struct vec2d_int xy;
	int angle_delta;
	struct vec2d_int xy_last;

	//defines 3D pos when clicked
	double dxdx;
	double dydx;
	double dzdx;
	double dxdy;
	double dydy;
	double dzdy;

	int last_object_clicked;		//This should be an object but this is for python workaround
};

struct gl_scale
{
	double z_mul;
	double x_mul;
	double y_mul;
	double z_start;
	double x_start;
	double y_start;
	double gl_universe_x0;
	double gl_universe_x1;
	double gl_universe_z0;
	double gl_universe_z1;

	int world_fills_mesh;
	int calculated_world_min_max;
	//real world cords
	struct vec world_min;
	struct vec world_max;
	struct vec electrical_world_min;
	struct vec electrical_world_max;
	struct vec thermal_world_min;
	struct vec thermal_world_max;
	//gl world cords
	struct vec gl_world_min;
	struct vec gl_world_max;
};

struct gl_view
{
	int enabled;
	double xRot;
	double yRot;
	double zRot;
	double x_pos;
	double y_pos;
	double zoom;
	double window_x;
	double window_y;
	double window_w;
	double window_h;
	int enable_view_move;
	struct obj_color background_color;
	int render_grid;
	int render_fdtd_grid;
	int render_cords;
	int render_photons;
	int render_plot;
	int draw_device;
	int optical_mode;
	int plot_graph;
	int show_world_box;
	int show_electrical_box;
	int show_thermal_box;
	int show_detectors;
	int text;
	int dimensions;
	int stars_distance;
	int transparent_objects;
	int draw_rays;
	int ray_solid_lines;
	int render_light_sources;
	int show_gl_lights;
	int show_buttons;
	int stars;
	char name[200];

	//OpenGL
    double projection[16];   // For storing the projection matrix
    double modelview[16];    // For storing the modelview matrix
    int viewport[4];         // For storing the viewport
	double max_angle_shift;
	double cut_through_frac_y;
	double cut_through_frac_z;
	struct color_map_item *color_map_graph;
	struct color_map_item *color_map_graph_last;

	//overlay
	int overlay_enabled;
	unsigned int overlay_texture;
	struct ui_graph *overlay;

	//render
	int last_width;
	int last_height;
};

struct gl_simple_shapes_lib
{
	struct dat_file box;
	struct dat_file stars;
	struct dat_file optical_mode;
};

struct  gl_light
{
	int enabled;

	double x0;
	double y0;
	double z0;

	double color_r;
	double color_g;
	double color_b;
	double color_alpha;

	char uid[100];
};

struct gl_main
{
	int objects_n;
	int objects_max;
	struct gl_base_object *objects;
	int false_color;
	struct text_lib text;
	struct gl_scale scale;
	struct gl_simple_shapes_lib simple_shapes_lib; 
	struct gl_view *active_view;
	struct gl_view *views;
	int n_views;
	int n_views_max;
	struct gl_view view_target;
	struct gl_light *lights;
	int n_lights;
	struct gl_mouse_event mouse_event;
	int ndata;				//graph data
	struct dat_file *data;
};



int gl_code_block_init(struct gl_code_block *in);
int gl_code_block_free(struct gl_code_block *in);


//vectors
int gl_vectors_get_min(struct vec *out,struct dat_file *in);
int gl_vectors_get_max(struct vec *out,struct dat_file *in);
int gl_vectors_sub_vec(struct dat_file *in,struct vec *my_vec);
int gl_vectors_add_vec(struct dat_file *in,struct vec *my_vec);
int gl_vectors_div_vec(struct dat_file *in,struct vec *my_vec);
int gl_vectors_dump(struct dat_file *in);

//code block
int gl_code_block_import_dat_file_ray(struct gl_code_block *out,struct dat_file *dat);
int gl_code_block_import_dat_file_triangles(struct gl_code_block *out,struct dat_file *dat);
int gl_code_block_import_rgb(struct gl_code_block *out,float r, float g, float b,float alpha, int points);
int gl_code_block_slice_triangles(struct gl_code_block *out);
int gl_code_bloc_gen_grid(struct gl_code_block *in,float x0,float x1,float y0,float y1,float z0, float z1,int nx, int ny , int nz);
int gl_photon_sheet(struct gl_code_block *in,float div, int tail);
int gl_code_block_import_rgb_from_dists(struct gl_code_block *out, int points,float div);
int gl_code_block_import_zxyrgb(struct gl_code_block *out,struct dat_file *dat);
int gl_code_block_import_zxyzxyrgb(struct gl_code_block *out,struct dat_file *dat);
int gl_code_block_import_dat_file_zxyd(struct gl_code_block *out,struct gl_scale *scale,struct dat_file *dat, double max_z, double max_y, struct color_map_item *cm);
int gl_code_block_import_dat_file_stars(struct gl_code_block *out,struct dat_file *dat);
int gl_code_block_import_dat_file_rgb(struct gl_code_block *out,struct dat_file *dat);

//gl_scale
int gl_scale_init(struct gl_scale *in);
float project_m2screen_x(struct gl_scale *in,float x);
float project_m2screen_y(struct gl_scale *in,float y);
float project_m2screen_z(struct gl_scale *in,float z);
float project_screen2m_x(struct gl_scale *in,float x);
float project_screen2m_y(struct gl_scale *in,float y);
float project_screen2m_z(struct gl_scale *in,float z);
int gl_project_m2screen_zxy(struct gl_code_block *out,struct gl_scale *s);
void set_m2screen(struct gl_scale *in);
int gl_scale_dump(struct gl_scale *in);

//gl_base_object
int gl_base_object_init(struct gl_base_object *in);
struct vec* gl_base_object_add_xyz(struct gl_base_object *in,float x, float y, float z);
int gl_base_object_free(struct gl_base_object *in);
int gl_base_object_get_xyz(struct vec *out,struct gl_base_object *in, int n);
int gl_base_object_set_xyz(struct gl_base_object *in, int n, struct vec *xyz);
int gl_base_object_match_false_color(struct gl_base_object *in, float r, float g, float b);
int gl_set_color(struct gl_base_object *in, int false_color);
int gl_draw_plane(struct gl_base_object *in, int false_color);
int gl_draw_arrows(struct gl_base_object *in, int false_color);
int gl_draw_cords(struct gl_main *in);
struct gl_code_block* gl_base_object_add_block(struct gl_base_object *in);
struct gl_code_block* gl_base_object_get_block(struct gl_base_object *in, int n);
int gl_render_object(struct gl_main *gl_main, struct gl_base_object *in);
int gl_render_ball(struct gl_main *gl_main, struct gl_base_object *in);
int gl_render_box(struct gl_main *gl_main, struct gl_base_object *in);
int gl_render_arrow(struct gl_main *gl_main, struct gl_base_object *in);
int gl_render_image(struct gl_main *gl_main, struct gl_base_object *obj);
void gl_base_object_set_false_color(struct gl_base_object *in,int rgb_char);
int gl_base_object_insert_rgba(struct gl_base_object *in,struct dat_file *dat);
int gl_base_object_get_min_max_zxy(struct gl_base_object *in, struct vec *min, struct vec *max);
int gl_render_marker(struct gl_main *gl_main, struct gl_base_object *in);

//objects
int gl_objects_render(struct gl_main *gl_main);
int gl_objects_selected_colide(struct gl_main *in, struct vec *pos, double dx, double dy, double dz);
int gl_objects_selected_move(struct gl_main *in, float dx, float dy, float dz);
int gl_objects_selected_rotate(struct gl_main *in, float rotate_x, float rotate_y);
int gl_objects_select_by_id(struct gl_main *in, char *id);
int gl_objects_selected_move(struct gl_main *in, float dx, float dy, float dz);
int gl_objects_select_by_inside_value(struct gl_main *in, int inside_value);
int gl_objects_selected_to_list(struct list *out,struct gl_main *in);
int gl_objects_get_min_max(struct gl_main *in, struct vec *min,struct vec *max,int object_type);
int gl_objects_selected_scale(struct gl_main *in, float dx, float dy, float dz);
int gl_optical_mode(struct gl_main *gl_main, char *file_path);

//gl_text
int gl_text_render(struct text_lib_item *in, struct gl_main *gl_main, float x, float y, float z, float size_mul, float rotate_x, float rotate_y);

struct text_lib_item * gl_text_search(struct text_lib *in, char *text, char *id);
int gl_draw_text(struct gl_main* gl_main,struct gl_base_object *obj, char *text, char *id, float x0, float y0, float z0, float size_mul, float rotate_x, float rotate_y);
struct text_lib_item *gl_text_make_new_texture(struct text_lib *in, char *text, char *id,int location);
int gl_render_text(struct gl_main *gl_main,struct gl_base_object *obj,double size_mul);
int gl_cords(struct gl_main *gl_main, float x0, float y0, float z0);

//gl_main
int gl_main_free(struct gl_main *in);
int gl_main_load(struct gl_main *in, struct paths *paths);
struct gl_base_object* gl_main_add_object(struct gl_main *in);
int gl_main_init(struct gl_main *in);
int gl_objects_selected_min_max_vec(struct gl_main *in, struct vec *min,struct vec *max);
int gl_main_object_delete_by_id(struct gl_main *in,char *id);
int gl_main_remove_selection_box(struct gl_main *in);
int gl_selection_box(struct gl_main *gl_main);
int gl_main_clear_objects(struct gl_main *in);
int gl_objects_deselect_all(struct gl_main *in);
struct gl_base_object * gl_objects_find(struct gl_main *in,char *id);
int gl_get_number_objects_selected(struct gl_main *in, int only_real);
int gl_main_link_to_id(struct gl_base_object* in_obj,struct gl_main *in,char *id);
int gl_main_dump(struct gl_main *in);
int gl_are_all_selected_inside_the_same_object(struct gl_main *in);
int gl_set_projection(struct gl_main *main,int w,int h);

//shapes lib - stars
int gl_shapes_lib_load(struct gl_main *in,struct paths *paths);
int gl_shapes_lib_free(struct gl_main *in);
int gl_shapes_lib_init(struct gl_main *in);

int gl_load_stars(struct gl_main *in, char *file_path);
int gl_render_stars(struct gl_main *in, char *file_path);

//gl_view
int gl_view_from_json(struct gl_view *out, struct json_obj *obj);
int gl_view_to_json(struct json_obj *obj, struct gl_view *in);
int gl_view_shift(struct gl_view *view, struct gl_view *target);
int gl_view_init(struct gl_view *in);
int gl_view_rotate_all(struct gl_main *main);
int gl_set_active_view_from_click(struct gl_main *main, int window_w, int window_h);
int gl_view_set_xy(struct gl_view *in);
int gl_view_set_xz(struct gl_view *in);
int gl_view_set_yz(struct gl_view *in);
int gl_view_save_projection_matrix(struct gl_view *view, int window_w, int window_h);
int gl_view_unproject(struct gl_mouse_event *event, struct gl_main *main, int x, int y);
int gl_view_free(struct gl_view *view);

//gl_views
int gl_views_modify_path(char *out, char *in);
int gl_views_enable_by_name(struct gl_main *main,char *name);
int gl_views_enable_by_hash(struct gl_main *main, char *name);
int gl_views_disable_all(struct gl_main *main);
int gl_views_dump(struct gl_main *main);
int gl_views_count_enabled(struct gl_main *main);
int gl_views_zoom(struct gl_main *main);
int gl_load_views(struct gl_main *main, struct json *j,char *views);
int gl_save_views(struct json *j, struct gl_main *main);
int gl_views_move_all_to_target(struct gl_main *main);
int gl_views_free(struct gl_main *main, int remove_array);
int gl_views_is_view(struct gl_main *main,char *view_name);
int gl_views_to_clip(struct json_string *buf, struct gl_main *main,struct json *j);
int gl_views_from_clip(struct json *j, struct gl_main *main, char * text, int text_len);

//main render loop
int gl_render_view(struct gl_main *gl_main,struct gl_view *view, struct paths *paths);

//gl_light
int gl_light_init(struct gl_light *in);
int gl_lights_dump(struct gl_main *main);
int gl_light_from_json(struct gl_light *out, struct json_obj *obj);
int gl_light_to_json(struct json_obj *obj, struct gl_light *in);
int gl_load_lights(struct gl_main *main, struct json *j);
int gl_save_lights(struct json *j, struct gl_main *main);
int gl_lights_add_to_world(struct gl_main *main);
int gl_lights_show(struct gl_main *main);
int gl_update_json(struct json *j, struct gl_main *main);

//detectors
int gl_detectors_show(struct gl_main *main, struct json *j);

//light_srcs
int gl_light_srcs_show(struct gl_main *main, struct json *j);

//import from json
int gl_import_from_json(struct gl_base_object* obj,struct gl_scale *scale,struct json_obj *json_in);

//fdtd
int gl_fdtd_mesh(struct gl_main *main, struct json *j);
int gl_world_grid(struct gl_main *main);
int gl_objects_add_grid(struct gl_main *main,double x0,double x1,double y0,double y1,double z0,double z1,char *uid,double r,double g, double b,char *direction);
int gl_objects_add_grid2(struct gl_main *main,struct json_obj *in);
struct gl_base_object* gl_shape_to_screen(struct gl_main *main, struct json *j, struct json_obj *s, char *base_id, int object_type,int epitaxy);
int gl_world_shapes_to_screen(struct gl_main *main, struct json *j);

//device
int gl_draw_device(struct gl_main *main, struct json *j, double z, double x);
int gl_make_new_shape_in_world(struct json *j, struct gl_main *main,struct paths *paths);
int gl_make_new_light_soruce_in_world(struct json *j, struct gl_main *main,struct paths *paths);
int gl_draw_emission(struct gl_main *main, struct json *j);
int gl_emission_arrow_to_screen(struct gl_main *main);

//groups
int gl_objects_selected_is_exact_group(char *uid,struct json *j,struct gl_main *main);
int gl_group_make_new_group_from_selected(struct json *j,struct gl_main *main);
int gl_group_ungroup_selected(struct json *j,struct gl_main *main);

//align
int gl_objects_align(struct json *j,struct gl_main *main, char *token, int opp_min);
int gl_objects_distribute(struct json *j,struct gl_main *main, char *token_x, char *token_dx);

//graphs
int gl_graph_load_file(struct gl_main *main, char *file_name, int rescale, int distribute);
int gl_graph_free_files(struct gl_main *main);
int gl_draw_graph(struct gl_main *main, struct dat_file *data);
int gl_draw_graphs(struct gl_main *main);
int draw_graph_rays(struct gl_main *main, struct dat_file *data);
int draw_graph_triangles(struct gl_main *main, struct dat_file *data, int solid, int line_width, double line_alpha);

//mouse event
int gl_mouse_event_init(struct gl_mouse_event *in);
int gl_mouse_move(struct gl_main *in, int w, int h);
int gl_mouse_release(struct gl_mouse_event *in);
int gl_mouse_press(struct gl_mouse_event *in);
int gl_mouse_wheel(struct gl_main *main, int w, int h);

//cordinates
int gl_world_box(struct gl_main *in);
int gl_electrical_mesh_box(struct gl_main *in);
int gl_thermal_mesh_box(struct gl_main *in);

//overlay
int gl_overlay_malloc(struct gl_view *view, struct paths *paths);
int gl_overlay_render(struct gl_main *gl_main,struct gl_view *view);
#endif
