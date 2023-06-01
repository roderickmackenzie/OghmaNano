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

/** @file util_str.c
	@brief Utility functions for string handeling.
*/



#include <enabled_libs.h>
#include <oghma_const.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <sys/stat.h>
#include <math.h>
#include <stdarg.h>
#include <util_str.h>
	 #include <fnmatch.h>

int is_number(char a)
{
switch(a)
{
	case '1':
		return TRUE;
	case '2':
		return TRUE;
	case '3':
		return TRUE;
	case '4':
		return TRUE;
	case '5':
		return TRUE;
	case '6':
		return TRUE;
	case '7':
		return TRUE;
	case '8':
		return TRUE;
	case '9':
		return TRUE;
	case '0':
		return TRUE;
	case 'e':
		return TRUE;
	case 'E':
		return TRUE;
	case '+':
		return TRUE;
	case '-':
		return TRUE;
	case '.':
		return TRUE;
	default:
		return FALSE;
}

}

//n==-1 counts all the numbers other values extract them
//If comment !=null then it terminates at a #
int get_number_in_string(double *out, char* in, int n, int *comment_pos)
{
	int i=0;
	int len=strlen(in);
	int m=0;
	int c=0;
	int number=0;

	if (comment_pos!=NULL)
	{
		*comment_pos=-1;
	}

	for (i=0;i<len;i++)
	{
		if (comment_pos!=NULL)
		{
			if ((in[i]=='#')&&(i!=len-1))
			{
				*comment_pos=i+1;
				break;
			}
		}

		if (i>0)
		{
			m=is_number(in[i-1]);
		}else
		{
			m=FALSE;
		}

		c=is_number(in[i]);

		if ((m==FALSE) && (c==TRUE))
		{
			if ((n!=-1)&&(out!=NULL))		//we want to extact a number not just count
			{
				if (number==n)
				{
					sscanf(&(in[i]),"%le",out);
					return 0;
				}
			}
			number++;
		}

		//printf("%c %d (%d %d)\n",in[i],number,m,c);
	}

if (n==-1)
{
	return number;
}

return -1;
}

int replace_number_in_string(char *buf, char* in, double replace, int n)
{
	int i=0;
	int len=strlen(in);
	int m=0;
	int c=0;
	int number=-1;
	int pos=0;
	strcpy(buf,"");

	for (i=0;i<len;i++)
	{
		if (i>0)
		{
		m=is_number(in[i-1]);
		}else
		{
			m=FALSE;
		}

		c=is_number(in[i]);

		if ((m==FALSE) && (c==TRUE))
		{
			number++;
			if (number==n)
			{
				char temp[200];
				sprintf(temp,"%le ",replace);
				strcat(buf,temp);
				pos=strlen(buf);
			}
		}

		if (number!=n)
		{
			buf[pos]=in[i];
			pos++;
			buf[pos]=0;

		}

	}

	return 0;
}

int str_isnumber(char *input)
{
    int start = 0;
	int len=strlen(input);
	int stop= len-1;
	if (len==0)
	{
		return FALSE;
	}

	//sort spaces
	while(input[start] == ' ')
	{
		start++;
		if (start>=len)
		{
			return FALSE;
		}
	}

	while(input[stop] == ' ')
	{
        stop--;
		if (stop<=0)
		{
			printf("b\n");
			return FALSE;
		}
	}


    // len==1 and first character not digit
    if(len == 1 && !(input[start] >= '0' && input[stop] <= '9'))
	{
		return FALSE;
	}

    // 1st char must be +, -, . or number
    if( input[start] != '+' && input[start] != '-' && !(input[start] >= '0' && input[start] <= '9'))
	{
		return FALSE;
	}

    int dot_or_e = FALSE;
    int seen_e = FALSE;
	int i=start;

    for (i = start ; i <= stop ; i++)
    {
        // Only allow numbers, +, - and e
        if(input[i] != 'e' && input[i] != 'E' && input[i] != '.' &&   input[i] != '+' && input[i] != '-' &&  !(input[i] >= '0' && input[i] <= '9'))
		{
			return FALSE;
		}

        if(input[i] == '.')
        {
            // a . as a last character is not allowed
            if(i == len-1)
			{
				return FALSE;
			}

            // have we seen a dot or e before
            if(dot_or_e == TRUE)
			{
                return FALSE;
			}

            // If we have a . we need a number after it
            if(!(input[i+1] >= '0' && input[i+1] <= '9'))
			{
				return FALSE;
			}

		}else
		if ((input[i] == 'e') || (input[i] == 'E'))
        {
            if (seen_e==TRUE)
			{
				return FALSE;
			}

            dot_or_e = TRUE;
			seen_e=TRUE;

            // e as the last character is also not allowed
            if(i == len-1)
			{
				return FALSE;
			}

            // an e first is not allowed we need a number before it
            if(!(input[i-1] >= '0' && input[i-1] <= '9'))
			{
				return FALSE;
			}

            // e must be followed by a + - or a number
            if (input[i+1] != '+' && input[i+1] != '-' && (input[i+1] >= '0' && input[i] <= '9'))
			{
				return FALSE;
			}
        }
    }


	return TRUE;
}



