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

#include <stdio.h>
#include <ray.h>
#include <oghma_const.h>
#include <math.h>
#include <stdlib.h>
#include <cal_path.h>
#include <log.h>
#include <ray_fun.h>
#include <triangle.h>
#include <triangles.h>
#include <object_fun.h>
#include <object.h>
#include <util_str.h>

/** @file ray_shapes.c
	@brief Basic shapes for ray tracing
*/


struct object *ray_add_object(struct device *dev,struct triangles *tri)
{
	//btm
	int i;
	struct world *w=&(dev->w);
	object_init(&(w->obj[w->objects]));
	object_malloc(&(w->obj[w->objects]));
	w->obj[w->objects].uid=w->objects;

	if (tri!=NULL)
	{
		for (i=0;i<tri->len;i++)
		{
			add_triangle(w,
							tri->data[i].xy0.x,tri->data[i].xy0.y,tri->data[i].xy0.z,
							tri->data[i].xy1.x,tri->data[i].xy1.y,tri->data[i].xy1.z,
							tri->data[i].xy2.x,tri->data[i].xy2.y,tri->data[i].xy2.z,
							w->objects,
							tri->data[i].object_type);
		}


		object_cal_min_max(&(w->obj[w->objects]));

		triangles_cal_edges(&(w->obj[w->objects].tri));
	}

	w->objects++;

	return &(w->obj[w->objects-1]);
}

int ray_objects_remove_detectors(struct simulation *sim,struct device *dev)
{
	int o;
	struct object *obj;
	struct world *w=&(dev->w);
	for (o=0;o<w->objects;o++)
	{
		obj=&(w->obj[o]);
		if (obj->det!=NULL)
		{
			ray_delete_object(sim,dev,obj->name);
		}
	}

	return 0;
}

int ray_delete_object(struct simulation *sim,struct device *dev,char *serach_name)
{
int o;
struct object *obj;
struct world *w=&(dev->w);
int deleted=FALSE;
	for (o=0;o<w->objects;o++)
	{
		obj=&(w->obj[o]);
		if (serach_name!=NULL)
		{
			if (strcmp(obj->name,serach_name)==0)
			{
				object_free(obj);
				deleted=TRUE;
			}
		}
		if (deleted==TRUE)
		{
			if (o<w->objects-1)
			{
				w->obj[o]=w->obj[o+1];
			}
		}

	}

	if (deleted==TRUE)
	{
		w->objects--;
		return 0;
	}

return -1;
}

void objects_dump(struct simulation *sim,struct device *dev)
{
int o=0;

struct object *obj;
struct world *w=&(dev->w);
printf("Objects (%d) :\n",w->objects);
	for (o=0;o<w->objects;o++)
	{
		obj=&(w->obj[o]);
		printf("%d:%s %d",o,obj->name,obj->tri.len);
		printf("\t(%le,%le,%le)",obj->min.x,obj->min.y,obj->min.z);
		printf("\t(%le,%le,%le) %p\n",obj->max.x,obj->max.y,obj->max.z,obj);
	}

}

int objects_fake_objs_to_array(struct object **objs,struct device *dev)
{
	int o=0;
	int pos=0;
	struct object *obj;
	struct world *w=&(dev->w);
	for (o=0;o<w->objects;o++)
	{
		obj=&(w->obj[o]);
		if (strcmp_begin(obj->name,"fake_obj_")==0)
		{
			objs[pos]=obj;
			pos++;
		}
		
	}

	return pos;
}
