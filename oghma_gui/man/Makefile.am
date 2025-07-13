HELP2MAN=help2man

lib=-L../../
inc=-I../../include/

all: oghma_gui.1
	echo "Man page built"


oghma_gui.1: ../oghma_gui
	cd ..; $(HELP2MAN) --output=./man/oghma_gui.1 --name="GUI for oghma_core, a solar cell device model" ./oghma_gui

clean:
	rm *.1 -f

