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

/** @file initial.c
@brief setup the initial guess for the solvers, this really is just a really bad guess.
*/

#include <enabled_libs.h>
#include <stdlib.h>
#include <dos.h>
#include "sim.h"
#include "dump.h"
#include "log.h"
#include <cal_path.h>
#include <dat_file.h>
#include <lang.h>
#include <string.h>
#include <contacts.h>
#include <cal_path.h>
#include <contacts.h>
#include <device_fun.h>
#include <g_io.h>

void init_dump(struct simulation *sim,struct device *in)
{
struct dat_file buf;
struct dimensions *dim=&in->ns.dim;

if (get_dump_status(sim,dump_first_guess)==TRUE)
{
	char out_dir[PATH_MAX];
	join_path(2,out_dir,get_output_path(in),"equilibrium");
	g_mkdir(out_dir);

	strcpy(out_dir,"equilibrium");

	dat_file_init(&buf);

	if (buffer_set_file_name(sim,in,&buf,"init_Fi.csv")==0)
	{
		dat_file_malloc(&buf);
		dim_info_to_buf(&buf,dim);
		sprintf(buf.title,"%s - %s",_("Equilibrium Fermi-level"),_("position"));
		strcpy(buf.data_label,_("Equilibrium Fermi-level"));
		strcpy(buf.data_units,"eV");
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.time=in->time;
		buf.Vexternal=0.0;
		dat_file_add_zxy_data(sim,&buf,dim,  in->Fi);
		dat_file_dump_path(sim,out_dir,NULL,&buf);
		dat_file_free(&buf);
	}

	if (buffer_set_file_name(sim,in,&buf,"init_Ec.csv")==0)
	{
		dat_file_malloc(&buf);
		dim_info_to_buf(&buf,dim);
		sprintf(buf.title,"%s - %s",_("LUMO"),_("position"));
		strcpy(buf.data_label,_("LUMO"));
		strcpy(buf.data_units,"eV");
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.time=in->time;
		buf.Vexternal=0.0;
		dat_file_add_zxy_data(sim,&buf,dim,  in->Ec);
		dat_file_dump_path(sim,out_dir,NULL,&buf);
		dat_file_free(&buf);
	}

	if (buffer_set_file_name(sim,in,&buf,"init_Ev.csv")==0)
	{
		dat_file_malloc(&buf);
		dim_info_to_buf(&buf,dim);
		sprintf(buf.title,"%s - %s",_("HOMO"),_("position"));
		strcpy(buf.data_label,_("HOMO"));
		strcpy(buf.data_units,"eV");
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.time=in->time;
		buf.Vexternal=0.0;
		dat_file_add_zxy_data(sim,&buf,dim,  in->Ev);
		dat_file_dump_path(sim,out_dir,NULL,&buf);
		dat_file_free(&buf);
	}

	if (buffer_set_file_name(sim,in,&buf,"init_n.csv")==0)
	{
		dat_file_malloc(&buf);
		dim_info_to_buf(&buf,dim);
		sprintf(buf.title,"%s - %s",_("Electron density"),_("position"));
		strcpy(buf.data_label,_("Electron density"));
		strcpy(buf.data_units,"m^{-3}");
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.time=in->time;
		buf.Vexternal=0.0;
		dat_file_add_zxy_data(sim,&buf,dim,  in->n);
		dat_file_dump_path(sim,out_dir,NULL,&buf);
		dat_file_free(&buf);
	}

	if (buffer_set_file_name(sim,in,&buf,"init_p.csv")==0)
	{
		dat_file_malloc(&buf);
		dim_info_to_buf(&buf,dim);
		sprintf(buf.title,"%s - %s",_("Hole density"),_("position"));
		strcpy(buf.data_label,_("Hole density"));
		strcpy(buf.data_units,"m^{-3}");
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.time=in->time;
		buf.Vexternal=0.0;
		dat_file_add_zxy_data(sim,&buf,dim,  in->pt_all);
		dat_file_dump_path(sim,out_dir,NULL,&buf);
		dat_file_free(&buf);
	}

	if (buffer_set_file_name(sim,in,&buf,"init_nt.csv")==0)
	{
		dat_file_malloc(&buf);
		dim_info_to_buf(&buf,dim);
		sprintf(buf.title,"%s - %s",_("Electron density"),_("position"));
		strcpy(buf.data_label,_("Electron density"));
		strcpy(buf.data_units,"m^{-3}");
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.time=in->time;
		buf.Vexternal=0.0;
		dat_file_add_zxy_data(sim,&buf,dim,  in->nt_all);
		dat_file_dump_path(sim,out_dir,NULL,&buf);
		dat_file_free(&buf);
	}

	if (buffer_set_file_name(sim,in,&buf,"init_pt.csv")==0)
	{
		dat_file_malloc(&buf);
		dim_info_to_buf(&buf,dim);
		sprintf(buf.title,"%s - %s",_("Hole density"),_("position"));
		strcpy(buf.data_label,_("Hole density"));
		strcpy(buf.data_units,"m^{-3}");
		buf.logscale_x=0;
		buf.logscale_y=0;
		buf.time=in->time;
		buf.Vexternal=0.0;
		dat_file_add_zxy_data(sim,&buf,dim,  in->p);
		dat_file_dump_path(sim,out_dir,NULL,&buf);
		dat_file_free(&buf);
	}
}
}

void get_initial(struct simulation *sim,struct device *in,int guess)
{
	if (in->ncontacts<1)
	{
		ewe(sim,"get_initial: You need to include contacts fror an electrical simulation\n");
	}

	in->Vbi=0.0;
	if (in->circuit_simulation==TRUE)
	{
		return;
	}

	int z=0;
	int x=0;
	int y=0;
	gdouble Ef=0.0;
	gdouble phi_ramp=0.0;
	gdouble Eg=0.0;
	gdouble Xi=0.0;
	gdouble charge_right=0.0;
	gdouble top_l=0.0;
	gdouble top_r=0.0;
	gdouble left_ref_to_zero=0.0;
	gdouble right_ref_to_zero=0.0;
	gdouble delta_phi=0.0;
	int c=0;
	gdouble top;
	int equs;
	struct newton_state *ns=&(in->ns);
	struct dimensions *dim=&in->ns.dim;
	struct shape *s;
	struct json_obj *json_math;
	int math_stop_on_inverted_fermi_level;

	json_math=json_obj_find(&(in->config.obj), "math");
	json_get_english(sim,json_math, &(math_stop_on_inverted_fermi_level),"math_stop_on_inverted_fermi_level",TRUE);

	Eg=in->Eg[0][0][0];
	Xi=in->Xi[0][0][0];

	for (z=0;z<dim->zlen;z++)
	{
		for (x=0;x<dim->xlen;x++)
		{
			for (y=0;y<dim->ylen;y++)
			{
				s=in->obj_zxy[z][x][y]->s;
				if (s->dosn.enabled==FALSE)
				{
					ewe(sim,"There is a shape (%s) covering the electrical mesh with no electrical parameters enabled",s->name);
				}
			}
		}
	}

	//getchar();
	charge_right=contacts_get_rcharge(sim,in);

	if (contacts_get_rcharge_type(sim,in)==ELECTRON)
	{
		s=in->obj_zxy[0][0][dim->ylen-1]->s;
		top_r=get_top_from_n(s,charge_right,in->Te[0][0][dim->ylen-1]);
		right_ref_to_zero=top_r-in->Xi[0][0][dim->ylen-1];
		check_fermi_inversion_n(sim,s,charge_right,math_stop_on_inverted_fermi_level);
	}else
	{
		s=in->obj_zxy[0][0][dim->ylen-1]->s;
		top_r= get_top_from_p(s,charge_right,in->Te[0][0][dim->ylen-1]);
		right_ref_to_zero=-(in->Eg[0][0][dim->ylen-1]+top_r)-in->Xi[0][0][dim->ylen-1];
		check_fermi_inversion_p(sim,s,charge_right,math_stop_on_inverted_fermi_level);
	}



	for (z=0;z<dim->zlen;z++)
	{
		for (x=0;x<dim->xlen;x++)
		{
			//Top
			c=in->n_contact_y0[z][x];
			Eg=in->Eg[z][x][0];		//Added for Jason
			Xi=in->Xi[z][x][0];

			if (c!=-1)
			{
				if (in->contacts[c].charge_type==HOLE)
				{
					s=in->obj_zxy[z][x][0]->s;
					top_l=get_top_from_p(s,in->contacts[c].np,in->Te[z][x][0]);
					in->Fi0_y0[z][x]= -(top_l+Xi+Eg);
					check_fermi_inversion_p(sim,s,in->contacts[c].np,math_stop_on_inverted_fermi_level);
				}else
				{
					s=in->obj_zxy[z][x][0]->s;
					top_l= get_top_from_n(s,in->contacts[c].np,in->Te[z][x][0]);
					in->Fi0_y0[z][x]= -Xi+top_l;
					check_fermi_inversion_n(sim,s,in->contacts[c].np,math_stop_on_inverted_fermi_level);
				}
			}else
			{		//No contact
				s=in->obj_zxy[z][x][0]->s;
				top_l=get_top_from_p(s,1e15,in->Te[z][x][0]);
				in->Fi0_y0[z][x]= -(top_l+Xi+Eg);
				check_fermi_inversion_p(sim,s,1e15,math_stop_on_inverted_fermi_level);
			}

			in->V_y0[z][x]=in->Fi0_y0[z][x]-in->Fi0_y0[0][0];		//Everything is referenced to the [0][0] point.

			//Btm

			c=in->n_contact_y1[z][x];
			Eg=in->Eg[z][x][dim->ylen-1];		//Added for Jason
			Xi=in->Xi[z][x][dim->ylen-1];

			if (c!=-1)
			{
				if (in->contacts[c].charge_type==HOLE)
				{
					s=in->obj_zxy[z][x][dim->ylen-1]->s;
					top_l=get_top_from_p(s,in->contacts[c].np,in->Te[z][x][dim->ylen-1]);
					in->Fi0_y1[z][x]= -(top_l+Xi+Eg);
					check_fermi_inversion_p(sim,s,in->contacts[c].np,math_stop_on_inverted_fermi_level);
				}else
				{
					s=in->obj_zxy[z][x][dim->ylen-1]->s;
					top_l= get_top_from_n(s,in->contacts[c].np,in->Te[z][x][dim->ylen-1]);
					in->Fi0_y1[z][x]= -Xi+top_l;
					check_fermi_inversion_n(sim,s,in->contacts[c].np,math_stop_on_inverted_fermi_level);
				}
			}else
			{		//No contact
				s=in->obj_zxy[z][x][dim->ylen-1]->s;
				top_l=get_top_from_p(s,1e15,in->Te[z][x][dim->ylen-1]);
				in->Fi0_y1[z][x]= -(top_l+Xi+Eg);
				check_fermi_inversion_p(sim,s,1e15,math_stop_on_inverted_fermi_level);
			}

			in->V_y1[z][x]=in->Fi0_y1[z][x]-in->Fi0_y0[0][0];		//Everything is referenced to the [0][0] point.

		}

		for (y=0;y<dim->ylen;y++)
		{
			//Left
			c=in->n_contact_x0[z][y];
			Eg=in->Eg[z][0][y];		//Added for Jason
			Xi=in->Xi[z][0][y];

			if (c!=-1)
			{
				if (in->contacts[c].charge_type==HOLE)
				{
					s=in->obj_zxy[z][0][y]->s;
					top_l=get_top_from_p(s,in->contacts[c].np,in->Te[z][0][y]);
					in->Fi0_x0[z][y]= -(top_l+Xi+Eg);
					check_fermi_inversion_p(sim,s,in->contacts[c].np,math_stop_on_inverted_fermi_level);
				}else
				{
					s=in->obj_zxy[z][0][y]->s;
					top_l= get_top_from_n(s,in->contacts[c].np,in->Te[z][0][y]);
					in->Fi0_x0[z][y]= -Xi+top_l;
					check_fermi_inversion_n(sim,s,in->contacts[c].np,math_stop_on_inverted_fermi_level);
				}
			}else
			{		//No contact
				s=in->obj_zxy[z][0][y]->s;
				top_l=get_top_from_p(s,1e15,in->Te[z][0][y]);
				in->Fi0_x0[z][y]= -(top_l+Xi+Eg);
				check_fermi_inversion_p(sim,s,1e15,math_stop_on_inverted_fermi_level);
			}

			in->V_x0[z][y]=in->Fi0_x0[z][y]-in->Fi0_y0[0][0];		//Everything is referenced to the [0][0] point.

			//Right

			c=in->n_contact_x1[z][y];
			Eg=in->Eg[z][dim->xlen-1][y];		//Added for Jason
			Xi=in->Xi[z][dim->xlen-1][y];

			if (c!=-1)
			{
				if (in->contacts[c].charge_type==HOLE)
				{
					s=in->obj_zxy[z][dim->xlen-1][y]->s;
					top_l=get_top_from_p(s,in->contacts[c].np,in->Te[z][dim->xlen-1][y]);
					in->Fi0_x1[z][y]= -(top_l+Xi+Eg);
					check_fermi_inversion_p(sim,s,in->contacts[c].np,math_stop_on_inverted_fermi_level);
				}else
				{
					s=in->obj_zxy[z][dim->xlen-1][y]->s;
					top_l= get_top_from_n(s,in->contacts[c].np,in->Te[z][dim->xlen-1][y]);
					in->Fi0_x1[z][y]= -Xi+top_l;
					check_fermi_inversion_n(sim,s,in->contacts[c].np,math_stop_on_inverted_fermi_level);
				}
			}else
			{		//No contact
				s=in->obj_zxy[z][dim->xlen-1][y]->s;
				top_l=get_top_from_p(s,1e15,in->Te[z][dim->xlen-1][y]);
				in->Fi0_x1[z][y]= -(top_l+Xi+Eg);
				check_fermi_inversion_p(sim,s,1e15,math_stop_on_inverted_fermi_level);
			}


			in->V_x1[z][y]=in->Fi0_x1[z][y]-in->Fi0_y0[0][0];		//Everything is referenced to the [0][0] point.

		}
	}

	//contacts_interpolate(sim,in, in->V_y0);

	//getchar();
	left_ref_to_zero=in->Fi0_y0[0][0];
	Ef=in->Fi0_y0[0][0];


	delta_phi=right_ref_to_zero-left_ref_to_zero;

	for (z=0;z<dim->zlen;z++)
	{
		for (x=0;x<dim->xlen;x++)
		{
			s=in->obj_zxy[z][x][0]->s;
			get_n_den(s,in->Fi0_y0[z][x]+in->Xi[z][x][0],in->Te[z][x][0],&(in->electrons_y0[z][x]),NULL,NULL);
			get_p_den(s,-(in->Fi0_y0[z][x]+in->Xi[z][x][0]+in->Eg[z][x][0]),in->Th[z][x][0],&(in->holes_y0[z][x]),NULL,NULL);

			s=in->obj_zxy[0][0][dim->ylen-1]->s;
			get_n_den(s,in->Fi0_y1[z][x]+in->Xi[z][x][dim->ylen-1],in->Te[0][0][dim->ylen-1],&(in->electrons_y1[z][x]),NULL,NULL);
			get_p_den(s,-(in->Fi0_y1[z][x]+in->Xi[z][x][dim->ylen-1]+in->Eg[z][x][dim->ylen-1]),in->Th[0][0][dim->ylen-1],&(in->holes_y1[z][x]),NULL,NULL);


		}

		for (y=0;y<dim->ylen;y++)
		{
			s=in->obj_zxy[z][0][y]->s;
			get_n_den(s,in->Fi0_x0[z][y]+in->Xi[z][0][y],in->Te[z][0][y],&(in->electrons_x0[z][y]),NULL,NULL);
			get_p_den(s,-(in->Fi0_x0[z][y]+in->Xi[z][0][y]+in->Eg[z][0][y]),in->Th[z][0][y],&(in->holes_x0[z][y]),NULL,NULL);

			s=in->obj_zxy[0][dim->xlen-1][y]->s;
			get_n_den(s,in->Fi0_x1[z][y]+in->Xi[z][dim->xlen-1][y],in->Te[0][dim->xlen-1][y],&(in->electrons_x1[z][y]),NULL,NULL);
			get_p_den(s,-(in->Fi0_x1[z][y]+in->Xi[z][dim->xlen-1][y]+in->Eg[z][dim->xlen-1][y]),in->Th[0][dim->xlen-1][y],&(in->holes_x1[z][y]),NULL,NULL);
		}
	}


	if (guess==TRUE)
	{
		int band;
		for (z=0;z<dim->zlen;z++)
		{
			for (x=0;x<dim->xlen;x++)
			{

				for (y=0;y<dim->ylen;y++)
				{
					equs=in->equs[y];
					phi_ramp=delta_phi*(dim->y[y]/dim->y[dim->ylen-1]);

					in->Fi[z][x][y]=Ef;

					in->Fn[z][x][y]=Ef;
					in->Fp[z][x][y]=Ef;

					ns->phi[z][x][y]=phi_ramp;

					ns->x[z][x][y]=ns->phi[z][x][y]+in->Fn[z][x][y];
					ns->xp[z][x][y]= -(ns->phi[z][x][y]+in->Fp[z][x][y]);
					//ns->x_Nion[z][x][y]=ns->xp[z][x][y];

					in->Ec[z][x][y]= -ns->phi[z][x][y]-in->Xi[z][x][y];
					if (in->Ec[z][x][y]<in->Fi[z][x][y])
					{
						ns->phi[z][x][y]= -(in->Fi[z][x][y]+in->Xi[z][x][y]);
						in->Ec[z][x][y]= -ns->phi[z][x][y]-in->Xi[z][x][y];
					}

					in->Ev[z][x][y]= -ns->phi[z][x][y]-in->Xi[z][x][y]-in->Eg[z][x][y];
					if (in->Ev[z][x][y]>in->Fi[z][x][y])
					{
						ns->phi[z][x][y]= -(in->Fi[z][x][y]+in->Xi[z][x][y]+in->Eg[z][x][y]);
						in->Ev[z][x][y]= -ns->phi[z][x][y]-in->Xi[z][x][y]-in->Eg[z][x][y];

						in->Ec[z][x][y]= -ns->phi[z][x][y]-in->Xi[z][x][y];
					}


					gdouble t=in->Fi[z][x][y]-in->Ec[z][x][y];
					gdouble tp=in->Ev[z][x][y]-in->Fi[z][x][y];
					if (equs & SOLVE_JE_Y)
					{
						in->n[z][x][y]=in->Nc[z][x][y]*exp(((t)*Qe)/(kb*in->Te[z][x][y]));
					}else
					{
						in->n[z][x][y]=0.0;
					}

					if (equs & SOLVE_JH_Y)
					{
						in->p[z][x][y]=in->Nv[z][x][y]*exp(((tp)*Qe)/(kb*in->Th[z][x][y]));
					}else
					{
						in->p[z][x][y]=0.0;
					}

					s=in->obj_zxy[z][x][y]->s;

					//ns->Nion[z][x][y]=in->p[z][x][y];
					if (ns->Nion_enabled==TRUE)
					{
						in->Nion[z][x][y]=get_dos_ion_density(s);
						top=get_top_from_ion(in->Nion[z][x][y]);
						ns->x_Nion[z][x][y]=-(ns->phi[z][x][y]+in->Ev[z][x][y]-top);
					}

					if (ns->singlet_enabled==TRUE)
					{
						top=get_top_from_singlet(1e22);
						ns->x_Ns[z][x][y]=top;
						ns->x_Nt[z][x][y]=top;
						ns->x_Nsd[z][x][y]=top;
						ns->x_Ntd[z][x][y]=top;
						ns->x_Nho=top;

						in->Ns[z][x][y]=1e22;
						in->Nt[z][x][y]=1e22;
						in->Nsd[z][x][y]=1e22;
						in->Ntd[z][x][y]=1e22;
						in->Nho=1e22;

					}

					for (band=0;band<dim->srh_bands;band++)
					{
						in->Fnt[z][x][y][band]= Ef;//-ns->phi[z][x][y]-in->Xi[z][x][y]+dos_srh_get_fermi_n(in,in->n[z][x][y], in->p[z][x][y],band,in->imat[z][x][y],in->Te[z][x][y]);
						//printf("%Le\n",Ef);
						in->Fpt[z][x][y][band]= Ef;//-ns->phi[z][x][y]-in->Xi[z][x][y]-in->Eg[z][x][y]-dos_srh_get_fermi_p(in,in->n[z][x][y], in->p[z][x][y],band,in->imat[z][x][y],in->Th[z][x][y]);
						ns->xt[z][x][y][band]=ns->phi[z][x][y]+in->Fnt[z][x][y][band];
						ns->xpt[z][x][y][band]= -(ns->phi[z][x][y]+in->Fpt[z][x][y][band]);

						if (equs & SOLVE_SRH_E)
						{
							//printf("%le %le\n",get_n_pop_srh(sim,s,ns->xt[z][x][y][band]+in->tt[z][x][y],in->Te[z][x][y],0),in->Te[z][x][y]);
							//getchar();
							in->nt[z][x][y][band]=get_n_pop_srh(sim,s,ns->xt[z][x][y][band]+in->tt[z][x][y],in->Te[z][x][y],band);
							in->dnt[z][x][y][band]=get_dn_pop_srh(sim,s,ns->xt[z][x][y][band]+in->tt[z][x][y],in->Te[z][x][y],band);
						}else
						{
							in->nt[z][x][y][band]=0.0;
							in->dnt[z][x][y][band]=0.0;
						}

						if (equs & SOLVE_SRH_H)
						{
							in->pt[z][x][y][band]=get_p_pop_srh(sim,s,ns->xpt[z][x][y][band]-in->tpt[z][x][y],in->Th[z][x][y],band);
							in->dpt[z][x][y][band]=get_dp_pop_srh(sim,s,ns->xpt[z][x][y][band]-in->tpt[z][x][y],in->Th[z][x][y],band);
						}else
						{
							in->pt[z][x][y][band]=0.0;
							in->dpt[z][x][y][band]=0.0;
						}
					}

				}
			}
		}

		ns->x_y0[0][0]=in->V_y0[0][0]+Ef;
		ns->xp_y0[0][0]=-(in->V_y0[0][0]+Ef);
		ns->x_y1[0][0]=in->V_y1[0][0]+Ef;
		ns->xp_y1[0][0]=-(in->V_y1[0][0]+Ef);
		//getchar();
		in->Vbi=delta_phi;
		init_dump(sim,in);
	}

return;
}

