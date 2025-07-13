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
#include <sim.h>
#include <string.h>
#include <savefile.h>
#include <lock.h>
#include <mesh.h>
#include <memory.h>
#include <log.h>
#include <gui_hooks.h>
#include <json.h>

void json_build_template_from_file(	struct json *j)
{
	//printf("FREE!\n");
	json_free(j);
	//printf("FREE! end\n");
	struct json_obj *bib;
	struct json_obj *obj_main;
	struct json_obj *obj_sims;
	j->is_template=TRUE;

	bib=&(j->bib_template);
	json_template_bib(bib);

	obj_main=&(j->obj);
	json_template_sim(obj_main);

	//sims
		obj_sims=json_obj_add(obj_main,"sims","",JSON_NODE);
		json_template_sims_jv(obj_sims);
		json_template_sims_sunsvoc(obj_sims);
		json_template_sims_sunsjsc(obj_sims);
		json_template_sims_pl_ss(obj_sims);
		json_template_sims_equilibrium(obj_sims);
		json_template_sims_eqe(obj_sims);
		json_template_sims_time_domain(obj_sims);
		json_template_sims_ce(obj_sims);
		json_template_sims_fx_domain(obj_sims);
		json_template_sims_cv(obj_sims);
		json_template_sims_spm(obj_sims);
		json_template_sims_transfer_matrix(obj_sims);
		json_template_sims_mode(obj_sims);
		json_template_sims_ray(obj_sims);
		json_template_sims_fdtd(obj_sims);
		json_template_sims_poly(obj_sims);

	json_template_math(obj_main);

	json_template_optical(obj_main);
	json_template_dump(obj_main);
	json_template_server(obj_main);
	json_template_epitaxy(obj_main);
	json_template_thermal(obj_main);
	json_template_exciton(obj_main);

	json_template_fits(obj_main);

	json_template_parasitic(obj_main);
	json_template_hard_limit(obj_main);
	json_template_perovskite(obj_main);

	json_template_electrical_solver(obj_main);
	json_template_singlet(obj_main);
	json_template_circuit(obj_main);
	json_template_gl(obj_main);


	//json_dump_obj(obj_main);
	//getchar();

	json_template_gui_config(obj_main);
	json_template_world(obj_main);
	json_template_ml(obj_main);
	json_template_scans(obj_main);


	json_obj_add(obj_main,"icon","diode",JSON_STRING);
	json_obj_add(obj_main,"sub_icon","",JSON_STRING);
	json_obj_add(obj_main,"name","default name",JSON_STRING);
	json_obj_add(obj_main,"hidden","False",JSON_BOOL);
	json_obj_add(obj_main,"password","",JSON_STRING);
	json_obj_add(obj_main,"status","public",JSON_STRING);
	//json_dump_all(j);


	
	//printf("%s\n",file_name);
	//exit(0);
	//json_dump_obj(obj_main);

}
