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

int json_clip_segment_replace(struct json *j, struct json_obj *obj_target_root, char *paste_object_type, char *buf, int buf_len, char *segment_name)
{
	int name_found=FALSE;
	char human_name[OGHMA_PATH_MAX];
	struct json_obj *obj_new;
	struct json_obj *obj_old;
	struct json_obj *json_seg;
	struct json json_clip;
	struct json_string json_import_segment_text;

	struct json_dump_settings settings;
	struct json_segment_counter counter;

	json_string_init(&json_import_segment_text);
	json_segment_counter_init(&counter);
	json_dump_settings_init(&settings);

	json_init(&json_clip);
	json_import_from_buffer(&json_clip,buf,buf_len);

	if (json_clip_check_paste_object(&json_clip, paste_object_type)!=0)
	{
		json_free(&json_clip);
		return -1;
	}

	json_segment_counter_load(&counter,&json_clip, "paste_data");

	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{

		obj_old=json_obj_find_by_path(obj_target_root, segment_name);
		if (obj_old!=NULL)
		{
			if (json_get_string(NULL, obj_old, human_name,"name",TRUE)==0)
			{
				name_found=TRUE;
			}
		}
		json_dump_to_string(&json_import_segment_text,json_seg,0, &settings);

		json_delete_segment(obj_target_root, segment_name);

		obj_new=json_segments_add(obj_target_root,"none", -1);
		json_import_ojb_from_buffer(j,obj_new,json_import_segment_text.data,json_import_segment_text.len);

		//preserve them name
		if (name_found==TRUE)
		{
			json_set_data_string(obj_new,"name",human_name);
		}

		json_string_free(&json_import_segment_text);
		json_update_random_ids(obj_new);
		break;
	}

	json_free(&json_clip);

	return 0;
}

int json_clip_segment_replace_at_path(struct json *j, char *root_path, char *paste_object_type, char *buf, int buf_len, char *segment_name)
{
	int ret;
	struct json_obj *obj_target_root;
	//target
	obj_target_root=json_obj_find_by_path(&(j->obj), root_path);
	if (obj_target_root==NULL)
	{
		printf("Paste target not found\n");
		return -1;
	}

	ret=json_clip_segment_replace(j, obj_target_root, paste_object_type,  buf, buf_len,segment_name);

	return ret;
}
