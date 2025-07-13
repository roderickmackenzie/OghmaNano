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

/** @file matrix.h
	@brief matrix file
*/

#ifndef matrix_2x2_h
#define matrix_2x2_h
#include <g_io.h>
#include <complex.h>

// a b
// c d
struct complex_matrix_2x2
{
	double complex a;
	double complex b;
	double complex c;	
	double complex d;
};

#define complex_matrix_2x2_set(IN , A , B, C, D) \
	(IN)->a=A; \
	(IN)->b=B; \
	(IN)->c=C; \
	(IN)->d=D; \

#define complex_matrix_2x2_invert(IN)	\
	{ \
	double complex DET=1.0/((IN)->a*(IN)->d-(IN)->b*(IN)->c);	\
	double complex A=(IN)->d*DET;	\
	double complex B=-(IN)->b*DET;	\
	double complex C=-(IN)->c*DET;	\
	double complex D=(IN)->a*DET;	\
	(IN)->a=A;	\
	(IN)->b=B;	\
	(IN)->c=C;	\
	(IN)->d=D;	\
	} \

#define complex_matrix_2x2_cpy(OUT, IN)\
	(OUT)->a=(IN)->a;\
	(OUT)->b=(IN)->b;\
	(OUT)->c=(IN)->c;\
	(OUT)->d=(IN)->d;\

//out=|out|*|in|
#define complex_matrix_2x2_multiply(OUT, IN) \
	{ \
	double complex A_=(OUT)->a*(IN)->a+(OUT)->b*(IN)->c; \
	double complex B_=(OUT)->a*(IN)->b+(OUT)->b*(IN)->d; \
	double complex C_=(OUT)->c*(IN)->a+(OUT)->d*(IN)->c; \
	double complex D_=(OUT)->c*(IN)->b+(OUT)->d*(IN)->d; \
	(OUT)->a=A_; \
	(OUT)->b=B_; \
	(OUT)->c=C_; \
	(OUT)->d=D_; \
	} \

void complex_matrix_2x2_dump(struct complex_matrix_2x2 *in);
void complex_matrix_2x2_unity(struct complex_matrix_2x2 *in);
void complex_matrix_1x2_multiply(double complex *out_a,double complex *out_b,struct complex_matrix_2x2 *in,double complex *a,double complex *b);
#endif
