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


int rpn_test(char *equation, struct rand_state *rand)
{
	struct rpn_calculator rpn_cal;
	struct rpn_equation rpn_equ;
	rpn_init(&rpn_cal);
	rpn_equation_init(&rpn_equ);
	rpn_cal.rand=rand;
	rpn_malloc(&rpn_cal);
	rpn_equation_clear(&rpn_equ);
	remove_quotes(equation);
	strcpy(rpn_equ.equ,equation);
	//rpn_equation_set_var(&rpn_equ,"x",x);
	if (rpn_evaluate(&rpn_cal,&rpn_equ)==-1)
	{
		printf("Error evaluating equation\n");
		exit(0);
	}

	printf("%le\n",rpn_equ.value);

	rpn_equation_free(&rpn_equ);
	rpn_free(&rpn_cal);

	return 0;
}


