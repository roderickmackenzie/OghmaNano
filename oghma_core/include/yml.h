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

/** @file yml.h
@brief yml decoder
*/

#ifndef yml_h
#define yml_h
#include <json_struct.h>
#include <math_xy.h>

struct material_yml
{
	char n_type[20];
	char alpha_type[20];
	double lambda_start_n;
	double lambda_stop_n;
	double lambda_start_alpha;
	double lambda_stop_alpha;
	struct math_xy n;
	struct math_xy alpha;
};

//
int material_yml_init(struct material_yml *in);
int material_yml_load_from_json(struct material_yml *out, struct json *j);
int material_yml_dump(struct material_yml *in);
int material_yml_project_n_to_math_xy(struct math_xy *out, struct material_yml *mat);
int material_yml_project_alpha_to_math_xy(struct math_xy *out, struct material_yml *mat);
int material_yml_free(struct material_yml *in);
int yml_peek_is_mat_file(char *buf, long len);

#endif
