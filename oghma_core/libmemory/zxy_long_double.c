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

/** @file memory_basic.c
@brief memory functions for 3D arrays
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lang.h>
#include "sim.h"
#include "dump.h"
#include "mesh.h"
#include <math.h>
#include "log.h"
#include <solver_interface.h>
#include "memory.h"
#include <g_io.h>
#include "zxy_math_kern.h"
#include <math_xy.h>

void malloc_zxy_long_double(struct dimensions *dim, gdouble * (***var))
{
	malloc_3d((void****)var,dim->zlen, dim->xlen, dim->ylen,sizeof(gdouble));
}

void free_zxy_long_double(struct dimensions *dim, gdouble * (***var))
{
	free_3d((void****)var,dim->zlen, dim->xlen, dim->ylen,sizeof(gdouble));
}

void cpy_zxy_long_double(struct dimensions *dim, gdouble * (***out), gdouble * (***in),int aloc)
{
	if (aloc==TRUE)
	{
		free_3d((void****)out,dim->zlen, dim->xlen, dim->ylen,sizeof(gdouble));
		if (*in==NULL)
		{
			return;
		}
		malloc_3d((void****)out,dim->zlen, dim->xlen, dim->ylen,sizeof(gdouble));
	}else
	{
		if (in==NULL)
		{
			printf("Warning copying null pointer\n");
		}

		if (out==NULL)
		{
			printf("Warning copying onto null pointer!\n");
			getchar();
		}

	}

	cpy_3d((void****)out, (void****)in, dim->zlen, dim->xlen, dim->ylen, sizeof(gdouble));
}

gdouble zxy_min_gdouble(struct dimensions *dim, gdouble ***var)
{
	int x=0;
	int y=0;
	int z=0;

	gdouble min=var[0][0][0];

	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			for (y = 0; y < dim->ylen; y++)
			{
				if (var[z][x][y]<min)
				{
					min=var[z][x][y];
				}
			}
		}
	}

return min;
}

double zxy_max_double(struct dimensions *dim, double ***var)
{
	int z_len=dim->zlen;
	int x_len=dim->xlen;
	int y_len=dim->ylen;
	max_zxy;
	return max;
}

//Finds the centre point of a distribution and the sides where the max value has decreased by a factor of 0.5 
void zxy_max_y_pos_slice_long_double(struct dimensions *dim, gdouble ***var,int z, int x,double *max_y_mid, double *max_yn, double *max_yp,double *val)
{
	int y;
	double tot=0.0;

	struct math_xy dat;
	math_xy_init(&dat);
	math_xy_malloc(&dat,dim->ylen);

	struct math_xy dat_intergral;
	math_xy_init(&dat_intergral);
	math_xy_malloc(&dat_intergral,dim->ylen);

	dat.len=dim->ylen;
	dat_intergral.len=dim->ylen;

	for (y = 0; y < dim->ylen; y++)
	{
		dat.data[y]=var[z][x][y];
		dat.x[y]=dim->y[y];

		dat_intergral.data[y]=tot;
		dat_intergral.x[y]=dim->y[y];
		tot+=var[z][x][y]*dim->dY[y];
	}

	inter_swap(&dat_intergral);

	if (max_y_mid!=NULL)
	{
		inter_get(&dat_intergral,tot*0.5,max_y_mid);
		if (val!=NULL)
		{
			inter_get(&dat,*max_y_mid,val);
		}
	}

	if (max_yn!=NULL)
	{
		inter_get(&dat_intergral,tot*0.25,max_yn);
		if (val!=NULL)
		{
			inter_get(&dat,*max_yn,val);
		}
	}

	if (max_yp!=NULL)
	{
		inter_get(&dat_intergral,tot*0.75,max_yp);
		if (val!=NULL)
		{
			inter_get(&dat,*max_yp,val);
		}
	}

	math_xy_free(&dat);
	math_xy_free(&dat_intergral);

}

void zxy_norm_gdouble(struct dimensions *dim, gdouble ***var)
{
	gdouble max=0.0;
	max=zxy_max_double(dim,var);
	zxy_mul_gdouble(dim, var, 1.0/max);
}

void set_zxy_long_double(struct dimensions *dim, gdouble ***var, gdouble val)
{
int x=0;
int y=0;
int z=0;

	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			for (y = 0; y < dim->ylen; y++)
			{
				var[z][x][y]=val;
			}

		}
	}

}


void three_d_sub_gdouble(struct dimensions *dim, gdouble ***var, gdouble ***sub)
{
int x=0;
int y=0;
int z=0;

	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			for (y = 0; y < dim->ylen; y++)
			{
				var[z][x][y]-=sub[z][x][y];
			}

		}
	}

}

void three_d_add_gdouble(struct dimensions *dim, gdouble ***a, gdouble ***b)
{
	add_zxy_zxy;
}

void add_zxy_long_double_double(struct dimensions *dim, gdouble ***a, double ***b)
{
	add_zxy_zxy;
}

void zxy_mul_gdouble(struct dimensions *dim, gdouble ***a, gdouble b)
{
	mul_zxy_double;
}

void zxy_long_double_mul_by_zxy_long_double(struct dimensions *dim, gdouble ***a, gdouble ***b)
{
	mul_zxy_zxy;
}

void zxy_long_double_div_by_zxy_long_double(struct dimensions *dim, gdouble ***a, gdouble ***b)
{
	div_zxy_zxy;
}


gdouble three_d_avg_raw(struct device *in, gdouble ***src)
{
gdouble sum=0.0;
gdouble ret=0.0;
gdouble count=0.0;

int x=0;
int y=0;
int z=0;

if (src==NULL)
{
	return 0.0;
}

struct dimensions *dim=&(in->ns.dim);

	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			for (y = 0; y < dim->ylen; y++)
			{

				sum+=src[z][x][y];
				count+=1.0;
			}

		}
	}

ret=sum/count;
return ret;
}

gdouble three_d_avg(struct device *in, gdouble ***src)
{
gdouble sum=0.0;
gdouble ret=0.0;

avg_vol_xzy;

return ret;
}


void three_d_printf(struct dimensions *dim, gdouble ***src)
{
int x=0;
int y=0;
int z=0;
	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			for (y = 0; y < dim->ylen; y++)
			{
				printf("%le\n",(double)src[z][x][y]);
			}

		}
	}

return;
}

gdouble three_d_avg_gfabs(struct device *in, gdouble ***src)
{
int x=0;
int y=0;
int z=0;
gdouble sum=0.0;
gdouble ret=0.0;

if (src==NULL)
{
	return 0.0;
}

struct dimensions *dim=&(in->ns.dim);
	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			for (y = 0; y < dim->ylen; y++)
			{
				sum+=gfabs(src[z][x][y])*dim->dX[x]*dim->dY[y]*dim->dZ[z];
			}

		}
	}

ret=sum/(in->zlen*in->xlen*in->ylen);
return ret;
}

gdouble three_d_integrate(struct dimensions *dim, gdouble ***src)
{
gdouble sum=0.0;

inter_zxy;

return sum;
}

gdouble zxy_sum_gdouble(struct dimensions *dim, gdouble ***src)
{
int x=0;
int y=0;
int z=0;
gdouble sum=0.0;

	for (z = 0; z < dim->zlen; z++)
	{
		for (x = 0; x < dim->xlen; x++)
		{
			for (y = 0; y < dim->ylen; y++)
			{
				sum+=src[z][x][y];
			}

		}
	}

return sum;
}

void zxy_mod_gdouble(struct dimensions *dim, gdouble ***src)
{
	mod_zxy;

}

void three_d_interpolate_gdouble(gdouble ***out, gdouble ***in, struct dimensions *dim_out, struct dimensions *dim_in)
{
int x=0;
int y=0;
int z=0;

int yi;
int xi;

gdouble y_out;
gdouble x_out;

gdouble y00;
gdouble y01;
gdouble yr;
gdouble y0;

gdouble y10;
gdouble y11;
gdouble y1;

gdouble x0;
gdouble x1;
gdouble xr;

gdouble c;

	z=0;
	for (x = 0; x < dim_out->xlen; x++)
	{

		x_out=dim_out->x[x];
		xi=hashget(dim_in->x,dim_in->xlen,x_out);

		for (y = 0; y < dim_out->ylen; y++)
		{
			y_out=dim_out->y[y];
			yi=hashget(dim_in->y,dim_in->ylen,y_out);

			y00=dim_in->y[yi];
			y01=dim_in->y[yi+1];
			yr=(y_out-y00)/(y01-y00);
			y0=in[z][xi][yi]+yr*(in[z][xi][yi+1]-in[z][xi][yi]);

			y10=dim_in->y[yi];
			y11=dim_in->y[yi+1];
			yr=(y_out-y10)/(y11-y10);
			y1=in[z][xi+1][yi]+yr*(in[z][xi+1][yi+1]-in[z][xi+1][yi]);

			x0=dim_in->x[xi];
			x1=dim_in->x[xi+1];
			xr=(x_out-x0)/(x1-x0);

			c=y0+xr*(y1-y0);
			out[z][x][y]=c;
		}

	}

}



void three_d_quick_dump(char *file_name, gdouble ***in, struct dimensions *dim)
{
int x=0;
int z=0;
	FILE *out=g_fopen(file_name,"w");

	for (z = 0; z < dim->zlen; z++)
	{

		for (x = 0; x < dim->xlen; x++)
		{

			//for (y = 0; y < dim->ylen; y++)
			//{
				fprintf(out,"%le %le %le\n",(double)dim->z[z],(double)dim->x[x],(double)in[z][x][2]);
			//}


		}
		fprintf(out,"\n");
		//fprintf(out,"\n\n");
	}

fclose(out);
}


void zxy_load_long_double(struct simulation *sim, struct dimensions *dim,gdouble **** data,char *file_name)
{
	char line[1000];
	FILE *file;
	int data_found=FALSE;
	int items_per_line=0;
	int x;
	int y;
	int z;
	double x_val;
	double z_val;
	double val;
	gdouble ***dat=*data;
	struct dat_file d;
	char *buf;
	long file_len;

	//This is messy as we are reading the file twice but it will do for now
	if (g_read_file_to_buffer(&buf, &file_len,file_name,-1)!=0)
	{
		ewe(sim,"Error opening file %s\n",file_name);
	}
	
	dat_file_load_info(sim,&d,buf,file_len);
	free(buf);
	if ((d.x_len!=dim->xlen)||(d.y_len!=dim->ylen)||(d.z_len!=dim->zlen))
	{
		ewe(sim,"not matching dim should be (%d,%d,%d)\n",d.x_len,d.y_len,d.z_len);
	}

	//zxy_malloc_gdouble(dim, data);

	items_per_line++;

	if (d.y_len>1)
	{
		items_per_line++;
	}

	if (d.x_len>1)
	{
		items_per_line++;
	}

	if (d.z_len>1)
	{
		items_per_line++;
	}

	file=g_fopen(file_name,"r");
	x=0;
	y=0;
	z=0;
	int ret=0;
	do
	{
		memset(line,0,1000);
		ret=oghma_fgets(line, 1000, file);

		if (strcmp(line,"#end")==0)
		{
			break;
		}

		if (data_found==TRUE)
		{
			if (ret>0)
			{

				if (items_per_line==3)
				{
					sscanf(line,"%le %le %le",&x_val,&z_val,&val);
					dat[z][x][y]=(gdouble)val;
					//printf("%Le %Le %Le %d %d %d\n",x_val,z_val,dat[z][x][y],z,x,y);
					//getchar();
				}else
				{
					ewe(sim,"I don't know how to read this type of file\n");
				}

				y++;
				if (y>=dim->ylen)
				{
					y=0;
					x++;
					if (x>=dim->xlen)
					{
						x=0;
						z++;
						if (z>=dim->zlen)
						{
							z=0;
						}
					}
				}



			}

		}

		if (strcmp(line,"#data")==0)
		{
			data_found=TRUE;
		}

	}while(!feof(file));
	fclose(file);
}

void flip_zxy_long_double_y(struct simulation *sim, struct dimensions *dim,gdouble *** data)
{
	int x=0;
	int y=0;
	int z=0;
	gdouble ***temp=NULL;

	malloc_zxy_long_double(dim, &temp);

	for (z=0;z<dim->zlen;z++)
	{

		for (x=0;x<dim->xlen;x++)
		{

			for (y=0;y<dim->ylen;y++)
			{
				temp[z][x][y]=data[z][x][y];
			}

		}
	}

	for (z=0;z<dim->zlen;z++)
	{
		for (x=0;x<dim->xlen;x++)
		{
			for (y=0;y<dim->ylen;y++)
			{
				data[z][x][dim->ylen-y-1]=temp[z][x][y];
			}
		}
	}


	free_zxy_long_double(dim, &temp);
}

//This shoudl be 3D interpolation but we are assuming the meshes are aligned.
gdouble interpolate_zxy_long_double(struct dimensions *dim, gdouble ***data,int z, int x, gdouble y_in)
{
	int y=0;
	gdouble x0=0.0;
	gdouble x1=0.0;
	gdouble y0=0.0;
	gdouble y1=0.0;

	gdouble ret;

	if (y_in<dim->y[0])
	{
		return 0.0;
	}


	if (y_in>=dim->y[dim->ylen-1])
	{
		//printf("here %Le %Le\n",y_in,dim->y[dim->ylen-1]);
		y=dim->ylen-1;
		x0=dim->y[y-1];
		x1=dim->y[y];
		y0=data[z][x][y-1];
		y1=data[z][x][y];

	}else
	{
		y=search(dim->y,dim->ylen,y_in);
		//printf("%d\n",y);
		x0=dim->y[y];
		x1=dim->y[y+1];

		y0=data[z][x][y];
		y1=data[z][x][y+1];
	}
	ret=y0+((y1-y0)/(x1-x0))*(y_in-x0);

return ret;

}
