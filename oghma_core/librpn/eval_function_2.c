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
#include <rand.h>

int eval_min(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a,struct stack_item *b)
{
	if (a->num<=b->num)
	{
		out->num=a->num;
	}else
	{
		out->num=b->num;
	}

	return 0;
}

int eval_max(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a,struct stack_item *b)
{
	
	if (a->num>=b->num)
	{
		out->num=a->num;
	}else
	{
		out->num=b->num;
	}
	return 0;
}

int eval_rand(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a,struct stack_item *b)
{
	if (cal->rand==NULL)
	{
		printf("no random number generator\n");
		return -1;
	}

	out->num=rand_lin_range_double(cal->rand, a->num, b->num);

	return 0;
}

int eval_rand_log(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a,struct stack_item *b)
{
	if (cal->rand==NULL)
	{
		printf("no random number generator\n");
		return -1;
	}

	out->num=rand_log_range_double(cal->rand, a->num, b->num);

	return 0;
}
