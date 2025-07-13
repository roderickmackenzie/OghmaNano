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

/** @file opp.c
@brief RPN opps.
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


int add_opp(struct rpn_calculator *in,char *name, int prec, int right_left,void *f,int number_to_take_from_stack)
{
	if (in->opp_count<=in->opp_max)
	{
		in->opp_max+=10;
		in->opps=realloc(in->opps,in->opp_max*sizeof(struct rpn_opperator_type));
	}
	strcpy(in->opps[in->opp_count].name,name);
	in->opps[in->opp_count].prec=prec;
	in->opps[in->opp_count].right_left=right_left;
	in->opps[in->opp_count].f=f;
	in->opps[in->opp_count].number_to_take_from_stack=number_to_take_from_stack;
	in->opp_count++;
	return 0;
}

int is_opp(struct rpn_calculator *in,char *val)
{
	int i;
	for (i=0;i<in->opp_count;i++)
	{
		if (strcmp(val,in->opps[i].name)==0)
		{

			return i;
		}
	}

return -1;
}

int opp_run(struct rpn_calculator *in,char *val,struct stack_item *out)
{
	int i;
	int n_opp=-1;
	struct stack_item a;
	struct stack_item b;
	stack_item_init(out);

	for (i=0;i<in->opp_count;i++)
	{
		if (strcmp(val,in->opps[i].name)==0)
		{
			n_opp=i;
			break;
		}
	}

	if (n_opp==-1)
	{
		sprintf(in->error,"Opp not found %s\n",val);
		return -1;
	}

	if (in->opps[n_opp].number_to_take_from_stack==1)
	{
		stack_pop(&a,in);

		if (a.type!=RPN_NUMBER)
		{
			sprintf(in->error,"a->type!=RPN_NUMBER %d\n",a.type);
			return -1;
		}

		(in->opps[n_opp].f)(out,&a,NULL);
		out->type=RPN_NUMBER;
		return 0;
	}else
	if (in->opps[n_opp].number_to_take_from_stack==2)
	{
		stack_pop(&a,in);
		stack_pop(&b,in);
		//printf("OPP:%s\n",in->opps[i].name);
		if (a.type!=RPN_NUMBER)
		{
			sprintf(in->error,"a->type!=RPN_NUMBER %d\n",a.type);
			return -1;
		}
		if (b.type!=RPN_NUMBER)
		{
			sprintf(in->error,"b->type!=RPN_NUMBER %d\n",b.type);
			return -1;
		}

		(in->opps[n_opp].f)(out,&a,&b);
		out->type=RPN_NUMBER;
		return 0;
	}

return -1;
}

int opp_pr(struct rpn_calculator *in,char *val)
{
	int pos=is_opp(in,val);
	if (pos==-1)
	{
		return -1;
	}

	return in->opps[pos].prec;
}

int opp_lr(struct rpn_calculator *in,char *val)
{
	int pos=is_opp(in,val);
	if (pos==-1)
	{
		return -1;
	}

	return in->opps[pos].right_left;
}



