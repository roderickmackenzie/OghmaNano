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

int json_template_optical_spctral2(struct json_obj *obj_optical)
{
	struct json_obj *obj_spctral2;
	obj_spctral2=json_obj_add(obj_optical,"spctral2","",JSON_NODE);
	json_obj_add(obj_spctral2,"spctral2_lat","36.0",JSON_DOUBLE);
	json_obj_add(obj_spctral2,"spctral2_day","322",JSON_INT);
	json_obj_add(obj_spctral2,"spctral2_hour","12",JSON_INT);
	json_obj_add(obj_spctral2,"spctral2_minute","30",JSON_INT);
	json_obj_add(obj_spctral2,"spctral2_preasure","1.0133",JSON_DOUBLE);
	json_obj_add(obj_spctral2,"spctral2_aod","0.27",JSON_DOUBLE);
	json_obj_add(obj_spctral2,"spctral2_water","1.42",JSON_DOUBLE);
	json_obj_add(obj_spctral2,"spctral2_no2","0.0",JSON_DOUBLE);

	return 0;
}
