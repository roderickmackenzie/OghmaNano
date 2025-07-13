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

/** @file sim.c
@brief init sim structure
*/


#include <enabled_libs.h>
#include <json.h>
#include <savefile.h>
#include <util.h>

int json_groups_get_all_linked_uids(struct json_string *buf,struct json *j,char *search_uid)
{
	int g=0;
	int segments=0;
	char uid[200];
	char temp[200];
	int found=FALSE;
	struct json_obj *json_seg;
	struct json_obj *json_group;
	struct json_segment_counter counter_groups;
	json_segment_counter_init(&counter_groups);
	json_segment_counter_load(&counter_groups,j, "world.groups");
	json_string_cat(buf,search_uid);
	json_string_cat(buf,"\n");

	while((json_group=json_segment_counter_get_next(&counter_groups))!=NULL)
	{
		json_get_int(NULL, json_group, &segments,"segments",TRUE);
		found=FALSE;
		for (g=0;g<segments;g++)
		{
			sprintf(temp,"segment%d",g);
			json_seg=json_obj_find_by_path(json_group, temp);
			if (json_seg==NULL)
			{
				printf("group item %s not found\n",temp);
			}

			json_get_string(NULL, json_seg, uid ,"gid",TRUE);
			if (strcmp(search_uid,uid)==0)
			{
				found=TRUE;
				break;
			}
		}

		if (found==TRUE)
		{
			for (g=0;g<segments;g++)
			{
				sprintf(temp,"segment%d",g);
				json_seg=json_obj_find_by_path(json_group, temp);
				if (json_seg==NULL)
				{
					printf("group item %s not found\n",temp);
				}

				json_get_string(NULL, json_seg, uid ,"gid",TRUE);
				if (strcmp(search_uid,uid)!=0)
				{
					json_string_cat(buf,uid);
					json_string_cat(buf,"\n");
				}
			}
		}
		
		
	}
	json_string_del_last_chars(buf,1);


	return 0;
}




