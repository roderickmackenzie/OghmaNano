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

/** @file path_ops.c
	@brief Code to manipulate file paths
*/

#include <enabled_libs.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <path_ops.h>
#include <util_str.h>
#include <stdarg.h>
#include <g_io.h>

int get_delta_path(char *out, char *root,char *file_name)
{
	int root_len=strlen(root);
	int file_name_len=strlen(file_name);
	if (root_len>file_name_len)
	{
		strcpy(out,file_name);
		return -1;
	}

	if (root_len==0)
	{
		strcpy(out,file_name);
		return 0;
	}
	if (strcmp_begin(file_name,root)==0)
	{
		strcpy(out,file_name+root_len+1);
		return 0;
	}

	return -1;
}


int get_file_name_from_path(char *out,char *in, int max_out)
{
	int i=0;
	int pos=0;
	int count=0;
	int len_in=strlen(in);

	if (len_in==0)
	{
		out[0]=0;
		return 0;
	}

	for (i=len_in-1;i>=0;i--)
	{
		if ((in[i]=='\\') || (in[i]=='/'))
		{
			pos=i+1;
			count++;
			break;
		}
	}

	if (count>max_out)
	{
		printf("Warning input bigger than output\n");
		return -1;
	}

	strncpy(out,(char*)(in+pos),max_out);

	return -1;
}

void get_dir_name(char *out,char *in)
{
	int i=0;

	strcpy(out,in);

	if (strlen(in)==0)
	{
		return;
	}

	for (i=strlen(out)-1;i>=0;i--)
	{
		if ((out[i]=='\\') || (out[i]=='/'))
		{
			out[i]=0;
			return;
		}
	}

}

int is_dir_in_path(char *long_path, char* search_dir)
{
	if( strstr(long_path, search_dir) != NULL)
	{
		return 0;
	}else
	{
		return -1;
	}

return -1;
}

void get_nth_dir_name_from_path(char *out,char *in,int n)
{
	int i=0;
	int ii=0;
	int pos=0;
	int start=0;
	int stop=0;
	int count=0;
	strcpy(out,in);

	if (strlen(in)==0)
	{
		return;
	}

	for (i=0;i<strlen(in);i++)
	{
		if ((in[i]=='\\') || (in[i]=='/') || (i==strlen(in)-1))
		{
			if (i!=0)
			{
				stop=i;
				if (i==strlen(in)-1)
				{
					stop++;
				}


				if (count==n)
				{

					for (ii=start;ii<stop;ii++)
					{
						out[pos]=in[ii];
						pos++;
					}
					out[pos]=0;
					return;
				}
				start=stop+1;
				count++;
			}else
			{
				start=i+1;		// move it past the first / in a unix string
			}
		}
	}

}




void join_path(int max, ...)
{
	max=max+1;
	char temp[PATH_MAX];
	strcpy(temp,"");
	va_list arguments;
	int i;
	va_start ( arguments, max );
	char *ret=va_arg ( arguments, char * );
	strcpy(ret,"");
	for (i = 1; i < max; i++ )
	{
		if ((i!=1)&&(strcmp(temp,"")!=0))
		{
			strcat(ret,PATH_SEP);
		}
		strcpy(temp,va_arg ( arguments, char * ));
		strcat(ret,temp);
	}
	va_end ( arguments );                  // Cleans up the list

	return;
}


/**Make sure the slashes go the right way in a string for which ever OS we are on.
@param path path to check
*/
void assert_platform_path(char * path)
{
	int i=0;
	char temp[PATH_MAX];
	strcpy(temp,"");
	int max=strlen(path);
	for (i=0;i<max;i++)
	{
		if ((path[i]=='\\')||(path[i]=='/'))
		{
			strcat(temp,PATH_SEP);
		}else
		{
			temp[i]=path[i];
			temp[i+1]=0;
		}


	}

	strcpy(path,temp);

	return;
}

void remove_file_ext(char *path)
{
	int i=0;
	for (i=strlen(path)-1;i>0;i--)
	{
		if (path[i]=='.')
		{
			path[i]=0;
			break;
		}
	}
}

int path_up_level(char *out, char *in)
{
int i=0;
strcpy(out,in);
int len=strlen(out);
if (len<1)
{
	return -1;
}

if (len!=3)
{
	if (out[len-1]=='\\')
	{
		out[len-1]=0;
		len=strlen(out);
	}
}

if (len!=1)
{
	if (out[len-1]=='/')
	{
		out[len-1]=0;
		len=strlen(out);
	}
}

for (i=len;i>=0;i--)
{

		if (out[i]=='\\')
		{
			out[i+1]=0;
			break;
		}



		if (out[i]=='/')
		{
			out[i+1]=0;
			break;
		}
}

return 0;
}


int get_dir_name_from_path(char *out, char *in)
{
strcpy(out,in);

int i=0;
int len=strlen(in);
for (i=len;i>0;i--)
{
		if ((in[i]=='\\')||(in[i]=='/'))
		{
			out[i]=0;
			return 0;
		}
}

if (len>0)
{
	out[0]=0;
	return 0;
}

return -1;
}

int str_get_file_ext(char *ext,char *in, int max)
{
	int i;
	int in_len=strlen(in);
	int count=0;
	strcpy(ext,"none");
	if (in_len<2)
	{
		return -1;
	}

	for (i=in_len-1;i>0;i--)
	{
		if (in[i]=='.')
		{
			if (count==0)
			{
				return -1;
			}

			strcpy(ext,&in[i+1]);
			return 0;
		}else
		if ((in[i]=='/')||(in[i]=='\\'))
		{
			return -1;
		}

		count++;

		if (count>=max)
		{
			return -1;
		}
	}

	return -1;
}

