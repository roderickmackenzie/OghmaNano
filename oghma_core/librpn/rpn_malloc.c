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
#include <ctype.h>

void rpn_malloc(struct rpn_calculator *in)
{
	//opps
	add_opp(in,"^", 4, RIGHT,&eval_pow,2);
	add_opp(in,"*", 3, LEFT,&eval_mul,2);
	add_opp(in,"~", 3, LEFT,&eval_negation,1);
	add_opp(in,"/", 3, LEFT,&eval_div,2);
	add_opp(in,"+", 2, LEFT,&eval_add,2);
	add_opp(in,"-", 2, LEFT,&eval_sub,2);
	add_opp(in,">", 3, LEFT,&eval_bg,2);
	add_opp(in,"<", 3, LEFT,&eval_sm,2);
	add_opp(in,">=", 3, LEFT,&eval_bg_eq,2);
	add_opp(in,"<=", 3, LEFT,&eval_sm_eq,2);

	//functions
	//1 opp
	add_function(in,"sin",&eval_sin,1);
	add_function(in,"cos",&eval_sin,1);
	add_function(in,"abs",&eval_abs,1);
	add_function(in,"pos",&eval_pos,1);
	add_function(in,"log",&eval_log10,1);
	add_function(in,"exp",&eval_exp,1);
	add_function(in,"sqrt",&eval_sqrt,1);
	//2 opps
	add_function(in,"min",&eval_min,2);
	add_function(in,"max",&eval_max,2);
	add_function(in,"rand",&eval_rand,2);
	add_function(in,"randlog",&eval_rand_log,2);
}

