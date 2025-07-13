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

/** @file function.c
@brief configure RPN functions
*/


#define _FILE_OFFSET_BITS 64
#define _LARGEFILE_SOURCE
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#include "util.h"
#include "cal_path.h"
#include "oghma_const.h"
#include <rpn.h>
#include <log.h>

int add_function(struct rpn_calculator *in,char *name,void *f,int number_to_take_from_stack)
{
	if (in->functions_count<=in->functions_max)
	{
		in->functions_max+=10;
		in->functions=realloc(in->functions,in->functions_max*sizeof(struct rpn_function_type));
	}

	strcpy(in->functions[in->functions_count].name,name);
	in->functions[in->functions_count].f=f;
	in->functions[in->functions_count].number_to_take_from_stack=number_to_take_from_stack;
	in->functions_count++;
	return 0;
}

int is_function(struct rpn_calculator *in,char *val)
{
	int i;
	for (i=0;i<in->functions_count;i++)
	{
		if (strcmp(val,in->functions[i].name)==0)
		{
			return i;
		}
	}
return -1;
}

int function_run(struct rpn_calculator *in,char *val,struct stack_item *out)
{
	int i;
	struct stack_item a;
	struct stack_item b;

	stack_item_init(out);
	out->type=RPN_NUMBER;
	//char *ret;
	//printf(">> %s %d\n",token,output_item->type);
	//printf("run: %s %s %s\n",in->functions[i].name,a->str,b->str);

	for (i=0;i<in->functions_count;i++)
	{
		if (strcmp(val,in->functions[i].name)==0)
		{

			if (in->functions[i].number_to_take_from_stack==1)
			{
				stack_pop(&a,in);
				((int (*)(struct rpn_calculator *,struct stack_item *, struct stack_item *))in->functions[i].f)(in,out,&a);
				return 0;
			}else
			if (in->functions[i].number_to_take_from_stack==2)
			{
				stack_pop(&a,in);
				stack_pop(&b,in);
				((int (*)(struct rpn_calculator *, struct stack_item *, struct stack_item *, struct stack_item *))in->functions[i].f)(in,out,&a,&b);
			}
		}
	}
return -1;
}



