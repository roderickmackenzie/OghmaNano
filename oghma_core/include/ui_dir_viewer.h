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

/** @file ui.h
@brief Code to read input files.
*/

#ifndef ui_dir_viewer_h
#define ui_dir_viewer_h

#include <json_struct.h>

#define DIR_VIEWER_DISK 0
#define DIR_VIEWER_JSON 1
struct inode
{
	char icon[128];
	char file_name[256];
	char display_name[256];
	int hidden;
	char type[128];
	int isdir;
	int allow_navigation;
	char sub_icon[128];
	int hide_this_json_file;
	char view_type[256];
	int can_delete;
};

struct dir_viewer
{
	int data_type;
	struct inode this_dir;
	struct inode *files;
	int nfiles;
	int nfiles_max;
	char path[OGHMA_PATH_MAX];
	char last_dir_sum[256];
	int show_hidden;
	int show_back_arrow;
	char root_dir[OGHMA_PATH_MAX];
	int allow_navigation;
	struct json *json_data; 

};

//inode decoder
void inode_init(struct inode *item);
void decode_inode(struct inode *item, char *file_name);
void decode_inode_file(struct inode *item, char *file_name);
int inode_dump(struct inode *item);
int inode_is_hidden(char *file_name);

//dir_viewer
int dir_viewer_reorder(struct dir_viewer *in);
int dir_viwer_sort(struct dir_viewer *viewer);
int dir_viewer_init(struct dir_viewer *in);
struct inode* dir_viewer_add_item(struct dir_viewer *in);
int dir_viewer_free(struct dir_viewer *in);
int dir_viewer_dump(struct dir_viewer *in);
int dir_viwer_build_inode_list(struct dir_viewer *in,struct paths* paths);
int dir_viwer_build_inode_list_disk(struct dir_viewer *in,struct paths* paths);
int dir_viwer_build_inode_list_json(struct dir_viewer *in,struct paths* paths);
int dir_viwer_update_needed(struct dir_viewer *in);
struct inode* dir_viewer_get_inode_from_display_name(struct dir_viewer *in,char *display_name);
int dir_viewer_add_back_arrow(struct dir_viewer *in);
//activated
int dir_viwer_on_item_activated(struct dir_viewer *in,struct paths* paths, char *display_name);
int dir_viwer_on_item_activated_json(struct dir_viewer *in, char *display_name);

#endif
