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

/** @file newton_state.h
	@brief The main structure which holds information about the device.
*/

#ifndef newton_state_fun_h
#define newton_state_fun_h
#include <newton_state.h>

//newton state
void newton_state_init(struct newton_state *ns);
int newton_state_malloc(struct newton_state *ns,struct device *dev, struct dimensions *dim);
int newton_state_alloc_traps(struct newton_state *ns);
void newton_state_free(struct newton_state *ns);
int newton_state_cpy(struct newton_state *out,struct newton_state *in);
void newton_state_save(struct simulation *sim,char *file_name,struct newton_state *ns);
int newton_state_load(struct simulation *sim,struct newton_state *ns,char *file_name);
void newton_state_update_device(struct simulation *sim,struct device *in, struct newton_state *ns);
void newton_state_set_last_error(struct simulation *sim, struct newton_state *ns,gdouble error);
void newton_state_reset_error(struct simulation *sim, struct newton_state *ns);
int newton_state_clever_exit(struct simulation *sim, struct newton_state *ns);
int newton_state_setup_dump(struct newton_state *ns,struct device *dev);

//newton states
int newton_states_init(struct newton_states *states);
struct newton_state *newton_states_add(struct newton_states *states,char *name);
int newton_states_cpy(struct newton_states *out,struct newton_states *in);
int newton_states_free(struct newton_states *states);
struct newton_state * newton_states_find(struct newton_states *states,char* name);
int newton_states_dump(struct newton_states *states);
int newton_states_delete(struct newton_states *states,char* name);
int newton_states_get_J(struct device *dev, struct newton_states *states);

//newton state complex
void newton_state_complex_init(struct newton_state_complex *ns);
void newton_state_complex_alloc_mesh(struct newton_state_complex *ns,struct dimensions *dim);
void newton_state_complex_alloc_traps(struct newton_state_complex *ns,struct dimensions *dim);
void newton_state_complex_free(struct newton_state_complex *ns);


#endif
