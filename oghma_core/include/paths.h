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


#ifndef paths_h
#define paths_h

struct paths
{
	char *html_path;
	char *user_home_dir;
	char *user_desktop_dir;
	char *user_music_dir;
	char *user_downloads_dir;
	char *python_script_path;
	char *shape_base_path;
	char *morphology_base_path;
	char *filters_base_path;
	char *scripts_base_path;
	char *atmosphere_path;
	char *device_lib_path;
	char *plugins_path;
	char *image_path;
	char *css_path;
	char *flag_path;
	char *lang_path;
	char *spectra_base_path;
	char *cluster_path;
	char *cluster_libs_path;
	char *bib_path;
	char *fonts_path;
	char *video_path;
	char *components_path;
	char *inp_template_path;
	char *guess_of_main_oghma_dir;
	char *materials_base_path;
	char *exe_command;
	char *src_path;
	char *li_path;
	char *text_dump;
	char *materials;
	char *filter_path;
	char *cie_color_path;
	char *shape_path;
	char *morphology_path;
	char *spectra_path;
	char *tmp_path;
	char *tmp_path_fast;
	char *updates;
	char *oghma_local;
	char *newton_cache_path;
	char *external_solver_path;
	char *root_simulation_path;		//Currently on the GUI uses this but the main solver should also

	int dirs;
	int files;
	int search_oghma_local;
	int installed_from_deb;
};

void paths_init(struct paths *in);
void paths_set_python_script_path(struct paths *in, char *path);
void paths_do_search(struct paths *in);
void paths_dump(struct paths *in);
void paths_dump_to_string(char **ret,struct paths *in);
int paths_search_std_locations(char **ret, struct paths *in, char *search_dir, char *file_to_find, char *key_file, int min_size);
int paths_is_file(char **ret,struct paths *in,char *path,char *file_name, char *key_file, int min_size);
int paths_search_for_file(char **ret, struct paths *in, char *file_to_find, char *key_file, int min_size);
void paths_free(struct paths *in);
void paths_dump_to_text(struct paths *in);
void paths_guess_main_oghma_dir_from_exe_path(struct paths *in);
int paths_is_installed_from_deb(struct paths *paths);
#endif
