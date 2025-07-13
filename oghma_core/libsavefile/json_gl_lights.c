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
#include <oghma_gl.h>

int json_gl_lights_fix_up(struct json_obj *obj_lights)
{
	struct gl_light light;
	struct json_obj *seg;

	int segments;

	json_get_int(NULL, obj_lights, &segments,"segments",TRUE);

	if (segments!=6)
	{
		json_clear_segments(obj_lights);

		seg=json_segments_add(obj_lights,"", -1);
		gl_light_from_json(&light, seg);
		light.enabled=TRUE;
		light.x0=0.0;
		light.y0=5.0;
		light.z0=-10.0;
		light.color_r=1.0;
		light.color_g=1.0;
		light.color_b=1.0;
		gl_light_to_json(seg, &light);

		seg=json_segments_add(obj_lights,"", -1);
		gl_light_from_json(&light, seg);
		light.enabled=TRUE;
		light.x0=0.0;
		light.y0=-5.0;
		light.z0=-10.0;
		light.color_r=1.0;
		light.color_g=1.0;
		light.color_b=1.0;
		gl_light_to_json(seg, &light);

		seg=json_segments_add(obj_lights,"", -1);
		gl_light_from_json(&light, seg);
		light.enabled=TRUE;
		light.x0=0.0;
		light.y0=5.0;
		light.z0=10.0;
		light.color_r=1.0;
		light.color_g=1.0;
		light.color_b=1.0;
		gl_light_to_json(seg, &light);

		seg=json_segments_add(obj_lights,"", -1);
		gl_light_from_json(&light, seg);
		light.enabled=TRUE;
		light.x0=0.0;
		light.y0=-5.0;
		light.z0=10.0;
		light.color_r=1.0;
		light.color_g=1.0;
		light.color_b=1.0;
		gl_light_to_json(seg, &light);

		seg=json_segments_add(obj_lights,"", -1);
		gl_light_from_json(&light, seg);
		light.enabled=TRUE;
		light.x0=-10.0;
		light.y0=-5.0;
		light.z0=0.0;
		light.color_r=1.0;
		light.color_g=1.0;
		light.color_b=1.0;
		gl_light_to_json(seg, &light);

		seg=json_segments_add(obj_lights,"", -1);
		gl_light_from_json(&light, seg);
		light.enabled=TRUE;
		light.x0=10.0;
		light.y0=-5.0;
		light.z0=0.0;
		light.color_r=1.0;
		light.color_g=1.0;
		light.color_b=1.0;
		gl_light_to_json(seg, &light);


		return -1;
	}

	return 0;
}

int json_gl_light_object(struct json_obj *obj)
{
	json_obj_add(obj,"enabled","false",JSON_BOOL);

	json_obj_add(obj,"x0","0.0",JSON_DOUBLE);
	json_obj_add(obj,"y0","0.0",JSON_DOUBLE);
	json_obj_add(obj,"z0","0.0",JSON_DOUBLE);

	json_obj_add(obj,"color_r","0.0",JSON_DOUBLE);
	json_obj_add(obj,"color_g","0.0",JSON_DOUBLE);
	json_obj_add(obj,"color_b","0.0",JSON_DOUBLE);
	json_obj_add(obj,"color_alpha","0.5",JSON_DOUBLE);

	json_obj_add(obj,"id","",JSON_RANDOM_ID);

	return 0;
}
