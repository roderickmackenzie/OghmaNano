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

## @package splash
#  The splash screen.
#

import os
import time
import glob

from PySide2.QtGui import QIcon, QPixmap,QFont, QImage
from gQtCore import QSize, Qt, QTimer
from PySide2.QtWidgets import QApplication,QGraphicsScene,QWidget,QGraphicsView,QLabel,QVBoxLayout,QProgressBar

#cal_path
from cal_path import get_image_file_path
import time
from sim_name import sim_name
from PIL import Image as Image
from PIL.ImageQt import ImageQt
from cal_path import sim_paths
from PIL import ImageDraw, ImageFont, ImageStat
from const_ver import const_ver

class splash_window(QLabel):

	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def callback_destroy(self):
		self.close()

	def pil2pixmap(self, im):

		if im.mode == "RGB":
			r, g, b = im.split()
			im = Image.merge("RGB", (b, g, r))
		elif  im.mode == "RGBA":
			r, g, b, a = im.split()
			im = Image.merge("RGBA", (b, g, r, a))
		elif im.mode == "L":
			im = im.convert("RGBA")

		im2 = im.convert("RGBA")
		data = im2.tobytes("raw", "RGBA")
		qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
		pixmap = QPixmap.fromImage(qim)

		return pixmap

	def __init__(self):
		QLabel.__init__(self)
		mul=1.1
		self.counts=0
		width=int(459*mul)
		self.setFixedSize(width, 260)
		self.center()
		self.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; }")
		#self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		#self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)

		self.font = QFont()
		self.font.setFamily('DejaVu Sans')
		self.font.setBold(True)
		self.font.setStyleHint(QFont.Monospace)
		self.font.setFixedPitch(True)
		

		window_h=self.height()
		window_w=self.width()

		QTimer.singleShot(2000, self.callback_destroy)

		files=glob.glob(os.path.join(get_image_file_path(),"splash","*.jpg"))
		files.extend(glob.glob(os.path.join(get_image_file_path(),"splash","*.png")))

		number=time.localtime().tm_yday

		number=number % len(files)

		if number>=len(files[number]):
			number=0

		image_file=files[number]

		fonts_path=os.path.join(sim_paths.get_fonts_path(),"Lato-Regular.ttf")
		self.font_big = ImageFont.truetype(fonts_path, 80, encoding="unic")
		self.font_small = ImageFont.truetype(fonts_path, 20, encoding="unic")
		
		image_path=os.path.join(get_image_file_path(),"splash",image_file)
		if os.path.isfile(image_path):
			scene = Image.open(image_path)
			h = self.height()
			w = int((float(h)/float(scene.size[1]))*float(scene.size[0]))
			scene = scene.resize((w,h))

			x_max=scene.size[0]-self.width()

			hour=float(time.strftime("%H"))*60
			m=float(time.strftime("%m"))
			tot=hour+m
			my_max=float(24*60)

			frac=tot/my_max

			xpos=int(x_max*frac)
			
			scene_new=scene.crop((xpos, 0, scene.size[0], scene.size[1]))
			img = Image.new('RGB', (self.width(), self.height()), (0, 0, 0))
			img.paste(scene_new, (0, 0))


			avg=ImageStat.Stat(img).median
			avg=(avg[0]+avg[1]+avg[2])/3
			color='white'
			if avg>150:
				color='black'

			draw = ImageDraw.Draw(img)
			draw.text((5, 5), sim_name.name, color, self.font_big)

			draw.text((self.width()*0.1, self.height()*0.5), "Version "+const_ver(), color, self.font_small)

			image = self.pil2pixmap(img)

			self.setPixmap(image)

		else:
			print("Image not found",image_path)

		self.pbar = QProgressBar(self)
		self.pbar.setGeometry(0, 261-20, width-5, 15)
		self.show()

	def inc_value(self):
		#print(self.counts)
		self.counts=self.counts+1
		value=int(100.0*self.counts/29.0)
		self.pbar.setValue(value)
		if value>=100.0:
			self.pbar.hide()
		QApplication.processEvents()

	def set_value(self,value):

		self.pbar.setValue(value)
		QApplication.processEvents()
		

		    




