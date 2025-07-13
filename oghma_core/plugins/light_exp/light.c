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
	@brief Exponential light solver.
*/


#include <util.h>
#include <dump_ctrl.h>
#include <oghma_const.h>
#include <light.h>
#include <device.h>
#include <g_io.h>

#include <functions.h>
#include <log.h>


EXPORT void light_dll_ver(struct simulation *sim)
{
        printf_log(sim,"Exponential light model\n");
}

EXPORT int light_dll_solve_lam_slice(struct simulation *sim,struct device *dev,struct light *li,double *sun_E, int z, int x, int l,int w)
{
	int y;
	char temp[100];
	struct shape* s0;
	struct object* obj0;
	struct shape* s1;
	struct object* obj1;

	struct dimensions *dim=&dev->dim_optical;

	if (sun_E[l]==0.0)
	{
		return 0;
	}

	sprintf(temp,"Solve light optical slice at %lf nm\n",dim->l[l]*1e9);
	waveprint(sim,temp,dim->l[l]);

	gdouble complex n0=0.0+0.0*I;

	//complex gdouble r=0.0+0.0*I;
	complex gdouble t=0.0+0.0*I;
	gdouble complex beta0=0.0+0.0*I;
	complex gdouble Ep=sun_E[l]+0.0*I;
	complex gdouble En=0.0+0.0*I;
	double yc=0.0;
	double yl=0.0;
	double dy=0.0;

	for (y=0;y<dim->ylen;y++)
	{

		if (y==0)
		{
			yl=dim->y[0]-(dim->y[1]-dim->y[0]);	

		}else
		{
			yl=dim->y[y-1];
		}

		yc=dim->y[y];
		dy=yc-yl;

		n0=li->nbar[z][x][y][l];
		beta0=(2*PI*n0/dim->l[l]);
		Ep=Ep*cexp(-beta0*dy*I);

		t=li->t[z][x][y][l];
		li->Ep[z][x][y][l]=creal(Ep);
		li->Epz[z][x][y][l]=cimag(Ep);
		li->En[z][x][y][l]=creal(En);
		li->Enz[z][x][y][l]=cimag(En);

		if (y!=(dim->ylen-1))
		{
			obj0=dev->obj_zxy_optical[z][x][y];
			s0=obj0->s;
			obj1=dev->obj_zxy_optical[z][x][y+1];
			s1=obj1->s;
			//printf("%le %le %le\n",s0->n.data[l],s0->alpha.data[l],li->nbar[z][x][y][l]);
			if ((s0->n.data[l]!=s1->n.data[l])||(s0->alpha.data[l]!=s1->alpha.data[l]))
			{
				Ep=Ep*t;
			}
		}
		//look at after x-mas.
		//printf("%d %lf %le %le\n",y,cabs(t),cabs(Ep),(gpow(li->Ep[z][x][y][l],2.0)+gpow(li->Epz[z][x][y][l],2.0)));

	}
	//getchar();
return 0;
}


