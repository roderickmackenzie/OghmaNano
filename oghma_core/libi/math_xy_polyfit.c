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

/** @file i.c
	@brief Simple functions to read in scientific data from text files and perform simple maths on the data.
*/
#define _FILE_OFFSET_BITS 64
#define _LARGEFILE_SOURCE
#include <enabled_libs.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sim_struct.h>
#include <math_xy.h>
#include "util.h"
#include "cal_path.h"
#include "oghma_const.h"
#include <log.h>
#include <memory.h>
#include <g_io.h>
#include <math_kern_1d.h>


int math_xy_polyfit(struct math_xy *in, int degree, double *coeffs)
{
    int i, j, k;
	double *x=in->x;
	double *y=in->data;
	int n_points=in->len;

    double **A = (double **)malloc((degree + 1) * sizeof(double *));
    double *B = (double *)malloc((degree + 1) * sizeof(double));

    for (i = 0; i <= degree; i++)
	{
        A[i] = (double *)malloc((degree + 1) * sizeof(double));
        for (j = 0; j <= degree; j++)
		{
            A[i][j] = 0.0;
        }
        B[i] = 0.0;
    }

    // Fill the normal equations
    for (i = 0; i < n_points; i++)
	{
        double *x_powers = (double *)malloc((2 * degree + 1) * sizeof(double));
        x_powers[0] = 1.0;
        for (j = 1; j <= 2 * degree; j++)
		{
            x_powers[j] = x_powers[j - 1] * x[i];
        }

        for (j = 0; j <= degree; j++)
		{
            for (k = 0; k <= degree; k++)
			{
                A[j][k] += x_powers[j + k];
            }
            B[j] += y[i] * x_powers[j];
        }

        free(x_powers);
    }

    // Solve the linear system A * coeffs = B using Gaussian elimination
    for (i = 0; i <= degree; i++)
	{
        // Partial pivoting for numerical stability
        int max_row = i;
        for (j = i + 1; j <= degree; j++)
		{
            if (fabs(A[j][i]) > fabs(A[max_row][i]))
			{
                max_row = j;
            }
        }

        // Swap rows if needed
        if (max_row != i)
		{
            double *temp_row = A[i];
            A[i] = A[max_row];
            A[max_row] = temp_row;
            double temp_val = B[i];
            B[i] = B[max_row];
            B[max_row] = temp_val;
        }

        // Eliminate below
        for (j = i + 1; j <= degree; j++)
		{
            double factor = A[j][i] / A[i][i];
            for (k = i; k <= degree; k++)
			{
                A[j][k] -= factor * A[i][k];
            }
            B[j] -= factor * B[i];
        }
    }

    // Back substitution
    for (i = degree; i >= 0; i--)	
	{
        coeffs[i] = B[i];
        for (j = i + 1; j <= degree; j++) {
            coeffs[i] -= A[i][j] * coeffs[j];
        }
        coeffs[i] /= A[i][i];
    }

    // Free memory
    for (i = 0; i <= degree; i++)
	{
        free(A[i]);
    }

    free(A);
    free(B);

	return 0;
}
