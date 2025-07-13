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

/** @file oghma_gui.h
	@brief Header file for oghma_gui.c
*/
#ifndef oghma_gui
#define oghma_gui
#include <dat_file.h>

int draw_all_traps(double *tot_lumo, double *tot_homo,struct dat_file *lumo,struct dat_file *homo,struct dat_file *numerical_lumo,struct dat_file *numerical_homo,struct json *j,char *json_path);
int draw_traps_malloc(struct dat_file *buf, double Ec, double Ev, int is_lumo);
int draw_traps(struct dat_file *buf, char *equation, double a, double b, double c);
double draw_traps_calculate_numerical_dos(struct dat_file *buf, struct dat_file *in,int bands,double srh_start,double srh_stop, int is_lumo);

#endif
