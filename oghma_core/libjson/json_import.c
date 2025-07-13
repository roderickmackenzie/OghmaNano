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

/** @file josn.c
	@brief Json file decoder
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>
#include <ctype.h>
#include <g_io.h>
#include <util_str.h>
#include <memory.h>
#include <zip.h>

int json_import_from_buffer(struct json *j,char *buf,int len)
{
	if (j->raw_data!=NULL)
	{
		printf("Warning buffer raw_data not NULL!\n");
	}
	j->pos=0;
	strcpy(j->path,"");
	j->level=0;
	j->raw_data_len = len;
	j->raw_data = malloc(((j->raw_data_len) + 1)*sizeof(char));
	memcpy(j->raw_data, buf, j->raw_data_len);
	j->raw_data[j->raw_data_len]=0;

	json_decode(j,&(j->obj));
	free_1d((void **)&(j->raw_data));

	return 0;
}

int json_import_ojb_from_buffer(struct json *j,struct json_obj *obj,char *buf,int len)
{
	if (j->raw_data!=NULL)
	{
		printf("Warning buffer raw_data not NULL!\n");
	}
	j->pos=0;
	strcpy(j->path,"");
	j->level=0;
	j->raw_data_len = len;
	j->raw_data = malloc(((j->raw_data_len) + 1)*sizeof(char));
	memcpy(j->raw_data, buf, j->raw_data_len);
	j->raw_data[j->raw_data_len]=0;

	int ret=json_decode(j,obj);
	//printf("DECODE!! '%s' %d\n",j->raw_data,ret);
	if (ret==-1)
	{
		printf("json decode error\n");
	}
	//json_dump_obj(obj);
	//exit(0);
	free_1d((void **)&(j->raw_data));
	return 0;
}
