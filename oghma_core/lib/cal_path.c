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

/** @file cal_path.c
	@brief Calculate the path of where stuff is, and if it can't find a file look harder.  Win/Linux.
*/

#include <enabled_libs.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "cal_path.h"
#include "util.h"
#include <log.h>

#include <unistd.h>
#include <fcntl.h>
#include <stdarg.h>
#include <oghma_const.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <g_io.h>

#include <limits.h>
#include <pwd.h>

int find_dll(struct simulation *sim, char *lib_path,char *lib_name)
{
	char full_name[PATH_MAX];
	char temp[PATH_MAX];
	struct find_file find;

		sprintf(full_name,"%s.so",lib_name);

	join_path(2,lib_path,get_plugins_path(sim),full_name);
	if (isfile(lib_path)==0)
	{
		return 0;
	}


	if (find_open(&find,get_plugins_path(sim))==0)
	{
		while(find_read(&find)==0)
		{
			split_dot(temp, find.file_name);
			if (strcmp(lib_name,temp)==0)
			{
				join_path(2,lib_path,get_plugins_path(sim),find.file_name);
				if (isfile(lib_path)==0)
				{
					find_close(&find);
					return 0;
				}

			}
		}

	find_close(&find);

	}

	ewe(sim,"I can't find the dll %s,\n",lib_name);

	return -1;
}

int set_path(struct simulation *sim,char *out, char *name)
{
char cwd[PATH_MAX];

char temp[PATH_MAX];



	//Check the home dir first
	join_path(3,temp,sim->home_path,"oghma_local",name);
	if ((isdir(temp)==0)||(isfile(temp)==0))
	{
		strcpy(out,temp);
		//printf(">>>>>>>>%s",temp);
		return 0;
	}

	//Check the cwd
	if (g_getcwd(cwd,PATH_MAX)==NULL)
	{
		ewe(sim,"cwd returned NULL, check if the directory exists.\n");
	}

	join_path(2,temp,cwd,name);

	if ((isdir(temp)==0)||(isfile(temp)==0))
	{
		strcpy(out,temp);
		return 0;
	}

	//check oghma_*
	join_path(3,temp,cwd,"oghma_data",name);

	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	join_path(3,temp,cwd,"oghma_core",name);

	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	//search the exe path
	join_path(2,temp,sim->exe_path,name);

	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	//search the exe path minus one level

	join_path(3,temp,sim->exe_path_dot_dot,"oghma_data",name);

	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	join_path(3,temp,sim->exe_path_dot_dot,"oghma_core",name);

	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	join_path(2,temp,"/usr/lib/oghma/",name);
	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	join_path(2,temp,"/usr/lib64/oghma/",name);
	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	join_path(2,temp,"/usr/share/oghma/",name);
	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	//Ubuntu
	join_path(2,temp,"/usr/lib/x86_64-linux-gnu/oghma/",name);
	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	join_path(2,temp,sim->share_path,name);
	if (isdir(temp)==0)
	{
		strcpy(out,temp);
		return 0;
	}

	return -1;
}

void cal_path(struct simulation *sim)
{
	char cwd[PATH_MAX];
	char temp[PATH_MAX];

	strcpy(cwd,"");
	strcpy(temp,"");

	strcpy(sim->share_path,"nopath");

	strcpy(sim->plugins_path,"");
	strcpy(sim->lang_path,"");


	if (get_exe_path(temp)!=0)
	{
		ewe(sim,"get_exe_path failed\n");
	}

	if (get_home_dir(sim->home_path)!=0)
	{
		ewe(sim,"get_home_dir failed\n");
	}

	get_dir_name_from_path(sim->exe_path, temp);
	get_dir_name_from_path(sim->exe_path_dot_dot, sim->exe_path);

	if (isfile("configure.ac")==0)
	{
		strcpy(sim->share_path,cwd);
		//printf_log(sim,"share path: %s\n",sim->share_path);
	}else
	if (isfile("ver.py")==0)
	{
		path_up_level(temp, cwd);
		strcpy(sim->share_path,temp);
		//printf_log(sim,"share path: %s\n",sim->share_path);
	}else
	{
		strcpy(sim->share_path,"/usr/lib64/oghma/");
	}



	if (g_getcwd(cwd,PATH_MAX)==NULL)
	{
		ewe(sim,"cwd returned NULL\n");
	}

	if (strcmp(sim->root_simulation_path,"")==0)
	{
		strcpy(sim->root_simulation_path,cwd);
		join_path(2,sim->cache_path,cwd,"cache");
	}else
	{
		join_path(2,sim->cache_path,sim->root_simulation_path,"cache");
	}

	set_path(sim,sim->plugins_path, "plugins");
	//set_path(sim,sim->lang_path, "lang");
	strcpy(sim->lang_path,"langdisabled");
	set_path(sim,sim->materials_path, "materials");
	set_path(sim,sim->filter_path, "filters");
	set_path(sim,sim->cie_color_path, "cie_color");
	set_path(sim,sim->shape_path, "shape");

	set_path(sim,sim->spectra_path, "spectra");

	join_path(3,sim->cache_path_for_fit,cwd,"sim","cache");
	join_path(2,sim->oghma_local_path,sim->home_path,"oghma_local");

	join_path(2,sim->tmp_path,sim->oghma_local_path,"tmp");

}





char *get_cache_path(struct simulation *sim)
{
	if ((sim->fitting==FIT_NOT_FITTING)||(sim->fitting==OPTIMIZER_RUNNING))
	{
		return sim->cache_path;
	}else
	{
		return sim->cache_path_for_fit;
	}
}


char *get_oghma_local_path(struct simulation *sim)
{
	return sim->oghma_local_path;
}

char *get_spectra_path(struct simulation *sim)
{
	return sim->spectra_path;
}


char *get_materials_path(struct simulation *sim)
{
	return sim->materials_path;
}

char *get_filter_path(struct simulation *sim)
{
	return sim->filter_path;
}

char *get_cie_color_path(struct simulation *sim)
{
	return sim->cie_color_path;
}

char *get_shape_path(struct simulation *sim)
{
	return sim->shape_path;
}

char *get_plugins_path(struct simulation *sim)
{
	return sim->plugins_path;
}

char *get_lang_path(struct simulation *sim)
{
	return sim->lang_path;
}

char *get_tmp_path(struct simulation *sim)
{
	return sim->tmp_path;
}

