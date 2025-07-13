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

## @package icon_lib
#  An icon cache.
#

import os
from win_lin import get_platform
from cal_path import sim_paths
from json_c import json_local_root

try:
	from gQtCore import QSize, Qt
	from PySide2.QtGui import QPainter,QIcon,QPixmap, QImage
except:
	pass


icon_db=[]

use_theme=None
class icon:
	def __init__(self):
		self.name=[]
		self.file_name=""
		self.icon16x16=None
		self.icon32x32=None
		self.icon64x64=None

class icon_data_base:
	def __init__(self):
		self.db={}
		self.load()

	def load(self):
		data=json_local_root()
		use_theme=data.get_token_value("gui_config","gui_use_icon_theme")

		path_64=os.path.join(sim_paths.get_image_file_path(),"64x64")

		for f in os.listdir(path_64):
			if f.endswith("png"):
				my_icon=icon()
				my_icon.name.append(f.split(".")[0])
				my_icon.file_name=f.split(".")[0]		#no ext
				found=False
				if get_platform()=="linux" and use_theme==True:
					image=QIcon()
					if image.hasThemeIcon(my_icon.name[0])==True:
						my_icon.icon64x64=image.fromTheme(my_icon.name[0])
						my_icon.icon32x32=my_icon.icon64x64
						my_icon.icon16x16=my_icon.icon64x64

						found=True
				if found==False:
					my_icon.icon16x16=QIcon(os.path.join(path_64,my_icon.file_name+".png"))
					my_icon.icon32x32=QIcon(os.path.join(path_64,my_icon.file_name+".png"))
					my_icon.icon64x64=QIcon(os.path.join(path_64,my_icon.file_name+".png"))

				self.db[my_icon.name[0]]=my_icon

		var_list=data.get_tokens_from_path("icon_lib")

		for name in var_list:
			value=data.get_token_value("icon_lib",name)
			for token in self.db:
				if value == self.db[token].file_name:
					self.db[token].name.append(name)


	def dump(self):
		for token in self.db:
			print(self.db[token].name,self.db[token].file_name)

	def icon_get(self,token,size=64):
		if token in self.db:
			if size==16:
				return self.db[token].icon16x16
			elif size==32:
				return self.db[token].icon32x32
			elif size==64:
				return self.db[token].icon64x64

		if size==16:
			return self.db['oghma_grey'].icon16x16
		elif size==32:
			return self.db['oghma_grey'].icon32x32
		elif size==64:
			return self.db['oghma_grey'].icon64x64

		return False


def icon_init_db():
	global icon_db
	icon_db=icon_data_base()

def icon_get_db():
	global icon_db
	return icon_db

def icon_get(token,size=64,sub_icon=None,grey_scale=False):
	global icon_db
	if sub_icon=="" or sub_icon==None:
		sub_icon=None

	if token!=".png" and token.endswith(".png")==True:
		token=token[:-4]

	icon_ret=icon_db.icon_get(token,size=size)

	if icon_ret!=False:
		if grey_scale==True:
			result = icon_ret.pixmap(QSize(size,size))
			Q_image = QPixmap.toImage(result)

			grayscale = Q_image.convertToFormat(QImage.Format_Grayscale8)
			pixmap = QPixmap.fromImage(grayscale)
			icon_ret=QIcon(pixmap.scaled(size,size))

	if sub_icon==None:
		return icon_ret

	if icon_ret!=False:
		if sub_icon!=None:
			icon1=icon_ret

			icon2=icon_db.icon_get(sub_icon)

			icon1_pixmap=icon1.pixmap(QSize(size,size))
			icon2_small = icon2.pixmap(QSize(int(size),int(size))).scaled(QSize(int(size/2),int(size/2)), Qt.KeepAspectRatio, Qt.SmoothTransformation);

			p=QPainter(icon1_pixmap)
			p.drawPixmap(int(size/2),int(size/2),icon2_small); 
			p.end()


			icon_ret=QIcon(icon1_pixmap)

		return icon_ret
	else:
		return False
