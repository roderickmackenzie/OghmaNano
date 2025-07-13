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

/** @file json_to_latex.c
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
#include <token_lib.h>
#include <json.h>
#include <latex.h>

int json_to_latex(struct json_string *buf,struct json_obj *obj,struct hash_list *token_lib)
{
	int i;
	struct json_obj *objs;
	struct json_obj *obj_next;
	struct token_lib_item* item;
	char name[OGHMA_PATH_MAX];
	char units[100];
	latex_document_start(buf);

	latex_tab_start(buf,"Physical constant,Value,Units");
	objs=(struct json_obj* )obj->objs;
	int found=FALSE;

	for (i=0;i<obj->len;i++)
	{
		obj_next=&(objs[i]);

		found=FALSE;
		if (token_lib!=NULL)
		{
			item=token_lib_find(token_lib,obj_next->name);
			if (item!=NULL)
			{
				strcpy(name,item->english);
				strcpy(units,item->units);
				found=TRUE;
			}
		}

		if (found==FALSE)
		{
			strcpy(name,obj_next->name);
			strcpy(name,"?");
		}

		latex_tab_add_row_item(buf,name);
		latex_insert_number(buf,obj_next->data);
		latex_tab_add_row_item(buf,units);
		latex_tab_add_row_end(buf);
	}
	latex_tab_end(buf,"");

	latex_document_end(buf);

	return 0;
}

