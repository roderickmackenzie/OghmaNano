# 
# General-purpose Photovoltaic Device Model oghma.com- a drift diffusion
# base/Shockley-Read-Hall model for 1st, 2nd and 3rd generation solarcells.
# The model can simulate OLEDs, Perovskite cells, and OFETs.
# 
# Copyright (C) 2012-2019 Roderick C. I. MacKenzie info at oghma dot com
# 
# https://www.oghma.com
# 
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU Lesser General Public License,
# version 2.1, as published by the Free Software Foundation.
# 
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 


AC_INIT([oghma_core], [5.3])
AC_CONFIG_SRCDIR([./src/main.c])
AC_CANONICAL_TARGET
AC_CANONICAL_HOST
#AM_GNU_GETTEXT([external])

AC_MSG_NOTICE([$target])
AC_MSG_NOTICE([$target_alias])
AC_MSG_NOTICE([$target_cpu])
AC_MSG_NOTICE([$target_vendor])
AC_MSG_NOTICE([$target_os])

AC_SUBST(WARN, ["-Wall -Wno-format-overflow"])

m4_include([os_target.m4])

AC_ARG_ENABLE(nocluster, "used to disable the cluster",
[AM_CONDITIONAL([INCLUDE_CLUSTER],[false])],
[AM_CONDITIONAL([INCLUDE_CLUSTER],[true])]
)


AC_ARG_ENABLE(noplots, "used to disable plot files",
[AM_CONDITIONAL([INCLUDE_PLOTS],[false])],
[AM_CONDITIONAL([INCLUDE_PLOTS],[true])]
)


AC_ARG_ENABLE(noman, "used to disable man page generation",
[AM_CONDITIONAL([INCLUDE_MAN],[false])],
[AM_CONDITIONAL([INCLUDE_MAN],[true])]
)


AC_ARG_ENABLE(useopencl, "Use this to enable OpenCL for the FDTD code",
[
AC_SUBST(OPEN_CL_LINK, "-lOpenCL")
AC_SUBST(OPEN_CL_COMPILE, "-D use_open_cl")
],
[
AC_SUBST(OPEN_CL_LINK, "")
AC_SUBST(OPEN_CL_COMPILE, "")
]
)

#libfreetype
AC_SUBST(FREETYPE_LIB,"-lfreetype")

AC_SUBST(WIN_ICON, "" )
AC_SUBST(WIN_RES_FILE, "" )
AC_SUBST(PNG_LIB,[""])
AC_SUBST(PNG_HEADER,[""])
AC_SUBST(INCLUDE_UMFPACK,"-I/usr/include/suitesparse/")
AC_SUBST(INCLUDE_SUPERLU,"-I/usr/include/superlu/")
AC_SUBST(INCLUDE_FREETYPE2,"-I/usr/include/freetype2/")
AC_SUBST(INCLUDE_LIBZIP, [""])
#This is a case statment the default is to compile for linux
AS_CASE([$target_os],
  [mingw32], [
AC_MSG_NOTICE([********************************])
AC_MSG_NOTICE([*Setting up config for windows *])
AC_MSG_NOTICE([********************************])

AC_SUBST(oghma_DIR, "" )
AC_SUBST(LINK_FLAG, "  ")
#-posix
#-posix
AC_SUBST(SLIB_EXT, "a")
AC_SUBST(DLIB_EXT, "dll")
AC_SUBST(EXE_EXT, ".exe")


AC_SUBST(DLL_LINKER, ["-L/home/rod/windll/compiled_dlls4_x86/ -Wl,--out-implib,plugin.a -Wl,--start-group -loghma_light -loghma_lib -loghma_dump -loghma_measure -loghma_contacts -loghma_dos -loghma_dumpctrl -loghma_light -loghma_ray -loghma_i -loghma_fdtd -loghma_fxdomain -loghma_simplex -loghma_newtontricks -loghma_perovskite -lzip   -llibpng16-16 -loghma_mesh -loghma_memory -loghma_basicmath -loghma_shape -loghma_emission  -loghma_lock -loghma_color -loghma_device -loghma_circuit -loghma_heat -Wl,--end-group  "])
#-lumfpack-5.0.2
AC_SUBST(DLL_COMPILE, [" "])	#-DBUILDING_EXAMPLE_DLL
AC_SUBST(DLL_DEBUG, ["-Wall"])	# -O2 -g2 -gstabs+ for gdb output 
AC_SUBST(SRC_DEBUG, ["-Wall -Wno-format-truncation"])
AC_SUBST(LIBS,["-L/home/rod/windll/compiled_dlls4_x86/ -lzip -luserenv"])
#-luserenv gives GetUserProfileDirectoryW
AC_SUBST(LIB_UMFPACK, "-lumfpack-5.0.2")
AC_SUBST(INCLUDE_UMFPACK, "-I/home/rod/windll/compiled_dlls4_x86/SuiteSparse-3.0.0_cut_down/SuiteSparse/UFconfig/ -I/home/rod/windll/compiled_dlls4_x86/SuiteSparse-3.0.0_cut_down/SuiteSparse/AMD/Include/ -I/home/rod/windll/compiled_dlls4_x86/SuiteSparse-3.0.0_cut_down/SuiteSparse/UMFPACK/Include/")

AC_SUBST(INCLUDE_SUPERLU,"")
	AC_ARG_ENABLE(hybrid, "hybrid exe",
	[
		AC_SUBST(INTERNET_LIB_FOR_PY_DLL,["-lcurl"])
		AC_SUBST(INTERNET_LIB_FOR_CORE,["-lwinhttp -lws2_32"])
		AC_SUBST(INCLUDE_DBUS_FOR_DLL, "-I/usr/include/dbus-1.0/ `pkg-config --cflags dbus-1`")
		AC_SUBST(INCLUDE_DBUS_FOR_CORE, "")
		AC_SUBST(LIBS_DBUS_FOR_DLL, "`pkg-config --libs dbus-1`")
		AC_SUBST(LIBS_DBUS_FOR_CORE, "")
		AC_SUBST(INCLUDE_LIBZIP_FOR_DLL, [""])
		AC_SUBST(INCLUDE_LIBZIP_FOR_CORE, ["-I/home/rod/windll/compiled_dlls4_x86/libzip-1.5.2/lib/ -I/home/rod/windll/compiled_dlls4_x86/libzip-1.5.2/"])
	],
	[
		AC_SUBST(INTERNET_LIB_FOR_PY_DLL,["-lwinhttp -lws2_32"])
		AC_SUBST(INTERNET_LIB_FOR_CORE,["-lwinhttp -lws2_32"])
		AC_SUBST(INCLUDE_DBUS_FOR_DLL, "")
		AC_SUBST(INCLUDE_DBUS_FOR_CORE, "")
		AC_SUBST(LIBS_DBUS_FOR_DLL, "")
		AC_SUBST(LIBS_DBUS_FOR_CORE, "")
		AC_SUBST(INCLUDE_LIBZIP_FOR_DLL, ["-I/home/rod/windll/compiled_dlls4_x86/libzip-1.5.2/lib/ -I/home/rod/windll/compiled_dlls4_x86/libzip-1.5.2/"])
		AC_SUBST(INCLUDE_LIBZIP_FOR_CORE, ["-I/home/rod/windll/compiled_dlls4_x86/libzip-1.5.2/lib/ -I/home/rod/windll/compiled_dlls4_x86/libzip-1.5.2/"])
	]
	)

AC_SUBST(PNG_LIB,["-llibpng16-16"])
AC_SUBST(PNG_HEADER,["-I/home/rod/windll/compiled_dlls4_x86/libpng/libpng-1.6.37/"])
#-lwininet
AC_SUBST(WIN_RES_FILE, "oghma.res" )
AC_SUBST(WIN_ICON, "x86_64-w64-mingw32-windres oghma.rc -O coff -o oghma.res" )
AC_SUBST(INSTALL_LANG,"")

#-lintl -lintl
], [

AC_MSG_NOTICE([*****************************])
AC_MSG_NOTICE([*Setting up config for linux*])
AC_MSG_NOTICE([*****************************])
AC_SUBST(oghma_DIR, "oghma" )
AC_SUBST(LINK_FLAG, "")

AC_SUBST(SLIB_EXT, "a")
AC_SUBST(DLIB_EXT, "so")
AC_SUBST(EXE_EXT, "")


AC_SUBST(DLL_LINKER, ["`dpkg-buildflags --get LDFLAGS` -Wl,-soname,plugin.so"])
AC_SUBST(DLL_COMPILE, ["-fPIC"])
AC_SUBST(DLL_DEBUG, ["-Wall -g "])
AC_SUBST(SRC_DEBUG, ["-Wall -g -Wno-format-truncation"])
#-g -fsanitize=address -fno-omit-frame-pointer -pg   -pg
# -fsanitize=address -fno-omit-frame-pointer

AC_ARG_ENABLE(hpc, "used to turn on HPC compatability",
  [
AC_MSG_NOTICE([*****************************])
AC_MSG_NOTICE([*Setting up for HPC         *])
AC_MSG_NOTICE([*****************************])

AC_SUBST(LIBS, " -lm -rdynamic -export-dynamic -ldl -lzip -lz -lpng -L/home/steve/oghma/cluster_libs/")
AC_SUBST(LIBS_DBUS_FOR_DLL, "")
AC_SUBST(LIBS_DBUS_FOR_CORE, "")
AC_SUBST(INCLUDE_LIBZIP_FOR_DLL, [""])
AC_SUBST(INCLUDE_LIBZIP_FOR_CORE, [""])
AC_SUBST(LIB_UMFPACK, " -lumfpack")
AC_SUBST(INCLUDE_UMFPACK, "-I/usr/include/suitesparse/")
AC_SUBST(INCLUDE_DBUS_FOR_DLL, "")
AC_SUBST(INCLUDE_DBUS_FOR_CORE, "")
AC_SUBST(INCLUDE_SUPERLU,"-I/usr/include/superlu/")

#-lgsl -lgslcblas
#-lmatheval -g -L/home/steve/rm/build/libmatheval-1.1.11/lib/.libs/

],[

	AC_SUBST(LIBS, " -lm -rdynamic -export-dynamic -ldl -lzip -lz -lOpenCL -lpng -g ")
	AC_SUBST(LIBS_DBUS_FOR_DLL, "`pkg-config --libs dbus-1`")
	AC_SUBST(LIBS_DBUS_FOR_CORE, "`pkg-config --libs dbus-1`")
	AC_SUBST(INCLUDE_LIBZIP_FOR_DLL, [""])
	AC_SUBST(INCLUDE_LIBZIP_FOR_CORE, [""])
	AC_SUBST(INTERNET_LIB_FOR_PY_DLL,["-lcurl"])
	AC_SUBST(INTERNET_LIB_FOR_CORE,["-lcurl"])
	AC_SUBST(LIB_UMFPACK, " -lumfpack")
	AC_SUBST(INCLUDE_UMFPACK, "-I/usr/include/suitesparse/")
	AC_SUBST(INCLUDE_DBUS_FOR_DLL, "-I/usr/include/dbus-1.0/ `pkg-config --cflags dbus-1` ")
	AC_SUBST(INCLUDE_DBUS_FOR_CORE, "-I/usr/include/dbus-1.0/ `pkg-config --cflags dbus-1` ")
	AC_SUBST(INCLUDE_SUPERLU,"-I/usr/include/superlu/")
 	#-I/usr/lib/x86_64-linux-gnu/openmpi/include/ -lmpi -ldmumps for mumps -lumfpack
	#-lgsl -lgslcblas
	
]
)


]
)


AC_PROG_RANLIB
AM_INIT_AUTOMAKE([-Wno-portability])
AC_PROG_CC

AC_ARG_ENABLE(hpc, "used to turn on HPC compatability",
  [ ],[

	AM_PATH_PYTHON([3.0], [], [AC_MSG_ERROR([You need python installed])])
	
	AC_CHECK_PROG([PKG_HELP2MAN], help2man, help2man,no)
	if test "$PKG_HELP2MAN" = "no"; then
		AC_MSG_ERROR([help2man is not installed.])
	fi

	AC_CHECK_PROG([PKG_XGETTEXT], xgettext, xgettext,no)
	if test "$PKG_XGETTEXT" = "no"; then
		AC_MSG_ERROR([xgettext is not installed.])
	fi

]
)

AC_CHECK_PROG([PKG_CONFIG], pkg-config, pkg-config,no)
if test "$PKG_CONFIG" = "no"; then
	AC_MSG_ERROR([pkg-config is not installed.])
fi




#i?86
#x86_64

m4_include([make_files.m4])
m4_include([local_link.m4])
m4_include([oghma_core_lib.m4])


m4_include([ar.m4])

AC_CHECK_HEADERS(math.h)
AC_FUNC_MALLOC
AC_CHECK_FUNCS([sqrt])


#AC_CONFIG_FILES

m4_include([config_files.m4])

AC_OUTPUT

AC_MSG_NOTICE([oghma_core build finished. (oghma_build_finished)])
