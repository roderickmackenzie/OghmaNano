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


int json_template_optical_detectors(struct json_obj *obj_optical)
{
	struct json_obj *obj_detectors;
	struct json_obj *obj_detector_template;
	struct json_obj *text;
	obj_detectors=json_obj_add(obj_optical,"detectors","",JSON_NODE);
	obj_detector_template=json_obj_add(obj_detectors,"template","",JSON_TEMPLATE);
	json_world_object(obj_detector_template);
	json_obj_add(obj_detector_template,"icon","jv",JSON_STRING);
	text=json_obj_add(obj_detector_template,"text_detector","",JSON_STRING);
	text->data_flags=JSON_PRIVATE;
	json_obj_add(obj_detector_template,"viewpoint_nx","8",JSON_INT);
	json_obj_add(obj_detector_template,"viewpoint_nz","8",JSON_INT);

	return 0;
}
