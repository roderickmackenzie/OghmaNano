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

/** @file matrix_solver_memory.h
	@brief matrix_solver_memory
*/

#ifndef matrix_solver_memory_h
#define matrix_solver_memory_h
#include <g_io.h>
#include <enabled_libs.h>
#include <stdio.h>
#include "cal_path.h"
#include "matrix_tx_data.h"

	#include <unistd.h>
	#include <time.h>
	#include <semaphore.h>


struct matrix_solver_memory
{
	//Matrix solver	-	external dll
		int last_col;
		int last_nz;
		double *x;
		int *Ap;
		int *Ai;
		double *Ax;
		double *b;
		double *Tx;
		int matrix_len_y;


	//electrical matrix options
		int solve_block_x0;
		int solve_block_y0;
		int solve_block_z0;

		int solve_block_x1;
		int solve_block_y1;
		int solve_block_z1;

	//Complex matrix solver - external dll
		int c_last_col;
		int c_last_nz;
		double *c_x;
		double *c_xz;
		int *c_Ap;
		int *c_Ai;
		double *c_Ax;
		double *c_Az;
		double *c_b;
		double *c_bz;
		double *c_Tx;
		double *c_Txz;

	//External solver
	    int fd;
		int shm_size;
	    struct matrix_tx_data *data;
	    sem_t *sem_producer;
		sem_t *sem_consumer;
		int consumer_pid;
		char shm_name[OGHMA_PATH_MAX];
		char sem_name_producer[OGHMA_PATH_MAX];
		char sem_name_consumer[OGHMA_PATH_MAX];
		char external_solver_path[OGHMA_PATH_MAX];
		int last_col_external;
		int last_nz_external;

	int solver_max_cpus;
	int use_lua;
	int dump_error;
	int dump_every_matrix;
	int dump_number;
};

void matrix_solver_memory_init(struct matrix_solver_memory *msm);
void matrix_solver_memory_free(struct simulation *sim,struct matrix_solver_memory *msm);
void matrix_solver_memory_check_memory(struct simulation *sim,struct matrix_solver_memory *msm,int col,int nz);
int matrix_solver_memory_dump_error(struct matrix_solver_memory *msm, double *A, int *Tx, int *Ty, double *x,double *b,int col);
#endif
