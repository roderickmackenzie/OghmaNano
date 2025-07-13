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

## @package materials_main
#  Dialog to show information about a material.
#

import os
from tab import tab_class
from icon_lib import icon_get

#qt
from gQtCore import QSize, Qt 
from PySide2.QtWidgets import QWidget,QVBoxLayout,QToolBar,QSizePolicy,QAction,QTabWidget,QDialog, QTextEdit
from PySide2.QtGui import QPainter,QIcon

from help import help_window

from win_lin import desktop_open

from ref import ref_window

from g_open import g_open

from QWidgetSavePos import QWidgetSavePos
from plot_widget import plot_widget

from ribbon_materials import ribbon_materials
from import_data_json import import_data_json
from equation_editor import equation_editor
from json_c import json_c
import webbrowser
from sim_name import sim_name
from bytes2str import str2bytes
from dat_file import dat_file
import ctypes

class materials_main(QWidgetSavePos):

	def __init__(self,path):
		QWidgetSavePos.__init__(self,"materials_main")
		self.bin=json_c("material_db")
		self.path=path
		self.setMinimumSize(900, 600)
		self.setWindowIcon(icon_get("organic_material"))

		self.setWindowTitle2(_("Material editor")+os.path.basename(self.path)) 
		

		self.main_vbox = QVBoxLayout()

		self.ribbon=ribbon_materials()
		self.ribbon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		self.ribbon.cost.triggered.connect(self.callback_cost)
		self.ribbon.import_data.clicked.connect(self.import_data)
		self.ribbon.equation.clicked.connect(self.callback_equation_editor)

		self.ribbon.tb_ref.triggered.connect(self.callback_ref)
		self.ribbon.help.triggered.connect(self.callback_help)

		self.main_vbox.addWidget(self.ribbon)

		self.notebook = QTabWidget()
		self.notebook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.notebook.setMovable(True)

		self.main_vbox.addWidget(self.notebook)
		self.disable_edits=False


		if self.path.endswith(".nk")==True:
			self.disable_edits=True
			self.data_n=dat_file()
			self.data_n.load_yd_from_csv(self.path,x_col=0, y_col=1)
			self.data_n.y_units=b"nm"
			self.data_n.y_label=b"Wavelength"
			self.data_n.data_units=b"au"
			self.data_n.data_label=b"n"

			self.data_k=dat_file()
			self.data_k.load_yd_from_csv(self.path,x_col=0, y_col=2)
			self.data_k.y_units=b"nm"
			self.data_k.y_label=b"Wavelength"
			self.data_k.data_units=b"au"
			self.data_k.data_label=b"k"

			self.n=plot_widget(enable_toolbar=False)
			self.n.show_title=False
			self.n.set_labels([_("Refractive index (n)")])
	

			self.n.load_data([self.data_n])
			self.n.do_plot()
			self.notebook.addTab(self.n,_("Refractive index"))

			self.k=plot_widget(enable_toolbar=False)
			self.k.show_title=False
			self.k.set_labels([_("k")])

			self.k.load_data([self.data_k])
			#self.k.data.append(self.data_k)
			self.k.do_plot()
			self.notebook.addTab(self.k,_("k"))
		elif self.path.endswith(".yml")==True:
			self.disable_edits=True
			self.data_n=dat_file()
			self.data_n.y_units=b"nm"
			self.data_n.y_label=b"Wavelength"
			self.data_n.data_units=b"au"
			self.data_n.data_label=b"n"
			self.data_n.y_mul=1e9

			self.data_k=dat_file()
			self.data_k.y_units=b"nm"
			self.data_k.y_label=b"Wavelength"
			self.data_k.data_units=b"m^{-1}"
			self.data_k.data_label=b"alpha"
			self.data_k.y_mul=1e9

			bib = ctypes.create_string_buffer(4000)
			self.bin.lib.material_yml_to_dat_files(ctypes.byref(self.data_n),ctypes.byref(self.data_k), bib, ctypes.c_char_p(str2bytes(self.path)))

			self.n=plot_widget(enable_toolbar=False)
			self.n.show_title=False
			self.n.set_labels([_("Refractive index (n)")])
			self.n.load_data([self.data_n])
			self.n.do_plot()
			self.notebook.addTab(self.n,_("Refractive index"))

			self.k=plot_widget(enable_toolbar=False)
			self.k.show_title=False
			self.k.set_labels([_("k")])
			self.k.load_data([self.data_k])
			self.k.do_plot()
			self.notebook.addTab(self.k,_("k"))

			self.reference_text=bib.value.decode('utf-8')
			self.ribbon.equation.setVisible(False)
			self.ribbon.import_data.setVisible(False)
		else:
			fname=os.path.join(self.path,"n.csv")
			self.n=plot_widget(enable_toolbar=False)
			self.n.show_title=False
			self.n.set_labels([_("Refractive index")])
			self.n.load_data([fname])
			self.n.do_plot()
			self.notebook.addTab(self.n,_("Refractive index"))

			fname=os.path.join(self.path,"alpha.csv")
			self.alpha=plot_widget(enable_toolbar=False)
			self.alpha.show_title=False
			self.alpha.set_labels([_("Absorption")])
			self.alpha.load_data([fname])

			self.alpha.do_plot()
			self.notebook.addTab(self.alpha,_("Absorption"))

			fname=os.path.join(self.path,"emission.csv")

			self.emission=plot_widget(enable_toolbar=False)
			self.emission.show_title=False
			self.emission.set_labels([_("Emission")])
			self.emission.load_data([fname])
			self.emission.do_plot()
			self.notebook.addTab(self.emission,_("Emission"))

			#Set up import
			mat_file=os.path.join(self.path,"data.json")
			self.bin.load(mat_file)
			self.bin.set_token_value("n_import","data_file","n.csv")
			self.bin.set_token_value("alpha_import","data_file","alpha.csv")
			self.bin.set_token_value("emission_import","data_file","emission.csv")

			tab=tab_class("",data=self.bin)
			self.notebook.addTab(tab,_("Basic"))
			tab.changed.connect(self.callback_edit)

			tab=tab_class("electrical_constants",data=self.bin)
			self.notebook.addTab(tab,_("Electrical parameters"))
			tab.changed.connect(self.callback_edit)

			tab=tab_class("thermal_constants",data=self.bin)
			self.notebook.addTab(tab,_("Thermal parameters"))
			tab.changed.connect(self.callback_edit)

			tab=tab_class("lca",data=self.bin)
			self.notebook.addTab(tab,_("Life cycle"))
			tab.changed.connect(self.callback_edit)


		self.setLayout(self.main_vbox)
		self.ribbon.cost.setVisible(False)
		self.notebook.currentChanged.connect(self.changed_click)
		self.changed_click()

	def __del__(self):
		self.bin.free()

	def changed_click(self):
		if self.path.endswith("yml"):
			self.ribbon.import_data.setEnabled(False)
			self.ribbon.equation.setEnabled(False)
			self.ribbon.tb_ref.setEnabled(True)
			return

		enalbe_import_buttons=False

		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Electrical parameters"):
			help_window().help_set_help("tab.png",_("<big><b>Electrical parameters</b></big><br>Use this tab to configure the electrical parameters for the material."))
		elif self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Absorption"):
			a=json_c("file_defined")
			if a.load(os.path.join(self.path,"mat.bib"))==False:
				return

			text=a.bib_cite("alpha")
			a.free()
			if text!=None:
				help_window().help_set_help("alpha.png",_("<big><b>Absorption</b></big><br>"+text))
			
			enalbe_import_buttons=True
		elif self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Refractive index"):
			a=json_c("file_defined")
			if a.load(os.path.join(self.path,"mat.bib"))==False:
				return
			a.json_py_bib_enforce_citation("n")
			text=a.bib_cite("n")
			a.free()
			if text!=None:
				help_window().help_set_help("n.png",_("<big><b>Refractive index</b></big><br>"+text))
			
			enalbe_import_buttons=True
		elif self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Emission"):
			a=json_c("file_defined")
			if a.load(os.path.join(self.path,"mat.bib"))==False:
				return

			text=a.bib_cite("emission")
			a.free()
			if text!=None:
				help_window().help_set_help("n.png",_("<big><b>Emission spectrum</b></big><br>"+text))

			enalbe_import_buttons=True

		if enalbe_import_buttons==True and self.disable_edits==False:
			self.ribbon.import_data.setEnabled(True)
			self.ribbon.equation.setEnabled(True)
			self.ribbon.tb_ref.setEnabled(True)
		else:
			self.ribbon.import_data.setEnabled(False)
			self.ribbon.equation.setEnabled(False)
			self.ribbon.tb_ref.setEnabled(False)

		if self.disable_edits==True:
			self.ribbon.cost.setEnabled(False)

	def callback_cost(self):
		desktop_open(os.path.join(self.path,"cost.xlsx"))


	def callback_equation_editor(self):
		equation_file=None
		file_name=None
		data_label=""
		data_units=""
		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Absorption"):
			file_name="alpha.csv"
			equation_file="alpha_eq.inp"
			data_label="Absorption"
			data_units="m^{-1}"

		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Refractive index"):
			file_name="n.csv"
			equation_file="n_eq.inp"
			data_label="n"
			data_units="au"

		if file_name!=None:
			os.path.join(self.path,file_name)
			os.path.join(self.path,file_name+"import.inp")

			self.equation_editor=equation_editor(self.path,equation_file,file_name)
			self.equation_editor.data_written.connect(self.update)

			self.equation_editor.data.y_label=b"Wavelength"
			self.equation_editor.data.data_label=str2bytes(data_label)

			self.equation_editor.data.y_units=b"nm"
			self.equation_editor.data.data_units=str2bytes(data_units)
			self.equation_editor.load()

			self.equation_editor.show()

	def import_data(self):
		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Absorption"):
			self.im=import_data_json(self.bin,"alpha_import",export_path=self.path)
			self.im.run()
			self.update()
			self.bin.save()

		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Refractive index"):
			self.im=import_data_json(self.bin,"n_import",export_path=self.path)
			self.im.run()
			self.update()
			self.bin.save()

	def update(self):
		self.n.update()
		self.alpha.update()

	def callback_ref(self):
		if self.path.endswith(".yml"):
			self.ref_window=ref_window(None,None,simple_text=self.reference_text)
			self.ref_window.show()
			return
		token=None
		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Absorption"):
			token="alpha"

		if self.notebook.tabText(self.notebook.currentIndex()).strip()==_("Refractive index"):
			token="n"

		if token!=None:
			#print("path=",os.path.join(self.path,"mat.bib"))
			self.ref_window=ref_window(os.path.join(self.path,"mat.bib"),token)
			self.ref_window.show()

	def callback_dir_open(self):
		dialog=g_open(self.path)
		ret=dialog.exec_()

		if ret==QDialog.Accepted:
			desktop_open(dialog.get_filename())

	def callback_help(self):
		webbrowser.open(+"/docs.html")

	def callback_edit(self):
		self.bin.save()

