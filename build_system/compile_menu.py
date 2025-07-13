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
try:
	from dialog import Dialog
except:
	from menu import Dialog

from make_m4 import make_m4

from pathlib import Path
from shutil import copyfile
from deb import deb_update_control_file_with_deps
from deb import deb_update_control_file_with_readme


def test(d):
	if d.yesno("Run oghma") == d.OK:
		os.system("./go.o  >log.txt 2>log.txt &")
		et=d.tailbox("log.txt", height=None, width=150)

def make_all(d):
	if d.yesno("Run make clean") == d.OK:
		os.system("cd oghma_core;make clean >../log.txt 2>../log.txt ;cd ../oghma_gui; make clean >../log.txt 2>../log.txt ;cd ../oghma_data; make clean >../log.txt 2>../log.txt&")
		et=d.tailbox("log.txt", height=None, width=150)

	if d.yesno("Run make in oghma_core") == d.OK:
		jobs=os.cpu_count()
		os.system("cd oghma_core; make  -j "+str(jobs)+" >../log.txt 2>../log.txt &")
		et=d.tailbox("log.txt", height=None, width=150)

	if d.yesno("Run make in oghma_gui") == d.OK:
		jobs=os.cpu_count()
		os.system("cd oghma_gui; make  -j "+str(jobs)+" >../log.txt 2>../log.txt &")
		et=d.tailbox("log.txt", height=None, width=150)

	if d.yesno("Run make in oghma_data") == d.OK:
		jobs=os.cpu_count()
		os.system("cd oghma_data; make  -j "+str(jobs)+" >../log.txt 2>../log.txt &")
		et=d.tailbox("log.txt", height=None, width=150)

    	#d.msgbox("You have been warned...")

def build_configure(directory):
	my_dir=os.getcwd()
	os.chdir(os.path.join(my_dir,directory))
	os.system("aclocal")
	os.system("automake --add-missing")
	os.system("automake")
	os.system("autoconf")
	os.chdir(my_dir)

def build_configure_all():
	build_configure("oghma_core")
	build_configure("oghma_gui")
	build_configure("oghma_data")

def configure_for_fedora(d):
	make_m4(hpc=False, win=False,usear=True,dbus=True)
	#d.infobox("aclocal", width=0, height=0, title="configure")
	build_configure_all()
	mpi_include="-I/usr/include/openmpi-x86_64/ -I/usr/include/MUMPS/ -L/usr/lib64/openmpi/lib/"
	os.system("cd oghma_core;./configure CPPFLAGS=\"-I/usr/include/suitesparse/ "+mpi_include+"\" --datadir=\"/usr/share/\" --bindir=\"/usr/bin/\" &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd oghma_gui;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd oghma_data;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)


def configure_for_ubuntu(d):
	make_m4(hpc=False, win=False,usear=True,dbus=True)

	control_file=os.path.join(os.getcwd(),"oghma_core/DEBIAN/control")
	deb_update_control_file_with_deps(control_file,os.path.join(os.getcwd(),"build_system/dependency_scripts/packages_ubuntu.sh"),target="native_ubuntu")
	deb_update_control_file_with_readme(control_file,"./oghma_core/README.md")

	build_configure_all()
	#oghma_core
	mpi_include="-I/usr/lib/x86_64-linux-gnu/openmpi/include/ -L/usr/lib64/openmpi/lib/"
	package_dirs=" --datadir=\"/usr/share/\" --bindir=\"/usr/bin/\" --libdir=\"/usr/lib/\" --mandir=\"/usr/share/man/\""
	command="cd oghma_core;./configure CPPFLAGS=\"-I/usr/include/ \" LDFLAGS=\"-lumfpack "+mpi_include+"\" "+package_dirs+">../log.txt 2>../log.txt &"
	print(command)
	os.system(command)
	et=d.tailbox("log.txt", height=None, width=100)

	#oghma_gui
	os.system("cd oghma_gui;./configure --prefix=\"/usr/\" &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	#oghma_data
	os.system("cd oghma_data;./configure --prefix=\"/usr/\" &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

def configure_for_windows(d):
	make_m4(hpc=False, win=True,usear=True,dbus=False)
	build_configure_all()

	home=str(Path.home())
	flags=" -I"+home+"/windll/libpng/libpng-1.6.37/"
	#+home+"-I/windll/OpenCL-Headers-master/"
	#+"-I/windll/gsl-1.16/
	os.system("cd oghma_core; ./configure --host=x86_64-w64-mingw32 CPPFLAGS=\""+flags+"\"  --enable-noplots --enable-noman  >../log.txt 2>../log.txt &")
	ret=d.tailbox("log.txt", height=None, width=100)

	os.system("cd oghma_gui;./configure --enable-nodesktop --enable-noman  &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd oghma_data;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

def configure_for_hybrid_wine(d):
	make_m4(hpc=False, win=True,usear=True,dbus=False,wine=True)

	control_file=os.path.join(os.getcwd(),"oghma_core/DEBIAN/control")
	deb_update_control_file_with_deps(control_file,os.path.join(os.getcwd(),"build_system/dependency_scripts/packages_ubuntu.sh"),target="hybrid")
	deb_update_control_file_with_readme(control_file,"./oghma_core/README.md")

	build_configure_all()

	home=str(Path.home())
	flags=" -I"+home+"/windll/libpng/libpng-1.6.37/"
	#+home+"-I/windll/OpenCL-Headers-master/"
	#+"-I/windll/gsl-1.16/
	package_dirs=" --datadir=\"/usr/share/\" --bindir=\"/usr/bin/\" --libdir=\"/usr/lib/\" --mandir=\"/usr/share/man/\""
	os.system("cd oghma_core; ./configure --host=x86_64-w64-mingw32 CPPFLAGS=\""+flags+"\"  --enable-hybrid --enable-noplots --enable-noman "+package_dirs+" >../log.txt 2>../log.txt &")
	ret=d.tailbox("log.txt", height=None, width=100)

	os.system("cd oghma_gui;./configure --enable-noman --prefix=\"/usr/\" &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd oghma_data;./configure --prefix=\"/usr/\" &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

def configure_for_ubuntu_with_flat_install(d):
	make_m4(hpc=False, win=False,usear=True,dbus=True)

	build_configure_all()

	os.system("cd oghma_core;./configure CPPFLAGS=\"-I/usr/include/\"  --enable-noplots --enable-noman --docdir=/ --datadir=/ --bindir=/  --libdir=/   >../log.txt 2>../log.txt &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd oghma_gui;./configure  --enable-nodesktop --enable-noman --docdir=/ --datadir=/ --bindir=/  --libdir=/  &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd oghma_data;./configure  --docdir=/ --datadir=/ --bindir=/  --libdir=/ &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)


def configure_autodetect(d):
	import distro
	plat=distro.linux_distribution(full_distribution_name=False)[0].lower()
	chipset=os.uname().machine
	configured=False
	if d.yesno("Configure for "+plat+" "+chipset) == d.CANCEL:
		return
	if plat=="fedora":
		configured=True
		configure_for_fedora(d)

	elif plat=="ubuntu":
		configured=True
		configure_for_ubuntu(d)
	elif plat=="arch":
		configured=True
		configure_for_arch(d)
	if configured==True:
		make_all(d)
		d.msgbox("Built")
	else:
		d.msgbox("Can't auto configure for this platform.")

def select_distro_menu(d):
	if os.geteuid() == 0:
		d.msgbox("Don't do a build as root")
		return
	code, tag = d.menu("build for:",
		               choices=[("(back)", "back"),
								("(win)", "Windows (x86_64)"),
								("(hybrid)", "Hybrid/Wine (x86_64)"),
								("(ubuntu)", "Ubuntu (x86_64)"),
								("(fedora)", "fedora (x86_64)"),
								("(default)", "generic Linux (x86_64)")
								])

	if code == d.OK:
		if tag=="(back)":
			configure_menu(d)

		if tag=="(default)":
			make_m4(hpc=False, win=False,usear=True)
			#d.infobox("aclocal", width=0, height=0, title="configure")
			build_configure_all()
			os.system("./configure CPPFLAGS=\"-I/usr/include/\"  &>../log.txt &")
			et=d.tailbox("log.txt", height=None, width=100)

			make_all(d)

			d.msgbox("Built")

		if tag=="(fedora)":
			configure_for_fedora(d)
			make_all(d)
			d.msgbox("Built")

		if tag=="(ubuntu)":
			configure_for_ubuntu(d)
			make_all(d)
			d.msgbox("Built")
		if tag=="(win)":
			configure_for_windows(d)
			make_all(d)
			d.msgbox("Built")
		elif tag=="(hybrid)":
			configure_for_hybrid_wine(d)
			make_all(d)
			d.msgbox("Built")

		
def compile_menu(d):
	if os.geteuid() == 0:
		d.msgbox("Don't do a build as root")
		return
	code, tag = d.menu("build for:",
		               choices=[("(auto)", "Configure for distro/architecture"),
								("(select)", "Select distro by hand"),
								("(docs)", "Build code documentation")
								])

	if code == d.OK:
		if tag=="(auto)":
			configure_autodetect(d)

		if tag=="(select)":
			select_distro_menu(d)

		if tag=="(docs)":
			if os.path.isdir("./code_docs")==False:
				os.mkdir("code_docs")

			os.system("doxygen ./docs/doxygen_gui.config >../log.txt 2>../log.txt &")
			os.system("doxygen ./docs/doxygen_core.config >../log.txt 2>../log.txt &")
			ret=d.tailbox("log.txt", height=None, width=100)
			#publish_code_docs()
			d.msgbox("Done")





