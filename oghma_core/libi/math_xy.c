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

/** @file i.c
	@brief Simple functions to read in scientific data from text files and perform simple maths on the data.
*/
#define _FILE_OFFSET_BITS 64
#define _LARGEFILE_SOURCE
#include <enabled_libs.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sim_struct.h>
#include <math_xy.h>
#include "util.h"
#include "cal_path.h"
#include "oghma_const.h"
#include <log.h>
#include <memory.h>
#include <g_io.h>
#include <math_kern_1d.h>

static int unused __attribute__((unused));
static char* unused_pchar __attribute__((unused));

void math_xy_sin(struct math_xy *in,double mag,double fx,double delta)
{
int i;
	for (i=0;i<in->len;i++)
	{
		in->data[i]=fabs(mag)*sin(2*M_PI*fx*(in->x[i]+delta));
	}
}

void math_xy_cos(struct math_xy *in,double mag,double fx,double phi)
{
int i;
	for (i=0;i<in->len;i++)
	{
		in->data[i]=fabs(mag)*cos(2*M_PI*fx*(in->x[i])+phi);
	}
}


/**Translate the input math_xy to a log struct
@param in inout math_xy
@param out output math_xy
*/
void inter_to_log_mesh(struct math_xy* out,struct math_xy* in)
{
	double a=log10(in->x[0]);
	double b=log10(in->x[in->len-1]);
	double step=(b-a)/((double)out->len);
	int i;
	double pos=a;
	for (i=0;i<out->len;i++)
	{
		out->x[i]=pow(10.0,pos);
		inter_get(in,pow(10.0,pos),&(out->data[i]));
		pos+=step;
	}

}

/**Use linear interpolation to project an math_xy array to a new linear mesh
@param in input math_xy
@param out output math_xy
*/
void inter_to_new_mesh(struct math_xy* in,struct math_xy* out)
{
int i;
int ii;
double pos=in->x[0];
double delta=(in->x[in->len-1]-in->x[0])/(double)out->len;
pos+=delta/2.0;
for (i=0;i<out->len;i++)
{
	ii=search_double(in->x,in->len,pos);

	double x0=in->x[ii];
	double x1=in->x[ii+1];

	double y0=in->data[ii];
	double y1=in->data[ii+1];

	out->x[i]=pos;
	out->data[i]=y0+((y1-y0)/(x1-x0))*(pos-x0);

	pos+=delta;
}

return;
}


/**Sum a 1D math_xy whilst taking the modulus of the data.
@param in input math_xy
*/
double inter_sum_mod(struct math_xy* in)
{
int i;
double sum=0.0;

for (i=0;i<in->len;i++)
{
	sum+=fabs(in->data[i]);
}
return sum;
}

/**Get the average value of the data in a 1D math_xy between two points
@param in input math_xy
@param start start point
@param stop stop point

*/
double inter_avg_range(struct math_xy* in,double start,double stop)
{
int i;
double sum=0.0;
double points=0.0;
for (i=0;i<in->len;i++)
{
	if ((in->x[i]>start)&&(in->x[i]<stop))
	{
		sum+=in->data[i];
		points+=1.0;
	}
}
return sum/points;
}

/**Sum a 1D math_xy (no modulus)
@param in input math_xy
*/
double inter_sum(struct math_xy* in)
{
int i;
double sum=0.0;

for (i=0;i<in->len;i++)
{
	sum+=in->data[i];
}
return sum;
}

/**Convolve two math_xys
@param one input/output math_xy
@param two input math_xy
*/
void inter_convolve(struct math_xy* one,struct math_xy* two)
{
int i;
//double sum=0.0;

for (i=0;i<one->len;i++)
{
	one->data[i]*=two->data[i];
}
}



double inter_norm_to_one_range(struct math_xy* in,double start,double stop)
{
int i;
double max=0.0;

for (i=0;i<in->len;i++)
{
	if (in->x[i]>start)
	{
		max=in->data[i];
		break;
	}
}

for (i=0;i<in->len;i++)
{
	if ((in->x[i]>start)&&(in->x[i]<stop))
	{
		if (in->data[i]>max) max=in->data[i];
	}
}

for (i=0;i<in->len;i++)
{
in->data[i]/=max;
}

return max;
}



/**Remove zeros from the data stored in math_xy
@param in input math_xy
*/
void inter_purge_zero(struct math_xy* in)
{
int i;
int write=0;
int read=0;
for (i=0;i<in->len;i++)
{
	in->data[write]=in->data[read];
	in->x[write]=in->x[read];
	if (in->data[read]==0.0)
	{
		write--;
	}
	read++;
	write++;
}
in->len=write;

inter_realloc(in,in->len);

}

void inter_purge_x_zero(struct math_xy* in)
{
int i;
int write=0;
int read=0;
for (i=0;i<in->len;i++)
{
	in->data[write]=in->data[read];
	in->x[write]=in->x[read];

	if (in->x[read]==0.0)
	{
		write--;
	}
	read++;
	write++;
}

in->len=write;

inter_realloc(in,in->len);

}



/**Chop an math_xy array between two points
@param min min point
@param min max point
*/
void math_xy_chop(struct math_xy* in,double min, double max)
{
int i;
int write=0;
int read=0;
for (i=0;i<in->len;i++)
{
	in->data[write]=in->data[read];
	in->x[write]=in->x[read];
	write++;
	if (in->x[read]<min)
	{
		write--;
	}

	if (in->x[read]>max) break;
	read++;




}
in->len=write;

inter_realloc(in,in->len);
}



/**Add a value from every x element in the array
@param value value to subtract from data
*/
void inter_add_x(struct math_xy* in,double value)
{
int i;
for  (i=0;i<in->len;i++)
{
in->x[i]+=value;
}

}

/**Subtract a value from every data element in the array
@param value value to subtract from data
*/
void inter_sub_long_double(struct math_xy* in,double value)
{
int i;
for  (i=0;i<in->len;i++)
{
in->data[i]-=value;
}

}



/**Add a number to an math_xy
@param in input math_xy
@param value value to add to math_xy
*/
void inter_add_long_double(struct math_xy* in,double value)
{
int i;
for  (i=0;i<in->len;i++)
{
in->data[i]+=value;
}

}

/**Normalize the area under a 1D math_xy to one multiplied by a constant
@param in input math_xy
@param mul number to multiply the math_xy by
*/
void math_xy_norm_area(struct math_xy* in,double mul)
{
int i;
double tot=0.0;
double dx=0.0;
for  (i=0;i<in->len;i++)
{
	if (i==0)
	{
		dx=in->x[1]-in->x[0];
	}else
	if (i==in->len-1)
	{
		dx=in->x[i]-in->x[in->len-2];
	}else
	{
		dx=(in->x[i+1]-in->x[i])/2.0+(in->x[i]-in->x[i-1])/2.0;
	}

	tot+=dx*in->data[i];
}

for  (i=0;i<in->len;i++)
{

	in->data[i]/=tot;
	in->data[i]*=mul;

}

}





int inter_get_col_n(struct simulation *sim,char *name)
{
int i=0;
char temp[10000];
char *token;
int col=0;

FILE *file;
file=g_fopen(name,"r");
if (file == NULL)
{
	printf_log(sim,"inter_get_col_n can not open file %s\n",name);
	exit(0);
}

do
{
	memset(temp,0,10000);
	unused_pchar=fgets(temp, 10000, file);
	const char s[2] = " ";
	for (i=0;i<strlen(temp);i++)
	{
		if (temp[i]=='\t') temp[i]=' ';
	}

	if ((temp[0]!='#')&&(temp[0]!='\n')&&(temp[0]!='\r')&&(temp[0]!=0))
	{
		col=0;
		token = strtok(temp, s);

		do
		{
			token = strtok(NULL, s);
			if (token==NULL) break;
			if (token[0]!='\n') col++;
		}
		while(token!=NULL);

		col--;
		break;

	}


}while(!feof(file));
fclose(file);
return col;
}



void math_xy_import_array(struct math_xy* in,double *x,double *y,int len,int alloc)
{
	int i;

	if (alloc==TRUE)
	{
		math_xy_malloc(in,len);
	}

	in->len=len;

	if (x!=NULL)
	{
		for  (i=0;i<in->len;i++)
		{
			in->x[i]=x[i];
		}
	}

	if (y!=NULL)
	{
		for  (i=0;i<in->len;i++)
		{
			in->data[i]=y[i];
		}
	}		

}

/**Take the derivative with respect to the x axis of an math_xy
@param in input math_xy
@param output math_xy
*/
void math_xy_deriv(struct math_xy* out,struct math_xy* in)
{
	int i;
	double yl=0.0;
	double yr=0.0;
	double xl=0.0;
	double xr=0.0;
	double dy=0.0;
	struct math_xy temp;
	math_xy_init(&temp);
	math_xy_cpy(&temp,in,TRUE);

	for (i=0;i<in->len;i++)
	{
		if (i==0)
		{
			xl=temp.x[i];
			yl=temp.data[i];
		}else
		{
			xl=temp.x[i-1];
			yl=temp.data[i-1];
		}

		if (i==(in->len-1))
		{
			xr=temp.x[i];
			yr=temp.data[i];
		}else
		{
			xr=temp.x[i+1];
			yr=temp.data[i+1];
		}
		if (yr!=yl)
		{
			dy=(yr-yl)/(xr-xl);
		}else
		{
			dy=0.0;
		}

		if (out!=NULL)
		{
			out->x[i]=temp.x[i];
			out->data[i]=dy;
		}else
		{
			in->data[i]=dy;
		}
	}

	math_xy_free(&temp);
}

/**Swap x and data column
@param in math_xy to operate on
*/
void inter_swap(struct math_xy* in)
{
	int i;
	double x_temp=0.0;
	double data_temp=0.0;


	for  (i=0;i<in->len;i++)
	{
		data_temp=in->data[i];
		x_temp=in->x[i];

		in->data[i]=x_temp;
		in->x[i]=data_temp;
	}
}



void math_xy_set_value(struct math_xy* in,double value)
{
int i=0;
for  (i=0;i<in->len;i++)
{
	in->data[i]=value;
}

}

/**Take segments of dx and multiply them by the y-axis.
@param in struct to work on
*/
void inter_y_mul_dx(struct math_xy* in)
{
int i=0;

double dx=0.0;
double d0=0.0;
double d1=0.0;
for  (i=0;i<in->len;i++)
{
		if (i==0)
		{
			d0=(in->x[0]);
		}else
		{
			d0=(in->x[i-1]);
		}

		if (i==in->len-1)
		{
			d1=(in->x[i]);
		}else
		{
			d1=(in->x[i+1]);
		}

		dx=(d1-d0)/2.0;
		in->data[i]=in->data[i]*dx;
}

}

/**Make a cumulative graph.
@param in struct to work on
*/
void inter_make_cumulative(struct math_xy* in)
{
int i=0;
double dx=0.0;
double d0=0.0;
double d1=0.0;
double tot=0.0;
for  (i=0;i<in->len;i++)
{
	if (i==0)
	{
		d0=(in->x[0]);
	}else
	{
		d0=(in->x[i-1]);
	}

	if (i==in->len-1)
	{
		d1=(in->x[i]);
	}else
	{
		d1=(in->x[i+1]);
	}

	dx=(d1-d0)/2.0;
	tot+=in->data[i]*dx;
	in->data[i]=tot;
}

}


int inter_search_pos(struct math_xy* in,double x)
{
return search_double(in->x,in->len,x);
}

int math_xy_get_closest_y_value(struct math_xy* in,double *out_x, double *out_y ,double y)
{
	int x=0;
	double delta=0.0;
	double delta_new=0.0;
	if (in->len>0)
	{
		delta=fabs(in->data[0]-y);
		*out_x=in->x[0];
		*out_y=in->data[0];
	}

	for  (x=0;x<in->len;x++)
	{
		delta_new=fabs(in->data[x]-y);
		if (delta_new<delta)
		{
			delta=delta_new;
			*out_x=in->x[x];
			*out_y=in->data[x];
		}

	}

	return 0;
}

/**Get interpolated data from a data set
@param in The structure holding the data
@param x the position of the data.
@return the interpolated data value
*/
int inter_get(struct math_xy* in,double x,double *ret)
{
	double x0;
	double x1;
	double y0;
	double y1;

	int i=0;

	if (in->len<1)
	{
		return -1;
	}

	//if (x>in->x[in->len-1]) return 0.0;
	if (x<in->x[0])
	{
		*ret=0.0;
		return 0;
	}


	if (x>=in->x[in->len-1])
	{
		i=in->len-1;
		x0=in->x[i-1];
		x1=in->x[i];

		y0=in->data[i-1];
		y1=in->data[i];

	}else
	{
		i=search_double(in->x,in->len,x);

		x0=in->x[i];
		x1=in->x[i+1];

		y0=in->data[i];
		y1=in->data[i+1];

	}
	*ret=y0+((y1-y0)/(x1-x0))*(x-x0);

	return 0;
}

double inter_get_hard(struct math_xy* in,double x)
{
	double ret=0.0;
	if (x>in->x[in->len-1])
	{
		return 0.0;
	}
	inter_get(in,x,&ret);

	return ret;
}



void inter_reset(struct math_xy* in)
{
in->len=0;
in->max_len=0;
}


int inter_join_bins(struct math_xy* in,double delta)
{
	int i;
	double tot=0.0;
	int pos=0;
	double bin=-1;
	int move_on=FALSE;

	if (in->data==NULL)
	{
		return -1;
	}

	if (in->len<=0)
	{
		return -1;
	}


	bin=in->x[0];

	for (i=0;i<in->len;i++)
	{
		move_on=FALSE;

		if (fabs(bin-in->x[i])<delta)
		{
			tot+=in->data[i];

		}else
		{
			move_on=TRUE;
		}

		if (i==in->len-1)
		{
			move_on=TRUE;
		}

		if (move_on==TRUE)
		{
			in->data[pos]=tot;
			in->x[pos]=bin;
			bin=in->x[i];
			tot=in->data[i];
			pos++;

		}

	}
	in->len=pos;
return 0;
}



