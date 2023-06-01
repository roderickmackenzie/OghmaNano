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

/** @file inp.c
	@brief Input file interface, files can be in .oghma files or stand alone files.
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zip.h>
#include <unistd.h>
#include <fcntl.h>
#include "inp.h"
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <list.h>
#include <g_io.h>

int zip_is_in_archive(char *full_file_name)
{
	char zip_path[OGHMA_PATH_MAX];
	char file_path[OGHMA_PATH_MAX];
	char file_name[OGHMA_PATH_MAX];
	get_dir_name_from_path(file_path,full_file_name);
	get_file_name_from_path(file_name,full_file_name,OGHMA_PATH_MAX);

	join_path(2,zip_path,file_path,"sim.oghma");

	int err = 0;
	struct zip *z = zip_open(zip_path, 0, &err);

	if (z!=NULL)
	{
		//Search for the file of given name
		struct zip_stat st;
		zip_stat_init(&st);
		int ret=zip_stat(z, file_name, 0, &st);
		zip_close(z);

		if (ret!=0)
		{
		 	return -1;
		}

		return 0;
	}else
	{
		return -1;
	}
}
