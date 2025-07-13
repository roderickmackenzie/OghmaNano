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

/** @file josn_dump.c
	@brief Json file decoder
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
#include <inp.h>
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>

int json_obj_delete_node(struct json_obj *root_node, char *token)
{
	int i;
	char search_token[100];
	struct json_obj *objs;
	struct json_obj *obj_tmp;
	int found=FALSE;
	objs=(struct json_obj* )root_node->objs;
	strcpy(search_token,token);

	for (i=0;i<root_node->len;i++)
	{
		obj_tmp=&(objs[i]);
		if (found==FALSE)
		{
			if (strcmp(obj_tmp->name,search_token)==0)
			{
				json_obj_all_free(obj_tmp);
				found=TRUE;
			}
		}

		if (found==TRUE)
		{
			if (i<root_node->len-1)
			{
				memcpy(&(objs[i]), &(objs[i+1]), sizeof(struct json_obj));

			}
		}
	}

	if (found==TRUE)
	{
		root_node->len--;
		return 0;
	}

	return -1;
}



