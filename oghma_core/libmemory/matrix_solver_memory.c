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

/** @file memory.c
@brief get/free memory
*/


#include <enabled_libs.h>

	#define _GNU_SOURCE
	#include <dlfcn.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lang.h>
#include "sim.h"
#include "dump.h"
#include "mesh.h"
#include <math.h>
#include "log.h"
#include <solver_interface.h>
#include <circuit.h>
#include "memory.h"
#include "ray_fun.h"
#include "newton_tricks.h"
#include "shape.h"

void matrix_solver_memory_check_memory(struct simulation *sim,struct matrix_solver_memory *msm,int col,int nz)
{
double *dtemp;
int *itemp;
	if (msm->last_col!=col)
	{
		//printf("realloc\n");
		dtemp = realloc(msm->x,col*sizeof(double));
		if (dtemp==NULL)
		{
			printf("realloc failed\n");
		}else
		{
			msm->x=dtemp;
		}


		dtemp = realloc(msm->b,col*sizeof(double));
		if (dtemp==NULL)
		{
			printf("realloc failed\n");
		}else
		{
			msm->b=dtemp;
		}

		itemp = realloc(msm->Ap,(col+1)*sizeof(int));
		if (itemp==NULL)
		{
			printf("realloc failed\n");
		}else
		{
			msm->Ap=itemp;
		}
	}

	if (msm->last_nz!=nz)
	{
		//printf("realloc\n");

		itemp = realloc(msm->Ai,(nz)*sizeof(int));
		if (itemp==NULL)
		{
			printf("realloc failed\n");
		}else
		{
			msm->Ai=itemp;
		}

		dtemp  = realloc(msm->Ax,(nz)*sizeof(double));
		if (dtemp==NULL)
		{
			printf("realloc failed\n");
		}else
		{
			msm->Ax=dtemp;
		}

		dtemp  = realloc(msm->Tx,(nz)*sizeof(double));
		if (dtemp==NULL)
		{
			printf("realloc failed\n");
		}else
		{
			msm->Tx=dtemp;
		}

	}

	msm->last_col=col;
	msm->last_nz=nz;
}


void matrix_solver_memory_init(struct matrix_solver_memory *msm)
{
		//Matrix solver -	external dll
	msm->last_col=0;
	msm->last_nz=0;
	msm->x=NULL;
	msm->Ap=NULL;
	msm->Ai=NULL;
	msm->Ax=NULL;
	msm->b=NULL;
	msm->Tx=NULL;

	//Complex matrix solver -	external dll
	msm->c_last_col=0;
	msm->c_last_nz=0;
	msm->c_x=NULL;
	msm->c_xz=NULL;
	msm->c_Ap=NULL;
	msm->c_Ai=NULL;
	msm->c_Ax=NULL;
	msm->c_Az=NULL;
	msm->c_b=NULL;
	msm->c_bz=NULL;
	msm->c_Tx=NULL;
	msm->c_Txz=NULL;

	msm->fd_ext_solver=-1;
	msm->ext_solver_buf_size=-1;
	msm->ext_solver_buf=NULL;
	strcpy(msm->ext_solver_pipe_name,"");
	strcpy(msm->fname_from_solver,"");
	strcpy(msm->fname_to_solver,"");
	msm->fd_from_solver=-1;

	msm->x_matrix_offset=0;
	msm->y_trap_n=0;
	msm->y_trap_p=0;
	msm->ylen_Je_y=0;
	msm->ylen_Jh_y=0;
	msm->ylen_Je_x=0;
	msm->ylen_Jh_x=0;

	/*msm->dll_matrix_handle=NULL;
	msm->dll_matrix_solve=NULL;
	msm->dll_matrix_solver_free=NULL;
	msm->dll_matrix_init=NULL;*/
}


void matrix_solver_memory_free(struct simulation *sim,struct matrix_solver_memory *msm)
{
	//Real part
	if (msm->x!=NULL)
	{
		free(msm->x);
		msm->x=NULL;	
	}

	if (msm->Ap!=NULL)
	{
		free(msm->Ap);
		msm->Ap=NULL;	
	}

	if (msm->Ai!=NULL)
	{
		free(msm->Ai);
		msm->Ai=NULL;	
	}

	if (msm->Ax!=NULL)
	{
		free(msm->Ax);
		msm->Ax=NULL;	
	}

	if (msm->b!=NULL)
	{
		free(msm->b);
		msm->b=NULL;	
	}

	if (msm->Tx!=NULL)
	{
		free(msm->Tx);
		msm->Tx=NULL;	
	}

	//Complex part
	if (msm->c_x!=NULL)
	{
		free(msm->c_x);
		msm->c_x=NULL;	
	}

	if (msm->c_xz!=NULL)
	{
		free(msm->c_xz);
		msm->c_xz=NULL;	
	}

	if (msm->c_b!=NULL)
	{
		free(msm->c_b);
		msm->c_b=NULL;	
	}

	if (msm->c_bz!=NULL)
	{
		free(msm->c_bz);
		msm->c_bz=NULL;	
	}

	if (msm->c_Ap!=NULL)
	{
		free(msm->c_Ap);
		msm->c_Ap=NULL;
	}

	if (msm->c_Ai!=NULL)
	{
		free(msm->c_Ai);
		msm->c_Ai=NULL;
	}

	if (msm->c_Ax!=NULL)
	{
		free(msm->c_Ax);
		msm->c_Ax=NULL;
	}

	if (msm->c_Az!=NULL)
	{
		free(msm->c_Az);
		msm->c_Az=NULL;
	}

	if (msm->c_Tx!=NULL)
	{
		free(msm->c_Tx);
		msm->c_Tx=NULL;
	}

	if (msm->c_Txz!=NULL)
	{
		free(msm->c_Txz);
		msm->c_Txz=NULL;
	}

	msm->c_last_col=0;
	msm->c_last_nz=0;

	msm->last_col=0;
	msm->last_nz=0;

}

