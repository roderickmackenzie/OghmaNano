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
#include <savefile.h>

int json_py_bib_enforce_citation(struct json *j, char *token)
{
	struct json_obj *obj;
	obj=json_obj_find(&(j->obj), token);	

	if (obj==NULL)
	{
		//printf("token %s not found\n",token);
		//json_dump_obj(&(j->obj));
		obj=json_obj_add(&(j->obj),token,"",JSON_NODE);
		json_template_bib(obj);
		json_save(j);
	}

	return 0;
}

int json_py_bib_short_cite(struct json_string *buf,struct json *j, char *json_path)
{
	struct json_obj *bib_obj;

	bib_obj=json_obj_find_by_path(&(j->obj), json_path);

	if (bib_obj==NULL)
	{
		return -1;
	}

	json_bib_cite(buf,bib_obj);

	return 0;
}


int json_py_bib_get_oghma_citations(struct json_string *single_quote,struct json_string *text,struct json *j,char *user_id)
{
	struct json_obj *obj;
	struct json_obj *objs;
	struct json_obj *json_main;
	int total_papers=0;
	int cite_pos=0;
	int found=0;
	char temp[200];
	int loop=0;

	json_main=&(j->obj);
	total_papers=json_main->len-1;

	if (total_papers<1)
	{
		return -1;
	}

	cite_pos=str_ckecksum(user_id, total_papers);
	cite_pos++;

	if (cite_pos>=json_main->len)
	{
		return -1;
	}

	objs=(struct json_obj *)(json_main->objs);
	while (found<3)
	{
		obj=&(objs[cite_pos]);
		if (found==0)
		{
			if (single_quote!=NULL)
			{
				json_string_cat(single_quote,"<b>If you publish results generated with OghmaNano in a paper, book or thesis you must cite this paper:</b> ");
				json_bib_cite(single_quote,obj);
				json_string_cat(single_quote," and <b>along with these <a href=\"https://scholar.google.co.uk/citations?user=jgQqfLsAAAAJ&hl=en\">two papers</a> in your work</b>.");
			}
		}

		if (text!=NULL)
		{
			sprintf(temp,"<b>%d</b>)",found+1);
			json_string_cat(text,temp);
			json_bib_cite(text,obj);
			
			json_string_cat(text,"<br><br>");
			cite_pos++;
			found++;
		}

		if (cite_pos>=json_main->len)
		{
			cite_pos=1;
		}

		//This is a saftynet function
		if (loop>7)
		{
			break;
		}
		loop++;
	}


	json_string_cat(text,"<br><b>Why do I have to cite these papers</b>?");
	json_string_cat(text,"Because it shows in a permanent way that OghmaNano is being used by the community and the many weekends I put into it produce a result.");
	json_string_cat(text,"This makes it much easier to apply for funding and to continue the development of OghmaNano.  Citing these papers is non-optional.");

	json_string_cat(text,"<br><br>Please do not cite the manual, it is not an officially published document. ");

	return 0;	
}

