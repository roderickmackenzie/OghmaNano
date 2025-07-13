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

/** @file rand_state.h
@brief generate random numbers for randomizing input files
*/



#ifndef rand_state_h
#define rand_state_h
	#define UPPER_MASK		0x80000000
	#define LOWER_MASK		0x7fffffff
	#define TEMPERING_MASK_B	0x9d2c5680
	#define TEMPERING_MASK_C	0xefc60000

	#define STATE_VECTOR_LENGTH 624
	#define STATE_VECTOR_M      397 // changes to STATE_VECTOR_LENGTH also require changes to this

	struct rand_state
	{
		//config
		int rand_function;
		int rand_seed;
		char noise_source[100];

		//mtwister
		unsigned long long mt[STATE_VECTOR_LENGTH];

		int index;
		//Box-Muller
		double n2;
		int n2_cached;
		
	};

#endif
