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

/** @file zxy_math_kern.c
@brief memory functions for 3D arrays
*/

#ifndef zxy_math_kern_h
#define zxy_math_kern_h

#define div_zxy									\
	int x=0;									\
	int y=0;									\
	int z=0;									\
												\
	for (z = 0; z < z_len; z++)					\
	{											\
		for (x = 0; x < x_len; x++)				\
		{										\
			for (y = 0; y < y_len; y++)			\
			{									\
				src[z][x][y]/=val;				\
			}									\
												\
		}										\
	}											\

#define max_zxy									\
	int x=0;									\
	int y=0;									\
	int z=0;									\
												\
	double max=var[0][0][0];					\
												\
	for (z = 0; z < z_len; z++)					\
	{											\
		for (x = 0; x < x_len; x++)				\
		{										\
			for (y = 0; y < y_len; y++)			\
			{									\
				if (var[z][x][y]>max)			\
				{								\
					max=var[z][x][y];			\
				}								\
			}									\
		}										\
	}											\

#define min_max_zxy								\
	int x=0;									\
	int y=0;									\
	int z=0;									\
	double max=-1;								\
	double min=-1;								\
	double val=0.0;								\
												\
	if (var==NULL)								\
	{											\
		return -1;								\
	}											\
												\
	max=var[0][0][0];							\
	min=max;									\
												\
	for (z = 0; z < z_len; z++)					\
	{											\
		for (x = 0; x < x_len; x++)				\
		{										\
			for (y = 0; y < y_len; y++)			\
			{									\
				val=var[z][x][y];				\
				if (val>max)					\
				{								\
					max=val;					\
				}								\
												\
				if (val<min)					\
				{								\
					min=val;					\
				}								\
												\
			}									\
		}										\
	}											\

#define min_max_fabs_zxy						\
	int x=0;									\
	int y=0;									\
	int z=0;									\
	double max=-1;								\
	double min=-1;								\
	double val=0.0;								\
												\
	if (var==NULL)								\
	{											\
		return -1;								\
	}											\
												\
	max=fabs(var[0][0][0]);						\
	min=max;									\
												\
	for (z = 0; z < z_len; z++)					\
	{											\
		for (x = 0; x < x_len; x++)				\
		{										\
			for (y = 0; y < y_len; y++)			\
			{									\
				val=fabs(var[z][x][y]);			\
				if (val>max)					\
				{								\
					max=val;					\
				}								\
												\
				if (val<min)					\
				{								\
					min=val;					\
				}								\
												\
			}									\
		}										\
	}											\

#define mul_zxy_double							\
	int x=0;									\
	int y=0;									\
	int z=0;									\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				a[z][x][y]*=b;					\
			}									\
												\
		}										\
	}											\

#define abs_zxy									\
	int x=0;									\
	int y=0;									\
	int z=0;									\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				a[z][x][y]=fabs(a[z][x][y]);	\
			}									\
												\
		}										\
	}											\

#define avg_vol_xzy								\
int x=0;										\
int y=0;										\
int z=0;										\
double dV=0.0;									\
double vol=0.0;									\
												\
if (src==NULL)									\
{												\
	return 0.0;									\
}												\
												\
struct dimensions *dim=&(in->ns->dim);			\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				if (isnan(src[z][x][y])==0)		\
				{								\
					dV=dim->dX[x]*dim->dY[y]*dim->dZ[z];	\
					sum+=src[z][x][y]*dV;					\
					vol+=dV;					\
				}								\
			}									\
												\
		}										\
	}											\
												\
ret=sum/vol;									\


#define inter_zxy								\
int x=0;										\
int y=0;										\
int z=0;										\
double dV=0.0;									\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				dV=dim->dX[x]*dim->dY[y]*dim->dZ[z];	\
				if (isnan(src[z][x][y])==0)		\
				{								\
					sum+=src[z][x][y]*dV;		\
				}								\
			}									\
												\
		}										\
	}											\

#define memset_zxy										\
														\
int x=0;												\
int z=0;												\
														\
for (z = 0; z < z_len; z++)							\
{														\
	for (x = 0; x < x_len; x++)							\
	{													\
		memset(data[z][x], val, y_len * var_size);		\
	}													\
}														\

#define add_zxy_zxy								\
int x=0;										\
int y=0;										\
int z=0;										\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				a[z][x][y]+=b[z][x][y];			\
			}									\
												\
		}										\
	}											\

#define sub_zxy_zxy								\
int x=0;										\
int y=0;										\
int z=0;										\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				a[z][x][y]-=b[z][x][y];			\
			}									\
												\
		}										\
	}		

#define pow_zxy									\
int x=0;										\
int y=0;										\
int z=0;										\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				a[z][x][y]=pow(a[z][x][y],val);	\
			}									\
												\
		}										\
	}											\


#define div_zxy_zxy								\
int x=0;										\
int y=0;										\
int z=0;										\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				a[z][x][y]/=b[z][x][y];			\
			}									\
												\
		}										\
	}											\


#define mul_zxy_zxy								\
int x=0;										\
int y=0;										\
int z=0;										\
												\
	for (z = 0; z < dim->zlen; z++)				\
	{											\
		for (x = 0; x < dim->xlen; x++)			\
		{										\
			for (y = 0; y < dim->ylen; y++)		\
			{									\
				a[z][x][y]*=b[z][x][y];			\
			}									\
												\
		}										\
	}											\



#define mod_zxy									\
int x=0;										\
int y=0;										\
int z=0;										\
												\
for (z = 0; z < dim->zlen; z++)					\
{												\
	for (x = 0; x < dim->xlen; x++)				\
	{											\
		for (y = 0; y < dim->ylen; y++)			\
		{										\
			if (src[z][x][y]<0.0)				\
			{									\
				src[z][x][y]*=-1.0;				\
			}									\
		}										\
												\
	}											\
}												\


#endif


