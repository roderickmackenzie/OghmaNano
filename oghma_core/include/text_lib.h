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

/** @file text_lib.h
	@brief Header file for text_lib.c
*/
#ifndef oghma_text_lib
#define oghma_text_lib

#include <ft2build.h>
#include <color.h>
#include <vec2d_int.h>
#include FT_FREETYPE_H

struct text_lib_item
{
	int x_size;
	int y_size;
	char text[STR_MAX];
	char id[STR_MAX];
	int false_color;
	unsigned int texture;
	float r_false;
	float g_false;
	float b_false;
	int deleted;
};

struct text_lib
{
	struct text_lib_item *items;
	int n_items;
	int n_items_max;
	char *buf;
	FT_Library    library;
	FT_Face       face;
	struct rgb_char rgb;
	int font_size;
	int line_spacing;
	int center_x;
	int center_y;
	int vertical;
};

int text_lib_init(struct text_lib *in);
int text_lib_free(struct text_lib *in);
int text_lib_load_fonts(struct text_lib *in, char *font_path);
int text_lib_clear(struct text_lib *in);
int text_lib_dump(struct text_lib *in);
int gen_text_from_font(struct text_lib *in,char *bit_buf, char *text, int *text_w, int *text_h, int output_image_w, int output_image_h, struct vec2d_int *xy, int dry_run);
void text_lib_draw_bitmap(char *bit_buf, FT_Bitmap*  bitmap, int x0, int y0, int out_max_x, int out_max_y, struct rgb_char *rgb);
void text_lib_write(struct text_lib *in,char *bit_buf, char *text, int output_image_w, int output_image_h, struct vec2d_int *xy, struct vec2d_int *ret_dxy);
int text_lib_cpy(struct text_lib *out, struct text_lib *in);
//text item
int text_lib_item_init(struct text_lib_item *in);
int text_lib_item_free(struct text_lib_item *in);

#endif
