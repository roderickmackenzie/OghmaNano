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

/** @file josn_fast.c
	@brief Json small and simple json decoder
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>

#define SEARCH_TOKEN_OPEN 0
#define SEARCH_TOKEN_CLOSE 1
#define SEARCH_VAL_OPEN 2
#define SEARCH_VAL_CLOSE 3

int json_fast_load(char *file_name, void (*callback)(), void *data)
{
	int i;
	FILE * in;
	char c;
	char *line;
	ssize_t read;
	char path[STR_MAX];
	strcpy(path,"");

	in = g_fopen(file_name, "r");
	if (in == NULL)
	{
		return -1;
	}

	line=malloc(sizeof(char)*STR_MAX);
	int search_for=SEARCH_TOKEN_OPEN;
	int build_token=FALSE;
	int build_val=FALSE;
	char token[STR_MAX];
	int token_len=0;
	char val[STR_MAX];
	int val_len=0;
	int just_changed=FALSE;
	strcpy(token,"");
	strcpy(val,"");
	int level=0;
	int found_token=FALSE;
	int found_val=FALSE;
	char full_path[STR_MAX];
	int ret=0;
	//printf("here\n");
	while (fgets (line, STR_MAX, in)!=NULL)
	{
		///printf("%s",line);
		search_for=SEARCH_TOKEN_OPEN;
		found_token=FALSE;
		found_val=FALSE;
		read=strlen(line);
		for (i=0;i<read;i++)
		{
			just_changed=FALSE;
			c=line[i];
			if (c=='{')
			{
				if (strlen(path)!=0)
				{
					strcat(path,"|");
				}
				strcat(path,token);

				search_for=SEARCH_TOKEN_OPEN;
				level++;
			}else
			if (c=='}')
			{
				if (split_reverse(path,'|')==-1)
				{
					strcpy(path,"");
				}

				search_for=SEARCH_TOKEN_OPEN;
				level--;
			}else
			if (c=='\"')
			{
				if (search_for==SEARCH_TOKEN_OPEN)
				{
					build_token=TRUE;
					search_for=SEARCH_TOKEN_CLOSE;
				}else
				if (search_for==SEARCH_TOKEN_CLOSE)
				{
					build_token=FALSE;
					found_token=TRUE;
					search_for=SEARCH_VAL_OPEN;
				}else
				if (search_for==SEARCH_VAL_OPEN)
				{
					build_val=TRUE;
					search_for=SEARCH_VAL_CLOSE;
				}else
				if (search_for==SEARCH_VAL_CLOSE)
				{
					build_val=FALSE;
					found_val=TRUE;
				}
				just_changed=TRUE;
			}

			if (just_changed==FALSE)
			{
				if (build_token==TRUE)
				{
					token[token_len++]=c;
					token[token_len]=0;
				}

				if (build_val==TRUE)
				{
					val[val_len++]=c;
					val[val_len]=0;
				}
			}

		}
		build_token=FALSE;
		build_val=FALSE;
		if ((found_token==TRUE)&&(found_val==TRUE))
		{
			strcpy(full_path,path);
			strcat(full_path,"|");
			strcat(full_path,token);
			str_replace_char(full_path,'|', '.');
			ret=0;
			(*callback)(full_path,val,data,&ret);
			if (ret==-1)
			{
				return 0;
			}
		}
		//printf("path=%s %d\n",path,level);
		//getchar();
		//printf("t='%s' v='%s'",token, val);
		//getchar();
		strcpy(line,"");
		strcpy(token,"");
		strcpy(val,"");
		token_len=0;
		val_len=0;
	}

	fclose(in);

	if (line!=NULL)
	{
		free(line);
	}

	return 0;
}

