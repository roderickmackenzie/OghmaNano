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

int json_template_bib(struct json_obj *obj)
{
	json_obj_add(obj,"author","",JSON_STRING);
	json_obj_add(obj,"title","",JSON_STRING);
	json_obj_add(obj,"journal","",JSON_STRING);
	json_obj_add(obj,"volume","",JSON_STRING);
	json_obj_add(obj,"number","",JSON_STRING);
	json_obj_add(obj,"pages","",JSON_STRING);
	json_obj_add(obj,"year","",JSON_STRING);
	json_obj_add(obj,"doi","",JSON_STRING);
	json_obj_add(obj,"publisher","",JSON_STRING);
	json_obj_add(obj,"address","",JSON_STRING);
	json_obj_add(obj,"booktitle","",JSON_STRING);
	json_obj_add(obj,"isbn","",JSON_STRING);
	json_obj_add(obj,"unformatted","",JSON_STRING);

	return 0;
}

