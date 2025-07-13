SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

CFLAGS=-Wall
inc=-I../../include/
lib=-L../../

all: $(OBJS)
	$(CC) -shared $(OBJS) $(lib) @DLL_DEBUG@ -loghma_core  -L../../ -Wall -o plugin.@DLIB_EXT@
	mv plugin.@DLIB_EXT@ ../light_exp.@DLIB_EXT@

.c.o : 
	$(CC) $(inc) $(CFLAGS) @DLL_DEBUG@ @DLL_COMPILE@ @COMPILE_FLAG@ @DEFINE_CORE@ -c $< -o $@ -Wno-unused-but-set-variable

clean:
	rm *.o *.dll *.so stk* -f
