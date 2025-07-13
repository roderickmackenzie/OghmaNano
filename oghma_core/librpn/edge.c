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

/** @file edge.c
@brief RPN detecting edges.
*/


#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <ctype.h>

#include "util.h"
#include "oghma_const.h"
#include <rpn.h>

int isnumber(char a)
{
int digit=isdigit(a);

	if ((digit!=0)||(a=='.'))
	{
		return 0;
	}

return -1;

}

//This needs to be run over ths string buf_max+1 times. The last time is to claer any
//tokens left in the buffer
int edge_detect(struct rpn_calculator *in,char *found_token, char *build_buf, char *buf, int buf_pos, int buf_max)
{
	if (buf_max==0)
	{
		goto ignore;
	}

	char c0=buf[buf_pos];
	char cm1=-1;
	char cm2=-1;
	char cm3=-1;
	if (buf_pos>0) cm1=buf[buf_pos-1];
	if (buf_pos>1) cm2=buf[buf_pos-2];
	if (buf_pos>2) cm3=buf[buf_pos-3];

	int build_buf_len=strlen(build_buf);

	if (buf_pos==buf_max)
	{
		//aprintf("E0\n");
		goto edge_detected;
	}

	if (isspace(c0)!=0)		//If it is not white space add it to the build string
	{
		goto ignore;	//ignore white space
	}

	if (cm1!=-1)
	{
		if ((isnumber(cm1)==0) && (c0=='e'))
		{
			goto no_edge;
		}

		if (cm2!=-1)
		{
			if ((isnumber(cm2)==0) && (cm1=='e') && ((c0=='+') || (c0=='-') || (isnumber(c0)==0)) )
			{
				goto no_edge;
			}
		}

		if (cm3!=-1)
		{
			if ((isnumber(cm3)==0) && (cm2=='e') && ((cm1=='+') || (cm1=='-')) && (isnumber(c0)==0))
			{
				goto no_edge;
			}
		}

		if ((isnumber(cm1)==0) && (isnumber(c0)!=0))
		{
			//aprintf("E1\n");
			goto edge_detected;
		}

		if ((isnumber(cm1)!=0) && (isnumber(c0)==0))
		{
			//aprintf("E2\n");
			goto edge_detected;
		}

	}

	if ((c0=='(') || (c0==')'))
	{
		//aprintf("E3\n");
		goto edge_detected;
	}

	if (c0==',')
	{
		//aprintf("E3\n");
		goto edge_detected;
	}

	if (strcmp(build_buf,")")==0)
	{
		//aprintf("E4\n");
		goto edge_detected;
	}

	if (strcmp(build_buf,"(")==0)
	{
		//aprintf("E5\n");
		goto edge_detected;
	}

	if (strcmp(build_buf,"*")==0)
	{
		//aprintf("E6\n");
		goto edge_detected;
	}

	int i;
	for (i=0;i<in->opp_count;i++)	//looking for >= and <=
	{
		if ((strcmp(build_buf,in->opps[i].name)==0)&&(c0=='='))
		{
			goto no_edge;
		}
	}

	for (i=0;i<in->opp_count;i++)
	{
		if ((strcmp(build_buf,in->opps[i].name)==0)||(in->opps[i].name[0]==c0))
		{
			//aprintf("E7\n");
			goto edge_detected;
		}
	}

	if (strcmp(build_buf,"^")==0)
	{
		goto edge_detected;
	}

	no_edge:
		build_buf[build_buf_len]=c0;
		build_buf[build_buf_len+1]=0;
		strcpy(found_token,"");
		return -1;

	edge_detected:
		strcpy(found_token,build_buf);
		build_buf[0]=c0;
		build_buf[1]=0;
		if (strcmp(found_token,"")==0)	//If the token we found is empty then it's not a token. Can happen at start of string.
		{
			return -1;
		}
		return 0;

	ignore:
		return -1;

}



