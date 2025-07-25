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

/** @file josn_chk_sum.c
	@brief Json checksum
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
#include "lock.h"
#include <json.h>
#include <g_io.h>

void json_chk_sum(struct simulation *sim,struct md5 *sum,struct json_obj *json_in)
{

	int i;

	struct json_obj *obj;
	struct json_obj *objs;

	objs=(struct json_obj* )json_in->objs;

	for (i=0;i<json_in->len;i++)
	{
		obj=&(objs[i]);
		md5_update(sum,obj->name,strlen(obj->name));

		if (obj->data_type==JSON_NODE)
		{
			json_chk_sum(sim,sum,obj);
		}else
		{
			if (strcmp_begin(obj->name,"mue_")!=0)
			{
				if (strcmp_begin(obj->name,"muh_")!=0)
				{
					md5_update(sum,obj->data,strlen(obj->data));
				}
			}
		}


	}

}

int json_checksum_check(struct simulation *sim,char *out_check_sum, char *chk_file,struct md5 *in_sum)
{
	FILE *file;
	char newcheck[100];
	char fromfile[100];
	md5_to_str(newcheck,in_sum);

	if (out_check_sum!=NULL)
	{
		strcpy(out_check_sum,newcheck);
	}

	file=g_fopen(chk_file,"r");

	if (!file)
	{
		return FALSE;
	}

	fscanf(file,"%s\n",fromfile);
	fclose(file);
	//printf("%s %s\n",newcheck,fromfile);
	//getchar();

	if (strcmp(newcheck,fromfile)==0)
	{
		return TRUE;
	}else
	{
		return FALSE;
	}

	return 0;

}




