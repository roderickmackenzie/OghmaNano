OBJS= de_DE zh_CN fr_FR pt_BR el_GR pt_PT es_ES fr_FR ja_JP ar ru_RU uk_UA pl_PL cy_GB et_EE it_IT tr_TR he_IL ka_GE ms_MY la_VA

all: $(OBJS)
	xgettext --language=Python --keyword=_ --no-location --output=oghmanano.pot `find ../../ \( -name "*.py" -or -name "*.c" \)|grep -v pub` --msgid-bugs-address=roderick.mackenzie@oghma-nano.com  --copyright-holder="Roderick C. I. MacKenzie" --package-name=oghmanano --package-version=8.0

% : %.po
	mkdir $@
	mkdir $@/LC_MESSAGES
	cp $@.bib $@/LC_MESSAGES/ref.bib
	msgfmt  $< -o $@/LC_MESSAGES/oghmanano.mo


clean:
	rm $(OBJS) -rf
	rm *.mo -f
	rm oghmanano.pot -f
