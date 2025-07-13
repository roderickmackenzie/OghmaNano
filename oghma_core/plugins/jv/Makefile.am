SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

lib=-L../../
inc=-I../../include/

all: $(OBJS)
	$(CC) -shared $(OBJS) $(lib) @DLL_DEBUG@ -loghma_core  -L../../ -Wall -o plugin.@DLIB_EXT@
	cp plugin.@DLIB_EXT@ ../jv.@DLIB_EXT@ -f
#$(CC) -shared $(OBJS) @DLL_LINKER@ $(lib) -o plugin.@DLIB_EXT@

.c.o : 
	$(CC) $(inc) @DLL_DEBUG@ @DLL_COMPILE@ @COMPILE_FLAG@ -Wno-error=unused-but-set-variable -Wno-error=unused-variable @DEFINE_CORE@ -s -c $< -o $@

clean:
	rm *.o *.dll *.so stk* -f

