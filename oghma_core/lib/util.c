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

/** @file util.c
	@brief Utility functions.
*/


#include <enabled_libs.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "log.h"
#include <oghma_const.h>
#include <lang.h>
#include <math.h>
#include <ctype.h>
#include <cal_path.h>
#include <g_io.h>

static char* unused_pchar __attribute__((unused));


void print_hex(struct simulation *sim,unsigned char *data)
{
	int i;
	for (i=0;i<16;i++)
	{
		printf_log(sim,"%02x",data[i]);
	}
	printf_log(sim,"\n");
}

void str_to_lower(char *out, char *in)
{
	int i=0;
	for (i=0;i<strlen(in);i++)
	{
		out[i]=tolower(in[i]);
	}
	out[i]=0;

}

int check_int(char *in)
{
int i=0;
int numeric=TRUE;
for (i=0;i<strlen(in);i++)
{
	if ((in[i]<48)||(in[i]>57))
	{
		numeric=FALSE;
		break;
	}
}
return numeric;
}
static int unused __attribute__((unused));

int english_to_bin(struct simulation *sim, char * in)
{
char temp[100];
int ret=0;

str_to_lower(temp, in);

if (check_int(temp)==TRUE)
{
sscanf(temp,"%d",&ret);
return ret;
}

if (strcmp(temp,"true")==0)
{
	return TRUE;
}else
if (strcmp(temp,"false")==0)
{
	return FALSE;
}else
if (strcmp(temp,"1")==0)
{
	return TRUE;
}else
if (strcmp(temp,"0")==0)
{
	return FALSE;
}else
if (strcmp(temp,"yes")==0)
{
	return TRUE;
}else
if (strcmp(temp,"no")==0)
{
	return FALSE;
}else
if (strcmp(temp,"left")==0)
{
	return LEFT;
}else
if (strcmp(temp,"right")==0)
{
	return RIGHT;
}else
if (strcmp(temp,"gaus")==0)
{
	return 0;
}else
if (strcmp(temp,"exp")==0)
{
	return 1;
}else
if (strcmp(temp,"lorentzian")==0)
{
	return 2;
}else
if (strcmp(temp,"exponential")==0)
{
	return dos_exp;
}else
if (strcmp(temp,"complex")==0)
{
	return dos_an;
}
else
if (strcmp(temp,"open_circuit")==0)
{
	return OPEN_CIRCUIT;
}else
if (strcmp(temp,"load")==0)
{
	return LOAD;
}else
if (strcmp(temp,"ideal_diode_ideal_load")==0)
{
	return IDEAL_DIODE_IDEAL_LOAD;
}else
if (strcmp(temp,"none")==0)
{
	return log_level_none;
}else
if (strcmp(temp,"screen")==0)
{
	return log_level_screen;
}else
if (strcmp(temp,"disk")==0)
{
	return log_level_disk;
}else
if (strcmp(temp,"screen_and_disk")==0)
{
	return log_level_screen_and_disk;
}else
if (strcmp(temp,"newton")==0)
{
	return FIT_NEWTON;
}else
if (strcmp(temp,"simplex")==0)
{
	return FIT_SIMPLEX;
}else
if (strcmp(temp,"bfgs")==0)
{
	return FIT_BFGS;
}else
if (strcmp(temp,"top")==0)
{
	return TOP;
}else
if (strcmp(temp,"bottom")==0)
{
	return BOTTOM;
}else
if (strcmp(temp,"right")==0)
{
	return RIGHT;
}else
if (strcmp(temp,"left")==0)
{
	return LEFT;
}else

if (strcmp(temp,"electron")==0)
{
	return ELECTRON;
}else
if (strcmp(temp,"hole")==0)
{
	return HOLE;
}else
if (strcmp(temp,"mb_equation")==0)
{
	return mb_equation;
}else
if (strcmp(temp,"mb_look_up_table")==0)
{
	return mb_look_up_table;
}else
if (strcmp(temp,"fd_look_up_table")==0)
{
	return fd_look_up_table;
}else
if (strcmp(temp,"mb_look_up_table_analytic")==0)
{
	return mb_look_up_table_analytic;
}else
if (strcmp(temp,"ohmic")==0)
{
	return contact_ohmic;
}else
if (strcmp(temp,"schottky")==0)
{
	return contact_schottky;
}else
if (strcmp(temp,"ray_run_never")==0)
{
	return ray_run_never;
}else
if (strcmp(temp,"ray_run_once")==0)
{
	return ray_run_once;
}else
if (strcmp(temp,"ray_run_step")==0)
{
	return ray_run_step;
}else
if (strcmp(temp,"ray_run_step_n")==0)
{
	return ray_run_step_n;
}else
if (strcmp(temp,"ray_emission_single_point")==0)
{
	return ray_emission_single_point;
}else
if (strcmp(temp,"ray_emission_electrical_mesh")==0)
{
	return ray_emission_electrical_mesh;
}else
if (strcmp(temp,"ray_emission_every_x_point")==0)
{
	return ray_emission_every_x_point;
}else
if (strcmp(temp,"measure_voltage")==0)
{
	return measure_voltage;
}else
if (strcmp(temp,"measure_current")==0)
{
	return measure_current;
}else
if (strcmp(temp,"contact")==0)
{
	return LAYER_CONTACT;
}else
if (strcmp(temp,"active")==0)
{
	return LAYER_ACTIVE;
}else
if (strcmp(temp,"other")==0)
{
	return LAYER_OTHER;
}else
if (strcmp(temp,"thermal_hydrodynamic")==0)
{
	return THERMAL_HYDRODYNAMIC;
}else
if (strcmp(temp,"thermal_lattice")==0)
{
	return THERMAL_LATTICE;
}else
if (strcmp(temp,"dirichlet")==0)
{
	return ISOTHERMAL;
}else
if (strcmp(temp,"dirichlet")==0)
{
	return DIRICHLET;
}else
if (strcmp(temp,"neumann")==0)
{
	return NEUMANN;
}else
if (strcmp(temp,"abc")==0)
{
	return A_B_C;
}else
if (strcmp(temp,"periodic")==0)
{
	return PERIODIC;
}else
if (strcmp(temp,"heatsink")==0)
{
	return HEATSINK;
}else
if (strcmp(temp,"dump_nothing")==0)
{
	return dump_nothing;
}
if (strcmp(temp,"dump_verbosity_key_results")==0)
{
	return dump_verbosity_key_results;
}else
if (strcmp(temp,"dump_verbosity_everything")==0)
{
	return dump_verbosity_everything;
}else
if (strcmp(temp,"large_signal")==0)
{
	return LARGE_SIGNAL;
}else
if (strcmp(temp,"small_signal")==0)
{
	return SMALL_SIGNAL;
}else
if (strcmp(temp,"fourier")==0)
{
	return FOURIER;
}else
if (strcmp(temp,"none")==0)
{
	return INTERFACE_NONE;
}else
if (strcmp(temp,"recombination")==0)
{
	return INTERFACE_RECOMBINATION;
}else
if (strcmp(temp,"recombination_srh")==0)
{
	return INTERFACE_RECOMBINATION_SRH;
}else
if (strcmp(temp,"interpolate")==0)
{
	return INTERPOLATE;
}else
if (strcmp(temp,"constant")==0)
{
	return INTERPOLATE2;
}else
if (strcmp(temp,"solver_verbosity_nothing")==0)
{
	return SOLVER_VERBOSITY_NOTHING;
}else
if (strcmp(temp,"solver_verbosity_every_step")==0)
{
	return SOLVER_VERBOSITY_EVERY_STEP;
}else
if (strcmp(temp,"solver_verbosity_at_end")==0)
{
	return SOLVER_VERBOSITY_AT_END;
}else
if (strcmp(temp,"spm_whole_device")==0)
{
	return SPM_WHOLE_DEVICE;
}else
if (strcmp(temp,"spm_box")==0)
{
	return SPM_BOX;
}else
if (strcmp(temp,"spm_x_cut")==0)
{
	return SPM_X_CUT;
}else
if (strcmp(temp,"fdtd_sin")==0)
{
	return FDTD_SIN;
}else
if (strcmp(temp,"fdtd_pulse")==0)
{
	return FDTD_PULSE;
}else
if (strcmp(temp,"energy_space_map")==0)
{
	return ENERGY_SPACE_MAP;
}else
if (strcmp(temp,"single_mesh_point")==0)
{
	return SINGLE_MESH_POINT;
}else
if (strcmp(temp,"point")==0)
{
	return GPVDM_POINT;
}else
if (strcmp(temp,"average")==0)
{
	return GPVDM_AVERAGE;
}else
if (strcmp(temp,"max")==0)
{
	return GPVDM_MAX;
}else
if (strcmp(temp,"min")==0)
{
	return GPVDM_MIN;
}else
if (strcmp(temp,"max_pos_y_slice")==0)
{
	return GPVDM_MAX_POS_Y_SLICE;
}else
if (strcmp(temp,"max_pos_y_slice0")==0)
{
	return GPVDM_MAX_POS_Y_SLICE0;
}else
if (strcmp(temp,"max_pos_y_slice1")==0)
{
	return GPVDM_MAX_POS_Y_SLICE1;
}else
if (strcmp(temp,"max_pos_y_val_slice")==0)
{
	return GPVDM_MAX_POS_Y_VAL_SLICE;
}else
if (strcmp(temp,"max_pos_y_val_slice0")==0)
{
	return GPVDM_MAX_POS_Y_VAL_SLICE0;
}else
if (strcmp(temp,"max_pos_y_val_slice1")==0)
{
	return GPVDM_MAX_POS_Y_VAL_SLICE1;
}else
if (strcmp(temp,"contacts")==0)
{
	return CONTACTS;
}else
if (strcmp(temp,"mid_point")==0)
{
	return MID_POINT;
}else
if (strcmp(temp,"avg")==0)
{
	return AVG;
}else
if (strcmp(temp,"yes_nk")==0)
{
	return yes_nk;
}else
if (strcmp(temp,"yes_k")==0)
{
	return yes_k;
}

ewe(sim,"%s %s\n",_(">I don't understand the command"),in);
return 0;
}


int scanarg( char* in[],int count,char * find)
{
int i;
for (i=0;i<count;i++)
{
if (strcmp(in[i],find)==0) return TRUE;
}
return FALSE;
}

int get_arg_plusone_pos( char* in[],int count,char * find)
{
int i;
for (i=0;i<count;i++)
{
if (strcmp(in[i],find)==0)
{
       if ((i+1)<count)
       {
               return i+1;
       }else
       {
               return FALSE;
       }
}
}
return FALSE;
}

char * get_arg_plusone( char* in[],int count,char * find)
{
int i;
static char no[] = "";
for (i=0;i<count;i++)
{

if (strcmp(in[i],find)==0)
{
       if ((i+1)<count)
       {
               return in[i+1];
       }else
       {
               return no;
       }
}
}

return no;
}




/**This is a version of the standard fgets, but it will also accept a 0x0d as a new line.
@param buf output buffer
@param len max length of buffer
@param file file handle
*/
int oghma_fgets(char *buf,int len,FILE *file)
{
	char dat;
	int pos=0;

	if (feof(file))
	{
		return -1;
	}

	do
	{
		dat=(char)fgetc(file);
		if (feof(file))
		{
			break;
		}

		if ((dat=='\n')||(dat=='\r')||(dat==0x0d))
		{
			break;
		}

		buf[pos]=dat;

		pos++;

		if (pos>len)
		{
			break;
		}

	}while(1);
	buf[pos]=0;

	return pos;
}

int copy_file(struct simulation *sim,char *output,char *input)
{
	long len;
	char *buf;
	//struct stat results;
	FILE* out_fd;
	int ret=0;
	ret=g_read_file_to_buffer(&buf, &len,input,-1);

	if (ret==-1)
	{
		return -1;//ewe(sim,"%s: %s\n",_("Can not open file"),input);
	}

	if (ret==-2)
	{
		return -2;
		//ewe(sim,"problem reading file size does not match %s\n ",input);
	}

	out_fd =  g_fopen(output, "wb");
	if (out_fd == NULL)
	{
		return -3;
		//ewe(sim,"File %s can not be opened for write\n",output);
	}

	fwrite( buf, len*sizeof(char),1,out_fd);

	free(buf);

	fclose(out_fd);
	return 0;
}

FILE *fopena(char *path,char *name,const char *mode)
{
	char wholename[PATH_MAX];
	join_path(2, wholename,path,name);

	FILE *pointer;
	pointer=g_fopen(wholename,mode);

	return pointer;
}

