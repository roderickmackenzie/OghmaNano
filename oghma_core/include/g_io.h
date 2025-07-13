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

/** @file g_io.h
@brief Replace the OS file access commands
*/
#include <enabled_libs.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>
#include <list.h>

#ifndef g_io_h
#define g_io_h

#include <oghma_const.h>
#include <g_io_defs.h>

FILE *g_fopen(char *filename, const char *mode);
int g_mkdir(char *file_name);
char *g_getcwd(char *buf, size_t size);
int isdir(char *path);
int isfile(char *file_name);
int islink(char *file_name);
void g_rmfile(char* file_name);
void g_rmdir(char* file_name);

int find_open(struct find_file* find,char *path);
int find_read(struct find_file* find);
int find_close(struct find_file* find);


void *g_dlopen(char *filename);
int g_dlclose(void *handle);

void g_usleep(long l_usec);
int g_get_max_cpus();
void* g_dlsym(void *lib_handle,char *function_name);
int g_fnmatch(char *pat,char *in);

void thread_lock_init(g_pthread_mutex_t *lock);
void thread_lock(g_pthread_mutex_t *lock);
void thread_unlock(g_pthread_mutex_t *lock);
void thread_lock_free(g_pthread_mutex_t *lock);

int running_on_real_windows();
int running_on_wine();
int get_home_dir(char *buffer);
int get_exe_path(char *buffer);
long get_file_modification_date(char *filename);
int g_read_file_to_buffer(char **buf, long *len,char *file_name,int max_read);
long get_file_size(char *filename);
long g_disk_writes();
unsigned long long g_disk_free_from_path(char *path);
int g_get_mounts(struct list *in);
int get_user_name(char **out);

void cpu_usage_init(struct cpu_usage *in);
int cpu_usage_get(struct cpu_usage *in);
size_t g_getline(char **lineptr, size_t *n, FILE *stream);

//internet
typedef void (*progress_callback_t)(int bytes_downloaded, void *user_data1, void *user_data2);
typedef struct
{
    progress_callback_t callback;
    void *user_data1;
    void *user_data2;
} progress_context_t;

int get_file_from_web(char **buffer, const char * const szUrl, progress_context_t *ctx);
long get_remote_file_size(const char *url);
int get_free_port_and_socket(oghma_socket *out_sock, int *out_port);
#endif
