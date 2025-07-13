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

/** @file json_struct.h
@brief Json decoder struct
*/

#ifndef json_struct_h
#define json_struct_h
#include <g_io.h>

enum JsonType {
    JSON_INT = 0,
    JSON_BOOL,
    JSON_DOUBLE,
    JSON_STRING,
    JSON_LONG_LONG,
    JSON_UNKNOWN_DATA,
    JSON_NODE,
    JSON_TEMPLATE,
    JSON_RANDOM_ID,
    JSON_STRING_HEX,
    JSON_DAT_FILE
};


#define JSON_PRIVATE    0x01


struct json_dump_settings
{
	int show_private;
	int show_templates;
};

struct json_obj
{
	char name[40];
	int len;
	int max_len;
	void *objs;

	char *data;
	int data_len;
	char data_type;
	unsigned char data_flags;

	void *json_template;
};

struct json_string
{
	char *data;
	int len;
	int pos;
	int compact;
};

struct json
{
	char *raw_data;
	long raw_data_len;
	long pos;
	int level;
	char path[OGHMA_PATH_MAX];
	struct json_obj obj;
	int compact;
	char file_path[OGHMA_PATH_MAX];
	int is_template;
	struct json_obj bib_template;
	int triangles_loaded;
	int bib_file;
	int yml_file;
};

struct json_segment_counter
{
	int i;
	int max;
	struct json_obj *segments;
	char path[OGHMA_PATH_MAX];
	char item[100];
	char item_path[OGHMA_PATH_MAX];
};

#endif
