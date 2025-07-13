

all: 
	@echo "[Desktop Entry]" > oghma.desktop
	@echo "Name=OghmaNano" >> oghma.desktop
	@echo "Icon=$(pkgdatadir)/images/application-oghma.svg" >> oghma.desktop
	@echo "Type=Application" >> oghma.desktop
	@echo "MimeType=application/oghma;" >> oghma.desktop
	@echo "Exec=$(DESTDIR)$(bindir)/oghma %F" >> oghma.desktop
	@echo "Terminal=true" >> oghma.desktop
	@echo "Categories=GTK;GNOME;Education;" >> oghma.desktop
	@echo


clean:
	rm oghma.desktop -f

install-desktop:
	mkdir -p $(DESTDIR)$(datadir)/applications
	cp oghma.desktop $(DESTDIR)$(datadir)/applications/oghma.desktop

uninstall:
	pwd
	-rm $(DESTDIR)$(datadir)/icons/hicolor/scalable/mimetypes/simulation-oghma.svg
	-rm $(DESTDIR)$(datadir)/mime/packages/oghma-oghma.xml
	-rm $(DESTDIR)$(datadir)/applications/oghma.desktop
