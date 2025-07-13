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

/** @file josn_dump.c
	@brief Json file decoder
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "util.h"
#include "code_ctrl.h"
#include "oghma_const.h"
#include <log.h>
#include <cal_path.h>
#include "lock.h"
#include <json.h>

void json_string_init(struct json_string *in)
{
	in->data=NULL;
	in->len=0;
	in->pos=0;
	in->compact=FALSE;

}

void json_string_free(struct json_string *in)
{
	if (in->data!=NULL)
	{
		free(in->data);
	}

	json_string_init(in);
}

void json_string_cat(struct json_string *buf,char *data)
{
	char *array;
	int str_len=strlen(data);
	int new_len=0;
	int bytes_left=buf->len-buf->pos;

	if (bytes_left<str_len+1)
	{
		if (buf->len > 0)
		{
			new_len = buf->len;
		}else
		{
			new_len = 512;
		}

        while (new_len - buf->pos < str_len + 1)
        {
            new_len *= 2;
        }

		buf->data=realloc(buf->data,new_len*sizeof(char));
		buf->len=new_len;

	}

	array=(buf->data+buf->pos);

	memcpy(array, data, str_len);
	array[str_len]=0;
	buf->pos += str_len;

	if (buf->compact==TRUE)
	{
		if (str_len>2)
		{
			if (buf->data[buf->pos-1]=='\n')
			{
				buf->data[buf->pos-1]=0;
				buf->pos--;
			}
		}
	}

}

int json_string_cat_char(struct json_string *buf,char in_data)
{
	char data[2];
	data[0]=in_data;
	data[1]=0;
	json_string_cat(buf,data);
	return 0;
}

int json_string_del_last_chars(struct json_string *buf,int n)
{
	if ((buf->pos-n)>=0)
	{
		buf->data[buf->pos-n]=0;
		buf->pos-=n;
	}

	return 0;
}

int json_string_clear(struct json_string *buf)
{
	buf->pos=0;
	if (buf->len>0)
	{
		buf->data[0]=0;
	}
	
	return 0;
}
