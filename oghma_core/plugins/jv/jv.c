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

/** @file jv.c
	@brief Simulate JV curve.
*/


#include <sim.h>
#include <exp.h>
#include "jv.h"
#include <dump.h>
#include <sweep.h>
#include "newton_tricks.h"
#include <dat_file.h>
#include <gui_hooks.h>
#include <pl.h>
#include <log.h>
#include <lang.h>
#include <remesh.h>
#include <cal_path.h>
#include <contacts.h>
#include <contacts_vti_store.h>
#include <light_fun.h>
#include <cache.h>
#include <ray_fun.h>
#include <enabled_libs.h>
#include <json.h>
#include <lock.h>
#include <device_fun.h>
#include <memory.h>
#include <g_io.h>
#include <optical_mode_fun.h>
#include <fom.h>
#include <outcoupling_fun.h>
#include <probes_fun.h>
#include <epitaxy.h>
#include <dump_ctrl_fun.h>

void jv_voltage_step(struct simulation *sim,struct device *dev,double *V, double *Vstep)
{
	double Vapplied=*V;
	double dV=0.05;
	int i;
	int steps=*Vstep/dV;
	double Vexternal;
	double J;
	if (dev->dynamic_mesh==TRUE)
	{
		if (*Vstep>0.1)
		{
			remesh_shrink(sim,dev);
			//printf("that's never going to work\n");
			for (i=0;i<steps;i++)
			{
				contact_set_active_contact_voltage(sim,dev,Vapplied);
				Vapplied+=dV;
				//printf_log(sim,".");
				if (dev->solver_verbosity>=SOLVER_VERBOSITY_AT_END)
				{
					Vexternal=get_equiv_V(sim,dev);
					J=get_equiv_J(sim,dev);
					printf_log(sim,"*%s=%lf (%lf) %s = %le mA (%le A/m^2) %le\n",_("Voltage"),Vapplied,Vexternal,_("Current"),(double)get_I(dev)/1e-3,J,dev->ns->last_error);
				}
				newton_sim_simple(sim,dev);
			}

			remesh_reset(sim,dev,0.0);
		}
	}
//	printf_log(sim,"\n");
	*V+=*Vstep;

}

int get_step_n(double step0,double step_mul,double V)
{
int n=0;
double pos=0;
double dv=fabs(step0);

while(pos<fabs(V))
{
	pos+=dv;
	dv*=step_mul;
	n++;
}
return n;
}

void sim_jv(struct simulation *sim,struct device *dev)
{

double Vapplied=0.0;
int up=TRUE;
struct jv config;
int ittr=0;
double J;
double Pden;
double Vlast=-1.0;
double Jlast;
double Pdenlast=-1e6;
double Vexternal=-1.0;
double V=0.0;

double mue=0.0;
double muh=0.0;
char mytemp[1000];
double eqe_Rtot;

struct json_obj *json_jv;
struct newton_state *ns=dev->ns;
struct dimensions *dim=&ns->dim;
struct heat* thermal=&(dev->thermal);

struct simmode *sm=&(dev->simmode);
struct fom fom;
fom_init(&fom);

ns->singlet_enabled=TRUE;
ns->singlet_enabled_Nho=FALSE;
solver_realloc(sim,dev);
find_n0(sim,dev,TRUE);

light_solve_and_update(sim,dev,&(dev->mylight),0.0);
//printf("%le\n",dev->Gn[0][0][0]);
//getchar();
if (sim->fitting==FIT_NOT_FITTING)
{
	printf_log(sim,_("Running JV simulation\n"));
}
struct dat_file buf;
dat_file_init(&buf);

struct sweep_store store;

sweep_init(sim,&store);

struct contacts_vti_store contact_store;
dump_contacts_init(sim,dev,&contact_store);
dump_contacts_malloc(sim,dev,&contact_store);

json_jv=json_find_sim_struct(sim, &(dev->config),sm->simmode);

jv_load_config(sim,&config,&store,json_jv);


double Vstop=config.Vstop;
double Vstep=config.Vstep;


struct math_xy charge;
math_xy_init(&charge);

struct math_xy charge_with_surface_charge;
math_xy_init(&charge_with_surface_charge);

struct math_xy charge_tot;
math_xy_init(&charge_tot);

struct math_xy klist;
math_xy_init(&klist);

struct math_xy lv;
math_xy_init(&lv);

struct math_xy v_eqe;
math_xy_init(&v_eqe);

struct math_xy v_eqe_R;
math_xy_init(&v_eqe_R);

struct math_xy lj;
math_xy_init(&lj);

struct math_xy R_list;
math_xy_init(&R_list);

struct math_xy n_list;
math_xy_init(&n_list);

struct math_xy tau_list;
math_xy_init(&tau_list);

struct math_xy tau_all_list;
math_xy_init(&tau_all_list);

struct math_xy Tl;
math_xy_init(&Tl);

struct math_xy v_optical_efficiency;
math_xy_init(&v_optical_efficiency);

struct math_xy jv;
math_xy_init(&jv);

struct math_xy temp;
math_xy_init(&temp);

double theta_jsc=-1.0;
double theta_voc=-1.0;
double theta_pmax=-1.0;

//contact_set_active_contact_voltage(sim,dev,Vapplied);
//char json_path[PATH_MAX];
//join_path(2,json_path,dev->output_path,"json.dat");
//dev->config.compact=TRUE;
//json_save_as(sim,json_path,&(dev->config));

//printf("%d\n",dev->cache.enabled);

if ((dim->zlen>1) || (dim->xlen>1))
{
	contact_set_wanted_active_contact_voltage(sim,dev,config.Vstart);
	//contact_set_active_contact_voltage(sim,dev,config.Vstart);
	ntricks_auto_ramp_contacts(sim,dev);
}else
{
	if (gfabs(config.Vstart-Vapplied)>0.2)
	{
		ramp_externalv(sim,dev,Vapplied,config.Vstart);
	}
}


remesh_reset(sim,dev,Vapplied);
//if (dev->remesh==TRUE)
//{
//
//}
//double start_Q=(three_d_integrate(dim, dev->n)+three_d_integrate(dim, dev->nt_all))*Qe;
double sun_orig=light_get_sun(&(dev->mylight));

if (strcmp(config.charge_carrier_generation_model,"transfer_matrix")==0)
{
	light_set_sun(&(dev->mylight),sun_orig*config.jv_light_efficiency);
	light_solve_and_update(sim,dev,&(dev->mylight),0.0);
}else
if (strcmp(config.charge_carrier_generation_model,"ray_trace")==0)
{
	ray_solve_all(sim,dev);
	ray_dump(sim,dev);
	device_import_photon_gen_rate(sim,dev);
}

thermal_ramp(sim,dev);
//newton_dump_bandwidth(sim,dev);
newton_push_state(dev);

newton_set_min_ittr(dev,30);

Vapplied=config.Vstart;
//contacts_dump(sim,dev);
//printf("wait c\n");
//getchar();

contact_set_active_contact_voltage(sim,dev,Vapplied);
//contacts_dump(sim,dev);
V=Vapplied;
newton_sim_simple(sim,dev);
//printf("wait d\n");
//getchar();

newton_pop_state(dev);
//newton_set_min_ittr(dev,0);

//double k_voc=0.0;
double n_voc=-1.0;
double r_voc=-1.0;
double nsc=0.0;

double n_trap=-1.0;
double p_trap=-1.0;
double n_free=-1.0;
double p_free=-1.0;

double n_trap_voc=-1.0;
double p_trap_voc=-1.0;
double n_free_voc=-1.0;
double p_free_voc=-1.0;

double np_voc_tot=-1.0;
double n_pmax=0.0;
double mue_pmax=0.0;
double muh_pmax=0.0;
double mue_jsc=0.0;
double muh_jsc=0.0;

//Device characterisation

double cal_step=0;

double n_steps=0.0;
char send_data[STR_MAX];
int power_min_pos=0;
int dump_step=0;

double mu_pmax=-1.0;
double mu_voc=-1.0;
double mu_jsc=0.0;
double mu_geom_pmax=-1.0;
double mu_geom_voc=-1.0;
double mu_geom_jsc=0.0;

double mu_harmonic_pmax=-1.0;
double mu_harmonic_voc=-1.0;
double mu_harmonic_jsc=0.0;

double mu_geom_micro_pmax=-1.0;
double mu_geom_micro_voc=0.0;
double mu_geom_micro_jsc=0.0;

double tau_voc=-1.0;
double tau_pmax=-1.0;
double tau_all_voc=-1.0;
double tau_all_pmax=-1.0;
double tau=-1.0;
double tau_all=-1.0;

double theta_srh_free=-1.0;
double theta_srh_free_trap=-1.0;
double k_voc=-1.0;

int dump_sim_info=FALSE;
double np_extracted;
double eqe;
double ret_sigma_e=-1.0;
double ret_sigma_h=-1.0;
double r_pmax=-1.0;
double sclc_x;
double sclc_y;
double sclc_mu;
double sclc_V=0.0;
double sclc_J=0.0;
struct epitaxy *epi=&(dev->my_epitaxy);
double device_length=-1.0;
double er=0.0;

n_steps=get_step_n(config.Vstep,config.jv_step_mul,config.Vstart);
n_steps+=get_step_n(config.Vstep,config.jv_step_mul,config.Vstop);

dev->stop=FALSE;

	if ((dump_can_i_dump(sim,dev, "sim_info.dat")==0)||(strcmp(sim->enable_optimizer,"")!=0))
	{
		dump_sim_info=TRUE;
	}

up=TRUE;
if (config.Vstop<config.Vstart)
{
	up=FALSE;
}
	dev->eng.call_count=0;
	ns->problem_type=ELEC_PROB_MAIN_LOOP;
	do
	{
		Vapplied=V;

		contact_set_active_contact_voltage(sim,dev,Vapplied);

		newton_sim_simple(sim,dev);

		contacts_cal_J_and_i(sim,dev);
		//contacts_dump_info(sim,dev);
		J=get_equiv_J(sim,dev);

		//circuit_printf_links(sim,&(dev->cir));

		Vexternal=get_equiv_V(sim,dev);
		//printf("%le %le\n",Vexternal,J);
		
		sprintf(send_data,"percent:%lf",(double)ittr/n_steps);
		gui_send_data(sim,gui_sub,send_data);

		sprintf(send_data,"text:Voltage %.2lf V/%.2lf V",V,config.Vstop);
		gui_send_data(sim,gui_sub,send_data);

		np_extracted=get_extracted_np(dev);
		inter_append(&charge,Vexternal,np_extracted);
		inter_append(&charge_tot,Vexternal,get_np_tot(dev));

		inter_append(&charge_with_surface_charge,Vexternal,np_extracted+(cal_contact_charge(dev)-dev->contact_charge));

		Pden=gfabs(J*Vexternal);

		inter_append(&jv,Vexternal,J);
		store.voltage=Vexternal;
		sweep_add_data(sim,&store,dev);

		dump_contacts_add_data(sim,dev,&contact_store);

		if (dev->solver_verbosity>=SOLVER_VERBOSITY_AT_END)
		{
			contacts_state_to_string(sim,mytemp, dev);
			if (sim->fitting==FIT_NOT_FITTING)
			{
				printf_log(sim," %s f()=%le %lf ms\n",mytemp,ns->last_error, ns->last_time);
			}
			
		}


		//check if we have crossed 0V
		if (dump_sim_info==TRUE)
		{
			//Jsc
			if ((Vlast<=0)&&(Vexternal>=0.0))
			{
				get_free_nf_pf_nt_pt_charge(dev,&n_free,&p_free,&n_trap,&p_trap);
				nsc=get_extracted_np(dev);
				get_avg_mu(dev,&mue_jsc,&muh_jsc);
				mu_jsc=(mue_jsc+muh_jsc)/2.0;
				mu_geom_jsc=sqrt(mue_jsc*muh_jsc);
				mu_harmonic_jsc=2.0/((1.0/mue_jsc)+(1.0/muh_jsc));
				get_avg_geom_micro_mu(dev,&mu_geom_micro_jsc);

				theta_jsc=(n_free+p_free)/(n_free+p_free+n_trap+p_trap);
			}

			if (light_get_sun(&(dev->mylight))!=0.0)
			{

				//Voc
				if ((Jlast<=0)&&(J>=0.0))
				{
					get_free_nf_pf_nt_pt_charge(dev,&n_free_voc,&p_free_voc,&n_trap_voc,&p_trap_voc);
					np_voc_tot=get_np_tot(dev);
					get_avg_mu(dev,&mue,&muh);
					mu_voc=(mue+muh)/2.0;
					mu_geom_voc=sqrt(mue*muh);
					mu_harmonic_voc=2.0/((1.0/mue)+(1.0/muh));
					get_avg_geom_micro_mu(dev,&mu_geom_micro_voc);
					theta_voc=(n_free_voc+p_free_voc)/(n_free_voc+p_free_voc+n_trap_voc+p_trap_voc);
				}
			}

			//Pmax
			if ((Pden>Pdenlast)&&(Vexternal>0.0)&&(J<0.0))
			{
				//mobility
				get_avg_mu(dev,&mue_pmax,&muh_pmax);
				mu_pmax=(mue_pmax+muh_pmax)/2.0;
				mu_geom_pmax=sqrt(mue_pmax*muh_pmax);
				mu_harmonic_pmax=2.0/((1.0/mue_pmax)+(1.0/muh_pmax));
				get_avg_geom_micro_mu(dev,&mu_geom_micro_pmax);

				get_avg_conductance(dev,&ret_sigma_e,&ret_sigma_h);

				//theta
				get_free_nf_pf_nt_pt_charge(dev,&n_free,&p_free,&n_trap,&p_trap);
				theta_pmax=(n_free+p_free)/(n_free+p_free+n_trap+p_trap);

				r_pmax=get_avg_recom(dev);

				Pdenlast=Pden;
			}

			inter_append(&R_list,Vexternal,get_avg_recom(dev));
			inter_append(&n_list,Vexternal,get_extracted_np(dev));
			get_tau(dev,&tau,&tau_all);

			inter_append(&tau_list,Vexternal,tau);
			inter_append(&tau_all_list,Vexternal,tau_all);


			if (thermal->newton_enable_external_thermal==TRUE)
			{
				inter_append(&Tl,Vexternal,get_avg_Tl(dev));
			}


		}

		if (config.jv_use_external_voltage_as_stop==TRUE)
		{
			if (up==TRUE)
			{
				if (Vexternal>Vstop)
				{
					if (sim->fitting==FIT_NOT_FITTING)
					{
						printf_log(sim,"%s %le>%le\n",_("Stopping because of Vexternal"),Vexternal,Vstop);
					}
					break;
				}
			}else
			{
				if (Vexternal<Vstop)
				{
					if (sim->fitting==FIT_NOT_FITTING)
					{
						printf_log(sim,"%s %le<%le\n",_("Stopping because of Vexternal"),Vexternal,Vstop);
					}
					break;
				}
			}
		}

		//printf("Vapplied=%le %le\n",Vapplied,contact_get_active_contact_voltage(sim,dev));
		//getchar();
		#ifdef oghma_next
		if (dev->emission_enabled==TRUE)
		{
				if (dev->high_voltage_limit==TRUE)
				{
					ewe(sim,"If you want to ray trace in the JV curve please get in contact with me.\n");
				}

			//printf("%d\n",dev->eng.ray_auto_run);
			if (dev->eng.ray_auto_run==ray_run_step)
			{
				dev->eng.call_count++;
				outcoupling_add_ray_srcs(sim,dev, TRUE, TRUE);
				ray_solve_all(sim,dev);
				ray_dump(sim,dev);
			}else
			if (dev->eng.ray_auto_run==ray_run_step_n)
			{
				//printf(">>>\n");
				if ((ittr%dev->eng.run_each_n_steps)==0)
				{
					dev->eng.call_count++;
					outcoupling_add_ray_srcs(sim,dev, TRUE, TRUE);
					ray_solve_all(sim,dev);
					ray_dump(sim,dev);
				}
			}
		}
		#endif

		Jlast=J;
		Vlast=Vexternal;
		
		if (config.dump_verbosity!=0)
		{
			if ((dump_step>=config.dump_verbosity)||(config.dump_verbosity==1))
			{
				dump_write_to_disk(sim,dev);

				if (config.dump_energy_space==ENERGY_SPACE_MAP)
				{
					dump_device_map(sim,dev->output_path,dev);
				}

				if (config.dump_energy_space==SINGLE_MESH_POINT)
				{
					dump_energy_slice(sim,dev,config.dump_x, config.dump_y, config.dump_z);
				}

				dump_step=0;
			}
			dump_step++;
		}
		
	
		if (calculate_photon_power_m2(sim,dev)==0)
		{
			inter_append(&lv,Vexternal,dev->optical_output_power);

			inter_append(&lj,J,dev->optical_output_power);
			inter_append(&v_optical_efficiency,Vexternal,100.0*dev->optical_output_power/(J*Vexternal));

			calculate_eqe(sim,dev, &eqe, NULL,&eqe_Rtot);
			inter_append(&v_eqe,Vexternal,eqe);
			inter_append(&v_eqe_R,Vexternal,eqe_Rtot);
		}

		jv_voltage_step(sim,dev,&V,&Vstep);
		if (config.jv_step_mul>1.0)
		{
			cal_step=get_step_n(config.Vstep,config.jv_step_mul,V);
			if (cal_step<0)
			{
				cal_step=1.0;
			}
			Vstep=config.Vstep*gpow(config.jv_step_mul,cal_step);
			//printf("%lf %lf %lf %lf\n",Vstep,cal_step,config.Vstep,config.jv_step_mul);
			//getchar();
		}



		if (config.jv_use_external_voltage_as_stop==TRUE)
		{
			if ((up==TRUE)&&(Vexternal>Vstop))
			{
				dev->stop=TRUE;
			}

			if ((up==FALSE)&&(Vexternal<Vstop))
			{
				dev->stop=TRUE;
			}

		}else
		{
			if ((up==TRUE)&&(V>Vstop))
			{
				dev->stop=TRUE;
			}

			if ((up==FALSE)&&(V<Vstop))
			{
				dev->stop=TRUE;
			}
		}

		if (-J>config.jv_max_j)
		{
			dev->stop=TRUE;
		}

		if (dev->stop==TRUE)
		{
			break;
		}

		inter_append(&klist,get_extracted_np(dev),get_avg_recom(dev)/(pow(get_extracted_np(dev),2.0)));

		//math_xy_dump(sim,&klist);


		poll_gui(sim);

		if (config.jv_single_point==TRUE)
		{
			break;
		}

		if (device_clock_poll(sim,dev)==0)
		{
			contacts_cal_external_jv(sim,dev,&contact_store);
			contacts_dump_calculated_curves(sim,dev,&contact_store);
		}

		//mode_dump(sim,dev,&(dev->mode),"./");
		//getchar();
		ittr++;
	}while(1);

	ns->problem_type=ELEC_PROB_NONE;

contacts_cal_external_jv(sim,dev,&contact_store);

if (contact_store.power_den.len>0)
{

	if (contact_store.found_voc==TRUE)
	{
		power_min_pos=inter_get_min_pos(&contact_store.power_den);


		if (power_min_pos<n_list.len)
		{
			n_pmax=n_list.data[power_min_pos];
		}

		if (power_min_pos<tau_list.len)
		{
			tau_pmax=tau_list.data[power_min_pos];
		}

		if (power_min_pos<tau_all_list.len)
		{
			tau_all_pmax=tau_all_list.data[power_min_pos];
		}

		inter_get(&R_list,contact_store.Voc,&r_voc);
		inter_get(&n_list,contact_store.Voc,&n_voc);

		inter_get(&tau_list,contact_store.Voc,&tau_voc);
		inter_get(&tau_all_list,contact_store.Voc,&tau_all_voc);
		k_voc=r_voc/n_voc;
	}

}

if (get_dump_status(sim,dump_print_text)==TRUE)
{
	if (sim->fitting==FIT_NOT_FITTING)
	{
		if (contact_store.Voc!=-1.0)
		{
			printf_log(sim,"Voc= %lf (V)\n",contact_store.Voc);
		}
		printf_log(sim,"Jsc= %lf (A/m^2)\n",contact_store.Jsc);
		if (contact_store.Pmax_den!=-1.0)
		{
			printf_log(sim,"Max possible Jsc = %lf\n",get_max_Jsc(dev));
			printf_log(sim,"Pmax= %lf (W/m^2)\n",contact_store.Pmax_den);
			printf_log(sim,"Pmax %s= %lf (V)\n",_("Voltage"),contact_store.V_pmax);
			printf_log(sim,"%s= %lf percent\n",_("Efficiency"),contact_store.pce);
		}

		if (contact_store.FF!=-1.0)
		{
			printf_log(sim,"FF= %lf\n",contact_store.FF*100.0);
		}
	}

}

if (dev->simmode.circuit_simulation==FALSE)
{
	theta_srh_free=((dev->mun_y[0][0][0]+dev->mup_y[0][0][0])/2.0)*tau_pmax*contact_store.Voc/(dim->ylen*dim->ylen);
	theta_srh_free=sqrt(theta_srh_free);

	theta_srh_free_trap=((mue_pmax+muh_pmax)/2.0)*tau_pmax*contact_store.Voc/(dim->ylen*dim->ylen);
	theta_srh_free_trap=sqrt(theta_srh_free_trap);
}

sweep_save(sim,dev,dev->output_path,&store);
sweep_free(sim,dev,&store);

if (config.dump_sclc==TRUE)
{
	if (buffer_set_file_name(sim,dev,&buf,"djdv.csv")==0)
	{
		math_xy_cpy(&temp,&jv,TRUE);
		math_xy_chop(&temp,1e-6, 1e6);
		math_xy_log_y_m(&temp);
		math_xy_log_x_m(&temp);
		math_xy_deriv(NULL,&temp);
		math_xy_get_closest_y_value(&temp,&sclc_x, &sclc_y ,2.0);
		device_length=epitaxy_get_electrical_length(epi);
		sclc_V=pow(10.0,sclc_x);
		sclc_J=inter_get_hard(&jv,sclc_V);
		er=avg_vol_zxy_double(dev, dev->epsilonr);
		sclc_mu=(8.0/9.0)*sclc_J*pow(device_length,3.0)/(sclc_V*sclc_V*er);

		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.data_mul=1.0;
		sprintf(buf.title,"%s - %s",_("Voltage"),_("dj/dv"));
		strcpy(buf.type,"xy");
		strcpy(buf.y_label,_("Voltage"));
		strcpy(buf.y_units,_("Volts"));

		strcpy(buf.data_label,_("dj/dv"));
		strcpy(buf.data_units,"Am^{-2}/V");
		buf.logscale_x=TRUE;
		buf.logscale_y=TRUE;
		dat_file_add_math_xy(sim,&buf,&temp);
		dat_file_dump_path(sim,dev->output_path,NULL,&buf);
		dat_file_free(&buf);

		math_xy_free(&temp);
	}
}

if ((config.dump_verbosity>=0)||(strcmp(sim->enable_optimizer,"")!=0))
{
	if ((buffer_set_file_name(sim,dev,&buf,"sim_info.dat")==0)||(strcmp(sim->enable_optimizer,"")!=0))
	{
		contacts_dump_stats(dev,&fom,&contact_store);

		if (sm->drift_diffision_simulations_enabled==TRUE)
		{

			fom_add_val(dev, &fom,"k_voc",k_voc);
			fom_add_val(dev, &fom,"Q_np_pmax",n_pmax);
			fom_add_val(dev, &fom,"voc_nt",n_trap_voc);
			fom_add_val(dev, &fom,"voc_pt",p_trap_voc);
			fom_add_val(dev, &fom,"voc_nf",n_free_voc);
			fom_add_val(dev, &fom,"voc_pf",p_free_voc);

			fom_add_val(dev, &fom,"jv_jsc_n",nsc);
			fom_add_val(dev, &fom,"jv_vbi",(double)dev->Vbi);
			fom_add_val(dev, &fom,"jv_gen",get_avg_gen(dev));
			fom_add_val(dev, &fom,"voc_np_tot",np_voc_tot);

			fom_add_val(dev, &fom,"mu_arithmetic_jsc",mu_jsc);
			fom_add_val(dev, &fom,"mu_geom_jsc",mu_geom_jsc);
			fom_add_val(dev, &fom,"mu_harmonic_jsc",mu_harmonic_jsc);

			fom_add_val(dev, &fom,"mu_arithmetic_pmax",mu_pmax);
			fom_add_val(dev, &fom,"mu_geom_pmax",mu_geom_pmax);
			fom_add_val(dev, &fom,"mu_harmonic_pmax",mu_harmonic_pmax);

			fom_add_val(dev, &fom,"mu_arithmetic_voc",mu_voc);
			fom_add_val(dev, &fom,"mu_geom_voc",mu_geom_voc);
			fom_add_val(dev, &fom,"mu_harmonic_voc",mu_harmonic_voc);

			fom_add_val(dev, &fom,"mu_geom_micro_jsc",mu_geom_micro_jsc);
			fom_add_val(dev, &fom,"mu_geom_micro_pmax",mu_geom_micro_pmax);
			fom_add_val(dev, &fom,"mu_geom_micro_voc",mu_geom_micro_voc);
			fom_add_val(dev, &fom,"mue_pmax",mue_pmax);
			fom_add_val(dev, &fom,"muh_pmax",muh_pmax);
			fom_add_val(dev, &fom,"mue_jsc",mue_jsc);
			fom_add_val(dev, &fom,"muh_jsc",muh_jsc);

			fom_add_val(dev, &fom,"tau_voc",tau_voc);
			fom_add_val(dev, &fom,"tau_pmax",tau_pmax);
			fom_add_val(dev, &fom,"tau_all_voc",tau_all_voc);
			fom_add_val(dev, &fom,"tau_all_pmax",tau_all_pmax);

			fom_add_val(dev, &fom,"R_pmax",r_pmax);
			fom_add_val(dev, &fom,"R_voc",r_voc);

			fom_add_val(dev, &fom,"theta_srh_free",theta_srh_free);
			fom_add_val(dev, &fom,"theta_srh_free_trap",theta_srh_free_trap);

			fom_add_val(dev, &fom,"theta_jsc",theta_jsc);
			fom_add_val(dev, &fom,"theta_voc",theta_voc);
			fom_add_val(dev, &fom,"theta_pmax",theta_pmax);

			fom_add_val(dev, &fom,"conductivity_n_pmax",ret_sigma_e);
			fom_add_val(dev, &fom,"conductivity_p_pmax",ret_sigma_h);
			fom_add_val(dev, &fom,"conductivity_avg_pmax",(ret_sigma_e+ret_sigma_h)/2.0);

			if (config.dump_sclc==TRUE)
			{
				fom_add_val(dev, &fom,"sclc_er",er);
				fom_add_val(dev, &fom,"sclc_device_length",device_length);
				fom_add_val(dev, &fom,"sclc_V",sclc_V);
				fom_add_val(dev, &fom,"sclc_J",sclc_J);
				fom_add_val(dev, &fom,"sclc_mu",sclc_mu);
			}

		}
		fom_add_val(dev, &fom,"device_C",(double)dev->C);
		probes_dump_to_json(sim,dev,&fom);
		fom_dump_as_json(dev, dev->output_path,"sim_info.dat",&fom);

	}
}

if (config.dump_verbosity==1)
{
	if (buffer_set_file_name(sim,dev,&buf,"jv_internal.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.data_mul=1.0;
		sprintf(buf.title,"%s",_("Voltage/Current across just the ideal diode"));
		strcpy(buf.type,"xy");
		strcpy(buf.y_label,_("Applied Voltage"));
		strcpy(buf.data_label,_("Current density"));
		strcpy(buf.y_units,"Volts");
		strcpy(buf.data_units,"A m^{-2}");
		buf.logscale_x=0;
		buf.logscale_y=0;
		dat_file_add_math_xy(sim,&buf,&contact_store.jv_internal);
		dat_file_dump_path(sim,dev->output_path,NULL,&buf);
		dat_file_free(&buf);
	}
}

if (buffer_set_file_name(sim,dev,&buf,"k.csv")==0)
{
	dat_file_malloc(&buf);
	buf.y_mul=1.0;
	buf.x_mul=1.0;
	sprintf(buf.title,"%s - %s",_("Recombination prefactor"),_("Applied voltage"));
	strcpy(buf.type,"xy");
	strcpy(buf.y_label,_("Excess carrier density"));
	strcpy(buf.data_label,_("Recombination prefactor"));
	strcpy(buf.y_units,"m^{-3}");
	strcpy(buf.data_units,"m^{-6}s^{-1}");
	buf.logscale_x=0;
	buf.logscale_y=0;
	buf.logscale_z=0;
	dat_file_add_math_xy(sim,&buf,&klist);
	dat_file_dump_path(sim,dev->output_path,NULL,&buf);
	dat_file_free(&buf);
}

if (buffer_set_file_name(sim,dev,&buf,"charge.csv")==0)
{
	dat_file_malloc(&buf);
	buf.y_mul=1.0;
	buf.data_mul=1.0;
	sprintf(buf.title,"%s - %s",_("Excess charge density above equilibrium"),_("Applied voltage"));
	strcpy(buf.type,"xy");
	strcpy(buf.y_label,_("Applied Voltage"));
	strcpy(buf.data_label,_("Charge density"));
	strcpy(buf.y_units,"Volts");
	strcpy(buf.data_units,"m^{-3}");
	buf.logscale_x=0;
	buf.logscale_y=0;
	buf.logscale_z=0;
	dat_file_add_math_xy(sim,&buf,&charge);
	dat_file_dump_path(sim,dev->output_path,NULL,&buf);
	dat_file_free(&buf);
}

if (buffer_set_file_name(sim,dev,&buf,"charge_with_surface.csv")==0)
{
	dat_file_malloc(&buf);
	buf.y_mul=1.0;
	buf.data_mul=1.0;
	sprintf(buf.title,"%s - %s",_("Charge density with correction for surface charge"),_("Applied voltage"));
	strcpy(buf.type,"xy");
	strcpy(buf.y_label,_("Applied Voltage"));
	strcpy(buf.data_label,_("Charge density"));
	strcpy(buf.y_units,"Volts");
	strcpy(buf.data_units,"m^{-3}");
	buf.logscale_x=0;
	buf.logscale_y=0;
	buf.logscale_z=0;
	dat_file_add_math_xy(sim,&buf,&charge_with_surface_charge);
	dat_file_dump_path(sim,dev->output_path,NULL,&buf);
	dat_file_free(&buf);
}


if (buffer_set_file_name(sim,dev,&buf,"charge_tot.csv")==0)
{
	dat_file_malloc(&buf);
	buf.y_mul=1.0;
	buf.data_mul=1.0;
	sprintf(buf.title,"%s - %s",_("Total charge density"),_("Applied voltage"));
	strcpy(buf.type,"xy");
	strcpy(buf.y_label,_("Applied Voltage"));
	strcpy(buf.data_label,_("Total charge density"));
	strcpy(buf.y_units,"Volts");
	strcpy(buf.data_units,"m^{-3}");
	buf.logscale_x=0;
	buf.logscale_y=0;
	buf.logscale_z=0;
	dat_file_add_math_xy(sim,&buf,&charge_tot);
	dat_file_dump_path(sim,dev->output_path,NULL,&buf);
	dat_file_free(&buf);
}

contacts_dump_calculated_curves(sim,dev,&contact_store);


if (thermal->newton_enable_external_thermal==TRUE)
{
	if (buffer_set_file_name(sim,dev,&buf,"v_Tl.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.data_mul=1.0;
		sprintf(buf.title,"%s - %s",_("Voltage"),_("Lattice temperature"));
		strcpy(buf.type,"xy");
		strcpy(buf.y_label,_("Voltage"));
		strcpy(buf.data_label,_("Lattice temperature"));
		strcpy(buf.y_units,_("Volts"));
		strcpy(buf.data_units,"K");
		buf.logscale_x=0;
		buf.logscale_y=0;
		dat_file_add_math_xy(sim,&buf,&Tl);
		dat_file_dump_path(sim,dev->output_path,NULL,&buf);
		dat_file_free(&buf);
	}
}

if (dev->emission_enabled==TRUE)
{
	if (config.eqe_smooth==TRUE)
	{
		v_eqe_poly_smooth(sim,dev, &v_eqe, &v_eqe_R);
	}

	if (buffer_set_file_name(sim,dev,&buf,"v_eqe.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.data_mul=1.0;
		sprintf(buf.title,"%s - %s",_("Voltage"),_("EQE"));
		strcpy(buf.type,"xy");
		strcpy(buf.y_label,("Applied Voltage"));
		strcpy(buf.data_label,("EQE"));
		strcpy(buf.y_units,"Volts");
		strcpy(buf.data_units,"(%)");
		buf.logscale_x=0;
		buf.logscale_y=0;
		dat_file_add_math_xy(sim,&buf,&v_eqe);
		dat_file_dump_path(sim,dev->output_path,NULL,&buf);
		dat_file_free(&buf);
	}


	if (buffer_set_file_name(sim,dev,&buf,"vl.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.data_mul=1.0;
		buf.data_mul=1;
		sprintf(buf.title,"%s - %s",_("Voltage"),_("Light flux"));
		strcpy(buf.type,"xy");
		strcpy(buf.y_label,("Applied Voltage"));
		strcpy(buf.data_label,("Light flux"));
		strcpy(buf.y_units,"Volts");
		strcpy(buf.data_units,"W m^{-2}");
		buf.logscale_x=0;
		buf.logscale_y=0;
		dat_file_add_math_xy(sim,&buf,&lv);
		dat_file_dump_path(sim,dev->output_path,NULL,&buf);
		dat_file_free(&buf);
	}

	if (buffer_set_file_name(sim,dev,&buf,"jl.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.data_mul=1.0;
		sprintf(buf.title,"%s - %s",_("Current density"),_("Light flux"));
		strcpy(buf.type,"xy");
		strcpy(buf.y_label,("Current density"));
		strcpy(buf.data_label,_("Light flux"));
		strcpy(buf.y_units,"A m^{-2}");
		strcpy(buf.data_units,"W m^{-2}");
		buf.logscale_x=0;
		buf.logscale_y=0;
		dat_file_add_math_xy(sim,&buf,&lj);
		dat_file_dump_path(sim,dev->output_path,NULL,&buf);
		dat_file_free(&buf);
	}

	if (buffer_set_file_name(sim,dev,&buf,"v_optical_efficiency.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.data_mul=1.0;
		sprintf(buf.title,"%s - %s",_("Voltage"),_("Power in Optical emission/Electrical power in"));
		strcpy(buf.type,"xy");
		strcpy(buf.y_label,("Voltage"));
		strcpy(buf.data_label,_("Efficiency"));
		strcpy(buf.y_units,"V");
		strcpy(buf.data_units,"%");
		buf.logscale_x=0;
		buf.logscale_y=0;
		dat_file_add_math_xy(sim,&buf,&v_optical_efficiency);
		dat_file_dump_path(sim,dev->output_path,NULL,&buf);
		dat_file_free(&buf);
	}


	if (buffer_set_file_name(sim,dev,&buf,"sigma.csv")==0)
	{
		dat_file_malloc(&buf);
		buf.y_mul=1.0;
		buf.data_mul=1.0;
		sprintf(buf.title,"%s - %s",_("Voltage"),_("Conductivity"));
		strcpy(buf.type,"xy");
		strcpy(buf.y_label,("Voltage"));
		strcpy(buf.data_label,_("Conductivity"));
		strcpy(buf.y_units,"V");
		strcpy(buf.data_units,"S/m");
		buf.logscale_x=0;
		buf.logscale_y=0;
		dat_file_add_math_xy(sim,&buf,&contact_store.sigma);
		dat_file_dump_path(sim,dev->output_path,NULL,&buf);
		dat_file_free(&buf);
	}
}


math_xy_free(&charge);
math_xy_free(&charge_with_surface_charge);
math_xy_free(&lv);
math_xy_free(&v_eqe);
math_xy_free(&v_eqe_R);
math_xy_free(&lj);
math_xy_free(&klist);
math_xy_free(&R_list);
math_xy_free(&n_list);
math_xy_free(&tau_list);
math_xy_free(&tau_all_list);
math_xy_free(&Tl);
math_xy_free(&v_optical_efficiency);
math_xy_free(&charge_tot);
math_xy_free(&jv);
math_xy_free(&temp);

fom_free(&fom);

contacts_dump(sim,dev,&contact_store,TRUE);
dump_contacts_free(sim,dev,&contact_store);

light_set_sun(&(dev->mylight),sun_orig);

	if (get_dump_status(sim,dump_remove_dos_cache)==TRUE)
	{
		char tmp_path[PATH_MAX];
		join_path(2,tmp_path,dev->output_path,"snapshots");
		remove_dir(sim,tmp_path);
	}

}




void jv_load_config(struct simulation *sim, struct jv* dev, struct sweep_store *sweep, struct json_obj *json_jv)
{
	struct json_obj *json_config;
	json_config=json_obj_find(json_jv, "config");
	if (json_config==NULL)
	{
		ewe(sim,"No config section found\n");
	}

	json_get_double(sim,json_config, &(dev->Vstart),"Vstart",TRUE);
	json_get_double(sim,json_config, &(dev->Vstop),"Vstop",TRUE);
	json_get_double(sim,json_config, &(dev->Vstep),"Vstep",TRUE);

	dev->Vstep=fabs(dev->Vstep);

	if (dev->Vstop<dev->Vstart)
	{
		dev->Vstep*=-1.0;
	}

	json_get_double(sim,json_config, &(dev->jv_step_mul),"jv_step_mul",TRUE);
	if (dev->jv_step_mul<1.0)
	{
		dev->jv_step_mul=1.0;
	}
	json_get_double(sim,json_config, &(dev->jv_light_efficiency),"jv_light_efficiency",TRUE);
	dev->jv_light_efficiency=gfabs(dev->jv_light_efficiency);

	if (dev->jv_light_efficiency<=0.0)
	{
		ewe(sim,"You can't have a photon efficiency of zero. Try turning the light off instead.\n");
	}

	json_get_double(sim,json_config, &(dev->jv_max_j),"jv_max_j",TRUE);


	json_get_english(sim,json_config, &(dev->jv_single_point),"jv_single_point",TRUE);

	json_get_int(sim,json_config, &(dev->dump_verbosity),"dump_verbosity",TRUE);


	json_get_english(sim,json_config, &(dev->dump_energy_space),"dump_energy_space",TRUE);
	json_get_int(sim,json_config, &(dev->dump_x),"dump_x",TRUE);
	json_get_int(sim,json_config, &(dev->dump_y),"dump_y",TRUE);
	json_get_int(sim,json_config, &(dev->dump_z),"dump_z",TRUE);


	json_get_english(sim,json_config, &(dev->jv_use_external_voltage_as_stop),"jv_use_external_voltage_as_stop",TRUE);
	json_get_string(sim,json_config, dev->charge_carrier_generation_model,"charge_carrier_generation_model",TRUE);
	json_get_english(sim,json_config, &(dev->dump_sclc),"dump_sclc",TRUE);
	json_get_english(sim,json_config, &(dev->eqe_smooth),"eqe_smooth",TRUE);

	json_get_english(sim,json_config, &(sweep->dump_level),"dump_sweep_save",TRUE);

}
