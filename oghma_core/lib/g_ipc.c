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

/** @file g_strings.c
	@brief Dealing with utf 16 /utf 8
*/

#include <enabled_libs.h>
#include <g_io.h>
#include <ipc.h>

#ifndef pydll
	#ifdef dbus
		#include <dbus/dbus.h>
	#endif
#endif


void ipc_init(struct ipc *in)
{
	in->connection=NULL;
}

void ipc_free(struct ipc *in)
{
	ipc_init(in);
}

void ipc_send(struct ipc *in, char *tx_data)
{
	#ifndef pydll
		#ifdef dbus
			DBusMessage *message;
			message = dbus_message_new_signal ("/org/my/test","org.my.oghmanano",tx_data);
			dbus_connection_send ((DBusConnection*)in->connection, message, NULL);
			dbus_connection_flush((DBusConnection*)in->connection);
			dbus_message_unref (message);
		#endif
	#endif

}

void ipc_close(struct ipc *in)
{

	#ifndef pydll
		#ifdef dbus
		if (in->connection!=NULL)
		{
			dbus_connection_unref ((DBusConnection*)in->connection);
			//dbus_connection_close(in->connection);
		}
		dbus_shutdown();
		#endif
	#endif
}

void ipc_open(struct ipc *in)
{
	#ifndef pydll
		#ifdef dbus
			DBusError error;
			dbus_error_init (&error);
			in->connection = (void*)dbus_bus_get (DBUS_BUS_SESSION, &error);
			dbus_connection_set_exit_on_disconnect(in->connection,FALSE);
			if (!in->connection)
			{
				printf("Failed to connect to the D-BUS daemon: %s\n", error.message);
				in->connection=NULL;
				dbus_error_free (&error);
				return;
			}
		#endif
	#endif

}

void ipc_open_listen(struct ipc *in)
{
}

int ipc_read(struct ipc *in)
{
		int nRead=0;
	return (int)nRead;
}
