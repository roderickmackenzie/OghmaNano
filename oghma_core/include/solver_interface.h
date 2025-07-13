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

/** @file solver_interface.h
@brief an interface load and run sparse solvers from various dlls.
*/

#ifndef h_solver_interface
#define h_solver_interface
#include <g_io.h>
#include <sim_struct.h>
#include <device.h>
int matrix_solver_dll_init(struct matrix_solver_dll *in);
void matrix_solver_dll_load(struct simulation *sim,struct matrix_solver_dll *in);
void matrix_solver_dll_get_mem(struct simulation *sim,struct matrix_solver_dll *in,struct matrix_solver_memory *msm);
void dump_matrix(struct simulation *sim,struct device *in);
void matrix_solver_dll_free(struct simulation *sim,struct matrix_solver_dll *in,struct matrix_solver_memory *msm);
void matrix_solver_dll_unload(struct simulation *sim,struct matrix_solver_dll *in);

//These complex call should be merged witht the above
void complex_solver_init(struct simulation *sim,char *solver_name);
void complex_solver_get_mem(struct simulation *sim,struct matrix_solver_memory *msm);
void complex_solver_free(struct simulation *sim,struct matrix_solver_memory *msm);
void complex_solver_unload_dll(struct simulation *sim);
#endif
