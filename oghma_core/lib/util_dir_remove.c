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

static char* unused_pchar __attribute__((unused));

struct remove_dir_struct
{
	int delete;
	int tot_files;
	int count;
	int progress_count;
};

void remove_dir_ittr(struct simulation *sim,char* dir_name,int depth, struct remove_dir_struct *data)
{
	depth++;
	struct find_file find;

	char filepath[PATH_MAX];
	if (depth==-1)
	{
		if (data->delete==TRUE)
		{
			printf_log(sim,"%s =%s:",_("Deleting directory: "),dir_name);
		}
		data->progress_count=0;
	}

	if (strcmp_end(dir_name,"..")==0)
	{
		return;
	}

	if (strcmp_end(dir_name,".")==0)
	{
		return;
	}

	if (islink(dir_name)==0)		//I don't delete links
	{
		return;
	}

	//printf("Called with %s\n",dir_name);

	int progress_delta;
	if (data->delete==TRUE)
	{
		progress_delta=data->tot_files/20;
	}

	if (find_open(&find,dir_name)==0)
	{
		while(find_read(&find)==0)
		{
			if ((strcmp(find.file_name,".")!=0)&&(strcmp(find.file_name,"..")!=0))
			{
				join_path(2, filepath,dir_name,find.file_name);
				if (isdir(filepath)==0)
				{
					remove_dir_ittr(sim,filepath,depth,data);
					if (data->delete==TRUE)
					{
						printf_log(sim,"%s: %s\r",_("Deleting directory"),filepath);
						g_rmdir(filepath);
						data->progress_count++;
						if (data->progress_count>progress_delta)
						{
							printf_log(sim,"#");
							data->progress_count=0;
						}
						
					}
					data->count++;
				}else
				{
					if (data->delete==TRUE)
					{
						g_rmfile(filepath);
						if (data->progress_count>progress_delta)
						{
							printf_log(sim,"#");
							data->progress_count=0;
						}
						data->progress_count++;
					}
					data->count++;
				}
			}
		}

		find_close(&find);

		if (depth==0)
		{
			if (data->delete==TRUE)
			{
				g_rmdir(dir_name);
				printf_log(sim,"\n");

			}
		}
	}

	
}

void remove_dir(struct simulation *sim,char* dir_name)
{
	if (strcmp(dir_name,"")==0)
	{
		return;
	}

	if (strcmp_end(dir_name,"..")==0)
	{
		return;
	}

	if (strcmp_end(dir_name,".")==0)
	{
		return;
	}

	if (islink(dir_name)==0)		//I don't delete links
	{
		return;
	}

	struct remove_dir_struct data;
	data.delete=FALSE;
	data.tot_files=0;
	data.count=0;

	remove_dir_ittr(sim,dir_name,-1,&data);

	data.tot_files=data.count;
	data.count=0;
	data.delete=TRUE;

	remove_dir_ittr(sim,dir_name,-1,&data);


}

