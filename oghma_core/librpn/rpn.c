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

/** @file rpn.c
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
#include <ctype.h>
#include <math.h>

char* rpn_decode(int num)
{
	if (num==RPN_FUNCTION)
	{
		return "RPN_FUNCTION";
	}else
	if (num==RPN_VAR)
	{
		return "RPN_VAR";
	}else
	if (num==RPN_NUMBER)
	{
		return "RPN_NUMBER";
	}else
	if (num==RPN_OPP)
	{
		return "RPN_OPP";
	}else
	{
		return "UNKNOWN";
	}

}

//This does the shunting algroytham
int rpn_process(struct rpn_calculator *in,struct rpn_equation *equ,char *token)
{
int ii=0;
int temp_n=0;
//int push=1;
int o1_lr=0;
int o1_pr=0;
//int o2_lr=0;
int o2_pr=0;
struct stack_item itm;
	//printf("%s\n",token);
	if (rpn_equation_is_var(equ,NULL,token)==0)		//https://www.youtube.com/watch?v=LQ-iW8jm6Mk
	{
		stack_item_init(&itm);
		strcpy(itm.str,token);
		itm.type=RPN_VAR;
		output_push(in,&itm);
		//printf("*\n");
		return 0;
	}else
	if (str_isnumber(token)==TRUE)
	{
		stack_item_init(&itm);
		strcpy(itm.str,token);
		itm.type=RPN_NUMBER;
		sscanf(token,"%le",&itm.num);
		output_push(in,&itm);
		return 0;
	}

	if (strcmp(token,")")==0)
	{
		temp_n=in->stack_pos;
		for (ii=0;ii<temp_n;ii++)
		{
			stack_pop(&itm,in);
			if (strcmp(itm.str,"(")!=0)
			{
				output_push(in,&itm);
			}else
			{
				stack_peak(&itm,in);
				if (itm.type==RPN_FUNCTION)
				{
					stack_pop(&itm,in);
					output_push(in,&itm);
				}
				break;
			}
		}

		return 0;
	}

	if (strcmp(token,"(")==0)
	{
		stack_item_init(&itm);
		strcpy(itm.str,token);
		stack_push(in,&itm);

		return 0;
	}

	if (is_opp(in,token)!=-1)
	{
		//printf("here %s\n",token);
		o1_lr=opp_lr(in,token);
		o1_pr=opp_pr(in,token);
		//printf("r\n");

		while(1)
		{
			stack_peak(&itm,in);
			if (is_opp(in,itm.str)==-1)
			{
				break;
			}
			//printf("r %s %s\n",token,stack_peak());
			stack_peak(&itm,in);
			o2_pr=opp_pr(in,itm.str);

			if (o1_lr==LEFT)
			{
				if (o1_pr<=o2_pr)
				{
					stack_pop(&itm,in);
					output_push(in,&itm);
				}else
				{
					break;
				}
			}else
			{
				if (o1_pr<o2_pr)
				{
					stack_pop(&itm,in);
					output_push(in,&itm);
				}else
				{
					break;
				}
			}
		}
		//printf("%s\n",token);
		//getchar();
		//printf(">>\n");
		stack_item_init(&itm);
		itm.type=RPN_OPP;
		strcpy(itm.str,token);
		stack_push(in,&itm);
		//print_stack(in);
		//print_output(in);
		//getchar();
	}

	if (is_function(in,token)!=-1)
	{
		stack_item_init(&itm);
		strcpy(itm.str,token);
		itm.type=RPN_FUNCTION;
		stack_push(in,&itm);
	}

	return 0;
}

//https://isaaccomputerscience.org/concepts/dsa_toc_rpn?examBoard=all&stage=all
int evaluate(double *answer,struct rpn_calculator *in,struct rpn_equation *equ)
{
	int i=0;
	//int n=in->output_pos;
	char *token;
	struct stack_item result;
	struct stack_item *output_item;

	if (in->output_pos==0)
	{
		sprintf(in->error,"The stack is empty '%s' \n",equ->equ);
		return -1;
	}

	for (i=0;i<in->output_pos;i++)
	{
		//print_stack(in);
		//print_output(in);
		//getchar();

		output_item=&(in->output[i]);
		token=in->output[i].str;

		if (output_item->type==RPN_VAR)
		{
			struct rpn_vars_type *tmp;
			rpn_equation_is_var(equ,&tmp,token);	//convert var to number
			output_item->num=tmp->value;
			//printf(">>%le %s\n",tmp->value,token);
			//sscanf(token,"%le",&);
			output_item->type=RPN_NUMBER;
			stack_push(in,output_item);
		}else
		if (output_item->type==RPN_NUMBER)
		{
			stack_push(in,output_item);
		}else
		if (output_item->type==RPN_OPP)
		{
			//print_output(in);
			//print_stack(in);

			//print_stack(in);
			//getchar();
			if (opp_run(in,token,&result)==-1)
			{
				return -1;
			}

			stack_push(in,&result);
		}else
		if (output_item->type==RPN_FUNCTION)
		{
			function_run(in,token,&result);
			stack_push(in,&result);
		}else
		{
			sprintf(in->error,"I don't know what to do with %s %d\n",token,output_item->type);
			return -1;
		}

	}

	//print_stack(in);
	//print_output(in);
	//getchar();

	*answer=in->stack[0].num;
	return 0;
}

int rpn_build_stack(struct rpn_calculator *in,struct rpn_equation *equ)
{
	int i=0;
	//char temp[100];
	char found_token[100];
	strcpy(found_token,"");
	char *string=equ->equ;
	int n=isnumber(string[0]);
	char build_buf[STR_MAX];
	strcpy(build_buf,"");
	int str_max=strlen(string);
	//int temp_n=0;
	in->stack_pos=0;
	in->output_pos=0;
	struct stack_item itm;
	for (i=0;i<str_max+1;i++)
	{

		if (edge_detect(in,found_token, build_buf, string, i,str_max)==0)		//This detects edges and breaks the math down into chunks
		{
			rpn_process(in,equ,found_token);
		}

	}

	n=in->stack_pos;
	for (i=0;i<n;i++)
	{
		stack_pop(&itm,in);
		output_push(in,&itm);
	}

	return 0;
}

int rpn_evaluate(struct rpn_calculator *in,struct rpn_equation *equ)
{
	if (equ->evaluated==TRUE)
	{
		return equ->value;
	}

	rpn_detect_negation(in,equ);
	rpn_build_stack(in, equ);
	//print_stack(in);
	//print_output(in);
	//getchar();
	if (evaluate(&equ->value,in,equ)==-1)
	{
		printf("rpn error: %s\n",in->error);
		return -1;
	}

	if (equ->return_abs==TRUE)
	{
		equ->value=fabs(equ->value);
	}
	equ->evaluated=TRUE;

	return 0;
}


