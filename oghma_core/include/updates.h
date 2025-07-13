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

/** @file updates.h
@brief Code to read input files.
*/

#ifndef updates_h
#define updates_h
#include <g_io.h>
#include <json.h>
#include <paths.h>

struct update_item
{
	char name[200];
	char web_path[OGHMA_PATH_MAX];
	char web_path_json[OGHMA_PATH_MAX];
	char local_path[OGHMA_PATH_MAX];
	char local_path_json[OGHMA_PATH_MAX];
	long long local_time;
	long long remote_time;
	char local_checksum[50];
	char remote_checksum[50];
	int downloaded;
	int remote_size;
	int local_size;
	int installed;
	int repository_type;
};

struct updates
{
	int nfiles;
	int max_files;
	struct update_item *items;
	int percent;
	char message[OGHMA_PATH_MAX];
	void (*callback)(const char*);
};

//update item
int update_item_init(struct update_item *item);
int update_item_dump(struct update_item *item);

//updates
int updates_init(struct updates *updates);
struct update_item * updates_add_lib(struct updates *updates,char *file_on_disk, char *url, struct paths *paths);
int updates_populate(struct updates *updates, struct paths *paths);
int updates_dump(struct updates *updates);
int updates_check(struct updates *updates);
int updates_get(struct updates *updates);
int updates_install(struct paths *paths, struct updates *updates);
#endif
