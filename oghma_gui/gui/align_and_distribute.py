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

## @package align_and_distribute
#  Align and distribute widget
#

#qt
from PySide2.QtWidgets import QAction
from gQtCore import QSize
from PySide2.QtWidgets import QVBoxLayout,QToolBar,QToolBar, QAction, QLabel
from QWidgetSavePos import QWidgetSavePos
from icon_lib import icon_get
from json_root import json_root

class align_and_distribute(QWidgetSavePos):
	def __init__(self,gl_interface):
		QWidgetSavePos.__init__(self,"align_and_distribute")
		self.main_vbox = QVBoxLayout()

		self.setWindowIcon(icon_get("thermal_kappa"))

		self.setWindowTitle2(_("Align and distribute")) 
		self.gl_interface=gl_interface
		toolbar_x=QToolBar()
		toolbar_x.setIconSize(QSize(48, 48))

		#spacer = QWidget()
		#spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.label_x=QLabel(_("x"))
		self.main_vbox.addWidget(self.label_x)

		self.align_left_x = QAction(icon_get("align_left"), _("Left"), self)
		toolbar_x.addAction(self.align_left_x)
		self.align_left_x.triggered.connect(self.callback_align_left_x)

		self.align_right_x = QAction(icon_get("align_right"), _("Right"), self)
		toolbar_x.addAction(self.align_right_x)
		self.align_right_x.triggered.connect(self.callback_align_right_x)

		self.main_vbox.addWidget(toolbar_x)

		############
		toolbar_y=QToolBar()
		toolbar_y.setIconSize(QSize(48, 48))

		self.label_y=QLabel(_("y"))
		self.main_vbox.addWidget(self.label_y)

		self.distribute_y = QAction(icon_get("align_left"), _("Distribute"), self)
		toolbar_y.addAction(self.distribute_y)
		self.distribute_y.triggered.connect(self.callback_align_y_min)

		self.main_vbox.addWidget(toolbar_y)

		self.setLayout(self.main_vbox)

		############
		toolbar_z=QToolBar()
		toolbar_z.setIconSize(QSize(48, 48))

		self.label_z=QLabel(_("z"))
		self.main_vbox.addWidget(self.label_z)

		self.distribute_z = QAction(icon_get("distribute_x"), _("Distribute"), self)
		toolbar_z.addAction(self.distribute_z)
		self.distribute_z.triggered.connect(self.callback_distribute_z)

		self.main_vbox.addWidget(toolbar_z)

		self.setLayout(self.main_vbox)

	def callback_align_left_x(self):
		data=json_root()
		x=[]

		objs=self.gl_interface.gl_objects_get_selected()
		for obj in objs:
			s=data.find_object_by_id(obj.id[0])
			if s!=None:
				x.append(s.x0)

		x_new=min(x)
		for obj in objs:
			s=data.find_object_by_id(obj.id[0])
			if s!=None:
				s.x0=x_new
		data.save()
		self.gl_interface.force_redraw() 

	def callback_align_y_min(self):
		data=json_root()
		y=[]

		objs=self.gl_interface.gl_objects_get_selected()
		for obj in objs:
			s=data.find_object_by_id(obj.id[0])
			if s!=None:
				y.append(s.y0)

		y_new=min(y)
		for obj in objs:
			s=data.find_object_by_id(obj.id[0])
			if s!=None:
				s.y0=y_new
		data.save()
		self.gl_interface.force_redraw() 

	def callback_align_right_x(self):
		data=json_root()
		x=[]

		objs=self.gl_interface.gl_objects_get_selected()
		for obj in objs:
			s=data.find_object_by_id(obj.id[0])
			if s!=None:
				x.append(s.x0+s.dx)

		x_new=max(x)
		for obj in objs:
			s=data.find_object_by_id(obj.id[0])
			if s!=None:
				s.x0=x_new-s.dx
		data.save()
		self.gl_interface.force_redraw() 

	def callback_distribute_z(self):
		data=json_root()
		z=[]
		objs=self.gl_interface.gl_objects_get_selected()

		for obj in objs:
			s=data.find_object_by_id(obj.id[0])
			if s!=None:
				z.append(s.z0+s.dz/2.0)

		z.sort()
		#for i in range(0,len(z)):
			
		return
		pos=s0.z0
		for obj in objs:
			s=data.find_object_by_id(obj.id[0])
			if s!=None:
				s.z0=pos
				pos=pos+dz

		#data.save()
		self.gl_interface.force_redraw() 

