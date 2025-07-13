SRCS := $(wildcard *.c)
OBJS := $(SRCS:c=o)

inc=-I../../include/ #last line is for debian compatibility
lib=-L../../

all: $(OBJS)
	$(CC) -shared $(OBJS) $(lib) @DLL_DEBUG@ @LIBS@ @LIB_UMFPACK@ -loghma_core  -L../../ -Wall -o plugin.@DLIB_EXT@
	mv plugin.@DLIB_EXT@ ../complex_umfpack.@DLIB_EXT@

.c.o : 
	$(CC) $(inc) $(CPPFLAGS) @INCLUDE_UMFPACK@ @DLL_DEBUG@ @DLL_COMPILE@ @COMPILE_FLAG@ @DEFINE_CORE@ -c $< -o $@

clean:
	rm *.o *.dll *.so stk* -f
