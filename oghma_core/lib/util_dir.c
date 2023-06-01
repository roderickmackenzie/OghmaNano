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

/** @file util.c
	@brief Utility functions.
*/


#include <enabled_libs.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "log.h"
#include <oghma_const.h>
#include <lang.h>
#include <math.h>
#include <ctype.h>
#include <cal_path.h>
#include <g_io.h>

long get_dir_size(char *path)
{
	struct find_file find;
	char full_path[PATH_MAX];
	long s;
	long tot=0;

	if (find_open(&find,path)==0)
	{
		while (find_read(&find)==0)
		{
			join_path(2,full_path,path,find.file_name);
			if (isfile(full_path)==0)
			{
				s=get_file_size(full_path);
				if (s>0)
				{
					tot=tot+s;
				}
				//printf("%s %ld %ld\n",full_path,s,tot);
			}
		}

		find_close(&find);
	}
	return tot;
}

int get_dir_min_max_file_age(char *path,long *min, long *max)
{
	struct find_file find;
	char full_path[PATH_MAX];
	long age=0;
	int n=0;
	if (find_open(&find,path)==0)
	{
		while (find_read(&find)==0)
		{
			join_path(2,full_path,path,find.file_name);
			if (isfile(full_path)==0)
			{
				age=get_file_modification_date(full_path);
				if (n==0)
				{
					*min=age;
					*max=age;
				}

				if (age<*min)
				{
					*min=age;
				}else
				if (age>*max)
				{
					*max=age;
				}

				n++;
			}
		}

		find_close(&find);
	}
	return 0;
}

void mkdirs(char *dir)
{

	int i;
	char temp[PATH_MAX];
	strcpy(temp,dir);
	for (i=0;i<strlen(dir);i++)
	{
		if (((temp[i]=='/')||(temp[i]=='\\'))&&(i!=0))
		{
			temp[i]=0;
			if (isdir(temp)!=0)
			{
				g_mkdir(temp);
			}
			strcpy(temp,dir);
		}
	}

	if (isdir(dir)!=0)
	{
		g_mkdir(dir);
	}

}
