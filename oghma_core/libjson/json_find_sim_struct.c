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

/** @file josn_search.c
	@brief Search the json tree
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zip.h>
#include <unistd.h>
#include <fcntl.h>
#include "inp.h"
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>

struct json_obj *json_find_sim_struct(struct simulation *sim, struct json *j,char *sim_command)
{
	char sim_experiment[100];
	char sim_mode[100];
	char *mode_pointer;
	struct json_obj *json_sims=NULL;
	struct json_obj *json_mode=NULL;
	struct json_obj *json_experiment=NULL;

	strextract_name(sim_experiment,sim_command);
	mode_pointer=strextract_domain(sim_command);
	strcpy(sim_mode,mode_pointer);

	json_sims=json_obj_find(&(j->obj), "sims");
	if (json_sims==NULL)
	{
		ewe(sim,"Simulation mode sims not found\n");
	}

	json_mode=json_obj_find(json_sims, sim_mode);
	if (json_mode==NULL)
	{
		ewe(sim,"Simulation mode %s not found\n",sim_mode);
	}

	json_experiment=json_obj_find(json_mode, sim_experiment);
	if (json_experiment==NULL)
	{
		ewe(sim,"Experiment %s not found in %s\n",sim_experiment,sim_mode);
	}

	return json_experiment;
}
