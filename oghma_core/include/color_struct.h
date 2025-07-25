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

/** @file color_struct.h
	@brief Header file for lib which handles cie_colors
*/

#ifndef color_struct_h
#define color_struct_h

	#define color_map_max 100

	struct color_map_item
	{
		const unsigned char *a;
		char text[100];
		int len;
	};

	struct rgb_char
	{
		unsigned char r;
		unsigned char g;
		unsigned char b;
		unsigned char alpha;
	};

	struct obj_color
	{
		int map;
		double r;
		double g;
		double b;
		double alpha;
	};

		#define fg_reset	0
		#define fg_wight	97
		#define fg_red		31
		#define fg_green	32
		#define fg_yellow	33
		#define fg_blue		34
		#define fg_purple	35

#endif
