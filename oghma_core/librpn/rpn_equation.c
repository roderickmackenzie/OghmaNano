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

/** @file rpn_equation.c
@brief RPN main
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
#include <memory.h>

void rpn_equation_clear(struct rpn_equation *in)
{
	strcpy(in->equ,"");
	in->vars_pos=0;
	in->evaluated=FALSE;
}

void rpn_equation_init(struct rpn_equation *in)
{
	strcpy(in->equ,"");
	in->vars=NULL;
	in->vars_pos=0;
	in->vars_pos_max=0;
	in->return_abs=FALSE;
	in->evaluated=FALSE;
	in->value=-1.0;
}

void rpn_equation_cpy(struct rpn_equation *out,struct rpn_equation *in)
{
	strcpy(out->equ,in->equ);
	cpy_1d((void **)(&out->vars), (void **)(&in->vars), in->vars_pos_max, sizeof(struct rpn_vars_type), TRUE);
	out->vars_pos_max=in->vars_pos_max;
	out->vars_pos=in->vars_pos;
	out->return_abs=in->return_abs;
	out->evaluated=in->evaluated;
	out->value=in->value;
}

void rpn_equation_free(struct rpn_equation *in)
{
	if (in->vars!=NULL)
	{
		free(in->vars);
	}

	rpn_equation_init(in);
}

struct rpn_vars_type *rpn_equation_set_var(struct rpn_equation *in,char *name,double value)
{
	struct rpn_vars_type *var;
	if (rpn_equation_is_var(in,&var,name)==0)
	{
		if (var->value!=value)
		{
			var->value=value;
			//printf(">>>SET %le %s\n",value,var->name);
			in->evaluated=FALSE;
		}
		return var;
	}

	if (in->vars_pos<=in->vars_pos_max)
	{
		in->vars_pos_max+=20;
		in->vars=realloc(in->vars,in->vars_pos_max*sizeof(struct rpn_vars_type));
	}
	var=&(in->vars[in->vars_pos]);
	strcpy(var->name,name);
	var->value=value;
	in->evaluated=FALSE;
	in->vars_pos++;
	return var;
}

int rpn_equation_set_std_vars(struct rpn_equation *in,double x,double y,double T)
{
	//printf("x=%le\n",x);
	rpn_equation_set_var(in,"x",x);
	//rpn_equation_dump(in);
	rpn_equation_set_var(in,"y",y);
	//rpn_equation_dump(in);
	rpn_equation_set_var(in,"T",T);
	//rpn_equation_dump(in);
	return 0;
}

int rpn_equation_is_var(struct rpn_equation *in,struct rpn_vars_type **out,char *name)
{
	int i;
	for (i=0;i<in->vars_pos;i++)
	{
		if (strcmp(name,in->vars[i].name)==0)
		{
			if (out!=NULL)
			{
				*out=&(in->vars[i]);
			}
			return 0;
		}
	}
return -1;
}

int rpn_equation_dump(struct rpn_equation *in)
{
	int i;
	printf("vars:\n");
	for (i=0;i<in->vars_pos;i++)
	{
		printf("var: %s %le\n",in->vars[i].name,in->vars[i].value);
	}
return 0;
}

