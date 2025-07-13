# -*- coding: utf-8 -*-
#
#   OghmaNano - Organic and hybrid Material Nano Simulation tool
#   Copyright (C) 2008-2022 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
#
#   https://www.oghma-nano.com
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#   SOFTWARE.
#

## @package register
#  Registration window
#

import os

from icon_lib import icon_get

from error_dlg import error_dlg

from win_lin import get_platform
from i18n import get_full_language

from threading import Thread

from const_ver import const_ver

if get_platform()=="win":
	import winreg

from i18n import get_full_language
from inp import inp
from cal_path import multiplatform_exe_command
from cal_path import sim_paths
import json
from str2bool import str2bool
from sim_name import sim_name
from bytes2str import str2bytes
from bytes2str import bytes2str
import ctypes

class lock(ctypes.Structure):
	_fields_ = [('status', ctypes.c_char * 100),
				('use_count', ctypes.c_int),
				('uid', ctypes.c_char * 100),
				('mac', ctypes.c_char * 100),
				('win_id', ctypes.c_char * 100),
				('reg_ver', ctypes.c_char * 100),
				('lver', ctypes.c_char * 10),
				('renew_date', ctypes.c_longlong),
				('loaded_ok', ctypes.c_int),
				('use_count_check_web', ctypes.c_int),
				('use_count_max', ctypes.c_int),
				('li_renew_date', ctypes.c_longlong),
				('li_expire_date', ctypes.c_longlong),
				('encode_output', ctypes.c_int),
				('li_oghma_next', ctypes.c_int),
				('locked_items', ctypes.c_char * 4000),
				('lock_simple', ctypes.c_int),
				('simple_id_tx', ctypes.c_char * 1000),
				('simple_id_ans', ctypes.c_char * 1000),
				('simple_id_file', ctypes.c_char * 1000),
				('simple_id_tx_raw', ctypes.c_char * 1000),
				('user_name', ctypes.c_char * 1000),
				('institution', ctypes.c_char * 1000),
				('machine_locked', ctypes.c_int),
				('update_available', ctypes.c_int),
				('message', ctypes.c_char * 4000),
				('time_lock', ctypes.c_int),
				('ret_val', ctypes.c_char * 400),
				('ver_when_li_fetched', ctypes.c_char * 100),
				('debug', ctypes.c_int)]

	def __init__(self):
		self.lock_enabled=True
		self.registered=False
		self.error=""
		self.open_gl_working=True
		self.ver_in_registry="ver"
		self.website="oghma-nano.com"
		self.port="/api"
		self.my_email="roderick.mackenzie@oghma-nano.com"
		self.get_help="https://www.oghma-nano.com/forum/"
		self.question="Questions? Ask on the user forum: "
		self.lib=sim_paths.get_dll_py()
		self.lib.lock_load.restype = ctypes.c_int
		self.locked={}
		self.lib.lock_init(ctypes.byref(self))
		self.load()
		ver_in_li=bytes2str(self.ver_when_li_fetched)
		ver_in_reg=bytes2str(self.ver_in_registry)
		if self.registered==True:
			if ver_in_reg.startswith(ver_in_li)==False:	#Checks if major ver is the same
				self.get_license()

	def __del__(self):
		self.lib.lock_free(ctypes.byref(self))

	def check_license(self):
		if self.lock_enabled==False:
			return None

		self.lib.lock_update_license(ctypes.byref(sim_paths),ctypes.byref(self))

	def report_bug(self,data):
		self.lib.lock_send_error_report(None,ctypes.byref(self),ctypes.c_char_p(str2bytes(data)),ctypes.c_char_p(str2bytes(const_ver()+" "+self.ver_in_registry)))

	def check_license_thread(self):
		if self.lock_enabled==False:
			return True

		p = Thread(target=self.check_license)
		p.daemon = True
		p.start()

	def register(self):
		if self.lock_enabled==False:
			return None

		if self.lib.lock_register(ctypes.byref(sim_paths),ctypes.byref(self))==-1:
			return False

		lines=bytes2str(self.ret_val)

		self.uid=str2bytes(lines)

		return True

	def html(self):
		text=""
		text=text+"UID:"+bytes2str(self.uid)+"<br>"
		return text

	def get_license(self,key="none",uid=None):
		if self.lock_enabled==False:
			return None

		if uid==None:
			uid=bytes2str(self.uid)

		self.lib.lock_get_li(ctypes.byref(sim_paths),ctypes.byref(self))
		lines=bytes2str(self.ret_val)
		if lines==False:
			return False

		if lines=="error:too_old":
			self.error="too_old"
			return False

		if lines=="error:error":
			self.error="uid_not_found"
			return False

		self.load()

		self.registered=True


		return True

	def get_uid(self):
		return bytes2str(self.uid)

	def is_next(self):
		return self.li_oghma_next


	def get_next_gui_action(self):
		if self.lock_enabled==False:
			return "ok"

		if self.registered==False:
			return "register"

		return "ok"

	def is_function_locked(self,id):
		if self.lock_enabled==False:
			return False

		for key in self.locked:
			if key==id:
				return True
		return False


	def load_new(self):
		if self.lock_enabled==False:
			return None

		if self.get_reg_key("new_install")=="true":
			print("fresh install.....")
			return False

		lines=[]
		data_path=None
		if sim_paths.get_li_path()==None:
			return False
		if sim_paths.get_li_path().endswith("settings.json"):
			data_path=sim_paths.get_li_path()
		else:
			data_path=os.path.join(sim_paths.get_user_settings_dir(),"settings3.inp")
		self.ver_in_registry=self.get_reg_key("ver")
		if self.ver_in_registry==False:
			self.ver_in_registry="8.1"	#then it is linux
		if self.lib.lock_load(ctypes.byref(self),ctypes.c_char_p(str2bytes(data_path)))==-1:
			return False
		self.registered=True
		return True

	def load(self):
		if self.lock_enabled==False:
			return None

		if self.load_new()==True:
			return

		value=self.get_reg_key("uid")
		if value!=False:
			self.uid=str2bytes(value)
		return

	def get_reg_key(self,token):
		if get_platform()=="win":
			try:
				registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\OghmaNano", 0, winreg.KEY_READ)
				value, regtype = winreg.QueryValueEx(registry_key, token)
				winreg.CloseKey(registry_key)
				return value
			except WindowsError:
				pass
		return False


	def is_trial(self):
		if bytes2str(self.status)=="no_key":
			return False

		if bytes2str(self.status)=="full_version":
			return False

		return True

	def validate_key(self,key):
		print("validate_key")
		if self.lib.lock_validate_key(ctypes.byref(sim_paths),ctypes.byref(self))==-1:
			self.error="no_internet"
			return False
		lines=bytes2str(self.ret_val)

		if lines=="ok":
			self.load()
			return True
		elif lines=="error:too_old":
			self.error="too_old"
			return False

		self.error=lines
		return False

	def lock_ping_server(self):
		p = Thread(target=self.lock_do_ping, args=(10,))
		p.daemon = True
		p.start()

	def lock_do_ping(self,n):
		self.lib.lock_ping_server(ctypes.byref(self))	

my_lock=lock()

def get_lock():
	global my_lock
	return my_lock

