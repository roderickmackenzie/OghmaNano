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


int eval_sin(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a)
{
	out->num=sin(a->num);
	return 0;
}

int eval_cos(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a)
{
	out->num=cos(a->num);
	return 0;
}

int eval_abs(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a)
{
	out->num=fabs(a->num);
	return 0;
}

int eval_log10(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a)
{
	out->num=log10(a->num);
	return 0;
}

int eval_exp(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a)
{
	out->num=exp(a->num);
	return 0;
}

int eval_sqrt(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a)
{
	out->num=sqrt(a->num);
	return 0;
}

int eval_pos(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a)
{
	if (a->num<0)
	{
		out->num=0.0;
	}else
	{
		out->num=a->num;
	}

	return 0;
}
