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

## @package cmp_class
#  Compare simulation results window as a function of time.
#

import os
from plot_widget import plot_widget
from icon_lib import icon_get

#qt
from gQtCore import QTimer, QBuffer, QByteArray
from PySide2.QtWidgets import QWidget, QStatusBar, QVBoxLayout,QSizePolicy,QAction,QHBoxLayout,QLabel,QComboBox
from open_save_dlg import save_as_filter

from PySide2.QtWidgets import QApplication

from QWidgetSavePos import QWidgetSavePos
from cal_path import sim_paths

from PIL import Image
from PySide2.QtGui import QImage
import io
from util_latex import latex
from snapshot_slider import snapshot_slider
from json_c import json_c
from inp import inp

class cmp_class(QWidgetSavePos):

	def __init__(self,path):
		QWidgetSavePos.__init__(self,"cmpclass")
		self.title_base=_("Simulation snapshots")
		self.setWindowTitle(self.title_base) 
		self.setWindowIcon(icon_get("cover_flow"))
		self.setMinimumSize(800,800)
		self.bin=json_c("snapshots")
		self.path=path
		self.timer=QTimer()

		self.main_vbox = QVBoxLayout()

		self.slider=snapshot_slider(self.path)
		
		self.slider.changed.connect(self.update)
		force_2d3d=False

		self.bin.load(os.path.join(self.path,"data.json"))
		default_plot_type=self.bin.get_token_value("","default_plot_type")
		widget_mode="graph"
		if default_plot_type=="3d":
			force_2d3d=True
		elif default_plot_type=="trap_map":
			widget_mode="graph"
		elif default_plot_type=="circuit":
			widget_mode="circuit"


		self.plot=plot_widget(widget_mode=widget_mode,force_2d3d=force_2d3d)
		self.plot.setMinimumHeight(300)

		self.tb_save_video = QAction(icon_get("video"), _("Save\nvideo"), self)
		self.plot.plot_ribbon.plot_toolbar.addAction(self.tb_save_video)
		self.tb_save_video.triggered.connect(self.callback_save)

		self.tb_storyboard = QAction(icon_get("storyboard"), _("Storyboard\nto clipboard"), self)
		self.plot.plot_ribbon.plot_toolbar.addAction(self.tb_storyboard)
		self.tb_storyboard.triggered.connect(self.callback_storyboard)


		self.plot.plot_ribbon.plot_toolbar.addAction(self.slider.tb_play)
	
		self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.plot.canvas.graph.show_key=True
		self.main_vbox.addWidget(self.plot)

		self.slider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		self.slider.setMaximumHeight(250)
		self.main_vbox.addWidget(self.slider)
		self.status_bar=QStatusBar()
		self.status_bar.showMessage(self.path)
		self.main_vbox.addWidget(self.status_bar)

		self.setLayout(self.main_vbox)

		self.update()

	def update(self):
		files=[]
		types=[]
		key=[]
		file_names,graph_types=self.slider.get_file_names()

		for i in range(0,len(file_names)):
			f=file_names[i]
			if f!=None:
				files.append(f)
				key.append(latex().str_to_latex(os.path.basename(f)))
				types.append(graph_types[i])

		if len(files)!=0:
			self.plot.load_data(files)
			self.plot.update()

		if len(files)>0:
			f=inp()
			json_file_name=os.path.join(os.path.dirname(files[0]),"data.json")
			j=f.load_json(json_file_name)

			V=None
			try:
				V=j['voltage']
			except:
				pass
			if V!=None:
				self.setWindowTitle(self.title_base+" @ "+str(V)+"V") 
				

	def callback_video(self):
		dir_name, ext = os.path.splitext(self.video_name)

		slider=self.slider.slider0
		if os.path.isdir(dir_name)==False:
			os.mkdir(dir_name)
		print(slider.value(),slider.maximum())

		if slider.value()+1<slider.maximum():
			slider.setValue(slider.value()+1)
			self.update()
			image_name=os.path.join(dir_name,"image_"+str(slider.value())+".jpg")
			self.plot.save_image(image_name)
			self.save_file_list=self.save_file_list+image_name+"\n"

			self.timer.singleShot(500,self.callback_video)
		else:

			files_list_path=os.path.join(dir_name,"files.txt")
			f=open(files_list_path,"w")
			f.write(self.save_file_list)
			f.close()

			fmax=slider.maximum()
			fps=int(fmax/60)
			encode_line="mencoder mf://@"+files_list_path+" -mf type=jpg:fps="+str(fps)+" -o "+self.video_name+" -ovc x264"
			print(encode_line)
			os.system(encode_line)

	def save_video(self,out_file_name):
		self.save_file_list=""
		self.video_name=out_file_name
		self.timer.singleShot(500,self.callback_video)


	def callback_save(self):
		file_name=save_as_filter(self,"avi (*.avi)")
		if file_name!=None:
			self.save_video(file_name)

	def callback_storyboard(self):
		number_of_images = 4
		slider = self.slider.slider0
		step = slider.maximum() / number_of_images
		pos = 0
		buf = []

		for i in range(number_of_images):
		    slider.setValue(pos)
		    QApplication.processEvents()
		    self.update()
		    
		    pixmap = self.plot.grab()

		    byte_array = QByteArray()
		    buffer = QBuffer(byte_array)
		    buffer.open(QBuffer.WriteOnly)

		    pixmap.save(buffer, "PNG")

		    byte_io = io.BytesIO(byte_array.data())
		    buf.append(byte_io)

		    pos += step

		rows = 4
		cols = (number_of_images + rows - 1) // rows  # Proper rounding

		buf[0].seek(0)
		image = Image.open(buf[0])
		w, h = image.size

		new_im = Image.new("RGB", (w * cols, h * rows))

		x, y = 0, 0

		for i in range(len(buf)):
			buf[i].seek(0)
			image = Image.open(buf[i])
			new_im.paste(image, (x, y))

			x += w

			if x >= w * cols:
				x = 0
				y += h

		final_buf = io.BytesIO()
		new_im.save(final_buf, format="JPEG")

		qimage = QImage.fromData(final_buf.getvalue())
		QApplication.clipboard().setImage(qimage)
		final_buf.close()



	def closeEvent(self, event):
		self.slider.anim_stop()
		event.accept()


