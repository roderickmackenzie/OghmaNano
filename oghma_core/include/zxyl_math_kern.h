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

/** @file zxyl_math_kern.c
@brief memory functions for 4D arrays
*/

#ifndef zxyl_math_kern_h
#define zxyl_math_kern_h

#define div_zxyl								\
	int x=0;									\
	int y=0;									\
	int z=0;									\
	int l=0;									\
												\
	for (z = 0; z < z_len; z++)					\
	{											\
		for (x = 0; x < x_len; x++)				\
		{										\
			for (y = 0; y < y_len; y++)			\
			{									\
				for (l = 0; l < l_len; l++)		\
				{								\
					data[z][x][y][l]/=val;		\
				}								\
			}									\
												\
		}										\
	}											\

#define max_zxyl								\
	int x=0;									\
	int y=0;									\
	int z=0;									\
	int l=0;									\
												\
	double max=data[0][0][0][0];					\
												\
	for (z = 0; z < z_len; z++)					\
	{											\
		for (x = 0; x < x_len; x++)				\
		{										\
			for (y = 0; y < y_len; y++)			\
			{									\
				for (l = 0; l < l_len; l++)		\
				{								\
					if (data[z][x][y][l]>max)	\
					{							\
						max=data[z][x][y][l];	\
					}							\
				}								\
			}									\
		}										\
	}											\

#define min_max_zxyl							\
	int x=0;									\
	int y=0;									\
	int z=0;									\
	int l=0;									\
												\
	double max=-1.0;							\
	double min=-1.0;							\
												\
	if (data==NULL)								\
	{											\
		return -1;								\
	}											\
												\
	max=data[0][0][0][0];						\
	min=data[0][0][0][0];						\
												\
	for (z = 0; z < z_len; z++)					\
	{											\
		for (x = 0; x < x_len; x++)				\
		{										\
			for (y = 0; y < y_len; y++)			\
			{									\
				for (l = 0; l < l_len; l++)		\
				{								\
					if (data[z][x][y][l]>max)	\
					{							\
						max=data[z][x][y][l];	\
					}							\
												\
					if (data[z][x][y][l]<min)	\
					{							\
						min=data[z][x][y][l];	\
					}							\
				}								\
												\
			}									\
		}										\
	}											\


#define memset_zxyl										\
														\
int x=0;												\
int y=0;												\
int z=0;												\
														\
for (z = 0; z < z_len; z++)								\
{														\
	for (x = 0; x < x_len; x++)							\
	{													\
		for (y = 0; y < y_len; y++)						\
		{												\
			memset(data[z][x][y], val, l_len * var_size);	\
		}												\
	}													\
}														\


#endif

