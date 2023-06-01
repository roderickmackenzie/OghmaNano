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

/** @file util_str_clean.c
	@brief Utility functions for string handeling.
*/



#include <enabled_libs.h>
#include <oghma_const.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <util_str.h>
#include <ctype.h>

void remove_space_after(char *in)
{
	int i;
	for (i=strlen(in)-1;i>0;i--)
	{
		if (isspace(in[i])!=0)
		{
			in[i]=0;
		}else
		{
			break;
		}
	}	
}

void remove_quotes(char *out)
{
	int i=0;
	int len;
	remove_space_after(out);
	len=strlen(out);
	if (len>1)
	{
		if (out[len-1]=='\"')				//So it ends with a quote so now remove it and hunt for the first quote
		{
			out[len-1]=0;
			len=strlen(out);
			int out_pos=0;
			int first_quote_found=FALSE;
			for (i=0;i<len;i++)
			{
				if ((out[i]!='\"')||(first_quote_found==TRUE))
				{
					out[out_pos]=out[i];
					out_pos++;
				}

				if (out[i]=='\"')
				{
					first_quote_found=TRUE;
				}
			}
			out[out_pos]=0;
		}
	}
}
