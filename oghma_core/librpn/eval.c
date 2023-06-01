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

/** @file eval.c
@brief evaluate math expresions for RPN
*/


#define _FILE_OFFSET_BITS 64
#define _LARGEFILE_SOURCE
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include "util.h"
#include "oghma_const.h"
#include <rpn.h>
#include <log.h>
#include <math.h>

int eval_sin(char *out,char* a,char* b)
{
	double aa=0.0;
	double sum=0.0;

	sscanf(a,"%le",&aa);
	sum=sin(aa);
	sprintf(out,"%le",sum);
	return 0;
}

int eval_abs(char *out,char* a,char* b)
{
	double aa=0.0;
	double sum=0.0;

	sscanf(a,"%le",&aa);
	sum=fabs(aa);
	sprintf(out,"%le",sum);
	return 0;
}

int eval_log10(char *out,char* a,char* b)
{
	double aa=0.0;
	double sum=0.0;

	sscanf(a,"%le",&aa);
	sum=log10(aa);
	sprintf(out,"%le",sum);
	return 0;
}

int eval_pos(char *out,char* a,char* b)
{
	double aa=0.0;
	double sum=0.0;

	sscanf(a,"%le",&aa);
	if (aa<0)
	{
		sum=0.0;
	}else
	{
		sum=aa;
	}
	sprintf(out,"%le",sum);
	return 0;
}

int eval_add(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);
	sum=aa+bb;
	sprintf(out,"%le",sum);
	return 0;
}

int eval_sub(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);
	sum=aa-bb;
	sprintf(out,"%le",sum);
	return 0;
}


int eval_mul(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);
	sum=aa*bb;
	sprintf(out,"%le",sum);
	return 0;
}

int eval_bg(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);

	if (aa>bb)
	{
		sum=1.0;
	}

	sprintf(out,"%le",sum);
	return 0;
}

int eval_bg_eq(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);

	if (aa>=bb)
	{
		sum=1.0;
	}

	sprintf(out,"%le",sum);
	return 0;
}

int eval_sm(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);

	if (aa<bb)
	{
		sum=1.0;
	}

	sprintf(out,"%le",sum);
	return 0;
}

int eval_sm_eq(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);

	if (aa<=bb)
	{
		sum=1.0;
	}

	sprintf(out,"%le",sum);
	return 0;
}

int eval_pow(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);
	sum=pow(aa,bb);
	sprintf(out,"%le",sum);
	return 0;
}

int eval_div(char *out,char* a,char* b)
{
	double aa=0.0;
	double bb=0.0;
	double sum=0.0;
	sscanf(a,"%le",&aa);
	sscanf(b,"%le",&bb);
	sum=aa/bb;
	sprintf(out,"%le",sum);
	return 0;
}



