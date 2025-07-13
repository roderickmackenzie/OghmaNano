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

## @package fx_selector
#  Select which wavelenght to display
#

import os
from tab import tab_class

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QSystemTrayIcon,QMenu, QComboBox, QMenuBar, QLabel
from PySide2.QtGui import QIcon

from cal_path import sim_paths
from inp import inp
from json_c import json_tree_c

class lam_file():
	def __init__(self):
		self.file_name=""
		self.lam=0.0
		self.layer=0

	def __str__(self):
		if self.file_name=="all":
			return _("All")
		else:
			return str(self.lam*1e9)+"nm "
		

class fx_selector(QWidget):

	def __init__(self,layout=QVBoxLayout()):
		QWidget.__init__(self)
		self.bin=json_tree_c()
		self.thefiles=[]
		self.dump_dir=os.path.join(sim_paths.get_sim_path(),"ray_trace")

		self.layout=layout
		label=QLabel(_("Wavelengths")+":")
		self.layout.addWidget(label)

		self.cb = QComboBox()
		self.layout.addWidget(self.cb)
		self.setLayout(self.layout)
		self.show()
		self.show_all=False

	def get_file_name(self):
		ret=[]
		txt=self.cb.currentText()
		if txt==_("All"):
			
			for f in self.thefiles:
				if str(f)!=txt:
					ret.append(os.path.join(self.dump_dir,f.file_name))
			return ret

		for f in self.thefiles:
			if str(f)==txt:
				ret.append(os.path.join(self.dump_dir,f.file_name))

		return ret

	def get_english_text(self):
		txt=self.cb.currentText()
		if txt==_("All"):
			return "all"
		else:
			for f in self.thefiles:
				if str(f)==txt:
					return os.path.basename(f.file_name)
		return ""

	def set_english_text(self,english):
		pos=None
		for i in range(0,len(self.thefiles)):
			if os.path.basename(self.thefiles[i].file_name)==english:
				pos=i
				break

		if pos!=None:
			self.cb.setCurrentIndex(pos)
	
	def find_modes(self,path):
		result = []
		lines=[]
		dump_dir=os.path.join(sim_paths.get_sim_path(),"outcoupling_snapshots_rays")
		if os.path.isdir(dump_dir)==False:
			dump_dir=os.path.join(sim_paths.get_sim_path(),"ray_trace")

		if os.path.isdir(dump_dir)==True:
			files=os.listdir(dump_dir)
			files.sort()
			if len(files)>0:
				a=lam_file()
				a.layer=0
				a.lam=0.0
				a.file_name="all"
				result.append(a)

			for f in files:
				sub_dir=os.path.join(dump_dir,f)
				if os.path.isdir(sub_dir)==True:
					json_file_name=os.path.join(sub_dir,"data.json")
					json_file=inp()
					if json_file.load_json(json_file_name)!=False:
						sub_files=os.listdir(sub_dir)
						for sf in sub_files:
							if sf.startswith("ray_"):
								try:
									a=lam_file()
									a.layer=0
									a.lam=json_file.json["wavelength"]
									a.file_name=os.path.join(sub_dir,sf)
									
									result.append(a)
									break
								except:
									pass
		return result

	def update(self):
		self.cb.blockSignals(True)

		self.thefiles=self.find_modes(self.dump_dir)

		if len(self.thefiles)==0:
			self.setEnabled(False)
		else:
			self.setEnabled(True)

		self.cb.clear()

		for i in range(0, len(self.thefiles)):
			path=os.path.join(self.dump_dir,self.thefiles[i].file_name)
			if os.path.isfile(path) or str(self.thefiles[i])==_("All"):
				self.cb.addItem(str(self.thefiles[i]))

		self.set_english_text(self.bin.get_token_value("optical.ray","rays_display"))
		
		self.cb.blockSignals(False)

