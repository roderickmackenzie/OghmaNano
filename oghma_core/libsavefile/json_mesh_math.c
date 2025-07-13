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

int json_mesh_get_points(struct json_obj *mesh_xyz)
{

	int i;
	int segments;
	int enabled;
	char temp[200];
	int count=0;
	int points=0;
	struct json_obj *json_seg;

	json_get_int(NULL, mesh_xyz, &segments,"segments",TRUE);


	json_get_english(NULL, mesh_xyz, &enabled,"enabled",TRUE);
	if (enabled==FALSE)
	{
		return count;
	}


	for (i=0;i<segments;i++)
	{
		sprintf(temp,"segment%d",i);
		json_seg=json_obj_find(mesh_xyz, temp);
		if (json_seg==NULL)
		{
			ewe(NULL,"Object segment not found\n");
		}

		json_get_int(NULL, json_seg, &points,"points",TRUE);
		count+=points;
	}

	return count;
}

double json_mesh_get_len(struct json_obj *mesh_xyz)
{

	int i;
	int segments;
	int enabled;
	char temp[200];
	double tot_len=0.0;
	double len=0.0;
	struct json_obj *json_seg;

	json_get_int(NULL, mesh_xyz, &segments,"segments",TRUE);

	json_get_english(NULL, mesh_xyz, &enabled,"enabled",TRUE);


	for (i=0;i<segments;i++)
	{
		sprintf(temp,"segment%d",i);
		json_seg=json_obj_find(mesh_xyz, temp);
		if (json_seg==NULL)
		{
			ewe(NULL,"Object segment not found\n");
		}

		json_get_double(NULL, json_seg, &len,"len",TRUE);
		tot_len+=len;
	}

	return tot_len;
}

