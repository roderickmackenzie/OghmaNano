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

## @package shape_bildverarbeitung
#  The shape editor
#

import os
from tab import tab_class
from icon_lib import icon_get

#qt
from PIL import Image, ImageFilter,ImageOps, ImageDraw
from gQtCore import QSize, Qt
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget, QDialog, QMenu
from PySide2.QtGui import QPainter,QIcon,QPixmap,QPen,QColor,QImage

#python modules

from help import help_window

from gQtCore import gSignal
from PIL import Image, ImageFilter,ImageOps 

class shape_bildverarbeitung():

	def __init__(self,path,json_bin_obj):
		super().__init__()
		self.path=path
		self.bin=json_bin_obj
		self.image_in=os.path.join(self.path,"image.png")
		self.image_out=os.path.join(self.path,"image_out.png")

	def apply_boundary(self,im):
		boundary_enabled=self.bin.get_token_value("boundary","boundary_enabled")
		if boundary_enabled==True:
			x0=self.bin.get_token_value("boundary","image_boundary_x0")
			color=self.bin.get_token_value("boundary","image_boundary_x0_color")
			r,g,b,alpha=color.split(",")
			x0_r=int(float(r)*255)
			x0_g=int(float(g)*255)
			x0_b=int(float(b)*255)

			x1=self.bin.get_token_value("boundary","image_boundary_x1")
			color=self.bin.get_token_value("boundary","image_boundary_x1_color")
			r,g,b,alpha=color.split(",")
			x1_r=int(float(r)*255)
			x1_g=int(float(g)*255)
			x1_b=int(float(b)*255)

			y0=self.bin.get_token_value("boundary","image_boundary_y0")
			color=self.bin.get_token_value("boundary","image_boundary_y0_color")
			r,g,b,alpha=color.split(",")
			y0_r=int(float(r)*255)
			y0_g=int(float(g)*255)
			y0_b=int(float(b)*255)

			y1=self.bin.get_token_value("boundary","image_boundary_y1")
			color=self.bin.get_token_value("boundary","image_boundary_y1_color")
			r,g,b,alpha=color.split(",")
			y1_r=int(float(r)*255)
			y1_g=int(float(g)*255)
			y1_b=int(float(b)*255)

			w, h = im.size
			dr=ImageDraw.Draw(im)
			dr.rectangle([(0, 0), (x0, h)], fill=(x0_r,x0_g,x0_b))
			dr.rectangle([(w-x1, 0), (w, h)], fill=(x1_r,x1_g,x1_b))

			if y0!=0:
				dr.rectangle([(0, 0), (w, y0)], fill=(y0_r,y0_g,y0_b))

			if y1!=0:
				dr.rectangle([(0, h-y1), (w, h)], fill=(y1_r,y1_g,y1_b))

		return im

	def apply_blur(self,im):
		shape_import_blur_enabled=self.bin.get_token_value("blur","shape_import_blur_enabled")
		shape_import_blur=self.bin.get_token_value("blur","shape_import_blur")
		if shape_import_blur_enabled==True:
			im = im.filter(ImageFilter.GaussianBlur(radius = shape_import_blur))
		return im

	def apply_rotate(self,im):
		shape_import_rotate=self.bin.get_token_value("import_config","shape_import_rotate")
		rotate=shape_import_rotate
		if rotate!=0:
			im=im.rotate(360-rotate)
		return im

	def norm_y(self,im):
		shape_import_y_norm=self.bin.get_token_value("import_config","shape_import_y_norm")
		shape_import_y_norm_percent=self.bin.get_token_value("import_config","shape_import_y_norm_percent")
		if shape_import_y_norm==True:
			print(shape_import_y_norm_percent,im.mode)
			im=ImageOps.autocontrast(im, cutoff=shape_import_y_norm_percent, ignore=None)
		return im

	def threshold(self,im):
		threshold_enabled=self.bin.get_token_value("threshold","threshold_enabled")
		if threshold_enabled==True:
			threshold_value=self.bin.get_token_value("threshold","threshold_value")
			fn = lambda x : 255 if x > threshold_value else 0
			im = im.convert('L').point(fn, mode='1')
			im = im.convert('RGB')

		return im

	def apply(self,im):
		im.save(self.image_in)
		im=self.norm_y(im)
		im=self.apply_blur(im)
		im=self.apply_rotate(im)
		im=self.threshold(im)
		im=self.apply_boundary(im)
		im.save(self.image_out)



	def this_was_z_norm(self):
		if os.path.isfile(self.image_in)==False:
			self.im=None
			return

		img=Image.open(self.image_in)
		if img.mode!="RGB":
			img=img.convert('RGB')

		self.y_norm=self.bin.get_token_value("","shape_import_y_norm")
		self.z_norm=self.bin.get_token_value("","shape_import_z_norm")
		self.y_norm_percent=self.bin.get_token_value("import_config","shape_import_y_norm_percent")

		if self.z_norm==True:
			img2 = img.resize((1, 1))
			color = img2.getpixel((0, 0))
			avg_pixel=(color[0]+color[1]+color[2])/3
			width, height = img.size
			for z in range(0,height):
				x_avg=0
				for x in range(0,width):
					color=img.getpixel((x, z))
					c=(color[0]+color[1]+color[2])/3
					x_avg=x_avg+c
				x_avg=x_avg/width
				delta=avg_pixel-x_avg
				for x in range(0,width):
					color=img.getpixel((x, z))
					c=(color[0]+color[1]+color[2])/3
					img.putpixel((x,z),(int(c+delta),int(c+delta),int(c+delta)))


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

#I got chat gpt to rewrite this without ImageQt from PIL
def paintEvent(self, event):
	painter = QPainter(self)

	if self.im is None:
		return

	# Convert PIL image to RGBA and then to raw bytes
	pil_im = self.im.convert("RGBA")
	width, height = pil_im.size
	data = pil_im.tobytes("raw", "RGBA")

	# Create QImage from raw data
	qimage = QImage(data, width, height, QImage.Format_RGBA8888)
	pixmap = QPixmap.fromImage(qimage)

	x_mul = self.height()
	z_mul = self.width()

	# Draw the image
	painter.drawPixmap(self.rect(), pixmap)

	# Set up red pen
	pen = QPen(Qt.red, 3)
	painter.setPen(pen)

	# Optional mesh overlay
	if self.show_mesh and self.dat_file.data is not None:
		for t in self.dat_file.data:
			painter.drawLine(t.xyz0.z * z_mul, t.xyz0.x * x_mul, t.xyz1.z * z_mul, t.xyz1.x * x_mul)
			painter.drawLine(t.xyz1.z * z_mul, t.xyz1.x * x_mul, t.xyz2.z * z_mul, t.xyz2.x * x_mul)
			painter.drawLine(t.xyz2.z * z_mul, t.xyz2.x * x_mul, t.xyz0.z * z_mul, t.xyz0.x * x_mul)



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


