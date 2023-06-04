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

## @package open_save_dlg
#  Open and save dlgs 
#


import os

try:
	from PySide2.QtWidgets import QTextEdit, QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout,QPushButton
	from PySide2.QtGui import QPixmap, QIcon
	from gQtCore import QSize, Qt, QTimer, QDir
	from QComboBoxLang import QComboBoxLang
except:
	pass

from cal_path import to_native_path

def save_as_simfile(parent,directory = QDir.homePath()):
	dialog = QFileDialog(parent,directory =directory)
	dialog.setWindowTitle(_("Save a the simulation as"))
	dialog.setNameFilter(_("Directory"))
	dialog.setAcceptMode(QFileDialog.AcceptSave)
	dialog.setOption(QFileDialog.ShowDirsOnly, True) 
	if dialog.exec_() == QDialog.Accepted:
		filename = dialog.selectedFiles()[0]
		filename = to_native_path(filename)
		return filename
	else:
		return None

def save_as_filter(parent,my_filter):
	dialog = QFileDialog(parent)
	dialog.setWindowTitle(_("Save as"))
	dialog.setNameFilter(my_filter)
	dialog.setAcceptMode(QFileDialog.AcceptSave)
	if dialog.exec_() == QDialog.Accepted:
		filename = dialog.selectedFiles()[0]
		s=dialog.selectedNameFilter()
		if s.count("(*")==1:
			s=s.split("(*")[1]
			s=s[:-1]

			if filename.endswith(s)==False and s!=".":
				filename=filename+s
			else:
				filename=filename

		return filename
	else:
		return None

def open_as_filter(parent,my_filter,path="",multi_files=False):
	if path=="":
		open_path=os.getcwd()
	else:
		open_path=path

	dialog = QFileDialog(parent,_("Open file"))
	dialog.setDirectory(open_path)

	dialog.setNameFilter(my_filter)
	dialog.setAcceptMode(QFileDialog.AcceptOpen)
	if multi_files==True:
		dialog.setFileMode(QFileDialog.ExistingFiles)

	if dialog.exec_() == QDialog.Accepted:
		ret_list=[]
		s=dialog.selectedNameFilter()
		if s.count("(*")==1:
			s=s.split("(*")[1]
			s=s[:-1]

		filenames = dialog.selectedFiles()
		for f in filenames:
			if f.endswith(s)==False:
				ret_list.append(f+s)
			else:
				ret_list.append(f)

		if multi_files==True:
			return ret_list
		else:
			return ret_list[0]
	else:
		return None
	
def save_as_jpg(parent):
	return save_as_filter(parent,"jpg (*.jpg)")


def save_as_image(parent):
	return save_as_filter(parent,"png (*.png);;jpg (*.jpg);;gnuplot (*.)")
