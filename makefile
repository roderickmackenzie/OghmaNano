all:
	cd oghma_core && make -j 8
	cd oghma_gui && make -j 8
py:
	cd libpy && make -j 8
clean:
	cd oghma_core && make clean
	rm *.c *.exe -f

easy:
	for i in `ls ./oghma_core|grep lib`; do echo $i; done
