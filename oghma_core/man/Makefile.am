HELP2MAN=help2man

lib=-L../../
inc=-I../../include/

all: oghma_core.1
	echo "Man page built"



oghma_core.1: ../oghma_core@EXE_EXT@
	cd ..; $(HELP2MAN) --output=./man/oghma_core.1 --name="A solar cell device model" ./oghma_core@EXE_EXT@

clean:
	rm *.1 stk* -f

