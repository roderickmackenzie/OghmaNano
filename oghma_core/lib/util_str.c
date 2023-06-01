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
#include <ctype.h>
	 #include <fnmatch.h>

int is_numbered_file(char *in,char *root)
{
	if (strcmp_end(in,".inp")!=0)
	{
		return -1;
	}

	if (strcmp_begin(in,root)!=0)
	{
		return -1;
	}

return 0;
}


void string_to_hex(char* out,char* in)
{
int i;
char temp[8];
strcpy(out,"");

for (i=0;i<strlen(in);i++)
{
	sprintf(temp,"%02x",in[i]);
	strcat(out,temp);
}

}

int hex_to_string(char* in)
{
	//This needs fixing.
	int i;
	int len;
	char temp[8];
	unsigned int val;

	len=strlen(in);

	if (len%2!=0)
	{
		return -1;
	}

	for (i=0;i<len/2;i++)
	{
		temp[0]=in[i*2];
		temp[1]=in[(i*2)+1];
		temp[2]=0;
		sscanf(temp,"%x",&val);
		in[i]=val;
	}

	in[i]=0;

	return 0;

}

int cmpstr_min(char * in1,char *in2)
{
int i;
int max=strlen(in1);
if (strlen(in2)<max) max=strlen(in2);
for (i=0;i<max;i++)
{
	if (in1[i]!=in2[i]) return 1;
}
return 0;
}

int strextract_name(char *out,char * in)
{
int i;
for (i=0;i<strlen(in);i++)
{
	if (in[i]=='@')
	{
		out[i]=0;
		return strlen(out);
	}
	out[i]=in[i];

}
strcpy(out,"");
return -1;
}

int strcmp_end(char * str,char *end)
{
if (strlen(str)<strlen(end)) return 1;
int pos=strlen(str)-strlen(end);
return strcmp((char *)(str+pos),end);
}

int strcmp_begin(char * str,char *begin)
{
return strcmp_begin_safe(str,strlen(str),begin,strlen(begin));
}

int strcmp_begin_safe(char * str,int str_len,char *begin,int begin_len)
{
	int i;

	if (str_len<begin_len) return 1;

	for (i=0;i<begin_len;i++)
	{
		if (str[i]!=begin[i]) return 1;
	}

	return 0;
}

char* strextract_domain(char * in)
{
int i=0;
for (i=0;i<strlen(in)-1;i++)
{
	if (in[i]=='@')
	{
		return (char *)(&in[i+1]);
	}
}
return NULL;
}

int is_domain(char * in)
{
int i=0;
for (i=0;i<strlen(in)-1;i++)
{
	if (in[i]=='@')
	{
		return 0;
	}
}


return -1;
}

int extract_str_number(char * in,char *cut)
{
int out;
int len=strlen(cut);
sscanf((in+len),"%d",&out);
return out;
}

int strextract_int(char * in)
{
char temp[200];
int i=0;
int ret=0.0;
int count=0;
for (i=0;i<strlen(in);i++)
{
	if ((in[i]>47)&&(in[i]<58))
	{
		temp[count]=in[i];
		count++;
	}

}
temp[count]=0;
sscanf(temp,"%d",&ret);
return ret;
}

void split_dot(char *out, char *in)
{
	int i=0;
	strcpy(out,in);
	for (i=0;i<strlen(out);i++)
	{
		if (out[i]=='.')
		{
			out[i]=0;
			break;
		}
	}
}


int get_line(char *out,char *data,long len,long *pos, int out_buffer_max)
{
	out[0]=0;
	//printf("%s\n",data);
	int i=0;
	if (*pos>=len)
	{
		return -1;
	}

		//printf("pos = %d\n",*pos);
		//getchar();
	while(*pos<len)
	{
		if ((data[*pos]=='\n')||(data[*pos]=='\r')||(data[*pos]==0))
		{
			out[i]=0;

			if (data[*pos]=='\r')
			{
				(*pos)++;
			}

			if (*pos<len)
			{
				if (data[*pos]=='\n')
				{
					(*pos)++;
				}
			}
			break;
		}

		out[i]=data[*pos];
		out[i+1]=0;
		i++;

		if (out_buffer_max!=-1)
		{
			if (i>=out_buffer_max)
			{
				printf("buffer smashed\n");
				return -1;
			}
		}

		(*pos)++;

	}

return i;
}

//This gets the number of text/number items in a line
//It assumes the first # encountered means everything after is a comment
int count_csv_items(char *in)
{
	int i;
	int end=strlen(in);
	int items=0;
	//find the end or comment #
	for (i=0;i<strlen(in);i++)
	{
		if (in[i]==0)
		{
			end=strlen(in);
		}

		if (in[i]=='#')
		{
			end=i;
		}
	}

	int space=FALSE;
	int last_char_space=TRUE;
	for (i=0;i<end;i++)
	{
		if (isspace(in[i])==0)		//Done as output from isspace is confusing
		{
			space=FALSE;
		}else
		{
			space=TRUE;
		}

		if ((last_char_space==FALSE)&&(space==TRUE))
		{
			items++;
		}else
		if ((space==FALSE)&&(i==end-1))
		{
			items++;
		}

		//printf("%c %d %d\n",in[i],space,items);

		last_char_space=space;
	}
	return items;
}

void str_split(char *in_string, ...)
{

	va_list arguments;
	int i;
	va_start ( arguments, in_string );
	char *ret=va_arg ( arguments, char * );
	strcpy(ret,"");
	int pos=0;
	for (i=0;i<strlen(in_string);i++)
	{
		ret[pos]=in_string[i];
		ret[pos+1]=0;


		if (in_string[i]==',')
		{
			ret[pos]=0;
			ret=va_arg ( arguments, char * );
			pos=0;
			ret[pos]=0;
		}else
		{
			pos++;
		}
		//printf("%s\n",ret);
	}

	va_end ( arguments );                  // Cleans up the list

	return;
}

void str_strip(char *in_string)
{
	int i;
	for (i=strlen(in_string)-1;i>=0;i--)
	{
		if (in_string[i]==13)
		{
			in_string[i]=0;
		}else
		if (in_string[i]==10)
		{
			in_string[i]=0;
		}else
		{
			break;
		}
	}

}

int str_is_ascii(char *in_string)
{
	int i;
	unsigned char val; 
	for (i=0;i<strlen(in_string);i++)
	{
		val=in_string[i];
		//printf("%c %d\n",val,val);
		if (val>127)
		{
			return -1;
		}

		if (val==63)
		{
			return -1;
		}
	}
	return 0;
}

int str_count(char *in,char *find)
{
	int i;
	int ii;
	int times=0;
	int found=FALSE;
	int in_len=0;
	int find_len=0;
	in_len=strlen(in);
	find_len=strlen(find);

	for (i=0;i<in_len;i++)
	{
		found=TRUE;
		for (ii=0;ii<find_len;ii++)
		{
			if (i+ii<in_len)
			{
				if (in[i+ii]!=find[ii])
				{
					found=FALSE;
				}
			}else
			{
				found=FALSE;
			}
		}

		if (found==TRUE)
		{
			times++;
		}
	}

	if (times==0)
	{
		return -1;
	}

	return times;
}

void str_replce(char **out, char *in,char *find,char *replace)
{
	int i;
	int ii;
	int times=0;
	int found=FALSE;
	int in_len=0;
	int find_len=0;
	int replace_len=0;
	int out_pos=0;
	int new_len=0;
	in_len=strlen(in);
	find_len=strlen(find);
	replace_len=strlen(replace);

	times=str_count(in,find);
	if (times==-1)
	{
		times=0;
	}

	new_len=in_len+1+find_len*times;
	*out=malloc(new_len);
	
	(*out)[out_pos]=0;
	for (i=0;i<in_len;i++)
	{
		found=TRUE;
		for (ii=0;ii<find_len;ii++)
		{
			if (i+ii<in_len)
			{
				if (in[i+ii]!=find[ii])
				{
					found=FALSE;
				}
			}else
			{
				found=FALSE;
			}
		}

		if (found==TRUE)
		{
			for (ii=0;ii<replace_len;ii++)
			{
				(*out)[out_pos++]=replace[ii];
			}
			i+=find_len-1;
		}else
		{
			(*out)[out_pos++]=in[i];
		}
	}

	if (out_pos>=new_len)
	{
		printf("str_replce error %d %d!\n",out_pos,new_len);
	}

	(*out)[out_pos++]=0;


}
