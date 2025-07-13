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

/** @file token_lib.h
@brief Stores tokens
*/

#ifndef token_lib_h
#define token_lib_h
#include <list_struct.h>

struct token_lib_item
{
	char token[100];
	char english[100];
	char widget[100];
	char units_widget[100];
	char units[100];
	int log;
	int hidden;
	struct list hide_on_token;
	struct list hide_on_value;

	struct list show_on_token;
	struct list show_on_value;

	struct list default_token;
	struct list default_value;

	struct list pack;
};

int token_lib_init(struct hash_list *in);
struct token_lib_item* token_lib_add_item(struct hash_list *in,char *token,char *english,char *widget,char *units,int log);
int token_lib_build(struct hash_list *in);
int token_lib_dump(struct hash_list *in);
int token_lib_dump_item(struct token_lib_item* item);
struct token_lib_item* token_lib_find(struct hash_list *in,char *token);
struct token_lib_item* token_lib_rfind(struct hash_list *in,char *english,int *last);
int token_lib_free(struct hash_list *in);
int token_lib_item_add_hide_on(struct token_lib_item* item,char *token, char *value);
int token_lib_item_add_show_on(struct token_lib_item* item,char *token, char *value);
int token_lib_item_add_default(struct token_lib_item* item,char *token, char *value);
int token_lib_item_add_pack(struct token_lib_item* item,char *token);

int token_lib_get_show_on(struct token_lib_item* item,char *token,char *val, int i);
int token_lib_get_hide_on(struct token_lib_item* item,char *token,char *val, int i);
int token_lib_get_default(struct token_lib_item* item,char *token,char *val, int i);
int token_lib_get_pack(struct token_lib_item* item,char *token, int i);
#endif
