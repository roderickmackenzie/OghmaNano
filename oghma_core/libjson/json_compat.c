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

/** @file josn.c
	@brief Json file decoder
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>
#include <ctype.h>
#include <g_io.h>
#include <util_str.h>
#include <memory.h>
#include <zip.h>
#include <savefile.h>

//moving things around in a major way
int json_import_old_oghma_file(struct json *j, char *file_name)
{
	int edited=FALSE;
	char str_tmp[OGHMA_PATH_MAX];
	double dbl_tmp;
	struct json_obj *obj_old;
	struct json_obj *obj_new;
	struct json_obj *json_obj;
	struct json whole_file;
	struct json_segment_counter counter;

	json_init(&whole_file);
	json_segment_counter_init(&counter);

	json_load(NULL,&whole_file,file_name);

	obj_old=json_obj_find_by_path(&(whole_file.obj), "jv");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.jv");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "suns_voc");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.suns_voc");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "suns_jsc");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.suns_jsc");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "ce");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.ce");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "pl_ss");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.pl_ss");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "eqe");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.eqe");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "fdtd");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.fdtd");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "time_domain");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.time_domain");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "fx_domain");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.fx_domain");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "cv");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.cv");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "spm");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.spm");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "transfer_matrix");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.transfer_matrix");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "transfer_matrix");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.transfer_matrix");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "ray");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.ray");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	obj_old=json_obj_find_by_path(&(whole_file.obj), "ray");
	if (obj_old!=NULL)
	{
		obj_new=json_obj_find_by_path(&(j->obj), "sims.ray");
		json_obj_all_free(obj_new);
		json_obj_cpy(obj_new,obj_old);
		edited=TRUE;
	}

	json_segment_counter_load(&counter,&whole_file, "epitaxy.contacts");

	while((json_obj=json_segment_counter_get_next(&counter))!=NULL)
	{

		snprintf(str_tmp,1000,"%s.contact",counter.item_path);
		obj_new=json_obj_find_by_path(&(j->obj), str_tmp);

		if (json_is_token(json_obj,"position")==0)
		{
			json_get_string(NULL,json_obj, str_tmp,"position",TRUE);
			json_set_data_string(obj_new,"position",str_tmp);

			json_get_string(NULL,json_obj, str_tmp,"applied_voltage_type",TRUE);
			json_set_data_string(obj_new,"applied_voltage_type",str_tmp);

			json_get_double(NULL,json_obj, &dbl_tmp,"applied_voltage",TRUE);
			json_set_data_double(obj_new,"applied_voltage",dbl_tmp);

			json_get_double(NULL,json_obj, &dbl_tmp,"contact_resistance_sq",TRUE);
			json_set_data_double(obj_new,"contact_resistance_sq",dbl_tmp);

			json_get_double(NULL,json_obj, &dbl_tmp,"shunt_resistance_sq",TRUE);
			json_set_data_double(obj_new,"shunt_resistance_sq",dbl_tmp);

			json_get_double(NULL,json_obj, &dbl_tmp,"np",TRUE);
			json_set_data_double(obj_new,"np",dbl_tmp);

			json_get_string(NULL,json_obj, str_tmp,"charge_type",TRUE);
			json_set_data_string(obj_new,"majority",str_tmp);

			if (strcmp(str_tmp,"electron")==0)
			{
				json_set_data_string(obj_new,"minority","hole");
			}else
			{
				json_set_data_string(obj_new,"minority","electron");
			}

			json_get_string(NULL,json_obj, str_tmp,"physical_model",TRUE);
			json_set_data_string(obj_new,"physical_model",str_tmp);

			json_get_double(NULL,json_obj, &dbl_tmp,"ve0",TRUE);
			json_set_data_double(obj_new,"ve0",dbl_tmp);

			json_get_double(NULL,json_obj, &dbl_tmp,"vh0",TRUE);
			json_set_data_double(obj_new,"vh0",dbl_tmp);
			edited=TRUE;
		}else
		{
			break;
		}

	}

	json_free(&whole_file);

	return edited;
}

//token level renaming
int json_compat(struct json *j,char *token, char *value)
{
	char orig_token[200];
	strcpy(orig_token,token);

	//printf(">'%s' '%s'\n",j->path,token);
	if (strcmp(token,"layer_type")==0)
	{
		strcpy(token,"obj_type");
		return 0;
	}

	if  (strcmp(j->path,"fits.fits")==0)
	{
		if (strcmp(token,"data_sets")==0)
		{
			strcpy(token,"segments");
			return 0;
		}else
		if (strcmp_begin(token,"data_set")==0)
		{
			strcpy(token,"segment");
			strcat(token,orig_token+8);		//get the number
			//printf("BING!\n");
			return 0;
		}

	}

	if  (strcmp(j->path,"epitaxy")==0)
	{
		if (strcmp(token,"layers")==0)
		{
			strcpy(token,"segments");
			return 0;
		}else
		if (strcmp_begin(token,"layer")==0)
		{
			if (strlen(token)>5)
			{
				if (str_isnumber(&token[5])==TRUE)
				{
					strcpy(token,"segment");
					strcat(token,orig_token+5);
				}
			}

			//printf("BING!\n");
			return 0;
		}
	}

	return -1;
}

//making sure things are present and set
int json_compat_fixup(struct json *j)
{
	struct json_obj *obj;
	struct json_obj *obj_new_seg;
	int segments=-1;

	obj=json_obj_find_by_path(&(j->obj), "optical.mesh.mesh_z");
	if (obj!=NULL)
	{
		json_get_int(NULL, obj, &(segments),"segments",FALSE);
		if (segments==0)
		{
			obj=json_obj_find_by_path(&(j->obj), "optical.mesh.mesh_x");
			if (obj!=NULL)
			{
				json_get_int(NULL, obj, &(segments),"segments",FALSE);
				if (segments==0)
				{
					obj=json_obj_find_by_path(&(j->obj), "optical.mesh.mesh_y");
					if (obj!=NULL)
					{
						json_get_int(NULL, obj, &(segments),"segments",FALSE);

						if (segments==0)
						{
							obj_new_seg=json_segments_add(obj,"", -1);

							obj=json_obj_find_by_path(obj_new_seg, "len");
							json_set_data(obj,"1e-6");

							obj=json_obj_find_by_path(obj_new_seg, "points");
							json_set_data(obj,"200");

							obj=json_obj_find_by_path(&(j->obj), "optical.mesh.mesh_x.enabled");
							json_set_data(obj,"False");

							obj=json_obj_find_by_path(&(j->obj), "optical.mesh.mesh_z.enabled");
							json_set_data(obj,"False");
						}
					}
				}
			}
		}
	}

	obj=json_obj_find_by_path(&(j->obj), "optical.mesh.mesh_l");
	if (obj!=NULL)
	{
		json_get_int(NULL, obj, &(segments),"segments",FALSE);
		if (segments==0)
		{
			obj_new_seg=json_segments_add(obj,"", -1);

			obj=json_obj_find_by_path(obj_new_seg, "start");
			json_set_data(obj,"300e-9");

			obj=json_obj_find_by_path(obj_new_seg, "stop");
			json_set_data(obj,"900e-9");

			obj=json_obj_find_by_path(obj_new_seg, "points");
			json_set_data(obj,"10");

			//obj=json_obj_find_by_path(obj_new_seg, "enabled");
			//json_set_data(obj,"False");
		}
	}

	obj=json_obj_find_by_path(&(j->obj), "gl.gl_lights");
	if (obj!=NULL)
	{
		json_gl_lights_fix_up(obj);
	}


	return -1;
}
