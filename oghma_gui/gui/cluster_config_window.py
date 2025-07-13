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

## @package cluster_config_window
#  A window used to configure the cluster done via ssh.
#

import os

#qt
from PySide2.QtGui import QIcon, QPixmap
from gQtCore import QSize, Qt, QTimer, gSignal
from PySide2.QtWidgets import QMenu,QToolBar,QSizePolicy, QVBoxLayout, QTabWidget, QAbstractItemView, QListWidgetItem,QPushButton, QListView,QWidget,QListWidget,QAction

#cal_path
from icon_lib import icon_get

from tab import tab_class

from help import help_window

from error_dlg import error_dlg

from inp import inp_get_token_value
from inp import inp_update_token_value
from cal_path import sim_paths

from QWidgetSavePos import QWidgetSavePos

from css import css_apply

import i18n
_ = i18n.language.gettext

import random

from experiment import experiment_bin
from json_c import json_local_root
from sim_name import sim_name

class cluster_config_window(experiment_bin):


	def __init__(self,data=None):	
		
		experiment_bin.__init__(self,window_save_name="cluster_window", window_title=_("Configure")+sim_name.web_window_title,name_of_tab_class="cluster_tab",json_search_path="cluster",icon="preferences-system",json_template="oghma_local")

		self.ribbon.addTab(self.cluser_ribbon_ssh(),_("SSH"))

		self.tb_install.triggered.connect(self.install_to_cluster)

		self.tb_boot.triggered.connect(self.boot_cluster)
		self.tb_generate_keys.triggered.connect(self.generate_keys)

		self.tb_stop.triggered.connect(self.kill_cluster)
		self.tb_remove.triggered.connect(self.remove_from_cluster)

		self.notebook.currentChanged.connect(self.switch_page)
		self.switch_page()

		self.changed.connect(self.callback_save)

	def callback_save(self):
		print("save")

	def cluser_ribbon_ssh(self):
		toolbar = QToolBar()
		toolbar.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
		toolbar.setIconSize(QSize(42, 42))


		self.tb_generate_keys = QAction(icon_get("gnome-dialog-password"), _("Generate keys"), self)
		self.tb_generate_keys.setStatusTip(_("Generate keys"))
		toolbar.addAction(self.tb_generate_keys)

		self.tb_install = QAction(icon_get("install-to-cluster"), _("Install to cluster"), self)
		self.tb_install.setStatusTip(_("Install to cluster"))
		toolbar.addAction(self.tb_install)

		self.tb_boot = QAction(icon_get("run-cluster"), _("Boot cluster"), self)
		self.tb_boot.setStatusTip(_("Boot cluster"))
		toolbar.addAction(self.tb_boot)

		self.tb_stop = QAction(icon_get("stop-cluster"), _("Stop cluster"), self)
		self.tb_stop.setStatusTip(_("Stop cluster"))
		toolbar.addAction(self.tb_stop)

		self.tb_remove = QAction(icon_get("remove-from-cluster"), _("Remove from cluster"), self)
		self.tb_remove.setStatusTip(_("Remove from cluster"))
		toolbar.addAction(self.tb_remove)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		self.tb_home_help = QAction(icon_get("internet-web-browser"), _("Help"), self)
		toolbar.addAction(self.tb_home_help)

		return toolbar

	def switch_page(self):
		self.notebook.currentWidget()

	def generate_keys(self):
		data=json_local_root()

		tab = self.notebook.currentWidget()

		iv = random.getrandbits(128)
		iv="%032x" % iv
		tab.data.config.cluster_iv=iv

		key = random.getrandbits(128)
		key="%032x" % key
		
		tab.data.config.cluster_key=key
		tab.tab.tab.update_values()
		data.save()

	def get_config(self):
		tab = self.notebook.currentWidget()
		file_name=tab.file_name

		self.user_name=inp_get_token_value(os.path.join(sim_paths.get_sim_path(),file_name), "#cluster_user_name")
		self.ip=inp_get_token_value(os.path.join(sim_paths.get_sim_path(),file_name), "#cluster_ip")
		self.cluster_dir=inp_get_token_value(os.path.join(sim_paths.get_sim_path(),file_name), "#cluster_cluster_dir")

	def write_cluster_config(self):
		tab = self.notebook.currentWidget()
		file_name=tab.file_name

		cluster_ip=inp_get_token_value(os.path.join(sim_paths.get_sim_path(),file_name), "#cluster_ip")
		inp_update_token_value(os.path.join(sim_paths.get_cluster_path(),"node.inp"),"#master_ip",cluster_ip)

		cluster_ip=inp_get_token_value(os.path.join(sim_paths.get_sim_path(),file_name), "#nodes")
		print(cluster_ip)
		inp_update_token_value(os.path.join(sim_paths.get_cluster_path(),"node_list.inp"),"#node_list",cluster_ip)

	def install_to_cluster(self):
		self.get_config()
		self.write_cluster_config()

		if len(self.cluster_dir)<2:
			return

		cpy_src="rsync -avh --delete -e ssh "+sim_paths.get_cluster_path()+"/ "+self.user_name+"@"+self.ip+":"+self.cluster_dir+"/"

		copy_to_nodes="ssh -n -f "+self.user_name+"@"+self.ip+" \"sh -c \'cd "+self.cluster_dir+"/; ./install.sh\'\""
		command=cpy_src+";"+copy_to_nodes
		print(command)

		os.system(command)

	def boot_cluster(self):
		self.get_config()
		command="ssh -n -f "+self.user_name+"@"+self.ip+" \"sh -c \'cd "+self.cluster_dir+"; ./boot.sh\'\""
		print(command)

		os.system(command)

	def kill_cluster(self):
		self.get_config()
		command="ssh -n -f "+self.user_name+"@"+self.ip+" \"sh -c \'cd "+self.cluster_dir+"; ./kill.sh\'\""
		print(command)

		os.system(command)

	def remove_from_cluster(self):
		self.get_config()
		command="ssh -n -f "+self.user_name+"@"+self.ip+" \"sh -c \'cd "+self.cluster_dir+"; ./remove.sh\'\""
		os.system(command)




