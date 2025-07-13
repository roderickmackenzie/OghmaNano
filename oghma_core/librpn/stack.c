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

/** @file stack.c
@brief RPN stack - all based off wikipedia
*/

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#include "util.h"
#include "cal_path.h"
#include "oghma_const.h"
#include <rpn.h>
#include <log.h>

void stack_item_init(struct stack_item *itm)
{
	strcpy(itm->str,"");
	itm->num=0.0;
	itm->type=-1;
}

void output_push(struct rpn_calculator *in,struct stack_item *itm)
{
	if (in->output_pos<=in->output_max)
	{
		in->output_max+=10;
		in->output=realloc(in->output,in->output_max*sizeof(struct stack_item));
	}

	memcpy(&(in->output[in->output_pos]), itm, sizeof(struct stack_item));
	in->output_pos++;
}

void stack_push(struct rpn_calculator *in,struct stack_item *itm)
{

	if (in->stack_pos<=in->stack_max)
	{
		in->stack_max+=10;
		in->stack=realloc(in->stack,in->stack_max*sizeof(struct stack_item));
	}

	memcpy(&(in->stack[in->stack_pos]), itm, sizeof(struct stack_item));
	in->stack_pos++;
}

int stack_pop(struct stack_item *itm, struct rpn_calculator *in)
{
	if (in->stack_pos==0)
	{
		strcpy(itm->str,"");
		return -1;
	}
	in->stack_pos--;
	memcpy(itm, &(in->stack[in->stack_pos]), sizeof(struct stack_item));
	return 0;
}

int stack_peak(struct stack_item *itm,struct rpn_calculator *in)
{
	if (in->stack_pos!=0)
	{
		memcpy(itm, &(in->stack[in->stack_pos-1]), sizeof(struct stack_item));
		return 0;
	}else
	{
		strcpy(itm->str,"");
	}

	return -1;
}

void print_stack(struct rpn_calculator *in)
{
	int i;
	printf("stack: (len=%d)\n",in->stack_pos);
	for (i=0;i<in->stack_pos;i++)
	{
		printf(">%s<\t%s\t%d",in->stack[i].str,rpn_decode(in->stack[i].type),in->stack[i].type);
		if (in->stack[i].type==RPN_NUMBER)
		{
			printf(" %le",in->stack[i].num);
		}
		printf("\n");

	}
}

void print_output(struct rpn_calculator *in)
{
	int i=0;
	printf("output (len=%d):\n",in->output_pos);
	for (i=0;i<in->output_pos;i++)
	{
		printf(">%s<\t%s\t%d\n",in->output[i].str,rpn_decode(in->output[i].type),in->output[i].type);
	}
}



