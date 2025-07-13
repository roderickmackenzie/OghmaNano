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

/** @file buffer.c
@brief used to save output files to disk with a nice header, so the user knows what was writtne to them
*/

#include <sys/stat.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>
#include "util.h"
#include "dat_file.h"
#include "cal_path.h"
#include "dump.h"
#include <log.h>
#include <g_io.h>
#include <triangle.h>
#include <triangles.h>
#include <json.h>
#include <color.h>

int yml_peek_is_mat_file(char *buf, long len)
{
	int ret=0;
	long pos=0;
	char line[STR_MAX];
	int data_found=FALSE;
	int type_found=FALSE;
	int lines=0;
	ret=get_line(line,buf,len,&pos,sizeof(line));
	while(ret!=-1)
	{
		if (ret>0)
		{
			remove_space_after(line);
			remove_space_before(line);
		}

		if (strcmp_begin(line,"DATA:")==0)
		{
			data_found=TRUE;
		}

		if (strcmp_begin(line,"- type")==0)
		{
			type_found=TRUE;
		}

		if (str_count(line,"pulse_duration")>0)	//can't do the n2 files
		{
			return -1;
		}

		lines++;

		if (lines>50)
		{
			break;
		}
		ret=get_line(line,buf,len,&pos,sizeof(line));
	}

	if ((data_found==TRUE)&&(type_found==TRUE))
	{
		return 0;
	}


return -1;
}

