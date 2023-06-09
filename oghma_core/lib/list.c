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

/** @file list.c
	@brief Simple list code
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "list_struct.h"
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
 #include <ctype.h>

void list_init(struct list *in)
{
	in->names=NULL;
	in->len=0;
	in->len_max=0;
}

void list_malloc(struct list *in)
{
	in->len=0;
	in->len_max=10;
	in->names=(char **)malloc(in->len_max*sizeof(char*));
}

void list_add(struct list *in,char *text)
{
	if (in->names==NULL)
	{
		list_malloc(in);
	}

	in->names[in->len]=(char *)malloc(sizeof(char)*STR_MAX);
	strcpy(in->names[in->len],text);
	in->len++;
	if (in->len==in->len_max)
	{
		in->len_max*=2;
		in->names=(char **)realloc(in->names,in->len_max*sizeof(char *));
	}
}

void list_free(struct list *in)
{
	int i=0;

	for (i=0;i<in->len;i++)
	{
		free(in->names[i]);
	}

	free(in->names);
	list_init(in);
}

int list_cmp(struct list *in,char *name)
{
	int i=0;

	for (i=0;i<in->len;i++)
	{
		if (strcmp(name,in->names[i])==0)
		{
			return 0;
		}
	}

return -1;
}

void list_dump(struct list *in)
{
	int i=0;

	for (i=0;i<in->len;i++)
	{
		printf("%s |",in->names[i]);
	}

	printf("\n");
}

void list_import_from_string(struct list *in, char *text)
{
	int i;
	int len=strlen(text);
	char build[STR_MAX];
	int pos=0;

	for (i=0;i<len;i++)
	{
		if (isspace(text[i])==0)
		{
			build[pos]=text[i];
			pos++;
			build[pos]=0;
		}

		if (pos!=0)
		{
			if ((isspace(text[i])!=0)||(i==(len-1)))
			{
				list_add(in,build);
				pos=0;
			}
		}

	}
	
}
