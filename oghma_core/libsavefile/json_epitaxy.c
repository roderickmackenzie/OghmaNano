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

int json_epitaxy_enforce_rules(struct json *j)
{
	double y_pos=0.0;
	double dx_inner;
	double dy,dy_inner;
	double dz_inner;
	double x_mesh_len=0.0;
	double z_mesh_len=0.0;
	struct json_obj *json_mesh_x;
	struct json_obj *json_mesh_z;
	struct json_obj *json_seg;
	struct json_obj *json_shape_dos;
	struct json_segment_counter counter;
	struct json_segment_counter counter_inner;
	char obj_type[200];
	json_segment_counter_init(&counter);
	json_segment_counter_init(&counter_inner);
	json_mesh_x=json_obj_find_by_path(&(j->obj), "electrical_solver.mesh.mesh_x");
	json_mesh_z=json_obj_find_by_path(&(j->obj), "electrical_solver.mesh.mesh_z");

	x_mesh_len=json_mesh_get_len(json_mesh_x);
	z_mesh_len=json_mesh_get_len(json_mesh_z);

	json_segment_counter_load(&counter,j, "epitaxy");

	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_get_string(NULL, json_seg, obj_type,"obj_type",TRUE);
		json_get_double(NULL, json_seg, &dy,"dy",TRUE);

		json_shape_dos=json_obj_find_by_path(json_seg, "shape_dos");
		json_set_data_bool(json_shape_dos,"enabled",FALSE);
		
		if (strcmp(obj_type,"active")==0)
		{
			json_set_data_bool(json_shape_dos,"enabled",TRUE);
		}

		json_set_data_double(json_seg,"x0",0.0);
		json_set_data_double(json_seg,"z0",0.0);
		json_set_data_double(json_seg,"y0",y_pos);

		json_set_data_double(json_seg,"dx",x_mesh_len);
		json_set_data_double(json_seg,"dz",z_mesh_len);

		y_pos+=dy;
		
		json_segment_counter_load(&counter_inner,j, counter.item_path);
		while((json_seg=json_segment_counter_get_next(&counter_inner))!=NULL)
		{
			json_get_double(NULL, json_seg, &dx_inner,"dx",TRUE);
			json_get_double(NULL, json_seg, &dy_inner,"dy",TRUE);
			json_get_double(NULL, json_seg, &dz_inner,"dz",TRUE);

			if (dx_inner>x_mesh_len)
			{
				json_set_data_double(json_seg,"dx",x_mesh_len);
			}

			if (dz_inner>z_mesh_len)
			{
				json_set_data_double(json_seg,"dz",z_mesh_len);
			}

		}
	}


	return 0;

}

int json_epitaxy_get_n_segments(struct json *j)
{
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy");
	return counter.max;
}

double json_epitaxy_get_layer_start(struct json *j,int layer)
{
	int i=0;
	double y_pos=0.0;
	struct shape s;
	struct json_obj *json_seg;
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy");
	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_populate_shape_from_json_world_object(&s, json_seg);
		i++;

		if (i>layer)
		{
			break;
		}

		y_pos+=s.dy;
	}

	return y_pos;
}

double json_epitaxy_get_layer_stop(struct json *j,int layer)
{
	int i=0;
	double y_pos=0.0;
	struct shape s;
	struct json_obj *json_seg;
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy");
	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_populate_shape_from_json_world_object(&s, json_seg);
		y_pos+=s.dy;
		i++;

		if (i>layer)
		{
			break;
		}
	}

	return y_pos;
}

int json_epitaxy_symc_to_mesh(struct json *j)
{
	int active_layers=0;
	double tot_dy=0.0;
	struct json_obj *json_seg;
	double dy;
	int pos=0;
	char obj_type[200];
	char path[OGHMA_PATH_MAX];
	struct json_segment_counter counter_epi;
	struct json_segment_counter counter_mesh;

	json_segment_counter_init(&counter_epi);
	json_segment_counter_load(&counter_epi,j, "epitaxy");

	json_segment_counter_init(&counter_mesh);
	json_segment_counter_load(&counter_mesh,j, "electrical_solver.mesh.mesh_y");

	while((json_seg=json_segment_counter_get_next(&counter_epi))!=NULL)
	{
		json_get_string(NULL, json_seg, obj_type,"obj_type",TRUE);
		json_get_double(NULL, json_seg, &dy,"dy",TRUE);
		
		if ((strcmp(obj_type,"active")==0)||(strcmp(obj_type,"bhj")==0))
		{
			active_layers++;
			tot_dy+=dy;
		}
	}

	if (counter_mesh.max==1)
	{
		json_seg=json_obj_find_by_path(&(j->obj), "electrical_solver.mesh.mesh_y.segment0");
		if (json_seg==NULL)
		{
			printf("mesh %s not found\n",path);
		}
		json_set_data_double(json_seg,"len",tot_dy);
	}else
	if (counter_epi.max==counter_mesh.max)
	{
		counter_epi.i=0;
		while((json_seg=json_segment_counter_get_next(&counter_epi))!=NULL)
		{
			json_get_string(NULL, json_seg, obj_type,"obj_type",TRUE);
			json_get_double(NULL, json_seg, &dy,"dy",TRUE);
			
			if ((strcmp(obj_type,"active")==0)||(strcmp(obj_type,"bhj")==0))
			{
				sprintf(path,"electrical_solver.mesh.mesh_y.segment%d",pos);
				json_seg=json_obj_find_by_path(&(j->obj), path);
				if (json_seg==NULL)
				{
					printf("mesh %s not found\n",path);
				}
				json_set_data_double(json_seg,"len",dy);
				pos++;
			}
		}
	}

	return 0;
}

double json_epitaxy_get_len(struct json *j)
{
	double y_len=0.0;
	struct shape s;
	struct json_obj *json_seg;
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy");
	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_populate_shape_from_json_world_object(&s, json_seg);
		y_len+=s.dy;
	}

	return y_len;
}

double json_epitaxy_get_device_start(struct json *j)
{
	double dy;
	double tot_dy=0.0;
	char obj_type[200];
	char solver_type[200];
	struct json_obj *json_seg;
	struct json_segment_counter counter;

	json_seg=json_obj_find_by_path(&(j->obj), "electrical_solver");
	if (json_seg==NULL)
	{
		printf("electrical_solver not found\n");
	}

	json_get_string(NULL, json_seg, solver_type,"solver_type",TRUE);
	if (strcmp(solver_type,"circuit")==0)
	{
		return 0.0;
	}

	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy");
	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_get_string(NULL, json_seg, obj_type,"obj_type",TRUE);
		json_get_double(NULL, json_seg, &dy,"dy",TRUE);
		
		if ((strcmp(obj_type,"active")==0)||(strcmp(obj_type,"bhj")==0))
		{
			return tot_dy;
		}
		tot_dy+=dy;
	}

	return -1.0;
}

int json_epitaxy_find_first_active_layer(struct json *j)
{
	int layer=0;
	struct json_obj *json_seg;
	char obj_type[200];
	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy");
	while((json_seg=json_segment_counter_get_next(&counter))!=NULL)
	{
		json_get_string(NULL, json_seg, obj_type,"obj_type",TRUE);
		
		if ((strcmp(obj_type,"active")==0)||(strcmp(obj_type,"bhj")==0))
		{
			return layer;
		}
		layer++;
	}

	return -1;
}

int json_epitaxy_project_values_to_mesh(double *x, double *y,int len, char *token0, char *token1, char *sub_path,struct json *j)
{
	int i=0;
	int layer=0;
	double dy;
	double y0=0.0;
	double y1=0.0;
	struct json_obj *json_layer;
	struct json_obj *json_dos;
	double device_start=json_epitaxy_get_device_start(j);
	double layer_start=0.0;
	double layer_stop=0.0;
	char obj_type[200];
	char path[OGHMA_PATH_MAX];

	if (json_epitaxy_find_first_active_layer(j)==-1)
	{
		return -1;
	}

	struct json_segment_counter counter;
	json_segment_counter_init(&counter);
	json_segment_counter_load(&counter,j, "epitaxy");

	while((json_layer=json_segment_counter_get_next(&counter))!=NULL)
	{
		layer_start=json_epitaxy_get_layer_start(j,layer);
		json_get_double(NULL, json_layer, &dy,"dy",TRUE);
		json_get_string(NULL, json_layer, obj_type,"obj_type",TRUE);
		
		layer_stop=layer_start+dy;

		if (strcmp(sub_path,"")!=0)
		{
			json_dos=json_obj_find_by_path(json_layer, sub_path);
			if (json_dos==NULL)
			{
				printf("shape_dos %s %s not found\n",path,sub_path);
			}
		}else
		{
			json_dos=json_layer;
		}

		if ((strcmp(obj_type,"active")==0)||(strcmp(obj_type,"bhj")==0))
		{

			json_get_double(NULL, json_dos, &y0,token0,TRUE);
			json_get_double(NULL, json_dos, &y1,token1,TRUE);

			while (i<len)
			{

				y[i]=y0+(y1-y0)*(x[i]-layer_start+device_start)/dy;

				i++;

				if (i<len)
				{
					if (x[i]+device_start>=layer_stop)
					{
						break;
					}
				}
			}
		}

		layer++;
	}

	return 0;
}


