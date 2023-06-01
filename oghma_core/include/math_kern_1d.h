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

/** @file math_kern_1d.h
@brief memory functions for 1d arrays
*/

#ifndef math_kern_1d
#define math_kern_1d

double bessel1( double x );

#define div_1d_1d				\
	int y;						\
	for (y=0;y<len;y++)			\
	{							\
		if (b[y]!=0)			\
		{						\
			a[y]/=b[y];			\
		}						\
	}							\
								
#define div_1d_double			\
	int y;						\
	for (y=0;y<len;y++)			\
	{							\
		if (b!=0.0)				\
		{						\
			a[y]/=b;			\
		}						\
	}							\
								\

#define chop_search_1d								\
if (N==1) return 0;									\
int pos=N/2;										\
int step=N/2;										\
do													\
{													\
	step=step/2 + (step % 2 > 0 ? 1 : 0);			\
													\
	if (x[pos]>find)								\
	{												\
		pos-=step;									\
	}else											\
	{												\
		pos+=step;									\
	}												\
													\
	if (pos<=0)										\
	{												\
		pos=0;										\
		break;										\
	}												\
	if (pos>=(N-1))									\
	{												\
		pos=N-1;									\
		break;										\
	}												\
	if (step==0) break;								\
	if (x[pos]==find) break;						\
	if ((x[pos]<=find)&&((x[pos+1]>find))) break;	\
													\
}while(1);											\
													\
if (pos==(N-1)) pos=N-2;							\
													\

#endif


