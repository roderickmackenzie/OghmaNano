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

/** @file gui_hooks.c
	@brief Handle GUI communcation dbus for Linux and pipes for windows.
*/



#define _DEFAULT_SOURCE
#include <enabled_libs.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <gui_hooks.h>
#include <util.h>
#include <oghma_const.h>
#include <log.h>
#include <string.h>
#include <cal_path.h>
#include <g_io.h>
#include <ipc.h>

struct timeval my_last_time;

void gui_send_finished_to_gui(struct simulation *sim)
{
	if (sim->gui==FALSE)
	{
		return;
	}

	//printf_log(sim,"finished signal=%s\n",sim->server.dbus_finish_signal);
	if (strcmp(sim->server.dbus_finish_signal,"")!=0)
	{
		gui_send_data(sim,gui_main,sim->server.dbus_finish_signal);
	}

	gui_close_pipe(sim);

}

void poll_gui(struct simulation *sim)
{
	if (sim->gui==FALSE)
	{
		return;
	}

char temp[PATH_MAX];
FILE *in;
char line[200];
strcpy(temp,"");
strcpy(line,"");
join_path(2,temp,sim->root_simulation_path,"tx.dat");
//printf("checking for tx from %s\n",temp);
if (isfile(temp)==0)
{
	in=g_fopen(temp,"r");
	if (in==NULL)
	{
		return;
	}
	fscanf(in,"%s",line);
	fclose(in);

	//printf("read from gui:%s\n", line);
	if (strcmp(line,"terminate")==0)
	{
		printf("terminate!!!");
		ewe(sim,"User terminated");
	}
}
//else
//{
//	printf("no file\n");
//}


}

void gui_terminal_reset(struct simulation *sim)
{
	if (sim->gui==TRUE)
	{
		printf_log(sim,"<clear_terminal>\n");
	}
}


int gui_send_data (struct simulation *sim,int from,char *tx_data_in)
{
	char tx_data[1024];
	char temp[1024];
	int ret;

	if (sim->gui==FALSE)
	{
		return 0;
	}

	if (sim->fitting>FIT_NOT_FITTING)
	{
		if (from==gui_sub)
		{
			return 0;
		}
	}
	if (sim->mindbustx==TRUE)
	{
		if ((strcmp_begin(tx_data_in,"pulse")==0)||(strcmp_begin(tx_data_in,"text")==0)||(strcmp_begin(tx_data_in,"percent")==0))
		{
			return 0;
		}
	}

	if ((strcmp_begin(tx_data_in,"pulse")==0)||(strcmp_begin(tx_data_in,"percent")==0))
	{
		struct timeval mytime;
		struct timeval result;

		gettimeofday (&mytime, NULL);

		timersub(&mytime,&my_last_time,&result);
		double diff=(double)result.tv_sec + ((double)result.tv_usec)/1000000.0;

		//printf("no %ld %ld %lf\n",(long)my_last_time.tv_sec,(long)my_last_time.tv_usec,diff);
		if (diff<0.15)
		{
			//printf("return\n");
			return 0;
		}

		gettimeofday (&my_last_time, NULL);
		//printf("reset\n");

	}


		string_to_hex(temp,tx_data_in);
		ret=snprintf(tx_data,1024,"hex%s",temp);
		if (ret<0)
		{
			ewe(sim,"tx_data error\n");
		}


			ipc_send(&(sim->ipc),tx_data);


return 0;
}

int dbus_init()
{
my_last_time.tv_sec=0;
my_last_time.tv_usec=0;
return 0;
}

void gui_close_pipe(struct simulation *sim)
{
	if (sim->gui==FALSE)
	{
		return;
	}
//DWORD numBytesRead = 0;
//DWORD lpTotalBytesAvail = 0;
//LPDWORD lpBytesLeftThisMessage =0;
//char tx_data[1000];
//int i=0;
/*for (i=0;i<10;i++)
{
	PeekNamedPipe((HANDLE)ipc->connection,(LPVOID)tx_data, 1000 * sizeof(char), &numBytesRead,  &lpTotalBytesAvail, lpBytesLeftThisMessage);
	if (numBytesRead==0)
	{
		break;
	}
//	printf_log(sim,"bytes left %lu %lu %lu",numBytesRead,lpTotalBytesAvail,lpBytesLeftThisMessage);
	sleep(1);
}*/
	//printf_log(sim,"I am going to wait 10 seconds\n");
	//sleep(3);
	//printf_log(sim,"Done waiting\n");

		ipc_close(&(sim->ipc));


}

void gui_start(struct simulation *sim)
{
	if (sim->gui==FALSE)
	{
		return;
	}

	gettimeofday (&my_last_time, NULL);


		ipc_open(&(sim->ipc));


	gui_send_data(sim,gui_main,"start");
}
