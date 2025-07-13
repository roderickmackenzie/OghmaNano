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
#include <vec.h>

int json_obj_rescale(struct json_obj *obj, double rx, double ry, double rz)
{
	struct shape s;
	json_populate_shape_from_json_world_object(&s, obj);
	s.x0*=rx;
	s.y0*=ry;
	s.z0*=rz;

	s.dx*=rx;
	s.dy*=ry;
	s.dz*=rz;

	s.dx_padding*=rx;
	s.dy_padding*=ry;
	s.dz_padding*=rz;

	json_save_shape_to_world_object(obj, &s);

	return 0;
}

int json_world_rescale(struct json *j, double rx, double ry, double rz)
{
	struct json_obj *json_seg;
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "world.world_data");
	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_obj_rescale(json_seg,rx,ry,rz);
	}

	json_segment_counter_load(&counter,j, "optical.detectors");
	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_obj_rescale(json_seg,rx,ry,rz);
	}

	json_segment_counter_load(&counter,j, "optical.light_sources.lights");
	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_obj_rescale(json_seg,rx,ry,rz);
	}

	return 0;
}
