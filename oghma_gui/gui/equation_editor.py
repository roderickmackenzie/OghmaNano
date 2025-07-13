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

## @package equation_editor
#  An equation editor
#

import os
import sys
from util import fx_with_units
from icon_lib import icon_get

import i18n
_ = i18n.language.gettext

#inp
from inp import inp_load_file
from inp import inp_read_next_item

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QDialog,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QTableWidget,QAbstractItemView

#windows
from open_save_dlg import save_as_filter

from error_dlg import error_dlg

#window

from help import help_window
from QWidgetSavePos import QWidgetSavePos
from gui_util import yes_no_dlg
from gQtCore import gSignal
from g_tab import g_tab
import ctypes
from bytes2str import str2bytes
from graph import graph_widget
from dat_file import dat_file

class equation_editor(QWidgetSavePos):

	data_written = gSignal()
	def save_data(self):

		out_text=[]
		out_text.append("#points")
		out_text.append(str(self.data.y_len))
		out_text.append("#equations")
		out_text.append(str(self.tab.rowCount()))

		for i in range(0,self.tab.rowCount()):
			out_text.append("#start"+str(i))
			out_text.append(str(self.tab.get_value(i, 0)))

			out_text.append("#stop"+str(i))
			out_text.append(str(self.tab.get_value(i, 1)))

			out_text.append("#equation"+str(i))
			out_text.append(str(self.tab.get_value(i, 2)))

		out_text.append("#ver")
		out_text.append("1.0")
		out_text.append("#end")
		
		dump=""
		for item in out_text:
			dump=dump+item+"\n"

		dump=dump.rstrip("\n")

		f=open(os.path.join(self.path,self.equation_file), mode='wb')
		f.write(str.encode(dump))
		f.close()


	def callback_add_section(self):

		self.tab.add(["100e-9","1000e-9",self.default_value])

		self.build_mesh()
		self.draw_graph()
		self.save_data()

	def callback_remove_item(self):
		self.tab.remove()

		self.build_mesh()

		self.draw_graph()
		self.save_data()

	def callback_move_down(self):
		self.tab.move_down()

		self.build_mesh()
		self.draw_graph()
		self.save_data()

	def callback_move_up(self):

		self.tab.move_up()

		self.build_mesh()
		self.draw_graph()
		self.save_data()

	def update(self):
		self.build_mesh()
		self.draw_graph()

	def draw_graph(self):
		self.data.cols=b"yd"
		self.data.type=b"xy"
		self.data.data_label=b"Value"
		self.data.data_units=b"au"
		self.data.y_label=b"Wavelength"
		self.data.y_units=b"nm"
		self.data.y_mul=1e9
		self.canvas2.graph.show_key=True
		self.canvas2.load([self.data])
		self.canvas2.update()

	def load_data(self):
		self.tab.clear()
		self.tab.setColumnCount(3)
		self.tab.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tab.setHorizontalHeaderLabels([_("start")+" (m)", _("stop")+" (m)", _("Python Equation")])
		self.tab.setColumnWidth(2, 400)
		lines=[]
		pos=0
		lines=inp_load_file(os.path.join(self.path,self.equation_file))
		if lines!=False:
			token,y_len,pos=inp_read_next_item(lines,pos)
			self.data.y_len=int(y_len)

			token,equations,pos=inp_read_next_item(lines,pos)
			equations=int(equations)
			self.data.y_len=int(self.data.y_len)

			self.data.init_mem()
			for i in range(0, equations):
				token,start,pos=inp_read_next_item(lines,pos)
				token,stop,pos=inp_read_next_item(lines,pos)
				token,equation,pos=inp_read_next_item(lines,pos)
				self.tab.add([str(start),str(stop),str(equation)])

	def build_mesh(self):
		data_min=100.0
		if self.tab.rowCount()!=0:
			for i in range(0,self.tab.rowCount()):
				val=float(self.tab.get_value(i, 0))
				if val<data_min:
					data_min=val

			#find max
			data_max=0.0
			for i in range(0,self.tab.rowCount()):
				val=float(self.tab.get_value(i, 1))
				if val>data_max:
					data_max=val

			w=data_min
			dx=(data_max-data_min)/(float(self.data.y_len))

			for i in range(0,self.data.y_len):
				val=0.0
				for ii in range(0,self.tab.rowCount()):
					range_min=float(self.tab.get_value(ii, 0))
					range_max=float(self.tab.get_value(ii, 1))
					command=self.tab.get_value(ii, 2)
					try:
						equ=eval(command)
					except:
						print(sys.exc_info())
						error_dlg(self,_("You've made a mistake in the equation, use w for wavelength. " + command))
						equ=-1
						return
					
					if w>=range_min and w <=range_max:
						val=val+equ
				if val<0.0:
					val=1.0
				#print(i,self.data.y_len)
				self.data.y_scaleC[i]=w
				self.data.py_data[0][0][i]=val

				w=w+dx
		#self.data.dump_info()

	def on_cell_edited(self, x,y):
		self.build_mesh()
		self.draw_graph()
		self.save_data()

	def set_default_value(self,value):
		self.default_value=value

	def set_ylabel(self,value):
		self.ylabel=value

	def callback_import(self):
		response=yes_no_dlg(self,_("Are you sure you wisht to import this, it will overwrite "))
		if response==True:
			out_file=os.path.join(self.path,self.out_file)

			self.data.save(out_file)
			self.data_written.emit()
			self.close()

	
	
	def callback_play(self):
		self.build_mesh()
		self.draw_graph()

	def load(self):
		self.data.x_len=1
		self.data.y_len=4000
		self.data.z_len=1

		self.data.y_mul=1e9

		self.canvas2.graph.lib.dat_file_malloc_py_data(ctypes.byref(self.data))

		self.load_data()
		self.build_mesh()

		self.draw_graph()

	def __del__(self):
		self.canvas2.graph.lib.dat_file_free(ctypes.byref(self.data))

	def __init__(self,path,equation_file,out_file):
		QWidgetSavePos.__init__(self,"equation_editor")

		self.data=dat_file()

		self.default_value="3.0"
		self.setMinimumSize(600,300)
		self.setWindowIcon(icon_get("vars"))
		self.setWindowTitle2(_("Equation editor"))

		self.path=path
		self.equation_file=equation_file
		self.out_file=out_file

		self.canvas2 = graph_widget()
		self.canvas2.graph.axis_y.log_scale_auto=False
		self.canvas2.graph.axis_y.log_scale=False
 
		self.canvas2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.canvas2.setMinimumSize(400, 400)

		self.main_vbox = QVBoxLayout()

		toolbar=QToolBar()
		toolbar.setIconSize(QSize(48, 48))
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)

		self.tb_ref= QAction(icon_get("import"), _("Import\ninto model"), self)
		self.tb_ref.triggered.connect(self.callback_import)
		toolbar.addAction(self.tb_ref)

		self.tb_play = QAction(icon_get("media-playback-start"), _("Calculate"), self)
		self.tb_play.triggered.connect(self.callback_play)
		toolbar.addAction(self.tb_play)

		self.main_vbox.addWidget(toolbar)


		self.main_vbox.addWidget(self.canvas2)

		#toolbar 2

		toolbar2=QToolBar()
		toolbar2.setIconSize(QSize(32, 32))

		self.tb_add = QAction(icon_get("list-add"), _("Add section"), self)
		self.tb_add.triggered.connect(self.callback_add_section)
		toolbar2.addAction(self.tb_add)

		self.tb_remove = QAction(icon_get("list-remove"), _("Delete section"), self)
		self.tb_remove.triggered.connect(self.callback_remove_item)
		toolbar2.addAction(self.tb_remove)

		self.tb_move = QAction(icon_get("go-down"), _("Move down"), self)
		self.tb_move.triggered.connect(self.callback_move_down)
		toolbar2.addAction(self.tb_move)

		self.tb_move_up = QAction(icon_get("go-up"), _("Move up"), self)
		self.tb_move_up.triggered.connect(self.callback_move_up)
		toolbar2.addAction(self.tb_move_up)

		self.main_vbox.addWidget(toolbar2)

		self.tab = g_tab()
		self.tab.resizeColumnsToContents()

		self.tab.verticalHeader().setVisible(False)

		self.main_vbox.addWidget(self.tab)

		self.setLayout(self.main_vbox)


		self.tab.cellChanged.connect(self.on_cell_edited)
