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

/** @file util.h
@brief header for cluster functions, too much is in here.
*/
#ifndef util_h
#define util_h

#define TRUE 1
#define FALSE 0

#define BACKLOG 10
#define LENGTH 512 // Buffer length
#include <state.h>

struct state *get_sim();

struct job
{
	char name[100];
	int done;
	int status;
	int cpus_needed;
	char target[100];
	char ip[100];
	int copy_state;
	time_t t_start;
	time_t t_stop;
	time_t t_force_stop;
	int pid;
};


struct node_struct
{
	char ip[100];
	char type[100];
	char host_name[100];
	int cpus;
	int load;
	int sock;
	double load0;
	int max_cpus;
	time_t alive;
};

#include "tx_packet.h"

void packet_init_mutex();
void state_init(struct state *sim);
int nodes_html_load(char *buf);
void stop_all_jobs();
void calpath_set_exe_name(char *in);
char* calpath_get_exe_name();
int send_all(int sock, void *buffer, int length, int encode);
int set_master_load();

struct node_struct* node_find_master();
struct node_struct* node_find(char *ip);

void nodes_print();
int node_add(char *name,char *ip, int cpus,int sock,char *host_name);

void copy_packet(struct tx_struct *out,struct tx_struct *in);
int send_file(struct state *sim,int sockfd,char *base_name,char *file_name,char *target);
void mkdirs(char *dir);
int cmpstr_min(char * in1,char *in2);
int english_to_bin( char * in);
int ewe( const char *format, ...);
char *get_file_name_from_path(char *in);
int get_dir_name_from_path(char *out, char *in);
void join_path(int max, ...);
int head(struct state *sim);
int node(struct state *sim);

int file_rx_and_save(char *file_name,int sock_han,int size);
int send_dir(struct state *sim,int sockfd,const char *name, int level,char *base_name,char *target);

int register_node(int sock);
int send_delete_node(int sock);

void node_delete(char *ip);
struct job* jobs_get_next();
int send_command(int sockfd,char *command,char *dir_name,int cpus);


char* get_my_ip();
int cal_my_ip(int sock);
int get_ip_from_sock(char *out,int sock);
double jobs_cal_percent_finished();
int jobs_remaining();
void jobs_clear_all();
int close_all_open();
int broadcast_to_nodes(struct tx_struct *packet);
int send_packet_to_node(char *node,struct tx_struct *packet);
int nodes_txnodelist();

void remove_dir(char* dir_name);
int isdir(char *dir);
void copy_dir_to_all_nodes(struct state *sim,char *dir);

void jobs_print();
void jobs_reset();
void jobs_add(char *name,char *target,int cpus);
int tx_job_list();

void *rx_loop(void *s);
void run_jobs(struct state *sim);
struct job* get_jobs_array();
int get_njobs();
void set_njobs(int n);


void calpath_set_store_path(char *in);
char* calpath_get_store_path();

struct job* jobs_find_job(char *name);



void textcolor(int color);
void set_porgress_color(int in);
void set_progress_colored();
void set_porgress_nospin();
void set_porgress_noreset();
void set_porgress_max(int in);
void text_progress(double percent);
void progress_clear(int n);
void text_progress_finish();
void set_progress_multi_line_text(char *in);
void set_progress_multi_line();
void text_progress_start(char *in);


int cmp_send_job_list(int sock_han,struct tx_struct *data);
int cmp_node_send_data(struct state *sim,int sock,struct tx_struct *data);
int cmp_get_data(struct state *sim,int sock,struct tx_struct *data);
int cmp_node_runjob(struct state *sim,struct tx_struct *data);
int cmp_addnode(int sock_han,struct tx_struct *data);
int cmp_rxfile(int sock_han,struct tx_struct *data,struct state *sim);
int cmp_addjob(int sock_han,struct tx_struct *data);
int cmp_deletenode(int sock_han,struct tx_struct *data);
int cmp_simfinished(struct state *sim,int sock,struct tx_struct *data);
int cmp_node_killall(int sock,struct tx_struct *data);
int cmp_node_killjob(int sock,struct tx_struct *data);
int cmp_head_killall(int sock,struct tx_struct *data);
int cmp_node_sleep(int sock,struct tx_struct *data);
int cmp_head_sleep(int sock,struct tx_struct *data);
int cmp_node_poweroff(int sock,struct tx_struct *data);
int cmp_head_poweroff(int sock,struct tx_struct *data);
int cmp_sendnodelist(int sock,struct tx_struct *data);
int cmp_head_exe(struct state *sim,int sock,struct tx_struct *data);
int cmp_register_master(int sock,struct tx_struct *data);
int cmp_master_clean(int sock,struct tx_struct *data);
int cmp_slave_clean(int sock,struct tx_struct *data);
int cmp_runjobs(struct state *sim,int sock_han,struct tx_struct *data);
int cmp_head_stop_all_jobs(int sock,struct tx_struct *data);
int cmp_rxloadstats(int sock,struct tx_struct *data);
int cmp_nodeload(int sock,struct tx_struct *data);
int cmp_node_quit(int sock,struct tx_struct *data);
int cmp_head_quit(int sock,struct tx_struct *data);
int cmp_rxsetmaxloads(int sock,struct tx_struct *data);
int cmp_sync_packet_one(int sock_han,struct tx_struct *data);
int cmp_sync_packet_two(struct state *sim,int sock,struct tx_struct *data);
int cmp_delete_all_jobs(int sock,struct tx_struct *data);
int cmp_job_pid(struct state *sim,int sock,struct tx_struct *data);

void encrypt(char *data,int round_len);
void decrypt(char *data,int round_len);
int send_node_load(int sock);

void encrypt_load();
int node_alive_time(struct node_struct* node);
int send_message(char *message);
int recv_all(int sock,char *buf, int buf_len);

int cal_abs_path_from_target(char *full_path,char *target,char *file_name);
int gen_dir_list(char ** out,int *len,int *pos,const char *path,char *base_path);
int tx_sync_packet_one(int sock,char *src, char* target);

void gen_job_list(char *buf);
int jobs_load();
void jobs_save();
int nodes_get_nnodes();
void log_alarm_wakeup (int i);
struct node_struct *nodes_list();
int update_pids(int *list, int *list_len,int want_id);
void kill_all(int want_id);
//Debug
void set_debug(int value);
void debug_printf( const char *format, ...);

#endif
