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

/** @file vec.h
	@brief Header file for vec.c
*/
#ifndef vech
#define vech
#include <stdio.h>
///Structure to hold vector
struct vec
{
	double x;
	double y;
	double z;
};

//Vector routines

double vec_mod(struct vec *my_vec);
void vec_plus(struct vec *my_vec1);
void vec_fprintf(FILE *out,struct vec *my_vec);
double deg(double in);
double vec_ang(struct vec *in_v0,struct vec *in_v1);
//void vec_sub(struct vec *my_vec1,struct vec *my_vec2);
#define vec_sub(X, Y)	\
	(X)->x-=(Y)->x;	\
	(X)->y-=(Y)->y;	\
	(X)->z-=(Y)->z;	\

void vec_add(struct vec *my_vec1,struct vec *my_vec2);
void vec_mul_add(struct vec *out,struct vec *in,double mul);
void vec_div(struct vec *my_vec1,double n);
void vec_mul(struct vec *my_vec1,double n);
void vec_div_vec(struct vec *my_vec1,struct vec *my_vec2);
void vec_mul_vec(struct vec *my_vec1,struct vec *my_vec2);
double vec_fabs(struct vec *my_vec);
void vec_rotate(struct vec *my_vec,double ang);
void vec_rotate_y(struct vec *my_vec,double ang);
void vec_rotate_x(struct vec *my_vec,double ang);
//double vec_dot(struct vec *a,struct vec *b);
#define vec_dot(X, Y) (((X)->x*(Y)->x)+((X)->y*(Y)->y)+((X)->z*(Y)->z))

//double vec_dist(struct vec *a,struct vec *b);
#define vec_dist(X, Y)	\
	sqrt(pow((X)->x-(Y)->x,2.0)+pow((X)->y-(Y)->y,2.0)+pow((X)->z-(Y)->z,2.0));

double vec_dist_zx(struct vec *a,struct vec *b);
//void vec_init(struct vec *my_vec);
#define vec_init(X )	\
	(X)->x=0.0;			\
	(X)->y=0.0;			\
	(X)->z=0.0;			\


//void vec_cross(struct vec *ret,struct vec *a,struct vec *b)
#define vec_cross(X , Y , Z) \
	(X)->x=((Y)->y*(Z)->z)-((Y)->z*(Z)->y);\
	(X)->y=((Y)->z*(Z)->x)-((Y)->x*(Z)->z);\
	(X)->z=((Y)->x*(Z)->y)-((Y)->y*(Z)->x);\


void vec_swap(struct vec *my_vec);
//void vec_cpy(struct vec *my_vec1,struct vec *my_vec2);
#define vec_cpy(X, Y) \
	(X)->x=(Y)->x;	\
	(X)->y=(Y)->y;	\
	(X)->z=(Y)->z;	\

void vec_norm(struct vec *my_vec);
void vec_print(struct vec *my_vec);
void vec_set(struct vec *my_vec,double x, double y, double z);
double overlap(double x0,double x1);
double vec_overlap(struct vec *a,struct vec *b);
double vec_get_dihedral(struct vec *a,struct vec *b,struct vec *c,struct vec *d);
void vec_rot(struct vec *in,struct vec *unit,struct vec *base, double ang);
void vec_add_values(struct vec *my_vec, double x,double y, double z);
void rotx_vec(struct vec *out, struct vec *in,double a);
void roty_vec(struct vec *out, struct vec *in,double a);
void rotz_vec(struct vec *out, struct vec *in,double a);
double vec_ang(struct vec *one,struct vec *two);
double vec_overlap_test(struct vec *a,struct vec *b);
void vec_flip_y_axis(struct vec *one,double y);
int vec_within_box(struct vec *l,struct vec *h,struct vec *v);
void vec_dump_to_file(char *file_name,struct vec *one);
int vec_cmp_exact(struct vec *my_vec1,struct vec *my_vec2);
int vec_cmp(struct vec *my_vec1,struct vec *my_vec2);
int vec_cmp_tol(struct vec *my_vec1,struct vec *my_vec2, double tol);
void vec_to_angles(struct vec *in,double *phi,double *theta);
void vec_take_max(struct vec *ret,struct vec *in);
void vec_take_min(struct vec *ret,struct vec *in);
void vec_sign(struct vec *my_vec);
#endif
