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

/** @file device.h
	@brief The main structure which holds information about the device.
*/

#ifndef device_h
#define device_h
#include <g_io.h>
#include <stdio.h>
#include "code_ctrl.h"
#include "light.h"
#include <epitaxy_struct.h>
#include "advmath.h"
#include <contact_struct.h>
#include <perovskite_struct.h>
#include <circuit_struct.h>
#include <dim.h>
#include <matrix.h>
#include <shape_struct.h>
#include <heat.h>
#include <exciton.h>
#include <singlet.h>
#include <mesh_struct.h>
#include <lib_fxdomain.h>
#include <time_mesh.h>
#include <matrix_solver_memory.h>
#include <json.h>
#include <world_struct.h>
#include <optical_mode.h>
#include <probes.h>
#include <ray.h>
#include <fom_struct.h>
#include <outcoupling.h>
#include <newton_state.h>
#include <dump_ctrl.h>

struct solver_cache
{
	char hash[100];
	long cache_max_size;
	long cache_min_disk_free;
	long cache_sims_to_keep;
	int enabled;
};


struct simmode
{
	char simmode[200];
	char optical_solver[200];
	int drift_diffision_simulations_enabled;
	int electrical_simulation_enabled;
	int optical_simulations_enabled;
	int exciton_simulations_enabled;
	int circuit_simulation;
};

struct device
{

	int sim_number;

	//times
		long long start_time;
		long long stop_time;
		long long last_poll;

	//Dimensions
		double xlen;
		double ylen;
		double zlen;

		double Vol;
		double area;

	//Meshing
		int remesh;
		int newmeshsize;
		int dynamic_mesh;

	//Current at contacts
		double **Jn_y0;
		double **Jn_y1;
		double **Jp_y0;
		double **Jp_y1;

		double **Jn_x0;
		double **Jn_x1;
		double **Jp_x0;
		double **Jp_x1;

		double **Jn_z0;
		double **Jn_z1;
		double **Jp_z0;
		double **Jp_z1;

	//The contact number
		int **n_contact_y0;
		int **n_contact_y1;
		int **n_contact_x0;
		int **n_contact_x1;
		int **n_contact_z0;
		int **n_contact_z1;

	//Contact fermi levels
		gdouble **Fi0_y0;		//This is the equilibrium fermi level of the contact were it in free space, i.e. with no phi subtracted
		gdouble **Fi0_y1;		
		gdouble **Fi0_x0;
		gdouble **Fi0_x1;
		gdouble **Fi0_z0;
		gdouble **Fi0_z1;

	//Built in potentials
		gdouble **V_y0;		//Diference between the equlibrium fermi level and the fermilevel at in->Fi0_y0[0][0]
		gdouble **V_y1;		//This is referenced to Fi0_y0[0][0], and is the difference between Fi0_y0[0][0] and Fi0_y0[z][x/y]
		gdouble **V_x0;		//, this difference must be equal to the built in potential on the contact
		gdouble **V_x1;
		gdouble **V_z0;
		gdouble **V_z1;

		gdouble Vbi;		//I have no idea why there are two

	//Charge densities on surfaces even away from contacts
		gdouble **electrons_y0;
		gdouble **electrons_y1;
		gdouble **electrons_x0;
		gdouble **electrons_x1;
		gdouble **electrons_z0;
		gdouble **electrons_z1;

		gdouble **holes_y0;
		gdouble **holes_y1;
		gdouble **holes_x0;
		gdouble **holes_x1;
		gdouble **holes_z0;
		gdouble **holes_z1;

	//optical mode
		struct optical_mode mode;
		double ***mode_epitaxy;

	//Bands
		double ***Eg;
		double ***Xi;

	//Generation
		double ***G;
		double ***Gn;
		double ***Gp;

	//Fermi levels
		gdouble ***Fi;
		double ***Nc;
		double ***Nv;
		double ***B;

	//Interfaces
		int interfaces_n;
		int interfaces_n_srh;
		int ***interface_type;
		gdouble ***interface_B;
		gdouble ***interface_Bt;
		gdouble ***interface_R;

		//Tunneling
		int interfaces_tunnels_e;
		int interfaces_tunnels_h;
		gdouble ***interface_Ge;
		gdouble ***interface_Gh;

	//Mobility
		int mun_symmetric;
		double ***mun_z;
		double ***mun_x;
		double ***mun_y;

		int mup_symmetric;
		double ***mup_z;
		double ***mup_x;
		double ***mup_y;

		gdouble ***muion;

	//Auger
		double ***Cn;
		double ***Cp;
		int auger_enabled;

	//SS SRH
		int ss_srh_enabled;
		gdouble ***n1;
		gdouble ***p1;
		gdouble ***tau_n;
		gdouble ***tau_p;

	//Electrostatics
		gdouble ***epsilonr;
		gdouble ***epsilonr_e0;

	//Temperature
		gdouble ***Tl;
		gdouble ***Te;
		gdouble ***Th;

	//Heating
		gdouble ***Hl;		//**move
		gdouble ***H_recombination;		//**move
		gdouble ***H_joule;		//**move

		gdouble ***He;		//**move
		gdouble ***Hh;		//**move

		gdouble ***ke;		//Thernal conductivities
		gdouble ***kh;

	//Applied voltages
		gdouble **Vapplied_y0;
		gdouble **Vapplied_y1;
		gdouble **Vapplied_x0;
		gdouble **Vapplied_x1;
		gdouble **Vapplied_z0;
		gdouble **Vapplied_z1;

	//Passivation
		int **boundary_y0;
		int **boundary_y1;
		int **boundary_x0;
		int **boundary_x1;
		int **boundary_z0;
		int **boundary_z1;


	//Device layout
		struct dimensions dim_optical;		//Optical dimensions

		struct dim_zx_epitaxy dim_epitaxy;				//This is a dim object with zx and the length of the epitaxy


	//Trap control
		int srh_sim;
		int ntrapnewton;
		int ptrapnewton;

	//Newton solver control
		int max_electrical_itt;
		double electrical_clamp;
		double min_cur_error;

		int max_electrical_itt0;
		double electrical_clamp0;
		double electrical_error0;
		int temperature_ramp0;

		int math_enable_pos_solver;

		char newton_name[20];

		int kl_in_newton;
		int config_kl_in_newton;
		void (*newton_aux)(struct simulation *sim, struct device* ,gdouble ,gdouble* ,gdouble* ,gdouble* ,gdouble* ,gdouble* ,gdouble* ,gdouble* ,gdouble*);

		int newton_clever_exit;

		int newton_only_fill_matrix;
		gdouble omega;

		int newton_min_itt;

		int newton_last_ittr;

	//block matrix normalization
		int block_auto;
		double block_phi_norm;
		double block_Je_norm;
		double block_Jh_norm;
		double block_srh_e_norm;
		double block_srh_h_norm;

	//Electrical components
		double Rshunt;
		double Rcontact;
		double Rload;
		double L;
		double C;
		double Rshort;
		double other_layers;
		double contact_charge;

	//Dump contorl
		gdouble dump_dynamic_pl_energy;	//This needs to be removed
		int dump_binary;

		int snapshot_number;

		int timedumpcount;

		struct probes pr;
		int dump_optical_probe;
		int dump_optical_probe_spectrum;
		int dump_probes;

	//time
		int go_time;
		gdouble dt;
		gdouble time;
		gdouble Ilast;

	//Run control
		int stop;
		int onlypos;
		int odes;
		int dd_conv;
		int high_voltage_limit;

	//Matrix
		struct matrix mx;

	//Newton solver internal memory
		//none

	//meshing
		struct mesh_obj mesh_data;
		struct mesh_obj mesh_data_save;
		struct mesh_obj optical_mesh_data;		//This should be in world

		gdouble layer_start[100];
		gdouble layer_stop[100];

	//epitaxy
		struct epitaxy my_epitaxy;

	//plugins
		struct simmode simmode;

	//Material concentrations
		double ***x;
		double ***y;

	//Doping
		double ***Nad;

	//Newton states
		struct newton_state *ns;
		struct newton_states ns_lib;

	//Light
		struct light mylight;
		struct light probe_modes;

		struct math_xy steady_stark;
		struct light_sources lights;

	//Emission
		int emission_enabled;
		double pl_intensity;
		double pl_intensity_tot;
		int pl_use_experimental_emission_spectra;
		double ***Photon_gen;
		double ****photons_escape_prob;
		double *** photons_escape_prob_lam_avg;
		double optical_output_power;			//Wm-2
		double optical_output_photon_flux;		//m-2

	//thermal
		struct heat thermal;

	//exciton
		struct exciton ex;

	//singlet
		struct singlet sing;
		struct singlet_opv sing_opv;

	//Preovskite
		struct perovskite mobileion;

	//Circuit simulation
		struct circuit cir;

	//Ray tracing
		struct ray_engine eng;
		struct shape big_box;

	//Contacts
		struct contact *contacts;
		int ncontacts;
		int active_contact;

		double flip_current;
		int cal_current_at;
		int use_sg_currents;

	//objects
		struct object ****obj_zxy;
		struct object ****obj_zx_layer;
		struct object ****obj_zxy_optical;

	//time mesh
		struct time_mesh tm;

	//solver cache
		char solver_type[200];
		struct solver_cache cache;

	//fxdomain config
		struct fxdomain fxdomain_config;
	
	//matrix solver memory
		struct matrix_solver_memory msm;

	//configure
		struct json config;

	//temp vars
		gdouble glob_wanted;

	//paths
	//paths
		char output_path[OGHMA_PATH_MAX];
		char input_path[OGHMA_PATH_MAX];

	//Newton solver
		int solver_verbosity;

	//the world
	struct world w;
	struct vec device_start;
	struct vec device_stop;

	//fom
	struct fom *fom;

	//outcoupling
	struct outcoupling outcoupling;

	struct dump_ctrl dump_ctrl;

};


#endif
