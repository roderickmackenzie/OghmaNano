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
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include <g_io.h>
#include <inp.h>

int zip_write_buffer(struct simulation *sim,char *full_file_name,char *buffer, int len)
{
int err = 0;
int	in_zip_file= -1;
int	outside_zip_file= -1;
char zip_path[OGHMA_PATH_MAX];
char file_path[OGHMA_PATH_MAX];
char file_name[OGHMA_PATH_MAX];

in_zip_file=zip_is_in_archive(full_file_name);
outside_zip_file=isfile(full_file_name);

if ((in_zip_file!=0)||(outside_zip_file==0))
{
	FILE* out_fd;
	out_fd =  g_fopen(full_file_name, "wb");

	if (sim!=NULL)
	{
		sim->files_written++;
	}

	if (out_fd== NULL)
	{
		ewe(sim,"File %s can not be opened\n",full_file_name);
	}

	fwrite( buffer, len*sizeof(char),1,out_fd);

	fclose(out_fd);
}else
{
	get_dir_name_from_path(file_path,full_file_name);
	get_file_name_from_path(file_name,full_file_name,OGHMA_PATH_MAX);

	join_path(2,zip_path,file_path,"sim.oghma");


	struct zip *z = zip_open(zip_path, 0, &err);
	zip_close(z);

	//Not sure why this is here taken out 30/03/2023
/*	z = zip_open(zip_path, 0, &err);
	zip_close(z);

	z = zip_open(zip_path, 0, &err);
	zip_close(z);

	z = zip_open(zip_path, 0, &err);
	zip_close(z);

	z = zip_open(zip_path, 0, &err);
	zip_close(z);*/

	z = zip_open(zip_path, 0, &err);

	if(!z || err != ZIP_ER_OK)
	{
		exit(0);
	}


	if (z!=NULL)
	{
		struct zip_source *s;
		s=zip_source_buffer(z, buffer, len,0);
		err=-1;
		//For cluster compatability this is defined in newver versions of zip lib
		#ifdef ZIP_FL_OVERWRITE
		err=zip_file_add(z, file_name, s, ZIP_FL_OVERWRITE);
		#endif
		if (err==-1)
		{
			ewe(sim,"zip write error");
		}
		zip_close(z);

	}else
	{
		ewe(sim,"zip write error");
		return -1;
	}

}
return 0;
}

