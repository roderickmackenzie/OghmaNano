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

int json_template_hard_limit(struct json_obj *obj_main)
{
	struct json_obj *obj_hard_limit;
	struct json_obj *obj_template;

	obj_hard_limit=json_obj_add(obj_main,"hard_limit","",JSON_NODE);
	json_obj_add(obj_hard_limit,"icon_","hard_limit",JSON_STRING);

	obj_template=json_obj_add(obj_hard_limit,"template","",JSON_TEMPLATE);
	json_obj_add(obj_template,"name","hard\\nlimit",JSON_STRING);
	json_obj_add(obj_template,"icon","hard_limit",JSON_STRING);
	json_obj_add(obj_template,"token","Eg",JSON_STRING);
	json_obj_add(obj_template,"min","0.1",JSON_DOUBLE);
	json_obj_add(obj_template,"max","5.0",JSON_DOUBLE);
	json_obj_add(obj_template,"id","",JSON_RANDOM_ID);

	return 0;
}
