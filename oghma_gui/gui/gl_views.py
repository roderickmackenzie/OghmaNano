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

## @package gl_views
#  The gl_views class for the OpenGL display.
#

import os
from gQtCore import QTimer
import ctypes
from bytes2str import str2bytes,bytes2str

class gl_views():

	def __init__(self):
		self.timer_save_files=False
		self.timer_save_files_number=0
		self.timer_end_callback=None
		self.enable_views(["3d"])

	def enable_views(self,names,by_hash=False):
		self.lib.gl_views_disable_all(ctypes.byref(self.gl_main))
		for name in names:
			if by_hash==False:
				self.lib.gl_views_enable_by_name(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes(name)))
			else:
				self.lib.gl_views_enable_by_hash(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes(name)))
			
	def view_move_to_xy(self):
		if self.lib.gl_views_is_view(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes("3d")))==0:
			self.enable_views(["3d"])

		if self.lib.gl_views_count_enabled(ctypes.byref(self.gl_main))!=1:
			return

		self.build_scene()
		self.lib.gl_view_set_xy(ctypes.byref(self.gl_main.view_target))
		self.timer=QTimer()
		self.timer.timeout.connect(self.ftimer_target)
		self.timer.start(25)

	def view_move_to_yz(self):
		if self.lib.gl_views_is_view(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes("3d")))==0:
			self.enable_views(["3d"])

		if self.lib.gl_views_count_enabled(ctypes.byref(self.gl_main))!=1:
			return

		self.build_scene()
		self.lib.gl_view_set_yz(ctypes.byref(self.gl_main.view_target))
		self.timer=QTimer()
		self.timer.timeout.connect(self.ftimer_target)
		self.timer.start(25)

	def view_move_to_xz(self):
		if self.lib.gl_views_is_view(ctypes.byref(self.gl_main),ctypes.c_char_p(str2bytes("3d")))==0:
			self.enable_views(["3d"])

		if self.lib.gl_views_count_enabled(ctypes.byref(self.gl_main))!=1:
			return

		self.build_scene()
		self.lib.gl_view_set_xz(ctypes.byref(self.gl_main.view_target))
		self.timer=QTimer()
		self.timer.timeout.connect(self.ftimer_target)
		self.timer.start(25)

	def view_move_to_orthographic(self):
		self.enable_views(["3d_small_0_0","3d_small_0_1","3d_small_1_0","3d_small_1_1"])
		self.bin.save()
		self.force_redraw()

	def my_timer(self):
		self.lib.gl_view_rotate_all(ctypes.byref(self.gl_main))
		self.update()

	def ftimer_target(self):
		if self.lib.gl_views_move_all_to_target(ctypes.byref(self.gl_main))==0:
			self.timer.stop()
			if self.timer_end_callback!=None:
				self.timer_end_callback()

		self.update()
		if self.timer_save_files==True:
			if os.path.isdir("flyby")==False:
				os.mkdir("flyby")

			self.grabFrameBuffer().save(os.path.join("flyby",str(self.timer_save_files_number)+".jpg"))
			self.timer_save_files_number=self.timer_save_files_number+1

	def fzoom_timer(self):
		if self.lib.gl_views_zoom(ctypes.byref(self.gl_main))==-1:
			self.timer.stop()
		self.update()

	def start_rotate(self):
		self.timer=QTimer()
		self.timer.timeout.connect(self.my_timer)
		self.timer.start(25)

	def view_dump(self):
		self.lib.gl_views_dump(ctypes.byref(self.gl_main))


