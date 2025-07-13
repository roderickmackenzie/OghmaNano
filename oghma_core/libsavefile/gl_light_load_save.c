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

/** @file gl_text.c
	@brief Memory management for i.c
*/
#define _FILE_OFFSET_BITS 64
#define _LARGEFILE_SOURCE
#include <stdlib.h>
#include <string.h>
#include "util.h"
#include "dump.h"
#include <log.h>
#include <g_io.h>
#include <json.h>
#include <memory.h>
#include <oghma_gl.h>

int gl_light_from_json(struct gl_light *out, struct json_obj *obj)
{

	json_get_english(NULL,obj, &(out->enabled),"enabled",TRUE);

	json_get_double(NULL,obj, &(out->x0),"x0",TRUE);
	json_get_double(NULL,obj, &(out->y0),"y0",TRUE);
	json_get_double(NULL,obj, &(out->z0),"z0",TRUE);

	json_get_double(NULL,obj, &(out->color_r),"color_r",TRUE);
	json_get_double(NULL,obj, &(out->color_g),"color_g",TRUE);
	json_get_double(NULL,obj, &(out->color_b),"color_b",TRUE);

	json_get_double(NULL,obj, &(out->color_alpha),"color_alpha",TRUE);
	json_get_string(NULL,obj, out->uid,"id",TRUE);

	return 0;
}

int gl_light_to_json(struct json_obj *obj, struct gl_light *in)
{

	json_set_data_bool(obj,"enabled",in->enabled);

	json_set_data_double(obj,"x0",in->x0);
	json_set_data_double(obj,"y0",in->y0);
	json_set_data_double(obj,"z0",in->z0);

	json_set_data_double(obj,"color_r",in->color_r);
	json_set_data_double(obj,"color_g",in->color_g);
	json_set_data_double(obj,"color_b",in->color_r);
	json_set_data_double(obj,"color_alpha",in->color_alpha);

	json_set_data_string(obj,"id",in->uid);
	return 0;
}


int gl_load_lights(struct gl_main *main, struct json *j)
{
	int i;
	int segments;
	char temp[200];
	struct json_obj *obj_lights;
	struct json_obj *json_segment;
	obj_lights=json_obj_find_by_path(&(j->obj), "gl.gl_lights");
	json_get_int(NULL,obj_lights, &segments,"segments",TRUE);

	if (segments!=6)
	{
		printf("lights is not equal to six\n");
		return -1;
	}

	for (i=0;i<segments;i++)
	{

		sprintf(temp,"segment%d",i);

		json_segment=json_obj_find(obj_lights, temp);
		if (json_segment==NULL)
		{
			printf("Object %s not found\n",temp);
			return -1;
		}

		gl_light_from_json(&(main->lights[i]), json_segment);

	}

	return 0;
}

int gl_save_lights(struct json *j, struct gl_main *main)
{
	int i;
	int segments;
	char temp[200];
	struct json_obj *obj_lights;
	struct json_obj *json_segment;
	obj_lights=json_obj_find_by_path(&(j->obj), "gl.gl_lights");
	json_get_int(NULL,obj_lights, &segments,"segments",TRUE);

	if (segments!=6)
	{
		printf("lights is not equal to six\n");
		return -1;
	}

	for (i=0;i<segments;i++)
	{

		sprintf(temp,"segment%d",i);

		json_segment=json_obj_find(obj_lights, temp);
		if (json_segment==NULL)
		{
			printf("Object %s not found\n",temp);
			return -1;
		}

		gl_light_to_json(json_segment,&(main->lights[i]));

	}

	return 0;
}


