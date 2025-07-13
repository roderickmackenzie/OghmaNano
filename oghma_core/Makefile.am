AUTOMAKE_OPTIONS = foreign
EXTRA_DIST = config.rpath m4/ChangeLog  materials
SUBDIRS = @BUILD_DIRS@

bin_PROGRAMS=oghma_core
oghma_core_SOURCES=



inp_templatedir = $(pkgdatadir)/inp_template
inp_template_DATA = inp_template/*.inp

inp_template_shapedir = $(pkgdatadir)/inp_template/shape/
inp_template_shape_DATA = inp_template/shape/*.inp inp_template/shape/*.py inp_template/shape/*.png

if INCLUDE_CLUSTER
clusterdir = $(pkgdatadir)/cluster_
cluster_DATA=cluster_/*.zip
endif

if INCLUDE_PLOTS
plotdir = $(pkgdatadir)/plot
plot_DATA=plot/*.plot
endif

licensesdir = $(pkgdatadir)/licenses
licenses_DATA=licenses/*.txt

pluginsdir = $(pkglibdir)/plugins
plugins_DATA=plugins/*.@DLIB_EXT@

dist_doc_DATA = README.md LICENSE.txt


if INCLUDE_MAN
man1_MANS = man/oghma_core.1
endif


clean-local:
	rm *.dat *.o ./plugins/*.so ./plugins/*.dll  *.log *.a  *.lib *.exe -f
	rm autom4te.cache -rf
	rm oghma_core -f
	rm oghma_core.@DLIB_EXT@ -f
	find . -type f -name '.~lock*' -delete
	
	
oghma_core$(EXEEXT):
	@printf ""


install-data-hook:
	echo "lang"
	cp liboghma_core.@DLIB_EXT@ $(DESTDIR)$(pkglibdir)/
	- cp ./windll/*.dll $(DESTDIR)$(pkglibdir)/
	cp liboghma_fdtd.@DLIB_EXT@ $(DESTDIR)$(pkglibdir)/
	cp liboghma_py.@DLIB_EXT@ $(DESTDIR)$(pkglibdir)/
	cp DEBIAN $(DESTDIR)/ -rf 2>/dev/null || :
	@echo "(oghma_build_finished)"

uninstall-hook:
	-rm $(DESTDIR)$(pkgdatadir) -rf
	-rm $(DESTDIR)$(bindir)/oghma_core

ACLOCAL_AMFLAGS = -I m4
