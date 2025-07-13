AUTOMAKE_OPTIONS = foreign
EXTRA_DIST = config.rpath m4/ChangeLog 
SUBDIRS = @BUILD_DIRS@

if INCLUDE_HTML
htmlsrcdir = $(pkgdatadir)/html
htmlsrc_DATA = html/*.html html/*.csv

bibsrcdir = $(pkgdatadir)/bib
bibsrc_DATA = bib/*.bib
endif

fontssrcdir = $(pkgdatadir)/fonts
fontssrc_DATA = fonts/*.ttf


if INCLUDE_VIDEO
videosrcdir = $(pkgdatadir)/video
videosrc_DATA = video/*.wmv
endif

if INCLUDE_IMAGES
imagedir = $(pkgdatadir)/images
image_DATA = images/*.jpg images/*.ico

#image16dir = $(pkgdatadir)/images/16x16
#image16_DATA = images/16x16/*.png

#image32dir = $(pkgdatadir)/images/32x32
#image32_DATA = images/32x32/*.png

image64dir = $(pkgdatadir)/images/64x64
image64_DATA = images/64x64/*.png

splashdir = $(pkgdatadir)/images/splash
splash_DATA = images/splash/*.png

flagdir = $(pkgdatadir)/images/48x32
flag_DATA = images/48x32/*.png

icon16dir = $(datadir)/icons/hicolor/16x16/mimetypes
icon16_DATA = images/icons/16x16/*.png
icon32dir = $(datadir)/icons/hicolor/32x32/mimetypes
icon32_DATA = images/icons/32x32/*.png
icon48dir = $(datadir)/icons/hicolor/48x48/mimetypes
icon48_DATA = images/icons/48x48/*.png
icon64dir = $(datadir)/icons/hicolor/64x64/mimetypes
icon64_DATA = images/icons/64x64/*.png
icon128dir = $(datadir)/icons/hicolor/128x128/mimetypes
icon128_DATA = images/icons/128x128/*.png
icon256dir = $(datadir)/icons/hicolor/256x256/mimetypes
icon256_DATA = images/icons/256x256/*.png
icon512dir = $(datadir)/icons/hicolor/512x512/mimetypes
icon512_DATA = images/icons/512x512/*.png

iconsdir=$(datadir)/icons/hicolor/scalable/mimetypes
icons_DATA=$(srcdir)/images/icons/scalable/*.svg
endif

cssdir = $(pkgdatadir)/css
css_DATA = css/*.css

scriptsdir = $(pkgdatadir)/scripts
scripts_DATA = scripts/*.py

pythondir = $(pkgdatadir)/gui
python_PYTHON=gui/*.py gui/*.bat

dist_doc_DATA = README.md LICENSE.txt

licensesdir = $(pkgdatadir)/licenses
licenses_DATA=licenses/*.txt

if INCLUDE_MAN
man1_MANS = man/oghma_gui.1
endif

if INCLUDE_DESKTOP
appicondir=$(pkgdatadir)/images
appicon_DATA=$(srcdir)/desktop/application-oghma.svg

desktopdir = $(datadir)/applications
desktop_DATA = $(srcdir)/desktop/oghma.desktop

packagesdir = $(datadir)/mime/packages
packages_DATA = $(srcdir)/desktop/oghma-oghma.xml

endif

clean-local:
	rm *.dat *.o *.log *.a  *.lib *.exe *.chk *.oplot -f
	rm ./gui/__pycache__/* -f
	rm autom4te.cache -rf
	find . -type f -name '.~lock*' -delete
	@echo "clean-local"
	@echo "(oghma_build_finished)"
	
all:
	@echo "all"
	@echo "(oghma_build_finished)"


install-data-hook:
	pwd
	chmod +x $(DESTDIR)$(pkgdatadir)/gui/oghmanano.py
	chmod +x $(DESTDIR)$(pkgdatadir)/gui/oghma_tool.py
	find ./ -name "*.mo" -exec cp --parents {} $(DESTDIR)$(datadir)/oghma_gui/ ";"
	-rm $(DESTDIR)$(pkgdatadir)/gui/__pycache__ -rf
	@echo "install-data-hook"
	@echo "(oghma_build_finished)"

uninstall-hook:
	-rm $(DESTDIR)$(pkgdatadir) -rf
	-rm $(DESTDIR)$(bindir)/oghma_gui
	@echo "uninstall-hook"

ACLOCAL_AMFLAGS = -I m4
