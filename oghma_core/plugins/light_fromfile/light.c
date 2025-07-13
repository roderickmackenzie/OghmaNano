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

/** @file light.c
	@brief Read an optical generation profile from a file.
*/


#include <util.h>
#include <dump_ctrl.h>
#include <oghma_const.h>
#include <light.h>
#include <device.h>
#include <g_io.h>
#include <string.h>
#include <functions.h>
#include <log.h>

EXPORT void light_dll_ver(struct simulation *sim)
{
        printf_log(sim,"External field light model\n");
}

EXPORT int light_dll_solve_lam_slice(struct simulation *sim,struct device *dev,struct light *li,double *sun_E, int z, int x, int l,int w)
{
	int y=0;
	char temp[1000];
	struct math_xy data;
	struct dimensions *dim_l=&(dev->dim_optical);

	if (sun_E[l]==0.0)
	{
		return 0;
	}

	li->disable_cal_photon_density=TRUE;

	sprintf(temp,"Reading in generation rate data from file %s\n",li->light_file_generation);
	waveprint(sim,temp,532e-9);

	if (math_xy_load(&data,li->light_file_generation)!=0)
	{
		ewe(sim,"file not found: %s\n",li->light_file_generation);
	}

	inter_add_x(&data,li->light_file_generation_shift);

	for (y=0;y<dim_l->ylen;y++)
	{
		li->Gn[z][x][y]=inter_get_hard(&data,dim_l->y[y]);
		li->Gp[z][x][y]=li->Gn[z][x][y];
	}

	math_xy_free(&data);

	li->finished_solveing=TRUE;

return 0;
}


