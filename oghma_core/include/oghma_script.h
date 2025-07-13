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

/** @file oghma_script.h
@brief RPN functions which oghma can handle.
*/

#ifndef oghma_script_h
#define oghma_script_h
#include <g_io.h>
#include <json.h>
#include <device.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

typedef struct {
    int step_z, step_x, step_y;
    int solve_pos_x, solve_pos_y, solve_pos_z;
    int solve_je_y, solve_jh_y;
    int solve_je_x, solve_jh_x;
    int solve_je_z, solve_jh_z;
    int solve_srh_e, solve_srh_h;
    int solve_nion;
	int verbose;
} dd_solver;

int script_load_from_json(lua_State *L, struct json_obj *obj, struct simulation *sim, struct device *dev);
int lua_dd_solver(lua_State *L);
int lua_dd_solver_run(lua_State *L);
int lua_dd_solver_set(lua_State *L);
int script_register(lua_State *L, struct simulation *sim, struct device *dev);
void store_pointer(lua_State *L, void *ptr, const char *key);
void *get_stored_pointer(lua_State *L, const char *key);
void register_dd_solver(lua_State *L);
int lua_dd_solver_set_newton_state(lua_State *L);

#endif
