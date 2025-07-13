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

//https://stackoverflow.com/questions/46861254/infix-to-postfix-for-negative-numbers
//Detects the difference between subtracttion and negation
int rpn_detect_negation(struct rpn_calculator *in,struct rpn_equation *equ)
{
	int i=0;
	char found_token[100];
	strcpy(found_token,"");

	char tmp[STR_MAX];
	char token_last[STR_MAX];
	char build_buf[STR_MAX];

	strcpy(tmp,"");
	strcpy(token_last,"");
	strcpy(build_buf,"");

	int str_max=strlen(equ->equ);
	int token=0;
	for (i=0;i<str_max+1;i++)
	{

		if (edge_detect(in,found_token, build_buf, equ->equ, i,str_max)==0)		//This detects edges and breaks the math down into chunks
		{
			if (strcmp(found_token,"-")==0)
			{
				if (token==0)
				{
					strcpy(found_token,"~");
				}else
				if (strcmp(token_last,"(")==0)
				{
					strcpy(found_token,"~");
				}else
				if (is_opp(in,token_last)!=-1)
				{
					strcpy(found_token,"~");
				}
				
			}
			strcat(tmp,found_token);
			strcpy(token_last,found_token);
			token++;
		}

	}
	strcpy(equ->equ,tmp);
	return 0;
}
