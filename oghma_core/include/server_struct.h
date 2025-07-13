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

/** @file server_struct.h
@brief a struct to hold server jobs in.
*/

#ifndef server_struct_h
#define server_struct_h

#include <g_io.h>
#include <ipc.h>
#include <time.h>
#include <enabled_libs.h>
	#include <pthread.h>

#include <oghma_const.h>

struct server_packet
{
	int val;
	char buf[20];
	int odes;
	int tot_jobs;
	double data_double0;
};

struct worker
{
	int working;
		pthread_t thread_han;
		int pipefd[2];
	int worker_n;
	void *job;		//points to the job
};

struct batch_id
{
	int id;
	int max_cpus;
};

struct job
{
	char name[400];
	int status;
	int batch_id;
		void *(* fun)(void *);		//Function to call
	void *sim;
	void *server;
	void * data0;
	void * data1;
	void * data2;
	void * data3;
	void * data4;
	void * data5;
	int data_int0;
	int data_int1;
	int data_int2;
	int data_int3;
	int data_int4;
	int data_int5;
	int cpus;
	struct worker *w;
	int process_type;	//SERVER_THREAD, SERVER_PROCESS, SERVER_SYSTEM	
	void * next;
	int micro_jobs_done;
	int micro_jobs_tot;
	
	//feedback
	int odes;
	int tot_jobs;
	double data_double0;

	//timings
	long long start_time;		//time_t
	long long end_time;			//time_t

	//data for system exec jobs
	char path[STR_MAX];
	char args[STR_MAX];
	char full_command[STR_MAX];
	char ip[40];
	char lock_file_name[40];	//This should not really be used

};

struct server_struct
{
	char dbus_finish_signal[256];
	char lock_file[OGHMA_PATH_MAX];
	int jobs;
	int jobs_running;

	int min_cpus;

	//run control
	int max_run_time;
	long long start_time;		//time_t
	long long end_time;			//time_t
	int last_job_ended_at;
	int allow_fake_forking_on_windows;

	//server2
	int max_threads;
	int worker_max;
	int steel;
	int poll_time;
	struct worker *workers;

	struct job *j;
	int send_progress_to_gui;

	//gpu
	int use_gpu;
	int enable_micro_job_reporting;

	//mutex
	g_pthread_mutex_t *lock;

	//Not sure needed
	int batch_id;
	int max_forks;

	//stats
	int quiet;
	int tot_odes;
	int tot_jobs;
	double stats_start_time;
	double stats_stop_time;
	double server_jobs_per_s;
	double server_odes_per_s;
	struct ipc ipc_data;
};



#endif
