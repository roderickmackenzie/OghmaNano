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

/** @file zip_buffer.c
	@brief Writing and reading zip buffer
*/
#include <enabled_libs.h>

#include <stdio.h>
#include <stdlib.h>

	#include <zlib.h>

#include <code_ctrl.h>
#include <sim.h>
#include <inp.h>
#include <util.h>
#include <dat_file.h>
#include <epitaxy.h>
#include <lang.h>
#include "dump.h"
#include "log.h"
#include "cal_path.h"
#include <g_io.h>

int write_zip_buffer(struct simulation *sim,char *outfile,gdouble *buf,int buf_len)
{
	//#ifndef windows
	//	gzFile file;
	//	file = gzopen (outfile, "w9b");
	//	gzwrite (file, (char*)buf, buf_len*sizeof(gdouble));
	//	gzclose (file);
	//#else
		FILE* file;
		file = g_fopen (outfile, "wb");
		if (file==NULL)
		{
			return -1;
		}
		fwrite ( (char*)buf, buf_len*sizeof(gdouble),1,file);
		fclose (file);
	//#endif
	FILE * file_append;
	file_append = g_fopen (outfile, "ab");
	if (file_append==NULL)
	{
		return -1;
	}
	int temp1=buf_len*sizeof(gdouble);
	fwrite ((char*)&temp1, sizeof(int),1,file_append);
	fclose (file_append);

	//out = g_fopen(outfile, "wb");
	//fwrite((char*)buf, buf_len*sizeof(gdouble), 1, out);
	//fclose(out);

	return 0;
}


int read_zip_buffer(struct simulation *sim,char *file_name,gdouble **buf)
{
	int len;

	FILE *tl=g_fopen(file_name,"rb");
	if (tl==NULL)
	{
		return -1;
	}

	fseek(tl, -4, SEEK_END);
	if (fread((char*)&len, 4, 1, tl)==0)
	{
		return -1;
	}

	fclose(tl);

	//#ifndef windows
	//	gzFile file_in;
	//	file_in = gzopen (file_name, "rb");
	//	if (file_in==Z_NULL)
	//	{
	//		ewe(sim,_("File not found\n"));
	//	}
	//#else
		FILE *file_in;
		file_in = g_fopen (file_name, "rb");
		if (file_in==NULL)
		{
			ewe(sim,_("File not found\n"));
		}
	//#endif



	int buf_len=len/sizeof(gdouble);

	(*buf)=(gdouble *)malloc(sizeof(gdouble)*buf_len);


	//#ifndef windows
	//	gzread (file_in, (char*)(*buf), len);
	//	gzclose(file_in);
	//#else
		fread((char*)(*buf), len, 1, file_in);
		fclose(file_in);
	//#endif

	return buf_len;
}


