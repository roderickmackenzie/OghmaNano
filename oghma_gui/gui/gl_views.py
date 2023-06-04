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

from gQtCore import QTimer
from json_gl import json_gl_view
from json_root import json_root
import ctypes

class gl_views():

	def __init__(self):


		self.viewtarget=json_gl_view()

		self.viewtarget.xRot=0.0
		self.viewtarget.yRot=0.0
		self.viewtarget.zRot=0.0
		self.viewtarget.x_pos=-2.0
		self.viewtarget.y_pos=-1.7
		self.viewtarget.zoom=-8.0

		self.timer_save_files=False
		self.timer_save_files_number=0
		self.timer_end_callback=None
		self.enabled_veiws=["3d"]
		self.find_active_view()


	def enable_views(self,views):
		self.enabled_veiws=[]
		for v in views:
			self.enabled_veiws.append(v)
		self.find_active_view()

	def find_active_view(self):
		for v in json_root().gl.views.segments:
			if v.name in self.enabled_veiws:
				self.active_view=v
				self.gl_main.active_view=ctypes.addressof(v)

	def view_move_to_xy(self):
		self.enable_views(["3d"])
		self.rebuild_scene()
		self.viewtarget.set_xy()
		self.timer=QTimer()
		self.timer.timeout.connect(self.ftimer_target)
		self.timer.start(25)

	def view_move_to_yz(self):
		self.enable_views(["3d"])
		self.rebuild_scene()
		self.viewtarget.set_yz()
		self.timer=QTimer()
		self.timer.timeout.connect(self.ftimer_target)
		self.timer.start(25)

	def view_move_to_xz(self):
		self.enable_views(["3d"])
		self.rebuild_scene()
		self.viewtarget.set_xz()
		self.timer=QTimer()
		self.timer.timeout.connect(self.ftimer_target)
		self.timer.start(25)

	def view_move_to_orthographic(self):
		self.enable_views(["3d_small","xy","xz","yz"])
		self.rebuild_scene()
		json_root().save()
		self.force_redraw()

	def view_push(self):
		self.stored_views=[]
		for v in json_root().gl.views.segments:
			self.stored_views.append(v)

	def view_pop(self):
		json_root().gl.views.segments=[]
		for v in json_root().gl.views.segments:
			self.view.append(v)
		
	def my_timer(self):
		#self.xRot =self.xRot + 2
		for v in json_root().gl.views.segments:
			v.yRot =v.yRot + 2
		#self.zRot =self.zRot + 5
		
		self.update()


	def ftimer_target(self):
		stopped=0
		for v in json_root().gl.views.segments:
			stop=v.shift(self.viewtarget)
			if stop==True:
				stopped=stopped+1

			self.update()
			if self.timer_save_files==True:
				if os.path.isdir("flyby")==False:
					os.mkdir("flyby")

				self.grabFrameBuffer().save(os.path.join("flyby",str(self.timer_save_files_number)+".jpg"))
				self.timer_save_files_number=self.timer_save_files_number+1

			if stopped==len(json_root().gl.views.segments):
				self.timer.stop()
				if self.timer_end_callback!=None:
					self.timer_end_callback()

	def view_count_enabled(self):
		enabled=0
		for v in json_root().gl.views.segments:
			if v.enabled==True:
				enabled=enabled+1

		return enabled

	def fzoom_timer(self):
		for v in json_root().gl.views.segments:
			v.zoom =v.zoom+4.0
			if v.zoom>16.0:
				self.timer.stop()
			self.update()

	def start_rotate(self):
		self.timer=QTimer()
		self.timer.timeout.connect(self.my_timer)
		self.timer.start(50)


	def view_dump(self):
		for v in json_root().gl.views.segments:
			print("xRot=",v.xRot)
			print("yRot=",v.yRot)
			print("zRot=",v.zRot)
			print("x_pos=",v.x_pos)
			print("y_pos=",v.y_pos)
			print("zoom=",v.zoom)

