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

#ifndef g_io_defs_h
#define g_io_defs_h

#include <oghma_const.h>



	//dll
		#define EXPORT
	//network
		#define OGHMA_INVALID_SOCKET -1
		#define CLOSESOCKET close
		typedef struct {
			int val;
			int padding;
		} oghma_socket;

	//paths
		#define PATH_SEP "/"
		#define PATH_SEP_CHAR '/'

	//threading
		typedef pthread_mutex_t g_pthread_mutex_t;

	//other
		#define _GNU_SOURCE
		#include <dlfcn.h>



#define gdouble double
#define gpow pow
#define gcabs cabs
#define gcreal creal
#define gcimag cimag
#define gfabs fabs
#define gexp exp
#define gsqrt sqrt
#define gsin sin
#define gcos cos
#define gtan tan
#define glog log
#define glog10 log10

struct cpu_usage
{
	double work_jiffies0;
	double total_jiffies0;

	double work_jiffies1;
	double total_jiffies1;

	int percent;
};

struct find_file
{
	int first_call;
	char file_name[OGHMA_PATH_MAX];
		DIR *han;
};

#endif
