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

/** @file josn_init.c
	@brief Json file decoder
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>
#include <rand.h>

struct json_obj *json_add_bib_item(struct json *j, struct json_obj *root_obj, char *token)
{
	struct json_obj *bib_obj;
	char bib_token[100];
	if (strcmp_begin(token,"bib_")!=0)
	{
		sprintf(bib_token,"bib_%s",token);
	}else
	{
		strcpy(bib_token,token);
	}

	bib_obj=json_obj_find(root_obj, bib_token);
	if (bib_obj==NULL)
	{
		bib_obj=json_obj_add(root_obj,bib_token,"",JSON_NODE);
	}
							
	json_obj_all_free(bib_obj);
	json_obj_cpy(bib_obj,&(j->bib_template));
	bib_obj->data_type=JSON_NODE;
	strcpy(bib_obj->name,bib_token);
	//json_dump_obj(obj);

	return bib_obj;
}


int json_bib_cite(struct json_string *buf,struct json_obj *bib_obj)
{
	int i;
	struct json_obj *obj;

	for (i=1;i<6;i++)
	{
		switch(i)
		{
			case 0:
				obj=json_obj_find_by_path(bib_obj, "author");
				break;
			case 1:
				obj=json_obj_find_by_path(bib_obj, "title");
				break;
			case 2:
				obj=json_obj_find_by_path(bib_obj, "journal");
				break;
			case 3:
				obj=json_obj_find_by_path(bib_obj, "volume");
				break;
			case 4:
				obj=json_obj_find_by_path(bib_obj, "pages");
				break;
			case 5:
				obj=json_obj_find_by_path(bib_obj, "year");
				break;
		};

		if (obj!=NULL)
		{
			if (strcmp(obj->data,"")!=0)
			{
				json_string_cat(buf,obj->data);
				json_string_cat(buf,", ");
			}
		}
	}
	
	json_string_del_last_chars(buf,2);

	return 0;
}
