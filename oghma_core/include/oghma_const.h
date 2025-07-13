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

/** @file oghma_const.h
	@brief Physical constants.
*/

#ifndef h_oghma_const
#define h_oghma_const

#include <enabled_libs.h>

//Physical constants
#define STR_MAX	4096
#define OGHMA_PATH_MAX	4096


#define INSTALL_DIR "OghmaNano"

#define CRYPTO_KEY_DAT_FILE "hello"
#define LICENSE_FILE "settings3.inp"
#define epsilon0 (double)8.85418782e-12			// m-3 kg-1 s4 A2;
#define epsilon0f (float)8.85418782e-12			// m-3 kg-1 s4 A2;

#define mu0 (double)1.25663706e-6
#define mu0f (float)1.25663706e-6			//

#define hp (gdouble)6.62606896e-34			//J S Wikipeda
#define PI (gdouble)3.14159265358979323846

#define PIf (float)3.14159265358979323846

#define hbar (gdouble)(6.62606896e-34/(2.0*PI))	//Calculated
#define kb (gdouble)1.3806504e-23			//J K-1 Wiki
#define Qe (gdouble)1.602176487e-19			//C Wikipeda
#define m0 (gdouble)9.10938215e-31 			//Kg Wikipeda
#define cl  (gdouble)2.99792458e8			//m/s Wikipieda
#define clf  (float)2.99792458e8			//m/s Wikipieda

#define LO_T 1e-7
#define HI_T 429.4967296

//SRH constants
#define srh_1	1
#define srh_2	2
#define srh_3	3
#define srh_4	4
#define interface_schottky	 1

//Interfaces
#define INTERFACE_NONE				0
#define INTERFACE_RECOMBINATION		1
#define INTERFACE_RECOMBINATION_SRH	2
//TRUE/FALSE
#define TRUE 1
#define FALSE 0

#define yes_nk 1
#define yes_k 2

#define TOP 0
#define BOTTOM 1
#define RIGHT 2
#define LEFT 3
#define FRONT 4
#define BACK 5
#define XYZ_POS 4

#define ELECTRON 0
#define HOLE 1

#define FIT_SIMPLEX 0
#define FIT_NEWTON 1
#define FIT_BFGS 2
#define FIT_MCMC 3
#define FIT_HMC 4
#define FIT_NUTS 5
#define FIT_ANNEALING 6

#define FIT_NOT_FITTING 0
#define FIT_SINGLE_FIT 1
#define FIT_RUN_FIT 2
#define OPTIMIZER_RUNNING 3

#define FIT_RUN 0
#define FIT_FINISH 1
#define FIT_RESET 2			//Reset to origonal state
#define FIT_RESET_SOFT 3	//Reset minimizer but reload best state

#define TINY 1.0e-10		//A small number.
#define SIMPLEX_CONVERGED 1
#define SIMPLEX_MAX 2

//newton_state problem_type
enum {
    ELEC_PROB_NONE		= 0,
    ELEC_PROB_MAIN_LOOP		= 1 << 1
};

//tpv light
#define tpv_set_light 0
#define tpv_set_voltage 1
#define tpv_mode_laser	0
#define tpv_mode_sun 1

//sim modes
#define IDEAL_DIODE_IDEAL_LOAD 2
#define LOAD 1
#define OPEN_CIRCUIT 0


//dump control
#define dump_write_converge 6
#define dump_print_text 7
#define dump_lock 11
#define dump_norm_time_to_one 12
#define dump_band_structure 14
#define dump_first_guess 17
#define dump_print_pos_error 19
#define dump_norm_y_axis 24
#define dump_write_out_band_structure 25

#define dump_write_headers 37
#define dump_remove_dos_cache 38

#define log_level_none 0
#define log_level_screen 1
#define log_level_memory 2
#define log_level_disk 3
#define log_level_screen_and_disk 4

//Atempt to put output in files
#define dump_nothing				-1
#define dump_verbosity_key_results	0	
#define dump_verbosity_everything	1

//energy space dump
#define ENERGY_SPACE_MAP 1
#define SINGLE_MESH_POINT 2

//dos types
#define dos_exp		0
#define dos_an		1
#define dos_fd		2
#define dos_exp_fd 	3

//fx_domain signal_types
#define LARGE_SIGNAL	0
#define SMALL_SIGNAL	1
#define FOURIER			2

//free dos types
#define mb_equation 0
#define mb_look_up_table 1
#define fd_look_up_table 2
#define mb_look_up_table_analytic 3

//contact types

#define contact_ohmic 0
#define contact_blocking 1
#define contact_ohmic_barrier 2
#define contact_schottky 3

//Ray tracer
#define ray_run_never		0
#define ray_run_once    	1
#define ray_run_step		2
#define ray_run_step_n		3
#define RAY_SIM_EDGE		0
#define RAY_VIEWPOINT		1
#define RAY_OBJECT			2
#define RAY_FAKE_OBJECT		3
#define ray_emission_single_point 0
#define ray_emission_electrical_mesh 1
#define ray_emission_every_x_point 2

//Heat model
#define THERMAL_HYDRODYNAMIC 	0
#define THERMAL_LATTICE 			1
#define T_thermal_ramp_needed 280.0

#define ISOTHERMAL	0
#define DIRICHLET	0
#define NEUMANN		1
#define HEATSINK	2
#define A_B_C 		3
#define PERIODIC	4
#define INTERPOLATE	5

//fdtd
#define FDTD_SIN 	0
#define FDTD_PULSE 	1

//circuit mesh
#define HAND_DRAWN 0
#define FROM_LAYERS 1
#define FROM_MESH 2

#define measure_voltage		0
#define measure_current		1

#define LAYER_ACTIVE 	0
#define LAYER_CONTACT 	1
#define LAYER_OTHER		2
#define LAYER_BHJ		3

	#include <linux/limits.h>

#define WAIT 0
#define READY 1
#define DONE 2

#define TRUE 1
#define FALSE 0
#define AUTO 2
	#define THREAD_NULL	-1
	#define THREAD_FUNCTION void *
	#define INVALID_HANDLE_VALUE -1

#define SOLVER_VERBOSITY_NOTHING 0
#define SOLVER_VERBOSITY_AT_END 1
#define SOLVER_VERBOSITY_EVERY_STEP 2

//spm
#define SPM_WHOLE_DEVICE 0
#define SPM_BOX 1
#define SPM_X_CUT 2

#define GPVDM_INT 0
#define GPVDM_FLOAT 1
#define GPVDM_DOUBLE 2
#define GPVDM_LONG_DOUBLE 3

enum {
    SOLVE_POS_Y			= 1 << 0,
    SOLVE_POS_X			= 1 << 1,
	SOLVE_POS_Z			= 1 << 2,
    SOLVE_JE_Y			= 1 << 3,
    SOLVE_JH_Y			= 1 << 4,
    SOLVE_JE_X			= 1 << 5,
    SOLVE_JH_X			= 1 << 6,
    SOLVE_JE_Z			= 1 << 7,
    SOLVE_JH_Z			= 1 << 8,
    SOLVE_SRH_E			= 1 << 9,
    SOLVE_SRH_H			= 1 << 10,
    SOLVE_NION			= 1 << 11,
    SOLVE_SINGLET		= 1 << 12,
    SOLVE_SINGLET_OPV 	= 1 << 13,
    SOLVE_AUGER 		= 1 << 14,
    SOLVE_SRH_SS 		= 1 << 15,
};

enum {
    BOUNDARY_POS_DIRICHLET		= 1 << 0,
    BOUNDARY_POS_NEUMANN		= 1 << 1,
	BOUNDARY_Je_DIRICHLET		= 1 << 2,
	BOUNDARY_Je_NEUMANN			= 1 << 3,
	BOUNDARY_Jh_DIRICHLET		= 1 << 4,
	BOUNDARY_Jh_NEUMANN			= 1 << 5
};

//probes
#define GPVDM_POINT 0
#define GPVDM_AVERAGE 1
#define GPVDM_MIN 2
#define GPVDM_MAX 3
#define GPVDM_MAX_POS_Y_SLICE 4
#define GPVDM_MAX_POS_Y_SLICE0 5
#define GPVDM_MAX_POS_Y_SLICE1 6
#define GPVDM_MAX_POS_Y_VAL_SLICE 7
#define GPVDM_MAX_POS_Y_VAL_SLICE0 8
#define GPVDM_MAX_POS_Y_VAL_SLICE1 9
#define GPVDM_VAL_AT_Y 10

#define PROBE_SRC_DOUBLE_ZXY 0
#define PROBE_SRC_MATH_XY 1

#define HTTP_REGISTRATION "www.gpvdm.com"
#define REPOSITORY_TYPE_OGHMA	0
#define REPOSITORY_TYPE_GIT		1
#define CONTACTS 0
#define MID_POINT 1
#define AVG 2

//OpenGL consts
#define OGHMA_GL_LIGHT 0
#define OGHMA_GL_REAL_WORLD_OBJECT 1

//math_xy
#define DIFF_DELTA 	0
#define DIFF_PDF 	1
#define DIFF_CHI 	2

//Random
#define RAND_TWISTER 0
#define RAND_C 1

//Server
#define SERVER_NO_THREAD	0
#define SERVER_THREAD		1
#define SERVER_PROCESS		2
#define SERVER_SYSTEM		3

#define JOB_NONE		0
#define JOB_WAIT		1
#define JOB_RUNNING		2
#define JOB_FINISHED	3

//mouse
#define NoButton        0x00000000
#define LeftButton      0x00000001
#define RightButton     0x00000002
#define MiddleButton    0x00000004
#endif
