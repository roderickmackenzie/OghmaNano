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
#include <savefile.h>

int json_dump_bib_to_string(struct json_string *buf,struct json_obj *obj, struct json_dump_settings *settings)
{
	int i;
	int ii;
	struct json_obj *bib_item;
	struct json_obj *bib_sub_item;
	struct json_obj *bib_sub_objs;
	struct json_obj *objs;
	objs=(struct json_obj* )obj->objs;
	struct json_string build;
	json_string_init(&build);

	for (i=0;i<obj->len;i++)
	{
		bib_item=&(objs[i]);

		if (bib_item->data_type==JSON_NODE)
		{

			bib_sub_objs=(struct json_obj* )bib_item->objs;
			json_string_clear(&build);

			for (ii=0;ii<bib_item->len;ii++)
			{
				bib_sub_item=&(bib_sub_objs[ii]);
				if (strcmp(bib_sub_item->data,"")!=0)
				{
					json_string_cat(&build,"  ");
					json_string_cat(&build,bib_sub_item->name);
					json_string_cat(&build," = {");
					json_string_cat(&build,bib_sub_item->data);
					json_string_cat(&build,"},\n");
				}
			}

			if (build.pos>0)
			{
				//printf("adding '%s' %d\n",build.data,build.pos);
				json_string_cat(buf,"@article{");
				json_string_cat(buf,bib_item->name);
				json_string_cat(buf,",\n");
				json_string_cat(buf,build.data);
				json_string_del_last_chars(buf,2);
				json_string_cat(buf,"\n}\n\n");
			}
			
		}
	}

	json_string_free(&build);
	return 0;
}
