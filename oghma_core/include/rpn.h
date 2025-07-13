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

/** @file rpn.h
@brief RPN functions which oghma can handle.
*/

#ifndef rpn_h
#define rpn_h
#include <g_io.h>
#include <rpn_struct.h>

//rpn
void rpn_init(struct rpn_calculator *in);
void rpn_malloc(struct rpn_calculator *in);
void rpn_free(struct rpn_calculator *in);
int add_function(struct rpn_calculator *in,char *name,void *f, int number_to_take_from_stack);
int is_function(struct rpn_calculator *in,char *val);
int function_run(struct rpn_calculator *in,char *val,struct stack_item *out);

//opp
int add_opp(struct rpn_calculator *in,char *name, int prec, int right_left,void *f,int number_to_take_from_stack);
int is_opp(struct rpn_calculator *in,char *val);
int opp_run(struct rpn_calculator *in,char *val,struct stack_item *out);
int opp_pr(struct rpn_calculator *in,char *val);
int opp_lr(struct rpn_calculator *in,char *val);

//stack
void stack_item_init(struct stack_item *itm);
void output_push(struct rpn_calculator *in,struct stack_item *itm);
void stack_push(struct rpn_calculator *in,struct stack_item *itm);
int stack_pop(struct stack_item *itm,struct rpn_calculator *in);
int stack_peak(struct stack_item *itm,struct rpn_calculator *in);
void print_stack(struct rpn_calculator *in);
void print_output(struct rpn_calculator *in);

int isnumber(char a);


int edge_detect(struct rpn_calculator *in,char *found_token, char *build_buf, char *buf, int buf_pos, int buf_max);
int rpn_detect_negation(struct rpn_calculator *in,struct rpn_equation *equ);
int rpn_process(struct rpn_calculator *in,struct rpn_equation *equ,char *token);
int rpn_evaluate(struct rpn_calculator *in,struct rpn_equation *equ);
int rpn_build_stack(struct rpn_calculator *in, struct rpn_equation *equ);

//Functions
//1 input
int eval_sin(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a);
int eval_abs(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a);
int eval_pos(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a);
int eval_log10(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a);
int eval_exp(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a);
int eval_sqrt(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a);

//2 input
int eval_min(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_max(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_rand(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_rand_log(struct rpn_calculator *cal, struct stack_item *out,struct stack_item *a,struct stack_item *b);

//ops
int eval_bg(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_sm(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_bg_eq(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_sm_eq(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_add(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_sub(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_negation(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_mul(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_pow(struct stack_item *out,struct stack_item *a,struct stack_item *b);
int eval_div(struct stack_item *out,struct stack_item *a,struct stack_item *b);

//vars - rpn_equation
char* rpn_decode(int num);
void rpn_equation_init(struct rpn_equation *in);
void rpn_equation_free(struct rpn_equation *in);
void rpn_equation_clear(struct rpn_equation *in);
struct rpn_vars_type *rpn_equation_set_var(struct rpn_equation *in,char *name,double value);
int rpn_equation_is_var(struct rpn_equation *in,struct rpn_vars_type **out,char *name);
int rpn_equation_set_std_vars(struct rpn_equation *in,double x,double y,double T);
void rpn_equation_cpy(struct rpn_equation *out,struct rpn_equation *in);
int rpn_equation_dump(struct rpn_equation *in);

//tests
int rpn_test(char *equation, struct rand_state *rand);
#endif
