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

/** @file server.h
@brief header file for the internal server used to run jobs across multiple CPUs
*/

#ifndef serverh
#define serverh
#include <g_io.h>
#include <sim_struct.h>
#include <server_struct.h>
#include <json.h>

//server2
void server2_malloc(struct simulation *sim,struct server_struct *server);
void server2_free(struct simulation *sim,struct server_struct *server);
void server2_add_job(struct simulation *sim,struct server_struct *server,struct job *j_in);
int server_add_cmd_line_job(struct server_struct *server,char *command, char *path, char *args);
void server2_jobs_run(struct simulation *sim,struct server_struct *server,struct batch_id *batch_id);
struct worker* server2_get_next_worker(struct simulation *sim,struct server_struct *server);
void server2_job_finished(struct simulation *sim,struct job *j);
void server2_run_until_done(struct simulation *sim,struct server_struct *server,struct batch_id *batch_id);
void server_config_load(struct simulation *sim,struct server_struct *server,struct json_obj *json_server);
void server2_free_finished_jobs(struct simulation *sim,struct server_struct *server, struct batch_id *batch_id);
void server2_get_next_batch_id(struct simulation *sim,struct batch_id *batch_id, struct server_struct *server);

int server_worker_detect_ended(struct server_struct *server, struct worker *w);
void server_stop_and_exit();
void server_shut_down(struct simulation *sim,struct server_struct *myserver);
void server_init(struct server_struct *server);
void change_cpus(struct simulation *sim,struct server_struct *myserver);
void server_set_lock_file(struct server_struct *myserver, char *file_name);
struct job *server_get_next_job(struct server_struct *server, struct batch_id *batch_id);

void server_set_dbus_finish_signal(struct server_struct *myserver, char *signal);

//jobs
struct job *server_jobs_find_by_lock_file_name(struct server_struct *server, char *lock_file_name);
int server_jobs_clear(struct server_struct *server);
struct job *server_jobs_find_by_number(struct server_struct *server, int number);

//Dump
void server2_dump_jobs(struct server_struct *server);
void server2_dump_workers(struct simulation *sim,struct server_struct *server);
void server2_dump_jobs_full(struct server_struct *server);

//Run control
void server_update_last_job_time(struct server_struct *server);
void server_check_wall_clock(struct simulation *sim,struct server_struct *myserver);

//job
void job_init(struct job *j);
void job_free_data(struct job *j);
void job_set_ip(struct job *j, char *ip);
void job_set_full_command(struct job *j, char *full_command);
void job_set_args(struct job *j, char *args);
void job_set_lock_file_name(struct job *j, char *lock_file_name);
void job_dump(struct job *j);

//worker
void server_worker_init(struct worker *w, int nw);
void server_worker_clean(struct worker *w);

//stats
int server_stats_init(struct server_struct *server);
int server_stats_print(struct simulation *sim,struct server_struct *server);
double server_get_odes_per_s(struct server_struct *server);
double server_get_jobs_per_s(struct server_struct *server);
int job_mark_as_running(struct job *j);
int job_mark_as_finished(struct job *j);

//errors
int server_jobs_check_warnings(struct server_struct *server, char *buf,int max_len);

//count
int server2_count_finished_micro_jobs(struct simulation *sim,struct server_struct *server);
int server2_count_all_micro_jobs(struct simulation *sim,struct server_struct *server);
int server2_count_all_jobs(struct server_struct *server);
int server2_jobs_left(struct server_struct *server, struct batch_id *batch_id);
int server2_count_finished_jobs(struct server_struct *server);
int server_count_jobs_running(struct server_struct *server, struct batch_id *batch_id);

//alarm
int server_stop_crashed_jobs(struct server_struct *server, int max_job_time);

//execute
void server_system_exe(struct server_struct *server,struct job *j,int pipe_to_null);

//batch id
void batch_id_init(struct batch_id *b);
void batch_id_cpy(struct batch_id *out,struct batch_id *in);
#endif
