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

## @package shape_editor
#  The shape editor
#

import os
from tab import tab_class
from icon_lib import icon_get

#qt
from PIL import Image, ImageFilter,ImageOps, ImageDraw
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget, QDialog, QMenu
from PySide2.QtGui import QPainter,QIcon,QPixmap,QPen,QColor

#python modules

from help import help_window

from plot_widget import plot_widget
from win_lin import desktop_open

from QWidgetSavePos import QWidgetSavePos

from ribbon_shape_import import ribbon_shape_import

from open_save_dlg import open_as_filter

from dat_file import dat_file

from gQtCore import gSignal
from PIL import Image, ImageFilter,ImageOps 
from PIL.ImageQt import ImageQt
from inp import inp

from PySide2.QtWidgets import QApplication
import time
import shutil
from vec import vec

class shape_image_flat_view(QWidget):
	changed = gSignal()

	def __init__(self,path,config):
		super().__init__()
		self.path=path
		self.config=config
		self.image_in=os.path.join(self.path,"image.png")
		self.image_out=os.path.join(self.path,"image_out.png")
		self.setGeometry(30, 30, 500, 300)
		self.len_x=800e-9
		self.len_y=800e-9
		self.len_z=800e-9
		self.im=None

		self.dat_file=dat_file()
		self.load_image()

	def build_mesh(self):
		if self.im==None:
			return

		if self.config.mesh.mesh_show==True:
			width, height = self.im.size
			self.dat_file.load(os.path.join(self.path,"shape.inp"),raw_data=True)
			if self.dat_file.data!=None:
				if self.dat_file.y_len>0:
					a=vec()
					min_vec=self.dat_file.gl_triangles_get_min()
					self.dat_file.gl_triangles_sub_vec(min_vec)
					max_vec=self.dat_file.gl_triangles_get_max()
					self.dat_file.gl_triangles_div_vec(max_vec)




	def force_update(self):
		self.load_image()
		self.build_mesh()
		self.repaint()


	def load_image(self):
		#print(self.image_out)
		if os.path.isfile(self.image_out)==False:
			if os.path.isfile(self.image_in)==False:
				self.im=None
				return
			else:
				shutil.copyfile(self.image_in, self.image_out)

		img=Image.open(self.image_out)
		if img.mode!="RGB":
			img=img.convert('RGB')

		self.im = img.convert('RGB')

		self.build_mesh()

	def mouseMoveEvent(self, event):
		width, height = self.im.size
		if event.buttons()==Qt.LeftButton:
			x=int(width*event.x()/self.width())
			y=int(height*event.y()/self.height())
			drawer=ImageDraw.Draw(self.im)
			drawer.rectangle([(x, y), (x+5, y+5)], fill="black")
			self.update()

	def mouseReleaseEvent(self, event):
		self.im.save(self.image_in)

	def paintEvent(self, event):

		if self.im==None:
			return

		painter = QPainter(self)

		width, height = self.im.size
		#print(type(self.im))
		qim = ImageQt(self.im)
		pixmap = QPixmap.fromImage(qim)
		#self.im=pixmap.toImage()
		x_mul=self.height()
		z_mul=self.width()

		painter.drawPixmap(self.rect(), pixmap)
		pen = QPen(Qt.red, 3)
		painter.setPen(pen)

		if self.dat_file.valid_data==False:
			return

		if self.config.mesh.mesh_show==True:
			if self.dat_file.data==None:
				self.build_mesh()

			dat=self.dat_file.py_data[0][0]
			p=0
			if self.dat_file.data!=None:
				for i in range(0,self.dat_file.y_len):
					z0=dat[p*3]
					x0=dat[p*3+1]
					y0=dat[p*3+2]
					p=p+1

					z1=dat[p*3]
					x1=dat[p*3+1]
					y1=dat[p*3+2]
					p=p+1

					z2=dat[p*3]
					x2=dat[p*3+1]
					y2=dat[p*3+2]
					p=p+1

					painter.drawLine(z0*z_mul, x0*x_mul, z1*z_mul, x1*x_mul)
					painter.drawLine(z1*z_mul, x1*x_mul, z2*z_mul, x2*x_mul)
					painter.drawLine(z2*z_mul, x2*x_mul, z0*z_mul, x0*x_mul)


	def callback_copy(self,event):
		self.menu.close()
		time.sleep(0.1)
		QApplication.processEvents()
		screen = QApplication.primaryScreen()
		QApplication.clipboard().setImage(screen.grabWindow(self.winId()).toImage())



	def contextMenuEvent(self, event):
		self.menu = QMenu(self)

		export=self.menu.addMenu(_("Export"))

		action=export.addAction(_("Copy"))
		action.triggered.connect(self.callback_copy)
		self.menu.exec_(event.globalPos())


