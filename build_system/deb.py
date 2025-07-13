import os
from shutil import rmtree
from install import do_install
import re
import textwrap
import shutil

import os
import shutil

def deb_replace_exe_with_wine_wrapper(bin_dir, lib_dir, exe_name="oghma_core.exe", install_lib_path="/usr/lib/oghma_core"):
	"""
	bin_dir: path in build env (e.g. ./debian/tmp/usr/bin)
	lib_dir: path in build env (e.g. ./debian/tmp/usr/lib/oghma_core)
	install_lib_path: final install-time path (e.g. /usr/lib/oghma_core)
	"""
	os.makedirs(lib_dir, exist_ok=True)

	exe_path = os.path.join(bin_dir, exe_name)
	new_exe_path = os.path.join(lib_dir, exe_name)
	wrapper_path = os.path.join(bin_dir, "oghma_core")

	if os.path.exists(exe_path):
		shutil.move(exe_path, new_exe_path)
		print(f"Moved {exe_path} -> {new_exe_path}")
	else:
		raise FileNotFoundError(f"{exe_path} does not exist")

	# Point to the final install path, not the build env path
	wrapper_script = f"""#!/bin/bash
wine "{install_lib_path}/{exe_name}" "$@"
"""

	with open(wrapper_path, "w") as f:
		f.write(wrapper_script)

	os.chmod(wrapper_path, 0o755)
	print(f"Created Wine wrapper at {wrapper_path} pointing to {install_lib_path}/{exe_name}")



def make_deb(d,hybrid=False):
	pub_path=os.path.join(os.getcwd(),"pub")
	output_path=os.path.join(pub_path,"oghma-8.1")
	usr_path=os.path.join(output_path,"usr")
	bin_path=os.path.join(usr_path,"bin")
	lib_path=os.path.join(usr_path,"lib","oghma_core")
	#print(pub_path)
	if os.path.isdir(pub_path)==True:
		rmtree(pub_path)

	do_install(d,output_path)

	#Write conf file for linking
	conf_dir = os.path.join(output_path, "etc", "ld.so.conf.d")
	conf_file = os.path.join(conf_dir, "oghma_core.conf")

	os.makedirs(conf_dir, exist_ok=True)

	with open(conf_file, "w") as f:
		f.write("/usr/lib/oghma_core\n")

	#build package
	if hybrid==True:
		deb_replace_exe_with_wine_wrapper(bin_path, lib_path, exe_name="oghma_core.exe")

	os.system("cd "+pub_path+"; dpkg --build oghma-8.1")
	


def deb_update_control_file_with_deps(control_file,apt_script_file,target="native_ubuntu"):
	if os.path.isfile(control_file)==False:
		return

	total=""

	if target=="native_ubuntu":
		f = open(apt_script_file, mode='rb')
		lines = f.read()
		f.close()

		lines=lines.decode('utf-8')
		lines=[str.strip() for str in lines.splitlines()]

		for l in lines:
			l=l.strip()
			process=False
			if l.startswith("apt-get -y install"):
				process=True
			if l.startswith("apt-get install"):
				process=True
			if l.startswith("apt install"):
				process=True

			if process==True:
				l=l.split("install")[1]
				if l.count("#")!=0:
					l=l.split("#")[0]

				total=total+l
		total=total.strip()
		total = re.sub(r"\s+", ",", total)
	elif target=="hybrid":
		total="python3-pyside2.qtcore,python3-pyside2.QtGui,python3-pyside2.qtwidgets,python3-opengl,python3-pyside2.qtopengl,wine"


	f = open(control_file, mode='rb')
	lines = f.read()
	f.close()

	lines=lines.decode('utf-8')
	lines=lines.splitlines()

	f = open(control_file, "w")
	
	for l in lines:
		if l.startswith("Depends:"):
			f.write("Depends: "+total+"\n")
		else:
			f.write(l+"\n")
	f.close()

def deb_update_control_file_with_readme(control_file,readme_file):
	if os.path.isfile(control_file)==False:
		return

	f = open(readme_file, mode='rb')
	lines = f.read()
	f.close()
	width=79
	lines=lines.decode('utf-8')
	lines=[str.strip() for str in lines.splitlines()]
	start=False
	out_text=""
	tot=""
	for l in lines:
		l=l.strip()
		if l.startswith("OghmaNano is a")==True:
			start=True

		if start==True:
			if l=="":
				if tot!="":
					out_text=out_text+'\n'.join(textwrap.wrap(tot, width))+"\n"
				out_text=out_text+"."+"\n"
				tot=""
			else:
				if l.startswith("-"):
					out_text=out_text+l+"\n"
				else:
					if tot!="":
						l=" "+l
					tot=tot+l

	if tot!="":
		out_text=out_text+'\n'.join(textwrap.wrap(tot, width))+"\n"
	out_text=" "+out_text
	out_text='\n '.join(out_text.splitlines())

	f = open(control_file, mode='rb')
	lines = f.read()
	f.close()

	lines=lines.decode('utf-8')
	lines=lines.splitlines()

	f = open(control_file, "w")
	
	for l in lines:
		if l.startswith("Description:"):
			f.write("Description: "+out_text)
		else:
			f.write(l+"\n")
	f.close()

