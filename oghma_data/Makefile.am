AUTOMAKE_OPTIONS = foreign
EXTRA_DIST = config.rpath m4/ChangeLog 
SUBDIRS = @BUILD_DIRS@

dist_doc_DATA = README.md LICENSE.md

#if INCLUDE_DEVICELIB
#device_libdir = $(pkgdatadir)/device_lib
#device_lib_DATA = $(wildcard device_lib/**/*)

#device_lib_DATA=device_lib/*.oghma device_lib/*.json

#device_lib_bhjdir = $(pkgdatadir)/device_lib/bhj/
#device_lib_bhj_DATA=device_lib/bhj/*.oghma device_lib/bhj/*.json

#device_lib_excitondir = $(pkgdatadir)/device_lib/exciton/
#device_lib_exciton_DATA=device_lib/exciton/*.json

#device_lib_perovskitedir = $(pkgdatadir)/device_lib/perovskite/
#device_lib_perovskite_DATA=device_lib/perovskite/*.json

#device_lib_ofetsdir = $(pkgdatadir)/device_lib/ofets/
#device_lib_ofets_DATA=device_lib/ofets/*.json

#device_lib_mode_solverdir = $(pkgdatadir)/device_lib/mode_solver/
#device_lib_mode_solver_DATA=device_lib/mode_solver/*.json

#device_lib_simple_diodedir = $(pkgdatadir)/device_lib/simple_diode/
#device_lib_simple_diode_DATA=device_lib/simple_diode/*.json

#device_lib_ray_tracedir = $(pkgdatadir)/device_lib/ray_trace/
#device_lib_ray_trace_DATA=device_lib/ray_trace/*.json

#device_lib_automationdir = $(pkgdatadir)/device_lib/automation/
#device_lib_automation_DATA=device_lib/automation/*.json device_lib/automation/*.oghma

#device_lib_large_areadir = $(pkgdatadir)/device_lib/large_area/
#device_lib_large_area_DATA=device_lib/large_area/*.oghma  device_lib/large_area/*.json

#device_lib_fdtddir = $(pkgdatadir)/device_lib/fdtd/
#device_lib_fdtd_DATA=device_lib/fdtd/*.json

#device_lib_interfacesdir = $(pkgdatadir)/device_lib/interfaces/
#device_lib_interfaces_DATA=device_lib/interfaces/*.json

#device_lib_oleddir = $(pkgdatadir)/device_lib/oleds/
#device_lib_oled_DATA=device_lib/oleds/*.json

#device_lib_mldir = $(pkgdatadir)/device_lib/ml/
#device_lib_ml_DATA=device_lib/ml/*.json

#device_lib_maeckel_et_aldir = $(pkgdatadir)/device_lib/maeckel_et_al/
#device_lib_maeckel_et_al_DATA=device_lib/maeckel_et_al/*.oghma
#endif

clean-local:
	echo "clean"
	@echo "(oghma_build_finished)"

all:
	@echo "(oghma_build_finished)"

install-data-hook:
	mkdir -p $(DESTDIR)$(datadir)/oghma_data
	cp materials $(DESTDIR)$(datadir)/oghma_data/materials -rf
	cp device_lib $(DESTDIR)$(datadir)/oghma_data/device_lib -rf
	cp spectra $(DESTDIR)$(datadir)/oghma_data/spectra -rf
	cp cie_color $(DESTDIR)$(datadir)/oghma_data/cie_color -rf
	cp atmosphere $(DESTDIR)$(datadir)/oghma_data/atmosphere -rf
	cp shape $(DESTDIR)$(datadir)/oghma_data/shape -rf
	cp morphology $(DESTDIR)$(datadir)/oghma_data/morphology -rf
	cp filters $(DESTDIR)$(datadir)/oghma_data/filters -rf
	cp components $(DESTDIR)$(datadir)/oghma_data/components -rf
	find ./ -name "*.mo" -exec cp --parents {} $(DESTDIR)$(datadir)/oghma_data/ ";"
	@echo "(oghma_build_finished)"

uninstall-hook:
	echo ""

ACLOCAL_AMFLAGS = -I m4
