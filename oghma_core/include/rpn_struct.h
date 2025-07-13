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

/** @file rpn_struct.h
@brief RPN functions which oghma can handle.
*/

#ifndef rpn_struct_h
#define rpn_struct_h

#include <rand_state.h>

#define RPN_STACK_MAX_LEN 100

#define RPN_FUNCTION 0
#define RPN_VAR 1
#define RPN_NUMBER 2
#define RPN_OPP 3


struct stack_item
{
	char str[40];
	double num;
	int type;
};

struct rpn_function_type
{
	char name[10];
	void *f;//char* (*f)(struct stack_item *out,struct stack_item *a,struct stack_item *b);
	int number_to_take_from_stack;		//args
};

struct rpn_opperator_type
{
	char name[10];
	int prec;
	int right_left;
	char* (*f)(struct stack_item *out,struct stack_item *a,struct stack_item *b);
	int number_to_take_from_stack;

};


struct rpn_vars_type
{
	char name[10];
	double value;
};

struct rpn_equation
{
	char equ[100];
	struct rpn_vars_type *vars;
	int vars_pos;
	int vars_pos_max;
	int return_abs;
	int evaluated;
	double value;
};

struct rpn_calculator
{
	struct stack_item *output;
	int output_pos;
	int output_max;

	struct stack_item *stack;
	int stack_pos;
	int stack_max;

	struct rpn_function_type *functions;
	int functions_count;
	int functions_max;

	struct rpn_opperator_type *opps;
	int opp_count;
	int opp_max;
	char error[STR_MAX];

	struct rand_state *rand;
};

#endif
