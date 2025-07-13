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

/** @file sim_struct.h
@brief define the sim structure, the sim structure is used to keep all simulation parameters which are physicaly part of the device. Such as dll locations.
*/


#ifndef ipc_h
#define ipc_h

#include <oghma_const.h>
#include <stdio.h>
#include <string.h>

#define usetpc

#ifndef usetpc
		#include <dbus/dbus.h>
#else
		#include <sys/types.h>
		#include <sys/socket.h>
		#include <netinet/in.h>
		#include <unistd.h>
		#include <fcntl.h>

#endif

struct ipc_client
{
	oghma_socket fd;
	char buf[OGHMA_PATH_MAX];
	int pos;
};

struct ipc
{
	void *connection;
	char buf[STR_MAX];
	oghma_socket sock;
	struct ipc_client *clients;
	int nclients;
	int port;
};

//ipc
void ipc_init(struct ipc *in);
void ipc_malloc(struct ipc *in);
void ipc_free(struct ipc *in);
void ipc_send(struct ipc *in, char *tx_data);
void ipc_open(struct ipc *in);
int ipc_open_listen(struct ipc *in);
int ipc_read(struct ipc *in);
int ipc_win_pipe_listen_open(struct ipc *in);
#endif

