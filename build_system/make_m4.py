#!/usr/bin/python
# 
# General-purpose Photovoltaic Device Model oghma-nano.com - a drift diffusion
# base/Shockley-Read-Hall model for 1st, 2nd and 3rd generation solarcells.
# The model can simulate OLEDs, Perovskite cells, and OFETs.
# 
# Copyright 2008-2022 Roderick C. I. MacKenzie https://www.oghma-nano.com
# r.c.i.mackenzie at googlemail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
# 

import os
import sys
import argparse

def make_m4(hpc=False, win=False,usear=False,dbus=True,wine=False):
	path=os.getcwd()
	make_m4_core(path,hpc=hpc, win=win,usear=usear,dbus=dbus,wine=wine)
	make_m4_gui(path,hpc=hpc, win=win,usear=usear)
	make_m4_data(path,hpc=hpc, win=win,usear=usear)

def make_m4_core(path,hpc=False, win=False,usear=False,dbus=True,wine=False):
	path=os.path.join(path,"oghma_core")
	config_files=[]
	oghma_lib=[]
	link_libs=""

	config_files.append("")

	if os.path.isdir(os.path.join(path,"lang")):
		config_files.append("lang")

	config_files.append("libi")
	oghma_lib.append("libi")

	config_files.append("libmath2d")
	oghma_lib.append("libmath2d")

	config_files.append("libbasicmath")
	oghma_lib.append("libbasicmath")

	if os.path.isdir(os.path.join(path,"libfxdomain")):
		config_files.append("libfxdomain")
		oghma_lib.append("libfxdomain")

	config_files.append("librpn")
	oghma_lib.append("librpn")

	config_files.append("libshape")
	oghma_lib.append("libshape")

	if os.path.isdir(os.path.join(path,"libemission")):
		config_files.append("libemission")
		oghma_lib.append("libemission")

	config_files.append("libmemory")
	oghma_lib.append("libmemory")

	config_files.append("libdos")
	oghma_lib.append("libdos")

	config_files.append("liblight")
	oghma_lib.append("liblight")

	config_files.append("libjson")
	oghma_lib.append("libjson")

	if os.path.isdir(os.path.join(path,"libheat")):
		config_files.append("libheat")
		oghma_lib.append("libheat")

	if os.path.isdir(os.path.join(path,"libexciton")):
		config_files.append("libexciton")
		oghma_lib.append("libexciton")

	if os.path.isdir(os.path.join(path,"libsinglet")):
		config_files.append("libsinglet")
		oghma_lib.append("libsinglet")

	if os.path.isdir(os.path.join(path,"libray")):
		config_files.append("libray")
		oghma_lib.append("libray")

	config_files.append("libcolor")
	oghma_lib.append("libcolor")

	config_files.append("libmeasure")
	oghma_lib.append("libmeasure")

	config_files.append("libcontacts")
	oghma_lib.append("libcontacts")

	config_files.append("libdump")
	oghma_lib.append("libdump")

	config_files.append("libpy")
	config_files.append("libgl")

	config_files.append("libscan")
	oghma_lib.append("libscan")

	config_files.append("libdevice")
	oghma_lib.append("libdevice")

	if os.path.isdir(os.path.join(path,"libserver")):
		config_files.append("libserver")
		oghma_lib.append("libserver")

	config_files.append("libmesh")
	oghma_lib.append("libmesh")

	if os.path.isdir(os.path.join(path,"libperovskite")):
		config_files.append("libperovskite")
		oghma_lib.append("libperovskite")

	config_files.append("libnewtontricks")
	oghma_lib.append("libnewtontricks")

	if os.path.isdir(os.path.join(path,"libfit")):
		config_files.append("libfit")
		link_libs=link_libs+" -loghma_fit"

	if os.path.isdir(os.path.join(path,"libsimplex")):
		config_files.append("libsimplex")
		oghma_lib.append("libsimplex")

	if os.path.isdir(os.path.join(path,"libmode")):
		config_files.append("libmode")
		oghma_lib.append("libmode")

	if os.path.isdir(os.path.join(path,"liblock")):
		config_files.append("liblock")
		oghma_lib.append("liblock")

	if os.path.isdir(os.path.join(path,"libcircuit")):
		config_files.append("libcircuit")
		oghma_lib.append("libcircuit")

	if win==False:
		if os.path.isdir(os.path.join(path,"mumps")):
			config_files.append("mumps")

	config_files.append("lib")					#Main lib dll
	oghma_lib.append("lib")



	link_libs=link_libs+" -loghma_core"

	#dlls past this point which need liboghma_core

	if os.path.isdir(os.path.join(path,"libfdtd")):
		config_files.append("libfdtd")
		#oghma_lib.append("libfdtd")
		link_libs=link_libs+" -loghma_fdtd"


	config_files.append("src")					#The exe

	for root, dirs, files in os.walk(os.path.join(path,"plugins")):
		for file in files:
			if file.endswith("Makefile.am"):
				name=os.path.join(root, file)[len(path)+1:-12]
				config_files.append(name)
	if win==True:
		try:
			config_files.remove("plugins/external_solver")
		except:
			pass

		try:
			config_files.remove("plugins/superlu")
		except:
			pass



	if hpc==False:
		config_files.append("cluster_")
		if win==False:
			config_files.append("man")

	config_files.append("inp_template")

	f = open(os.path.join(path,"config_files.m4"), "w")
	f.write( "#This file has been autogenerated\n")
	for i in range(0,len(config_files)):
		f.write( "AC_CONFIG_FILES(["+os.path.join(config_files[i],"Makefile")+"])\n")

	f.close()

	f = open(os.path.join(path,"os_target.m4"), "w")
	f.write( "#This file has been autogenerated\n")
	if win==False:
		#linux
		f.write( "AC_SUBST(GUIC, \"gcc\")\n")
		f.write( "AC_SUBST(LIBOPENGL, \"-lGL -lGLU\")\n")
		f.write( "AC_SUBST(DEFINE_CORE, \"-Denable_server -Duse_open_cl\")\n")
		f.write( "AC_SUBST(DEFINE_GUI, \"-Denable_server -Duse_open_cl -Dpydll\")\n")
		f.write( "AC_SUBST(LIBS_GUI, \" -lm -rdynamic -export-dynamic -ldl -lzip -lz -lpng\")\n")
		f.write( "AC_SUBST(COMPILE_FLAG, \" -fPIC \")\n")	#this is for the core
		f.write( "AC_SUBST(COMPILE_FLAG_GUI, \" -fPIC \")\n")
	else:
		if wine==True:
			#hybrid
			f.write( "AC_SUBST(GUIC, \"gcc\")\n")
			f.write( "AC_SUBST(LIBOPENGL, \"-lGL -lGLU\")\n")
			f.write( "AC_SUBST(DEFINE_CORE, \"-Dwindows \")\n")
			f.write( "AC_SUBST(DEFINE_GUI, \" -Dpydll \")\n")
			f.write( "AC_SUBST(LIBS_GUI, \" -lm -rdynamic -export-dynamic -ldl -lzip -lz -lpng\")\n")
			f.write( "AC_SUBST(COMPILE_FLAG, \" \")\n")	#this is for the core
			f.write( "AC_SUBST(COMPILE_FLAG_GUI, \" -fPIC \")\n")
		else:
			#windows
			f.write( "AC_SUBST(GUIC, \"x86_64-w64-mingw32-gcc\")\n")
			f.write( "AC_SUBST(LIBOPENGL, \"-lopengl32 -lglu32\")\n")
			f.write( "AC_SUBST(DEFINE_CORE, \"-Dwindows \")\n")
			f.write( "AC_SUBST(DEFINE_GUI, \" -Dwindows -Dpydll \")\n")
			f.write( "AC_SUBST(LIBS_GUI, \" -luserenv -lzip -L/home/rod/windll/compiled_dlls4_x86/\")\n")
			f.write( "AC_SUBST(COMPILE_FLAG, \" \")\n")	#this is for the core
			f.write( "AC_SUBST(COMPILE_FLAG_GUI, \" \")\n")
	f.close()


	f = open(os.path.join(path,"make_files.m4"), "w")
	f.write( "#This file has been autogenerated\n")
	f.write( "AC_SUBST(BUILD_DIRS,\"")
	for i in range(0,len(config_files)):
		f.write(config_files[i]+" ")

	f.write("\")")

	f.close()



	f = open(os.path.join(path,"local_link.m4"), "w")
	f.write( "AC_SUBST(LOCAL_LINK,\"")
	f.write(link_libs)
	f.write("\")")

	f.close()

	f = open(os.path.join(path,"ar.m4"), "w")

	if usear==True:
		f.write("AM_PROG_AR")
	else:
		f.write("")

	f.close()


	f = open(os.path.join(path,"oghma_core_lib.m4"), "w")
	f.write( "AC_SUBST(OGHMA_CORE_LIB_FILES,\"")
	for file_name in oghma_lib:
		f.write("../"+file_name+"/*.o ")
	f.write("\")")

	f.close()


	f = open(os.path.join(path,"include","enabled_libs.h"), "w")
	f.write("//This file is auto_generated do not edit.\n")
	for lib_name in oghma_lib:
		f.write("#define "+lib_name+"_enabled\n")

	if config_files.count("libfit")!=0:
		f.write("#define libfit_enabled\n")

	if dbus==True:
		f.write("#define dbus\n")


	f.close()

def make_m4_gui(path,hpc=False, win=False,usear=False):
	path=os.path.join(path,"oghma_gui")
	config_files=[]
	link_libs=""

	config_files.append("")
	config_files.append("gui")
	config_files.append("lang")

	if hpc==False:
		config_files.append("images/16x16")
		config_files.append("images/32x32")
		config_files.append("images/48x32")
		config_files.append("images/64x64")

		config_files.append("images/icons/16x16")
		config_files.append("images/icons/32x32")
		config_files.append("images/icons/48x48")
		config_files.append("images/icons/64x64")
		config_files.append("images/icons/128x128")
		config_files.append("images/icons/256x256")
		config_files.append("images/icons/512x512")

		config_files.append("css")
		config_files.append("scripts")
		config_files.append("html")
		config_files.append("bib")
		config_files.append("video")

		if os.path.isdir(os.path.join(path,"desktop")):
			config_files.append("desktop")

		if win==False:
			config_files.append("man")

	f = open(os.path.join(path,"config_files.m4"), "w")
	f.write( "#This file has been autogenerated\n")
	for i in range(0,len(config_files)):
		f.write( "AC_CONFIG_FILES(["+os.path.join(config_files[i],"Makefile")+"])\n")

	f.close()

	f = open(os.path.join(path,"make_files.m4"), "w")
	f.write( "#This file has been autogenerated\n")
	f.write( "AC_SUBST(BUILD_DIRS,\"")
	for i in range(0,len(config_files)):
		f.write(config_files[i]+" ")

	f.write("\")")

	f.close()


	f = open(os.path.join(path,"local_link.m4"), "w")
	f.write( "AC_SUBST(LOCAL_LINK,\"")
	f.write(link_libs)
	f.write("\")")

	f.close()

	f = open(os.path.join(path,"ar.m4"), "w")

	if usear==True:
		f.write("AM_PROG_AR")
	else:
		f.write("")

	f.close()

def make_m4_data(path,hpc=False, win=False,usear=False):
	path=os.path.join(path,"oghma_data")
	config_files=[]
	link_libs=""

	config_files.append("")
	config_files.append("cie_color")

	if os.path.isdir(os.path.join(path,"docs","man")):
		config_files.append("docs/man")

	f = open(os.path.join(path,"config_files.m4"), "w")
	f.write( "#This file has been autogenerated\n")

	if os.path.isdir(os.path.join(path,"docs","man")):
		f.write( "AC_CONFIG_SRCDIR([./docs/man/understanding_oghma_nano.tex])")

	for i in range(0,len(config_files)):
		f.write( "AC_CONFIG_FILES(["+os.path.join(config_files[i],"Makefile")+"])\n")

	f.close()

	f = open(os.path.join(path,"make_files.m4"), "w")
	f.write( "#This file has been autogenerated\n")
	f.write( "AC_SUBST(BUILD_DIRS,\"")
	for i in range(0,len(config_files)):
		f.write(config_files[i]+" ")

	f.write("\")")

	f.close()


	f = open(os.path.join(path,"local_link.m4"), "w")
	f.write( "AC_SUBST(LOCAL_LINK,\"")
	f.write(link_libs)
	f.write("\")")

	f.close()

	f = open(os.path.join(path,"ar.m4"), "w")

	if usear==True:
		f.write("AM_PROG_AR")
	else:
		f.write("")

	f.close()



